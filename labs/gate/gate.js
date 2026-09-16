/*
 * Sign-in gate and progress sync for the CSC/EE 8001 class labs.
 *
 * Loaded by every lab page (the build injects it) and by the instructor
 * dashboard. It needs labs/gate/config.js first, which deploy.sh writes.
 *
 * On a lab page it:
 *   - covers the lab until the student signs in, signs up, or resets a password
 *   - gives this tab a unique "rl" query parameter before marimo starts; the
 *     notebook runs in a web worker and reads that parameter to find the
 *     BroadcastChannel it should talk to, so two open tabs never cross wires
 *   - answers the notebook's load, save and submit messages by calling the API
 *     with the signed-in student's token (tokens never reach the notebook)
 *
 * Everywhere it exposes window.radiantLabAuth = { ready, api, signOut, user }.
 *
 * Script attributes:  data-mode="lab" (default) or "admin"
 *                     data-lab="week_04" (default: taken from the URL)
 *
 * Emailed codes (verification, password reset) are off unless config.js sets
 * `emailCodes: true`: university mail holds Cognito's messages. Instead an
 * instructor approves new accounts on the dashboard, and a forgotten password
 * means the account is deleted and created again (saved work is kept).
 *
 * For previewing a lab locally without AWS, set `mock: true` in config.js.
 * Sign-in is skipped and the API is faked in this browser's localStorage;
 * `mockAdmin: true` makes the fake user an admin.
 */
(function () {
  "use strict";

  var script = document.currentScript;
  var cfg = window.RADIANT_LAB_CONFIG;
  if (!cfg || !cfg.apiUrl || !cfg.clientId) {
    console.warn("[labs] no config.js; sign-in and saving are switched off");
    return;
  }

  var mode = (script && script.dataset.mode) || "lab";
  var labId = (script && script.dataset.lab) || labFromPath();
  var PENDING = "rl-pending";
  var early = document.createElement("style");
  early.textContent = "html." + PENDING + " body>*:not(.rl-gate){visibility:hidden!important}";
  document.head.appendChild(early);
  document.documentElement.classList.add(PENDING);
  var STORE_KEY = "radiantLab.session." + cfg.clientId;
  var COGNITO = "https://cognito-idp." + cfg.region + ".amazonaws.com/";
  var SAVE_DELAY_MS = 1200;
  var MOCK = cfg.mock === true;
  var EMAIL_CODES = cfg.emailCodes === true;
  var ALIASES = (cfg.aliasDomains || ["umsystem.edu", "missouri.edu", "mail.missouri.edu"])
    .map(function (d) { return String(d).trim().toLowerCase(); });

  // x@missouri.edu, x@mail.missouri.edu and x@umsystem.edu are one mailbox, so they
  // are one account: the Cognito username is always the first domain's spelling.
  // The email attribute keeps what was typed, so codes go where the person expects.
  function username(email) {
    var e = String(email || "").trim().toLowerCase();
    var at = e.lastIndexOf("@");
    if (at > 0 && ALIASES.indexOf(e.slice(at + 1)) >= 0) return e.slice(0, at + 1) + ALIASES[0];
    return e;
  }

  function labFromPath() {
    var m = location.pathname.match(/\/labs\/([a-z0-9_]+)\/?/);
    return m ? m[1] : null;
  }

  function randomId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID().replace(/-/g, "");
    return Math.random().toString(36).slice(2) + Date.now().toString(36);
  }

  // -- tab id for the notebook, set before marimo reads the URL -----------------

  var channel = null;
  if (mode === "lab" && labId) {
    var tab = randomId();
    var url = new URL(location.href);
    url.searchParams.set("rl", tab);
    history.replaceState(history.state, "", url.toString());
    if ("BroadcastChannel" in window) {
      channel = new BroadcastChannel("radiant-lab-" + tab);
    }
  }

  // -- session storage ----------------------------------------------------------

  function readSession() {
    try {
      return JSON.parse(localStorage.getItem(STORE_KEY)) || null;
    } catch (e) {
      return null;
    }
  }

  function writeSession(s) {
    try {
      if (s) localStorage.setItem(STORE_KEY, JSON.stringify(s));
      else localStorage.removeItem(STORE_KEY);
    } catch (e) { /* private window: the session lasts for this page only */ }
    session = s;
  }

  function claims(jwt) {
    try {
      var part = jwt.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
      var json = decodeURIComponent(escape(atob(part + "===".slice((part.length + 3) % 4))));
      return JSON.parse(json);
    } catch (e) {
      return {};
    }
  }

  function sessionFrom(result, previous) {
    var c = claims(result.IdToken);
    return {
      idToken: result.IdToken,
      refreshToken: result.RefreshToken || (previous && previous.refreshToken),
      expiresAt: (c.exp || 0) * 1000,
      email: c.email || (previous && previous.email) || "",
    };
  }

  var session = readSession();

  // -- Cognito ------------------------------------------------------------------

  function cognito(action, body) {
    return fetch(COGNITO, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "AWSCognitoIdentityProviderService." + action,
      },
      body: JSON.stringify(Object.assign({ ClientId: cfg.clientId }, body)),
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (res.ok) return data;
        var err = new Error(friendly(data));
        err.code = String(data.__type || "").split("#").pop();
        throw err;
      });
    }, function () {
      throw new Error("Could not reach the sign-in service. Check your connection and try again.");
    });
  }

  var WRONG_LOGIN = "Wrong email or password. Check the address you typed, or use " +
    "Forgot password? below.";

  function friendly(data) {
    var type = String(data.__type || "").split("#").pop();
    var msg = String(data.message || data.Message || "");
    switch (type) {
      case "NotAuthorizedException":
        if (/disabled/i.test(msg)) return "This account has been disabled.";
        return WRONG_LOGIN;
      case "UserNotFoundException":
        return WRONG_LOGIN;
      case "UsernameExistsException":
        return "There is already an account for that email. Sign in instead.";
      case "CodeMismatchException":
        return "That code is not right. Check the email and try again.";
      case "ExpiredCodeException":
        return "That code has expired. Ask for a new one.";
      case "InvalidPasswordException":
        return "Use at least 8 characters, with at least one lowercase letter and one number.";
      case "LimitExceededException":
      case "TooManyRequestsException":
      case "TooManyFailedAttemptsException":
        return "Too many attempts. Wait a few minutes and try again.";
      case "UserLambdaValidationException":
        return msg.replace(/^PreSignUp failed with error\s*/i, "").replace(/\.*$/, ".");
      case "InvalidParameterException":
        return /email/i.test(msg) ? "Enter a valid email address." : msg;
      case "CodeDeliveryFailureException":
        return "We could not send the email. Try again in a little while.";
      default:
        return msg || "Something went wrong. Please try again.";
    }
  }

  var refreshing = null;

  function idToken() {
    if (MOCK) return Promise.resolve("mock");
    if (!session) return Promise.reject(signInNeeded());
    if (session.expiresAt - Date.now() > 120000) return Promise.resolve(session.idToken);
    if (!session.refreshToken) return Promise.reject(signInNeeded());
    if (!refreshing) {
      var previous = session;
      refreshing = cognito("InitiateAuth", {
        AuthFlow: "REFRESH_TOKEN_AUTH",
        AuthParameters: { REFRESH_TOKEN: previous.refreshToken },
      }).then(function (data) {
        writeSession(sessionFrom(data.AuthenticationResult, previous));
        return session.idToken;
      }, function (err) {
        if (err.code === "NotAuthorizedException") {
          writeSession(null);
          throw signInNeeded();
        }
        throw err;
      }).finally(function () { refreshing = null; });
    }
    return refreshing;
  }

  function signInNeeded() {
    var e = new Error("Please sign in again.");
    e.code = "SignInNeeded";
    return e;
  }

  // -- API ----------------------------------------------------------------------

  function api(method, path, body, options) {
    if (MOCK) return mockApi(method, path, body);
    return idToken().then(function (token) {
      return fetch(cfg.apiUrl.replace(/\/$/, "") + path, {
        method: method,
        headers: Object.assign(
          { Authorization: token },
          body !== undefined ? { "Content-Type": "application/json" } : {}
        ),
        body: body !== undefined ? JSON.stringify(body) : undefined,
        keepalive: !!(options && options.keepalive),
        cache: "no-store",
      });
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (res.ok) return data;
        var err = new Error(data.error || data.message || ("Request failed (" + res.status + ")."));
        err.status = res.status;
        if (res.status === 401) {
          writeSession(null);
          err.code = "SignInNeeded";
        }
        throw err;
      });
    });
  }

  // A stand-in for the real API, kept in localStorage, for local previews only.
  function mockApi(method, path, body) {
    var KEY = "radiantLab.mock";
    var db;
    try { db = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { db = {}; }
    db.progress = db.progress || {};
    db.labs = db.labs || {};
    db.admins = db.admins || [];
    db.pending = db.pending || [];
    var address = (cfg.mockEmail || "student@umsystem.edu").toLowerCase();
    var email = username(address);
    var admin = cfg.mockAdmin === true;
    var now = new Date().toISOString().replace(/\.\d+Z$/, "+00:00");
    var m, out;

    function persist() { localStorage.setItem(KEY, JSON.stringify(db)); }
    function fail(status, message) {
      var e = new Error(message);
      e.status = status;
      return Promise.reject(e);
    }
    function row(lab) {
      var r = db.progress[lab];
      return {
        id: email, email: email, state: r.state, submitted: !!r.submitted,
        submittedAt: r.submittedAt || null, submissions: r.submissions || 0,
        updatedAt: r.updatedAt, createdAt: r.createdAt, saves: r.saves || 0,
        locked: !!r.locked, lockedBy: r.lockedBy || null,
      };
    }

    if (path === "/me") {
      out = { email: email, address: address, admin: admin, owner: admin };
    } else if ((m = path.match(/^\/labs\/([a-z0-9_]+)\/progress$/))) {
      var lab = m[1], rec = db.progress[lab] || null;
      var labLocked = !!db.labs[lab], studentLocked = !!(rec && rec.locked);
      if (method === "GET") {
        out = {
          lab: lab, state: rec ? rec.state : {}, submitted: !!(rec && rec.submitted),
          submittedAt: rec ? rec.submittedAt || null : null,
          updatedAt: rec ? rec.updatedAt : null,
          locked: (labLocked || studentLocked) && !admin,
          labLocked: labLocked, studentLocked: studentLocked, admin: admin,
        };
      } else {
        if (!admin && labLocked) return fail(423, "An instructor has locked this lab.");
        if (!admin && studentLocked) return fail(423, "An instructor has locked your answers for this lab.");
        rec = rec || { createdAt: now, saves: 0, submissions: 0 };
        rec.state = body.state;
        rec.updatedAt = now;
        rec.saves += 1;
        if (body.submit) {
          rec.submitted = true;
          rec.submittedAt = now;
          rec.submissions += 1;
        }
        db.progress[lab] = rec;
        persist();
        out = { lab: lab, updatedAt: now, submitted: !!rec.submitted,
                submittedAt: rec.submittedAt || null, saves: rec.saves };
      }
    } else if (!admin && path.indexOf("/admin/") === 0) {
      return fail(403, "This needs instructor access.");
    } else if (path === "/admin/labs") {
      out = { labs: Object.keys(db.labs).map(function (k) {
        return { lab: k, locked: db.labs[k], lockedBy: email, lockedAt: now };
      }) };
    } else if ((m = path.match(/^\/admin\/labs\/([a-z0-9_]+)\/progress$/))) {
      out = { lab: m[1], locked: !!db.labs[m[1]],
              students: db.progress[m[1]] ? [row(m[1])] : [] };
    } else if ((m = path.match(/^\/admin\/labs\/([a-z0-9_]+)\/lock$/))) {
      db.labs[m[1]] = !!body.locked;
      persist();
      out = { lab: m[1], locked: !!body.locked, lockedBy: email, lockedAt: now };
    } else if ((m = path.match(/^\/admin\/labs\/([a-z0-9_]+)\/students\/[^/]+\/lock$/))) {
      if (!db.progress[m[1]]) return fail(404, "That student has not opened this lab yet.");
      db.progress[m[1]].locked = !!body.locked;
      db.progress[m[1]].lockedBy = email;
      persist();
      out = row(m[1]);
    } else if (path === "/admin/accounts") {
      db.approved = db.approved || [];
      out = { accounts: db.pending.map(function (a) {
        return { username: username(a), email: a, status: "UNCONFIRMED", approved: false,
                 createdAt: now, staff: false, you: false };
      }).concat(db.approved.concat([address]).map(function (a) {
        return { username: username(a), email: a, status: "CONFIRMED", approved: true,
                 createdAt: now, staff: a === address, you: a === address };
      })) };
    } else if (path === "/admin/accounts/confirm") {
      db.approved = db.approved || [];
      out = { results: body.usernames.map(function (u) {
        var match = db.pending.filter(function (a) { return username(a) === u; });
        db.pending = db.pending.filter(function (a) { return username(a) !== u; });
        db.approved = db.approved.concat(match);
        return { username: u, confirmed: match.length > 0 };
      }) };
      persist();
    } else if ((m = path.match(/^\/admin\/accounts\/(.+)$/)) && method === "DELETE") {
      var dropped = decodeURIComponent(m[1]);
      db.pending = db.pending.filter(function (a) { return username(a) !== dropped; });
      db.approved = (db.approved || []).filter(function (a) { return username(a) !== dropped; });
      persist();
      out = { username: dropped, removed: true };
    } else if (path === "/admin/admins" && method === "GET") {
      out = { admins: [{ email: email, owner: true }].concat(db.admins.map(function (a) {
        return { email: a, owner: false, addedBy: email, addedAt: now };
      })) };
    } else if (path === "/admin/admins" && method === "POST") {
      var added = username(body.email);
      if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(added)) return fail(400, "That does not look like an email address.");
      if (db.admins.indexOf(added) < 0) db.admins.push(added);
      persist();
      out = { email: added, owner: false, addedBy: email };
    } else if ((m = path.match(/^\/admin\/admins\/(.+)$/)) && method === "DELETE") {
      var gone = username(decodeURIComponent(m[1]));
      db.admins = db.admins.filter(function (a) { return a !== gone; });
      persist();
      out = { email: gone, removed: true };
    } else {
      return fail(404, "Not found.");
    }
    return new Promise(function (resolve) {
      setTimeout(function () { resolve(JSON.parse(JSON.stringify(out))); }, 150);
    });
  }

  // -- the overlay --------------------------------------------------------------

  var STYLE = [
    ".rl-gate{position:fixed;inset:0;z-index:2147483000;background:#faf8f2;",
    "display:flex;align-items:center;justify-content:center;padding:24px 16px;overflow:auto;",
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1c1c1c}",
    ".rl-gate[hidden]{display:none!important}",
    ".rl-card{width:100%;max-width:400px;background:#fff;border:1px solid #e6e6e6;",
    "border-top:6px solid #f1b82d;border-radius:14px;padding:26px 26px 22px;",
    "box-shadow:0 12px 32px rgba(17,17,17,.08)}",
    ".rl-eyebrow{margin:0 0 6px;color:#6a5314;font-size:.74rem;font-weight:800;",
    "letter-spacing:.08em;text-transform:uppercase}",
    ".rl-card h1{margin:0 0 6px;font-size:1.4rem;line-height:1.25;color:#111}",
    ".rl-card p.rl-sub{margin:0 0 18px;color:#4a4a4a;font-size:.93rem;line-height:1.55}",
    ".rl-card label{display:block;margin:0 0 12px;font-size:.84rem;font-weight:700;color:#333}",
    ".rl-card input{display:block;width:100%;box-sizing:border-box;margin-top:5px;",
    "padding:10px 12px;border:1px solid #d6d6d6;border-radius:8px;font:inherit;font-size:.98rem;",
    "background:#fff;color:#111}",
    ".rl-card input:focus{outline:2px solid #f1b82d;outline-offset:1px;border-color:#e0a91c}",
    ".rl-btn{display:block;width:100%;margin-top:6px;padding:11px 14px;border:1px solid #e0a91c;",
    "border-radius:999px;background:#f1b82d;color:#111;font:inherit;font-weight:800;",
    "font-size:.97rem;cursor:pointer}",
    ".rl-btn:hover{background:#e8ad19}",
    ".rl-btn[disabled]{opacity:.6;cursor:progress}",
    ".rl-links{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;margin-top:14px;font-size:.86rem}",
    ".rl-link{background:none;border:0;padding:0;color:#6a5314;font:inherit;font-weight:700;",
    "cursor:pointer;text-decoration:underline;text-underline-offset:2px}",
    ".rl-msg{margin:0 0 12px;padding:9px 12px;border-radius:8px;font-size:.87rem;line-height:1.45}",
    ".rl-msg.err{background:#fdecec;color:#8a1f1f;border:1px solid #f3c4c4}",
    ".rl-msg.ok{background:#edf7ee;color:#1e5b22;border:1px solid #c6e3c8}",
    ".rl-msg[hidden]{display:none}",
    ".rl-note{margin:14px 0 0;color:#6f6f6f;font-size:.78rem;line-height:1.5}",
    ".rl-card ol{list-style:decimal outside!important;margin:0 0 16px;padding:0 0 0 22px}",
    ".rl-card li{display:list-item!important;list-style:inherit!important;border:0!important;",
    "margin:0 0 6px;padding:0;color:#2f2f2f;font-size:.92rem;line-height:1.5;background:none}",
    ".rl-pill{position:fixed;left:12px;bottom:12px;z-index:2147482000;display:flex;",
    "align-items:center;gap:10px;flex-wrap:wrap;max-width:calc(100vw - 24px);box-sizing:border-box;",
    "padding:6px 12px;border:1px solid #e6e6e6;border-radius:999px;background:rgba(255,255,255,.96);",
    "box-shadow:0 4px 14px rgba(17,17,17,.08);font:500 .78rem/1.3 -apple-system,BlinkMacSystemFont,",
    "'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#3a3a3a}",
    ".rl-pill .rl-dot{width:8px;height:8px;border-radius:50%;background:#9a9a9a;flex:0 0 auto}",
    ".rl-pill .rl-dot.ok{background:#2e7d32}.rl-pill .rl-dot.busy{background:#f1b82d}",
    ".rl-pill .rl-dot.bad{background:#c62828}",
    ".rl-pill a,.rl-pill button{color:#6a5314;font:inherit;font-weight:700;background:none;border:0;",
    "padding:0;cursor:pointer;text-decoration:underline;text-underline-offset:2px}",
    ".rl-banner{position:fixed;top:0;left:0;right:0;z-index:2147482500;padding:9px 16px;",
    "background:#fff3cc;border-bottom:1px solid #f2dfaa;color:#62490a;text-align:center;",
    "font:600 .88rem/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}",
    ".rl-banner[hidden]{display:none}",
  ].join("");

  var gate, pill, banner, view = null, pendingEmail = "";

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "hidden") node.hidden = !!attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(c); });
    return node;
  }

  function mount() {
    if (gate) return;
    document.head.appendChild(el("style", { text: STYLE }));
    gate = el("div", { class: "rl-gate", role: "dialog", "aria-modal": "true",
                       "aria-labelledby": "rl-title" });
    document.body.appendChild(gate);
  }

  function lockScroll(on) {
    document.documentElement.style.overflow = on ? "hidden" : "";
  }

  function whenBody(fn) {
    if (document.body) fn();
    else document.addEventListener("DOMContentLoaded", fn, { once: true });
  }

  function heading() {
    return mode === "admin"
      ? { eyebrow: "CSC/EE 8001 · Instructors", title: "Lab dashboard" }
      : { eyebrow: "CSC/EE 8001 · Class labs", title: labTitle() };
  }

  function labTitle() {
    var m = (labId || "").match(/^week_(\d+)$/);
    return m ? "Week " + Number(m[1]) + " lab" : "Class lab";
  }

  function showView(name, message) {
    mount();
    view = name;
    lockScroll(true);
    gate.hidden = false;
    gate.textContent = "";
    var h = heading();
    var card = el("div", { class: "rl-card" });
    card.appendChild(el("p", { class: "rl-eyebrow", text: h.eyebrow }));

    var err = el("p", { class: "rl-msg err", role: "alert", hidden: true });
    var ok = el("p", { class: "rl-msg ok", role: "status", hidden: true });
    function fail(e) { ok.hidden = true; err.textContent = e.message || String(e); err.hidden = false; }
    function note(text) { err.hidden = true; ok.textContent = text; ok.hidden = false; }

    function form(fields, button, onSubmit) {
      var f = el("form", { novalidate: "" });
      f.appendChild(err);
      f.appendChild(ok);
      fields.forEach(function (x) { f.appendChild(x); });
      var btn = el("button", { class: "rl-btn", type: "submit", text: button });
      f.appendChild(btn);
      f.addEventListener("submit", function (ev) {
        ev.preventDefault();
        err.hidden = true;
        btn.disabled = true;
        Promise.resolve().then(onSubmit).catch(fail).finally(function () { btn.disabled = false; });
      });
      return f;
    }

    function input(label, type, name, autocomplete, extra) {
      var i = el("input", Object.assign({ type: type, name: name, autocomplete: autocomplete,
                                          required: "" }, extra || {}));
      return { label: el("label", { text: label }, [i]), input: i };
    }

    function link(text, target) {
      var b = el("button", { class: "rl-link", type: "button", text: text });
      b.addEventListener("click", function () { showView(target); });
      return b;
    }

    var email, pass, again, code, f;

    function samePassword() {
      if (pass.input.value !== again.input.value) {
        throw new Error("The two passwords do not match.");
      }
    }
    if (name === "signin") {
      card.appendChild(el("h1", { id: "rl-title", text: h.title }));
      card.appendChild(el("p", { class: "rl-sub", text:
        mode === "admin"
          ? "Sign in with the account you use for the class labs."
          : "Sign in to open the lab. Your answers save as you go, so you can come back to them later." }));
      email = input("University email", "email", "email", "username", { value: pendingEmail });
      pass = input("Password", "password", "password", "current-password");
      f = form([email.label, pass.label], "Sign in", function () {
        pendingEmail = email.input.value.trim();
        return signIn(pendingEmail, pass.input.value).catch(function (e) {
          if (e.code === "UserNotConfirmedException") {
            pendingPassword = pass.input.value;
            showView(EMAIL_CODES ? "verify" : "waiting");
            return;
          }
          throw e;
        });
      });
      card.appendChild(f);
      card.appendChild(el("div", { class: "rl-links" }, [
        link("Create an account", "signup"), link("Forgot password?", "forgot"),
      ]));
    } else if (name === "signup") {
      card.appendChild(el("h1", { id: "rl-title", text: "Create your lab account" }));
      card.appendChild(el("p", { class: "rl-sub", text: EMAIL_CODES
        ? "Use your University of Missouri email. We will send a code to check it is yours."
        : "Use your University of Missouri email. Your instructor approves new accounts, " +
          "then you can sign in." }));
      email = input("University email", "email", "email", "username", { value: pendingEmail });
      var emailAgain = input("Retype university email", "email", "email2", "off");
      pass = input("New password", "password", "password", "new-password", { minlength: "8" });
      again = input("Retype new password", "password", "password2", "new-password", { minlength: "8" });
      f = form([email.label, emailAgain.label, pass.label, again.label], "Create account", function () {
        pendingEmail = email.input.value.trim();
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(pendingEmail)) throw new Error("Enter a valid email address.");
        if (pendingEmail.toLowerCase() !== emailAgain.input.value.trim().toLowerCase()) {
          throw new Error("The two email addresses do not match.");
        }
        samePassword();
        return cognito("SignUp", {
          Username: username(pendingEmail),
          Password: pass.input.value,
          UserAttributes: [{ Name: "email", Value: pendingEmail.toLowerCase() }],
        }).then(function () {
          pendingPassword = pass.input.value;
          showView(EMAIL_CODES ? "verify" : "waiting",
                   EMAIL_CODES ? "We sent a 6-digit code to " + pendingEmail + "." : null);
        });
      });
      card.appendChild(f);
      card.appendChild(el("p", { class: "rl-note", text:
        "At least 8 characters, with a lowercase letter and a number." }));
      card.appendChild(el("div", { class: "rl-links" }, [link("I already have an account", "signin")]));
    } else if (name === "verify") {
      card.appendChild(el("h1", { id: "rl-title", text: "Almost there" }));
      card.appendChild(el("p", { class: "rl-sub", text:
        "We emailed you a 6-digit code. University mail often holds these messages, " +
        "so if nothing arrives, your instructor will approve your account instead. " +
        "Once that is done, sign in with the password you chose." }));
      code = input("Verification code", "text", "code", "one-time-code",
                   { inputmode: "numeric", pattern: "[0-9]*", maxlength: "6" });
      f = form([code.label], "I have a code", function () {
        return cognito("ConfirmSignUp", {
          Username: username(pendingEmail), ConfirmationCode: code.input.value.trim(),
        }).then(function () {
          if (pendingPassword) {
            var p = pendingPassword;
            pendingPassword = "";
            return signIn(pendingEmail, p);
          }
          showView("signin", "Email verified. Sign in to continue.");
        });
      });
      card.appendChild(f);
      var resend = el("button", { class: "rl-link", type: "button", text: "Send a new code" });
      resend.addEventListener("click", function () {
        cognito("ResendConfirmationCode", { Username: username(pendingEmail) })
          .then(function () { note("A new code is on its way."); }, fail);
      });
      card.appendChild(el("div", { class: "rl-links" }, [resend, link("Back to sign in", "signin")]));
      card.appendChild(el("p", { class: "rl-note", text:
        "No code? Let your instructor know you have signed up. After they approve " +
        "your account, use Back to sign in." }));
    } else if (name === "waiting") {
      card.appendChild(el("h1", { id: "rl-title", text: "Waiting for approval" }));
      card.appendChild(el("p", { class: "rl-sub", text:
        "Your account is created, but your instructor has not approved it yet. Let them " +
        "know you have signed up. Once they approve it, sign in with the password you chose." }));
      card.appendChild(el("p", { class: "rl-sub" }, [
        document.createTextNode("Your account: "),
        el("strong", { text: pendingEmail || "the address you entered" }),
      ]));
      card.appendChild(el("p", { class: "rl-note", text:
        "No email is sent, so there is nothing to wait for in your inbox. If that address " +
        "has a typo, tell your instructor so they can delete it, then create the account " +
        "again with the right address." }));
      card.appendChild(el("div", { class: "rl-links" }, [
        link("Back to sign in", "signin"), link("Create the account again", "signup"),
      ]));
    } else if (name === "forgot" && !EMAIL_CODES) {
      card.appendChild(el("h1", { id: "rl-title", text: "Forgot your password?" }));
      card.appendChild(el("p", { class: "rl-sub", text:
        "Tell your instructor. Then:" }));
      var steps = el("ol");
      [
        "Your instructor deletes your account.",
        "You create it again with the same email and a new password.",
        "Your instructor approves it, and you sign in.",
      ].forEach(function (t) { steps.appendChild(el("li", { text: t })); });
      card.appendChild(steps);
      card.appendChild(el("p", { class: "rl-note", text:
        "Everything you saved in the labs is kept. No email is sent." }));
      var back = el("button", { class: "rl-btn", type: "button", text: "Back to sign in" });
      back.addEventListener("click", function () { showView("signin"); });
      card.appendChild(back);
    } else if (name === "forgot") {
      card.appendChild(el("h1", { id: "rl-title", text: "Reset your password" }));
      card.appendChild(el("p", { class: "rl-sub", text:
        "We will email you a code to set a new password. University mail often holds " +
        "these, so if nothing arrives, ask your instructor to reset your password. They " +
        "will give you a temporary one to sign in with." }));
      email = input("University email", "email", "email", "username", { value: pendingEmail });
      f = form([email.label], "Email me a code", function () {
        pendingEmail = email.input.value.trim();
        return cognito("ForgotPassword", { Username: username(pendingEmail) }).then(function () {
          showView("reset", "If there is an account for " + pendingEmail + ", a code is on its way.");
        });
      });
      card.appendChild(f);
      card.appendChild(el("div", { class: "rl-links" }, [link("Back to sign in", "signin")]));
    } else if (name === "reset") {
      card.appendChild(el("h1", { id: "rl-title", text: "Choose a new password" }));
      card.appendChild(el("p", { class: "rl-sub", text: "Enter the code from the email and a new password." }));
      code = input("Code", "text", "code", "one-time-code", { inputmode: "numeric", maxlength: "6" });
      pass = input("New password", "password", "password", "new-password", { minlength: "8" });
      again = input("Retype new password", "password", "password2", "new-password", { minlength: "8" });
      f = form([code.label, pass.label, again.label], "Set password and sign in", function () {
        samePassword();
        return cognito("ConfirmForgotPassword", {
          Username: username(pendingEmail), ConfirmationCode: code.input.value.trim(),
          Password: pass.input.value,
        }).then(function () { return signIn(pendingEmail, pass.input.value); });
      });
      card.appendChild(f);
      card.appendChild(el("div", { class: "rl-links" }, [link("Back to sign in", "signin")]));
    } else if (name === "newpass") {
      card.appendChild(el("h1", { id: "rl-title", text: "Choose your own password" }));
      card.appendChild(el("p", { class: "rl-sub", text:
        "Your account was set up with a temporary password. Pick a new one that only " +
        "you know." }));
      pass = input("New password", "password", "password", "new-password", { minlength: "8" });
      again = input("Retype new password", "password", "password2", "new-password", { minlength: "8" });
      f = form([pass.label, again.label], "Save password and continue", function () {
        samePassword();
        if (!challenge) throw new Error("Please sign in again.");
        return cognito("RespondToAuthChallenge", {
          ChallengeName: "NEW_PASSWORD_REQUIRED",
          Session: challenge.session,
          ChallengeResponses: { USERNAME: challenge.username, NEW_PASSWORD: pass.input.value },
        }).then(function (data) {
          challenge = null;
          writeSession(sessionFrom(data.AuthenticationResult));
          return start();
        }, function (e) {
          if (e.code === "NotAuthorizedException") {
            challenge = null;
            showView("signin", "That took too long. Sign in again with the temporary password.");
            return;
          }
          throw e;
        });
      });
      card.appendChild(f);
      card.appendChild(el("p", { class: "rl-note", text:
        "At least 8 characters, with a lowercase letter and a number." }));
    } else if (name === "loading") {
      card.appendChild(el("h1", { id: "rl-title", text: h.title }));
      card.appendChild(el("p", { class: "rl-sub", text: message || "Opening your lab…" }));
      message = null;
    } else if (name === "error") {
      card.appendChild(el("h1", { id: "rl-title", text: "Something went wrong" }));
      card.appendChild(el("p", { class: "rl-sub", text: message }));
      var retry = el("button", { class: "rl-btn", type: "button", text: "Try again" });
      retry.addEventListener("click", function () { location.reload(); });
      card.appendChild(retry);
      message = null;
    }

    if (message) note(message);
    gate.appendChild(card);
    var first = gate.querySelector("input");
    if (first) first.focus();
  }

  var pendingPassword = "";

  function hideGate() {
    document.documentElement.classList.remove(PENDING);
    if (gate) {
      gate.hidden = true;
      gate.textContent = "";
    }
    view = null;
    lockScroll(false);
  }

  // -- sign-in flow -------------------------------------------------------------

  var resolveUser;
  var ready = new Promise(function (resolve) { resolveUser = resolve; });
  var user = null;
  var afterSignIn = [];

  function signedIn() {
    resolveUser(user);
    afterSignIn.splice(0).forEach(function (fn) { fn(); });
  }

  var challenge = null;

  function signIn(email, password) {
    return cognito("InitiateAuth", {
      AuthFlow: "USER_PASSWORD_AUTH",
      AuthParameters: { USERNAME: username(email), PASSWORD: password },
    }).then(function (data) {
      if (data.ChallengeName === "NEW_PASSWORD_REQUIRED") {
        // An instructor reset the password; the temporary one must be replaced.
        challenge = { session: data.Session, username: username(email) };
        showView("newpass");
        return;
      }
      if (!data.AuthenticationResult) {
        throw new Error("This account needs a step the lab page cannot do. Ask your instructor.");
      }
      writeSession(sessionFrom(data.AuthenticationResult));
      return start();
    });
  }

  function signOut() {
    if (MOCK) {
      location.reload();
      return Promise.resolve();
    }
    var s = session;
    writeSession(null);
    var done = s && s.refreshToken
      ? cognito("RevokeToken", { Token: s.refreshToken }).catch(function () {})
      : Promise.resolve();
    return done.then(function () {
      var url = new URL(location.href);
      url.searchParams.delete("rl");
      location.replace(url.toString());
    });
  }

  function start() {
    showView("loading");
    return api("GET", "/me").then(function (me) {
      user = me;
      if (mode === "admin") {
        hideGate();
        renderPill();
        signedIn();
        return;
      }
      return api("GET", "/labs/" + labId + "/progress").then(function (progress) {
        hideGate();
        renderPill();
        applyLock(progress);
        setStatus(progress.updatedAt ? "ok" : "idle",
                  progress.updatedAt ? "Progress restored" : "Answers save as you go");
        resolveProgress(progress);
        signedIn();
      });
    }).catch(function (e) {
      if (e.code === "SignInNeeded") {
        showView("signin", "Your session ended. Please sign in again.");
        return;
      }
      showView("error", e.message);
    });
  }

  // -- status pill and lock banner ----------------------------------------------

  var statusDot, statusText;

  function renderPill() {
    if (pill) pill.remove();
    statusDot = el("span", { class: "rl-dot", "aria-hidden": "true" });
    statusText = el("span", { role: "status", text: "" });
    var out = el("button", { type: "button", text: "Sign out" });
    out.addEventListener("click", function () {
      flush().finally(signOut);
    });
    var parts = [statusDot, el("span", { text: user.address || user.email }), statusText];
    if (user.admin && mode !== "admin") {
      parts.push(el("a", { href: "../admin/", text: "Dashboard" }));
    }
    parts.push(out);
    pill = el("div", { class: "rl-pill" }, parts);
    document.body.appendChild(pill);
  }

  function setStatus(kind, text) {
    if (!statusDot) return;
    statusDot.className = "rl-dot " + (kind || "");
    statusText.textContent = text ? "· " + text : "";
  }

  function applyLock(progress) {
    var message = null;
    if (progress.locked) {
      message = progress.studentLocked && !progress.labLocked
        ? "Your instructor has locked your answers for this lab. You can look, but changes will not be saved."
        : "Your instructor has locked this lab. You can look, but changes will not be saved.";
    } else if (progress.admin && (progress.labLocked || progress.studentLocked)) {
      message = "This lab is locked for students. You are an admin, so your changes still save.";
    }
    if (!message) {
      if (banner) banner.hidden = true;
      return;
    }
    if (!banner) {
      banner = el("div", { class: "rl-banner", role: "status" });
      document.body.appendChild(banner);
    }
    banner.textContent = message;
    banner.hidden = false;
  }

  // -- progress sync with the notebook ------------------------------------------

  var resolveProgress;
  var progressReady = new Promise(function (resolve) { resolveProgress = resolve; });
  var latestState = null;
  var saveTimer = null;
  var saving = Promise.resolve();
  var lockedOut = false;

  function reply(message) {
    if (channel) channel.postMessage(JSON.stringify(Object.assign({ from: "gate" }, message)));
  }

  function scheduleSave(state) {
    latestState = state;
    if (lockedOut) return;
    setStatus("busy", "Saving…");
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { send(false); }, SAVE_DELAY_MS);
  }

  function send(submit, options) {
    clearTimeout(saveTimer);
    saveTimer = null;
    if (latestState === null) return Promise.resolve(null);
    var state = latestState;
    var attempt = 0;

    function once() {
      return api("PUT", "/labs/" + labId + "/progress", { state: state, submit: submit }, options);
    }

    function tryIt() {
      return once().catch(function (e) {
        if (e.status === 423) throw e;
        if (e.code === "SignInNeeded") {
          // Keep the answers, ask for the password, then send them.
          return new Promise(function (resolve, reject) {
            afterSignIn.push(function () { once().then(resolve, reject); });
            showView("signin", "Your session ended. Sign in again and your answers will be saved.");
          });
        }
        if (attempt++ < 3 && !(e.status >= 400 && e.status < 500)) {
          setStatus("bad", "Not saved yet, retrying…");
          return new Promise(function (r) { setTimeout(r, 1500 * attempt); }).then(tryIt);
        }
        throw e;
      });
    }

    saving = saving.catch(function () {}).then(tryIt).then(function (res) {
      if (latestState === state) latestState = null;
      setStatus("ok", submit ? "Submitted" : "Saved " + clock(res.updatedAt));
      return res;
    }, function (e) {
      if (e.status === 423) {
        lockedOut = true;
        latestState = null;
        var whole = /locked this lab/.test(e.message);
        applyLock({ locked: true, labLocked: whole, studentLocked: !whole });
        setStatus("bad", "Locked, not saved");
      } else {
        setStatus("bad", "Not saved: " + e.message);
      }
      throw e;
    });
    return saving;
  }

  function flush() {
    return saveTimer ? send(false).catch(function () {}) : saving.catch(function () {});
  }

  function clock(iso) {
    var d = iso ? new Date(iso) : new Date();
    return "at " + d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }

  if (channel) {
    channel.onmessage = function (event) {
      var msg;
      try { msg = JSON.parse(event.data); } catch (e) { return; }
      if (!msg || msg.from !== "notebook" || !msg.id) return;

      if (msg.op === "load") {
        progressReady.then(function (p) {
          reply({ id: msg.id, ok: true, state: p.state || {}, locked: !!p.locked,
                  submitted: !!p.submitted, submittedAt: p.submittedAt || null,
                  admin: !!p.admin });
        });
      } else if (msg.op === "save") {
        if (msg.state && typeof msg.state === "object") scheduleSave(msg.state);
      } else if (msg.op === "submit") {
        if (msg.state && typeof msg.state === "object") latestState = msg.state;
        send(true).then(function (res) {
          reply({ id: msg.id, ok: true, submittedAt: res && res.submittedAt });
        }, function (e) {
          reply({ id: msg.id, ok: false, error: e.message, locked: e.status === 423 });
        });
      }
    };

    // Last chance to send unsaved answers when the tab is hidden or closed.
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden" && saveTimer) send(false, { keepalive: true }).catch(function () {});
    });
    window.addEventListener("pagehide", function () {
      if (saveTimer) send(false, { keepalive: true }).catch(function () {});
    });
  }

  window.radiantLabAuth = {
    ready: ready,
    api: api,
    signOut: signOut,
    get user() { return user; },
    config: cfg,
  };

  // -- go -----------------------------------------------------------------------

  whenBody(function () {
    if (mode === "lab" && !labId) {
      document.documentElement.classList.remove(PENDING);
      return;
    }
    if (MOCK) {
      console.info("[labs] mock mode: nothing leaves this browser");
      start();
    } else if (session && (session.refreshToken || session.expiresAt > Date.now())) start();
    else showView("signin");
  });
})();
