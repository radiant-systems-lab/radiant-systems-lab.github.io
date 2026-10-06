import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 5 - Data That Stops Describing the World")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json
    return json, mo


@app.cell(hide_code=True)
async def _(json, mo):
    # Progress saving. On the course site, labs/gate/gate.js signs the student in
    # and tags this tab with an "rl" query parameter. The notebook runs in a web
    # worker, so it talks to that script over a BroadcastChannel named after the
    # tag, and the script makes the API calls. Opened any other way (marimo edit,
    # a plain export) there is no tag and nothing is saved.
    import sys as _sys

    class LabSync:
        def __init__(self, tab):
            from js import BroadcastChannel
            from pyodide.ffi import create_proxy

            self.state = {}
            self.last_submitted = None
            self._waiting = {}
            self._channel = BroadcastChannel.new("radiant-lab-" + tab)
            self._listener = create_proxy(self._receive)
            self._channel.onmessage = self._listener

        def _receive(self, event):
            try:
                message = json.loads(event.data)
            except (TypeError, ValueError):
                return
            waiting = self._waiting.pop(message.get("id"), None)
            if waiting is not None and not waiting.done():
                waiting.set_result(message)

        def _send(self, op, message_id, **fields):
            message = {"id": message_id, "op": op, "from": "notebook"}
            message.update(fields)
            self._channel.postMessage(json.dumps(message))

        async def _request(self, op, timeout=None, **fields):
            import asyncio
            import uuid

            message_id = uuid.uuid4().hex
            reply = asyncio.get_event_loop().create_future()
            self._waiting[message_id] = reply
            self._send(op, message_id, **fields)
            try:
                return await (reply if timeout is None else asyncio.wait_for(reply, timeout))
            except asyncio.TimeoutError:
                return {"ok": False, "error": "the page did not answer in time"}
            finally:
                self._waiting.pop(message_id, None)

        async def load(self):
            """Wait for sign-in, then return what this student saved before."""
            reply = await self._request("load")
            self.state = dict(reply.get("state") or {})
            return reply

        def record(self, **answers):
            """Remember these answers; the page saves them a moment later."""
            import uuid

            changed = {k: v for k, v in answers.items()
                       if k not in self.state or self.state[k] != v}
            if changed:
                self.state.update(changed)
                self._send("save", uuid.uuid4().hex, state=self.state)

        def record_once(self, **answers):
            """For marked questions: the first answer is the one that counts."""
            fresh = {k: v for k, v in answers.items()
                     if v is not None and self.state.get(k) is None}
            if fresh:
                self.record(**fresh)

        async def submit(self, **answers):
            """Save everything now and mark the lab as submitted."""
            self.state.update(answers)
            reply = await self._request("submit", timeout=45, state=self.state)
            if reply.get("ok"):
                self.last_submitted = reply.get("submittedAt") or "today"
            return reply

    def pick(options, value):
        """The label a radio should show for a saved value, or None."""
        return next((label for label, v in options.items() if v == value), None)

    lab_sync = None
    lab_status = {}
    saved = {}
    locked = False
    _tab = mo.query_params().get("rl") if "pyodide" in _sys.modules else None
    if _tab:
        lab_sync = LabSync(_tab)
        lab_status = await lab_sync.load()
        saved = dict(lab_sync.state)
        locked = bool(lab_status.get("locked"))
    return lab_status, lab_sync, locked, pick, saved


@app.cell(hide_code=True)
def _(mo):
    # Which marked questions have been answered. These count towards the grade, so
    # each one takes a single answer and then stops accepting input.
    get_given, set_given = mo.state({})
    return get_given, set_given


@app.cell(hide_code=True)
def _(get_given, locked, mo, pick, saved, set_given):
    def ask(prompt, options, correct, because, key):
        """A marked question. One answer, then the explanation. No second go."""
        labels = {value: label for label, value in options.items()}
        BREAK = chr(10) + chr(10)
        given = get_given().get(key, saved.get(key))

        def choose(value):
            if value is not None and get_given().get(key, saved.get(key)) is None:
                set_given(lambda d: dict(d, **{key: value}))

        radio = mo.ui.radio(
            options=options, label=prompt,
            value=pick(options, given),
            disabled=locked or given is not None,
            on_change=choose,
        )

        def render(value):
            answer = given if given is not None else value
            if answer is None:
                return mo.callout(
                    mo.md("This one is marked, so you get one answer. Take a moment."),
                    kind="neutral")
            ok = answer == correct
            head = ("**Right.** " if ok
                    else f"**Not quite. The answer is _{labels[correct]}_.** ")
            return mo.callout(mo.md(head + BREAK + because),
                              kind="success" if ok else "warn")

        def summarise(value):
            answer = given if given is not None else value
            if answer is None:
                return "not answered", None
            return labels[answer], answer == correct

        return radio, render, summarise
    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    LAB_CSS = mo.Html(
        """
        <style>
          .w5-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w5-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w5-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w5-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w5-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w5-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w5-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w5-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w5-split { grid-template-columns: 1fr; } }
          .w5-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w5-split > .body p:last-child { margin-bottom: 0; }

          .w5-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w5-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w5-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w5-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w5-aside li:last-child { margin-bottom: 0; }
          .w5-aside li::marker { color: #6a5314; font-weight: 800; }
          .w5-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w5-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w5-aside .meta div:last-child { margin-bottom: 0; }
          .w5-aside .meta dt { color: #6f6f6f; }
          .w5-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w5-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w5-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w5-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }

          .w5-note { color: #6f6f6f; font-size: .85rem; margin: 2px 0 0; line-height: 1.5; }

          .w5-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
                      margin: 16px 0; }
          @media (max-width: 900px) { .w5-cards { grid-template-columns: 1fr 1fr; } }
          @media (max-width: 520px) { .w5-cards { grid-template-columns: 1fr; } }
          .w5-card { border: 1px solid #e6e6e6; border-top: 5px solid #dcdcdc;
                     border-radius: 12px; background: #fff; padding: 13px 14px; }
          .w5-card.ok { border-top-color: #2e7d32; }
          .w5-card.bad { border-top-color: #c62828; background: #fefafa; }
          .w5-card.gold { border-top-color: #f1b82d; }
          .w5-card h4 { margin: 0 0 2px; font-size: .95rem; color: #111; }
          .w5-card .where { color: #6f6f6f; font-size: .78rem; margin: 0 0 9px;
                            font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
          .w5-card p { margin: 0; color: #3a3a3a; font-size: .86rem; line-height: 1.5; }

          .w5-line { position: relative; height: 92px; margin: 20px 0 42px;
                     border-bottom: 2px solid #dcdcdc; }
          .w5-line .dot { position: absolute; bottom: -7px; width: 12px; height: 12px;
                          margin-left: -6px; border-radius: 50%; background: #9a9a9a;
                          border: 2px solid #fff; }
          .w5-line .dot.out { background: #c62828; width: 16px; height: 16px;
                              bottom: -9px; margin-left: -8px; }
          .w5-line .band { position: absolute; bottom: 0; top: 34px; background: #eef5ee;
                           border-left: 2px dashed #7cb47f; border-right: 2px dashed #7cb47f; }
          .w5-line .tag { position: absolute; top: 4px; font-size: .72rem; color: #6a5314;
                          font-weight: 800; letter-spacing: .04em; text-transform: uppercase;
                          transform: translateX(-50%); white-space: nowrap; }
          .w5-line .val { position: absolute; bottom: -34px; font-size: .78rem; color: #6f6f6f;
                          transform: translateX(-50%); }

          .w5-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                     gap: 12px; margin: 14px 0; }
          .w5-stat { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff;
                     padding: 11px 13px; }
          .w5-stat .k { color: #6a5314; font-size: .72rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .w5-stat .v { display: block; color: #111; font-size: 1.45rem; font-weight: 800;
                        line-height: 1.2; margin-top: 2px; }
          .w5-stat .why { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 3px;
                          line-height: 1.4; }
          .w5-stat.green .v { color: #2e7d32; }
          .w5-stat.red .v { color: #c62828; }

          .w5-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w5-bar { display: grid; grid-template-columns: 210px 1fr 130px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w5-bar { grid-template-columns: 110px 1fr 90px; } }
          .w5-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w5-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 26px; overflow: hidden; }
          .w5-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w5-bar.good .fill { background: #7cb47f; }
          .w5-bar.bad .fill { background: #d98080; }
          .w5-bar.gold .fill { background: #f1b82d; }
          .w5-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }

          table.w5-table { border-collapse: collapse; margin: 14px 0; font-size: .92rem;
                           width: 100%; }
          table.w5-table th, table.w5-table td { border: 1px solid #e6e6e6;
                                                 padding: 9px 13px; text-align: left;
                                                 vertical-align: top; }
          table.w5-table th { background: #fffdf5; color: #6a5314; font-size: .76rem;
                              text-transform: uppercase; letter-spacing: .04em; }
          table.w5-table td.yes { background: #edf7ee; color: #2e7d32; }
          table.w5-table td.no { background: #fdecec; color: #c62828; }
          table.w5-table code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                                font-size: .85rem; }

          .w5-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w5-report .row { display: grid; grid-template-columns: 190px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w5-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w5-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w5-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w5-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w5-report .tick { color: #2e7d32; font-weight: 800; }
          .w5-report .cross { color: #c62828; font-weight: 800; }
          .w5-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                              color: #333; font-style: italic; }
          .w5-score { display: inline-block; background: #fff3cc; border: 1px solid #f2dfaa;
                      border-radius: 8px; padding: 3px 11px; font-weight: 800; color: #62490a; }
        </style>
        """
    )
    LAB_CSS
    return (LAB_CSS,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w5-hero">
          <p class="w5-eyebrow">CSC/EE 8001 &middot; Week 5</p>
          <h1>Data That Stops Describing the World</h1>
          <p class="sub">A card with three years of groceries and petrol, nothing over
          &pound;200. This morning there is a charge for &pound;5,000. That one row could be a
          typo, a family holiday, a new job, or a terminal that has started double-charging
          everyone it touches. You delete the first and keep the second. The other two are
          telling you something about your pipeline.</p>
          <div class="w5-chips">
            <span class="w5-chip">Outliers</span>
            <span class="w5-chip">MCAR / MAR / MNAR</span>
            <span class="w5-chip">Distribution shift</span>
            <span class="w5-chip-plain w5-chip">Checks are marked</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <h2>Before we start</h2>
        <div class="w5-split">
          <div class="body">
            <p>Telling those four apart takes a minute of looking at the actual row. Getting
            it wrong costs you either a real event or a month of quietly corrupted data, and
            the training loss will not mention either.</p>
            <p>That is the shape of the week. A model never sees a customer. It sees a row of
            fourteen numbers and a label, so it inherits every decision made while that row
            was collected: who got measured, which fields somebody could be bothered to fill
            in, what the sensor did on the day it was failing.</p>
            <p>Three things go wrong, each with its own literature and its own remedy. Values
            that do not belong. Values that are not there. And a dataset that was accurate
            until the world it described moved on.</p>
            <p>The third is why this is a systems course rather than a statistics one.
            Covariate shift does not raise an exception. Your dashboards stay green because
            they are measuring the right things: the service really is returning 200s at the
            usual latency. It is the answers inside them that are getting worse.</p>
          </div>
          <aside class="w5-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Give four reasons a value can be an outlier, and say why the response
              differs for each.</li>
              <li>Apply Tukey's fences and a z-score, and say which breaks on skewed data
              and why.</li>
              <li>Classify missingness as MCAR, MAR or MNAR, and say what each permits.</li>
              <li>Say what complete-case deletion does to the composition of a dataset.</li>
              <li>Tell covariate, concept and prior shift apart from monitoring alone.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 45 min</dd></div>
              <div><dt>Before this</dt><dd>Weeks 1 to 4</dd></div>
              <div><dt>Marked?</dt><dd>checks and quiz, one answer each</dd></div>
            </div>
          </aside>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w5-question">
          <span class="lbl">The question this lab answers</span>
          <p>"Nothing is throwing errors and the model is getting worse. What do I
          measure?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: Four reasons a value looks wrong""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Back to that £5,000 charge.

    Flagging it took eight lines of pandas: the amount is far from everything else on the
    account, which is all an outlier is. A point far from the rest of the distribution. That
    definition is correct and it is not much use on its own, because it says nothing about
    what to do next.

    Here are the four things it could be. The row is byte-for-byte identical in all four.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w5-cards">
          <div class="w5-card bad">
            <h4>A data entry error</h4>
            <p class="where">drop or correct</p>
            <p>The charge was £50 and somebody's finger slipped. The value was never real,
            so there is nothing in it to preserve.</p>
          </div>
          <div class="w5-card ok">
            <h4>A rare but legitimate event</h4>
            <p class="where">keep</p>
            <p>Four plane tickets. Unusual for this cardholder and entirely true. Delete it
            and you have taught the model to disbelieve things that happen.</p>
          </div>
          <div class="w5-card gold">
            <h4>The generating process changed</h4>
            <p class="where">investigate upstream</p>
            <p>New job, higher income, different spending. The point is not anomalous in the
            new world; your idea of normal is stale. Distribution shift, arriving one row at
            a time.</p>
          </div>
          <div class="w5-card bad">
            <h4>A failing measurement system</h4>
            <p class="where">fix the instrument</p>
            <p>A terminal double-charging everything it touches. The value describes your
            hardware, not your customer, and there will be thousands more of them.</p>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Two of those four say nothing about the cardholder. "The process changed" and "the
    instrument failed" are statements about your pipeline. An outlier check is often the
    cheapest monitoring you have on data collection itself, which is a better reason to run
    one than cleaning is.

    It is also why `df = df[df.amount < threshold]` as a preprocessing step is a bad habit. It
    handles the first case correctly and destroys the evidence in the other three.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q1, q1_render, q1_sum = ask(
        "You find forty rows sitting far from the rest of the distribution. What is the right "
        "first move?",
        {
            "Drop them. Outliers degrade model performance": "a",
            "Keep them all. The tails are where the interesting cases live": "b",
            "Work out which of the four causes applies, because the response differs for each": "c",
            "Replace them with the column median to preserve the sample size": "d",
        },
        "c",
        "Outlying and erroneous are different properties. A typo should go; a genuine rare "
        "event has to stay or you train the model to reject reality; a failing sensor is a "
        "hardware ticket; a changed process means your training distribution is going stale. "
        "The only way to tell is to open a handful of the actual rows and look.",
        key="q1",
    )
    q1
    return q1, q1_render, q1_sum


@app.cell(hide_code=True)
def _(q1, q1_render):
    q1_render(q1.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md('## Part 2: Two ways to put a number on "unusual"')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Both standard univariate methods are one line of code. They disagree in a way that
    matters, and the disagreement is the thing worth understanding.

    **Tukey's fences** work from order statistics. Sort the values, take the first quartile
    $Q_1$ and the third $Q_3$, and call the gap between them the interquartile range. Flag
    anything below $Q_1 - 1.5 \times \mathrm{IQR}$ or above $Q_3 + 1.5 \times \mathrm{IQR}$.
    These are the whiskers on a boxplot.

    **The z-score** works from moments. Subtract the mean, divide by the standard deviation,
    flag anything beyond about three.

    The slider moves one value in a nine-point sample.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    odd = mo.ui.slider(
        12, 90, value=saved.get("odd", 50), step=1, disabled=locked,
        label="The last reading", show_value=True,
    )
    mo.vstack([
        mo.md("The other eight never change: **5, 7, 8, 9, 10, 12, 15, 18**."),
        odd,
    ])
    return (odd,)


@app.cell(hide_code=True)
def _(odd):
    import statistics as _stats

    BASE = [5, 7, 8, 9, 10, 12, 15, 18]
    points = sorted(BASE + [odd.value])

    # Tukey's hinges: split at the median, then take the median of each half. With
    # nine points the middle value belongs to neither half.
    _half = len(points) // 2
    q1_val = _stats.median(points[:_half])
    q3_val = _stats.median(points[_half + 1:])
    iqr = q3_val - q1_val
    low_fence = q1_val - 1.5 * iqr
    high_fence = q3_val + 1.5 * iqr
    tukey_flags = odd.value > high_fence or odd.value < low_fence

    # The z-score, computed on the sample including the suspect point, which is how
    # it is normally done and is exactly where the trouble comes from.
    mean_val = sum(points) / len(points)
    sd_val = _stats.pstdev(points)
    z_val = (odd.value - mean_val) / sd_val if sd_val else 0.0
    z_flags = abs(z_val) > 3
    return (
        high_fence,
        iqr,
        low_fence,
        mean_val,
        points,
        q1_val,
        q3_val,
        sd_val,
        tukey_flags,
        z_flags,
        z_val,
    )


@app.cell(hide_code=True)
def _(LAB_CSS, high_fence, low_fence, mo, odd, points):
    _ = LAB_CSS
    _lo, _hi = 0, 95

    def _at(v):
        return max(0.0, min(100.0, (v - _lo) / (_hi - _lo) * 100.0))

    _band_left = _at(max(low_fence, _lo))
    _band_right = _at(min(high_fence, _hi))
    _dots = ""
    for _p in points:
        _cls = "dot out" if (_p > high_fence or _p < low_fence) else "dot"
        _dots += f'<span class="{_cls}" style="left:{_at(_p):.2f}%"></span>'
    mo.vstack([
        mo.Html(
            f"""
            <div class="w5-line">
              <span class="band" style="left:{_band_left:.2f}%;
                    width:{max(0.0, _band_right - _band_left):.2f}%"></span>
              <span class="tag" style="left:{_band_left:.2f}%">lower fence</span>
              <span class="val" style="left:{_band_left:.2f}%">{low_fence:.1f}</span>
              <span class="tag" style="left:{_band_right:.2f}%">upper fence</span>
              <span class="val" style="left:{_band_right:.2f}%">{high_fence:.1f}</span>
              {_dots}
            </div>
            """
        ),
        mo.md(f"Green is inside Tukey's fences. Your value is at **{odd.value}**."),
    ])
    return


@app.cell(hide_code=True)
def _(
    LAB_CSS,
    high_fence,
    iqr,
    mean_val,
    mo,
    q1_val,
    q3_val,
    sd_val,
    tukey_flags,
    z_flags,
    z_val,
):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w5-grid">
          <div class="w5-stat">
            <span class="k">Q1 to Q3</span>
            <span class="v">{q1_val:.1f} to {q3_val:.1f}</span>
            <span class="why">the middle half of the sample</span>
          </div>
          <div class="w5-stat">
            <span class="k">Interquartile range</span>
            <span class="v">{iqr:.1f}</span>
            <span class="why">fences sit 1.5 of these outside each quartile</span>
          </div>
          <div class="w5-stat {'red' if tukey_flags else 'green'}">
            <span class="k">Tukey's fences</span>
            <span class="v">{'flagged' if tukey_flags else 'not flagged'}</span>
            <span class="why">upper fence is {high_fence:.1f}</span>
          </div>
          <div class="w5-stat {'red' if z_flags else 'green'}">
            <span class="k">z-score</span>
            <span class="v">{'flagged' if z_flags else 'not flagged'}</span>
            <span class="why">z = {z_val:.2f}; mean {mean_val:.1f}, sd {sd_val:.1f};
            threshold 3</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(high_fence, mo, odd, tukey_flags, z_flags, z_val):
    if tukey_flags and not z_flags:
        _msg = (
            f"Tukey flags **{odd.value}**. The z-score puts it at **{z_val:.2f}** and lets it "
            "through.\n\n"
            "The suspect point is in the sample used to compute the mean and the standard "
            "deviation. It pulls the mean towards itself and inflates the denominator, so the "
            "further out it goes the more it raises the bar it is being measured against. "
            "This is called **masking**, and with a cluster of outliers it compounds: they "
            "mask each other.\n\n"
            "Quartiles are order statistics. Moving one extreme value does not move the middle "
            "of a sorted list. The usual way to say this is that the median has a breakdown "
            "point of 50 per cent and the mean has one of zero."
        )
        _kind = "success"
    elif tukey_flags and z_flags:
        _msg = (
            f"Both flag it. At **{odd.value}** the point is extreme enough to clear even its "
            "own inflated threshold. Bring it back to around 50 and the two methods part "
            "company."
        )
        _kind = "info"
    else:
        _msg = (
            f"**{odd.value}** is inside both. Tukey starts flagging past **{high_fence:.1f}**. "
            "Keep pushing after that and see how much further you have to go before the "
            "z-score agrees."
        )
        _kind = "neutral"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "When neither works: more than one column": mo.md(
            r"""
Both methods above want a single column. Real tables have fifty, and a row can be perfectly
ordinary in every one of them and still be an impossible combination: age 7, income £90,000,
twenty years of driving experience. No univariate test will ever see that.

**k-nearest-neighbour distance.** Measure the distance to your $k$ nearest neighbours. Dense
neighbourhood, low score; if even your closest neighbour is far away, high score. Local
Outlier Factor refines it by comparing your density to your neighbours' density, which copes
with datasets that have naturally dense and sparse regions.

The catch is the curse of dimensionality. As dimensions grow, the ratio between the nearest
and the furthest neighbour tends towards 1, so "distance to neighbours" stops separating
anything. That is a property of high-dimensional space, not a tuning problem, and it is why
people reach for the next two.

**Isolation Forest.** Build random trees by picking a random feature and a random split
point. Points in sparse regions get isolated into their own leaf after very few splits, so
the average path length to isolate a point is the anomaly score. Cheap, copes with many
dimensions, needs no distance metric.

**Autoencoders.** Train a network to reproduce its own input through a narrow bottleneck.
Train it mostly on normal data and it becomes good at reconstructing normal patterns; feed it
something structurally unlike anything it saw and the reconstruction error is large. The
error is the score. This is the standard move for images, audio and sensor streams, where
handcrafting a distance is hopeless.

For both of the last two, the representation matters more than the algorithm. Run k-NN on raw
pixels and you are measuring brightness. Run it on embeddings from a trained network and you
are measuring something closer to content.
            """
        ),
    })
    return


@app.cell(hide_code=True)
def _(ask):
    q2, q2_render, q2_sum = ask(
        "You are screening a column of household incomes. The distribution is strongly "
        "right-skewed: most households are modest, a long tail earns far more. Which method?",
        {
            "The z-score, since income is continuous": "a",
            "Tukey's fences, since the mean and standard deviation are pulled by the tail": "b",
            "Either. On the same data they flag the same points": "c",
        },
        "b",
        "The tail is a real feature of income, not contamination, and it inflates both the "
        "mean and the standard deviation, so a z-score goes quiet exactly where you wanted it "
        "to speak. Quartiles do not care how extreme the tail is, only how many points are in "
        "it. In practice people often log-transform income first, which makes the distribution "
        "roughly symmetric and brings the z-score back into play.",
        key="q2",
    )
    q2
    return q2, q2_render, q2_sum


@app.cell(hide_code=True)
def _(q2, q2_render):
    q2_render(q2.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: Outlier detection and anomaly detection""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    These two get used interchangeably and they describe different setups.

    **Outlier detection** is retrospective. You hold the whole dataset. Which of these 10,000
    rows are unusual relative to the other 9,999? Every method above fits this, because they
    all need the sample in order to compute quartiles, densities or splits.

    **Anomaly detection** is prospective. You learned what normal looked like during training.
    A new row arrives at 03:14 and the question is whether it came from that distribution. You
    cannot recompute quartiles on a sample of one.

    Turning the first into the second is mechanical, and worth writing down because it is the
    shape of every production anomaly detector:

    1. Fit the scorer on reference data you believe is clean.
    2. Freeze it, and score that reference data to get the distribution of normal scores.
    3. Pick a threshold from that distribution, the 99.5th percentile say, chosen by
       how many false alarms the people on call will tolerate.
    4. In production, score each arriving row against the frozen threshold.

    Step three is the one that gets skipped, and it decides whether anybody is still reading
    the alerts in six weeks.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q3, q3_render, q3_sum = ask(
        "What actually separates outlier detection from anomaly detection?",
        {
            "Outlier methods are statistical; anomaly methods are learned": "a",
            "Outlier detection scores rows against the dataset they sit in; anomaly detection scores new rows against a frozen notion of normal": "b",
            "Anomalies are always errors; outliers are sometimes legitimate": "c",
        },
        "b",
        "It is about what is available when you ask, not which maths you use. Isolation "
        "Forest will do either job. Over a dataset you hold, you can ask what is unusual "
        "relative to the rest of it. In production you have one row and a scorer fitted "
        "earlier, and the threshold has to have been chosen in advance.",
        key="q3",
    )
    q3
    return q3, q3_render, q3_sum


@app.cell(hide_code=True)
def _(q3, q3_render):
    q3_render(q3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: Why a value is missing decides what you may do""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The instinct on seeing a null is to ask what to put there. The prior question is why it is
    empty, because the answer decides whether imputation is valid at all.

    Rubin's 1976 taxonomy is the standard vocabulary. The names are unhelpfully similar, so
    anchor each one to an example and keep it.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <table class="w5-table">
          <tr>
            <th>Mechanism</th>
            <th>Missingness depends on</th>
            <th>Example</th>
            <th>What it permits</th>
          </tr>
          <tr>
            <td><strong>MCAR</strong><br>missing completely at random</td>
            <td>Nothing in the data</td>
            <td>A scanner jams and destroys a batch of returned forms</td>
            <td class="yes">Deletion and imputation are both unbiased. You lose precision,
            not validity.</td>
          </tr>
          <tr>
            <td><strong>MAR</strong><br>missing at random</td>
            <td>Observed variables only</td>
            <td>Younger respondents skip the income question, and you recorded age</td>
            <td class="yes">Imputation is valid if you condition on the variables that
            explain it. Naive deletion is biased.</td>
          </tr>
          <tr>
            <td><strong>MNAR</strong><br>missing not at random</td>
            <td>The unobserved value itself</td>
            <td>High earners decline to state their income</td>
            <td class="no">Neither is safe from the data alone. You need an explicit model
            of the missingness, or information from outside the dataset.</td>
          </tr>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    MNAR is the one to be frightened of, and the mechanism of the damage is worth spelling
    out. If the people declining are the high earners, every income you can observe is drawn
    from the lower part of the distribution. Impute the observed mean into the blanks and the
    error is not noise, it is bias: wrong in the same direction every time. Your dataset now
    says the population is poorer than it is, and no diagnostic run on it will say otherwise,
    because the evidence you would need is exactly what is missing.

    One more thing that catches people out. **MAR and MNAR are not properties of the world,
    they are properties of the data you collected.** The same real process is MAR if you
    recorded the variable explaining the missingness and MNAR if you did not. That is not a
    technicality: it makes "record why a field is blank" a design decision with statistical
    consequences, and one that has to be made before collection rather than after.

    Three cases. One answer each.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    m1, m1_render, m1_sum = ask(
        "**1.** A hospital dataset has a lab result column. The test is expensive, so it is "
        "ordered mainly for patients who already present as seriously ill. Everyone else has a "
        "null. The dataset also contains triage severity at admission.",
        {"MCAR": "mcar", "MAR": "mar", "MNAR": "mnar"},
        "mar",
        "Ordering depends on how ill the patient looked, and triage severity is in the "
        "dataset, so the missingness is explained by an observed variable. Condition on it and "
        "imputation is defensible. Drop that column from the extract and the identical "
        "clinical situation becomes MNAR, because the only thing explaining the blank is now "
        "something you no longer hold. This is the example that shows the classification "
        "depends on your schema, not on the hospital.",
        key="m1",
    )
    m1
    return m1, m1_render, m1_sum


@app.cell(hide_code=True)
def _(m1, m1_render):
    m1_render(m1.value)
    return


@app.cell(hide_code=True)
def _(ask):
    m2, m2_render, m2_sum = ask(
        "**2.** Paper surveys are returned by post. A sorting machine at the depot destroys one "
        "sack. Those responses never arrive.",
        {"MCAR": "mcar", "MAR": "mar", "MNAR": "mnar"},
        "mcar",
        "The machine had no access to the contents and no preference about whose form it "
        "destroyed, so nothing about the respondent changed the probability of loss. This is "
        "the only mechanism where complete-case deletion costs you nothing but statistical "
        "power. It is also the rarest in practice: most real missingness has a reason.",
        key="m2",
    )
    m2
    return m2, m2_render, m2_sum


@app.cell(hide_code=True)
def _(m2, m2_render):
    m2_render(m2.value)
    return


@app.cell(hide_code=True)
def _(ask):
    m3, m3_render, m3_sum = ask(
        "**3.** An app asks for a star rating. People who are mildly satisfied ignore the "
        "prompt. The ones who respond are either delighted or furious.",
        {"MCAR": "mcar", "MAR": "mar", "MNAR": "mnar"},
        "mnar",
        "Whether somebody answers depends on what their answer would have been. The middle of "
        "the distribution is missing precisely because it is the middle, and no column you "
        "hold reconstructs it. Imputing the observed mean inherits the J-shaped bias you were "
        "trying to remove. The honest options are to state the limitation, or to go and sample "
        "the quiet majority deliberately instead of waiting for volunteers.",
        key="m3",
    )
    m3
    return m3, m3_render, m3_sum


@app.cell(hide_code=True)
def _(m3, m3_render):
    m3_render(m3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: What complete-case deletion costs""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    `df.dropna()` is one call and it is the most common thing anybody does about missing data.
    It is defensible under MCAR. Under MAR it changes the composition of the dataset, and the
    change does not appear in any summary statistic you are likely to look at.

    Ten thousand customers. Eight thousand arrived through a sign-up route that has existed
    for years and makes the field required. Two thousand came through a newer route where the
    same field is optional.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    gap = mo.ui.slider(
        5, 85, value=saved.get("gap", 50), step=5, disabled=locked,
        label="How often the newer route leaves the field blank (per cent)", show_value=True,
    )
    gap
    return (gap,)


@app.cell(hide_code=True)
def _(gap):
    OLD_N, NEW_N = 8000, 2000
    OLD_BLANK = 0.04                      # the established route, nearly always complete

    old_left = round(OLD_N * (1 - OLD_BLANK))
    new_left = round(NEW_N * (1 - gap.value / 100.0))
    total_left = old_left + new_left

    share_before = NEW_N / (OLD_N + NEW_N) * 100
    share_after = new_left / total_left * 100 if total_left else 0.0
    rows_lost = (OLD_N + NEW_N) - total_left
    return (
        NEW_N,
        OLD_N,
        new_left,
        old_left,
        rows_lost,
        share_after,
        share_before,
        total_left,
    )


@app.cell(hide_code=True)
def _(
    LAB_CSS,
    NEW_N,
    mo,
    new_left,
    rows_lost,
    share_after,
    share_before,
    total_left,
):
    _ = LAB_CSS
    _drop = share_before - share_after
    mo.Html(
        f"""
        <div class="w5-bars">
          <div class="w5-bar gold">
            <span class="t">Newer route, before dropna</span>
            <span class="track"><span class="fill" style="width:{share_before:.1f}%"></span></span>
            <span class="n">{share_before:.1f}% of rows</span>
          </div>
          <div class="w5-bar {'bad' if _drop > 5 else 'good'}">
            <span class="t">Newer route, after dropna</span>
            <span class="track"><span class="fill" style="width:{share_after:.1f}%"></span></span>
            <span class="n">{share_after:.1f}% of rows</span>
          </div>
        </div>
        <div class="w5-grid">
          <div class="w5-stat">
            <span class="k">Rows dropped</span>
            <span class="v">{rows_lost:,}</span>
            <span class="why">of 10,000</span>
          </div>
          <div class="w5-stat">
            <span class="k">Rows remaining</span>
            <span class="v">{total_left:,}</span>
            <span class="why">a respectable sample size</span>
          </div>
          <div class="w5-stat {'red' if _drop > 5 else 'green'}">
            <span class="k">Newer route remaining</span>
            <span class="v">{new_left:,}</span>
            <span class="why">was {NEW_N:,}</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, new_left, share_after, share_before, total_left):
    _drop = share_before - share_after
    if _drop < 3:
        _msg = (
            "Close to MCAR, and deletion is close to harmless here: you lose sample size and "
            "the mix survives. Push the slider further to leave that regime."
        )
        _kind = "info"
    else:
        _msg = (
            f"You still have **{total_left:,}** rows. Nothing in `df.shape`, `df.describe()` "
            "or your validation accuracy will suggest anything is wrong.\n\n"
            f"The newer route has gone from **{share_before:.0f}%** of the data to "
            f"**{share_after:.0f}%**, which is {new_left:,} people. You did not decide to train "
            "mainly on long-standing customers. `dropna()` decided it as a side effect.\n\n"
            "Then the model serves both routes equally. Headline accuracy is an average "
            "weighted by group size, so a group that shrank to a tenth of the data can be "
            "served badly for months without moving the number anyone watches. Per-group "
            "evaluation is the only thing that catches it, and only if you kept the group "
            "label."
        )
        _kind = "warn"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "The alternatives, and what each one costs": mo.md(
            r"""
**Mean, median or mode imputation.** One line, and it compresses the variance of that column:
every imputed row sits exactly at the centre. Anything downstream will be overconfident about
the column, and correlations involving it are attenuated. Fine for a quick baseline, rarely
fine for anything you report.

**Model-based imputation.** Predict the missing column from the others. MICE (multiple
imputation by chained equations) does this iteratively and produces *several* completed
datasets, so the uncertainty introduced by imputing survives into your final error bars
instead of vanishing. Single imputation hides that uncertainty entirely.

**A missingness indicator.** Keep the imputed value and add a binary column that is 1 where
the original was null. If the fact of being missing carries signal, and under MAR and MNAR
it usually does, the model can use it directly instead of being misled by your fabricated value.
Cheap, and it preserves information every other method discards.

**Drop the column.** At 95 per cent null you do not have a sparse column, you have a handful
of observations and an imputation rule. Keeping it mostly means training on the rule.

**Fix the collection.** A field blank half the time on one route is usually a form with a bad
default or a validation rule that never fires. That is a day's work upstream that removes the
problem permanently, against a modelling workaround you maintain forever.

One rule holds for all of them: **fit the imputer on the training split only.** Computing a
median over the full dataset and splitting afterwards leaks test information into training,
in exactly the way Week 4's resampling example did.
            """
        ),
    })
    return


@app.cell(hide_code=True)
def _(ask):
    q4, q4_render, q4_sum = ask(
        "Why is complete-case deletion risky even when thousands of rows remain?",
        {
            "Smaller training sets always produce worse models": "a",
            "Whoever had the nulls is now under-represented, so you silently changed the population the model learns from": "b",
            "Dropping rows invalidates the train/test split": "c",
        },
        "b",
        "Nulls cluster: by sign-up route, by device, by region, by clinic, by age. Deleting "
        "them is not random thinning, it is a reweighting of the population towards whoever "
        "fills forms in completely. Sample size tells you nothing about it, and neither does "
        "aggregate accuracy, because the group that shrank contributes proportionally less to "
        "that average.",
        key="q4",
    )
    q4
    return q4, q4_render, q4_sum


@app.cell(hide_code=True)
def _(q4, q4_render):
    q4_render(q4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 6: When the world stops matching the training set""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Supervised learning assumes training and deployment data come from the same joint
    distribution $P(X, Y)$. Every accuracy figure you have ever quoted is conditional on that,
    and deployed systems break it routinely. The standard example is a model trained on 2019
    retail behaviour and run through 2020: not a line of code changed, and the inputs stopped
    meaning what they had meant.

    "The distribution changed" is not actionable. The joint factorises two ways, and which
    factor moved decides what you can do about it.

    $$P(X, Y) = P(Y \mid X)\,P(X) = P(X \mid Y)\,P(Y)$$
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w5-cards">
          <div class="w5-card gold">
            <h4>Covariate shift</h4>
            <p class="where">P(X) moves, P(Y|X) fixed</p>
            <p>The inputs change; the rule mapping input to output does not. A house-price
            model trained on suburban stock, now pricing city flats. It is right wherever it
            has seen examples and extrapolating where it has not.</p>
          </div>
          <div class="w5-card bad">
            <h4>Concept shift</h4>
            <p class="where">P(Y|X) moves</p>
            <p>The same input now implies a different output. The relationship between
            financial characteristics and default, after an economic shock. The expensive
            one, because the target itself moved.</p>
          </div>
          <div class="w5-card gold">
            <h4>Prior probability shift</h4>
            <p class="where">P(Y) moves, P(X|Y) fixed</p>
            <p>Each class still looks exactly as it did; the proportions changed. A
            screening model built on general-population prevalence, deployed in a specialist
            clinic.</p>
          </div>
          <div class="w5-card">
            <h4>In practice, several at once</h4>
            <p class="where">and gradually</p>
            <p>Real shifts are mixed and often slow. The three questions are still worth
            asking separately, because the remedies differ and only one of them is cheap.</p>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Prior shift, with the arithmetic

    Prior shift is the one people find hardest to believe, so here it is in numbers.

    A test has fixed operating characteristics: **sensitivity 90 per cent** (it catches 90 of
    every 100 genuine cases) and **specificity 95 per cent** (it wrongly flags 5 of every 100
    negatives). Those are properties of the test and nothing below changes them.

    The only thing moving is prevalence. Watch the positive predictive value.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    prevalence = mo.ui.slider(
        1, 40, value=saved.get("prevalence", 1), step=1, disabled=locked,
        label="Prevalence: cases per 100 people in the room", show_value=True,
    )
    prevalence
    return (prevalence,)


@app.cell(hide_code=True)
def _(prevalence):
    PEOPLE = 10000
    SENSITIVITY = 0.90
    SPECIFICITY = 0.95

    ill = round(PEOPLE * prevalence.value / 100.0)
    healthy = PEOPLE - ill
    caught = round(ill * SENSITIVITY)
    false_alarms = round(healthy * (1 - SPECIFICITY))
    flagged = caught + false_alarms
    trust = caught / flagged * 100 if flagged else 0.0
    return caught, false_alarms, flagged, healthy, ill, trust


@app.cell(hide_code=True)
def _(LAB_CSS, caught, false_alarms, flagged, healthy, ill, mo, trust):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w5-grid">
          <div class="w5-stat">
            <span class="k">Genuine cases</span>
            <span class="v">{ill:,}</span>
            <span class="why">of 10,000 tested</span>
          </div>
          <div class="w5-stat green">
            <span class="k">True positives</span>
            <span class="v">{caught:,}</span>
            <span class="why">90% of cases, unchanged</span>
          </div>
          <div class="w5-stat red">
            <span class="k">False positives</span>
            <span class="v">{false_alarms:,}</span>
            <span class="why">5% of the {healthy:,} negatives, unchanged</span>
          </div>
          <div class="w5-stat {'green' if trust >= 50 else 'red'}">
            <span class="k">Positive predictive value</span>
            <span class="v">{trust:.0f}%</span>
            <span class="why">{caught:,} true of {flagged:,} flagged</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, prevalence, trust):
    if prevalence.value <= 2:
        _msg = (
            f"Sensitivity 90, specificity 95, and a positive result means a **{trust:.0f} per "
            "cent** chance the person has it. Four in five of the people you flag are fine and "
            "have just been told otherwise.\n\n"
            "The arithmetic is unavoidable: 5 per cent of a large negative population "
            "outnumbers 90 per cent of a small positive one. This is the base rate fallacy, "
            "and it is why screening for rare conditions needs specificity far beyond what "
            "sounds impressive in a paper. **Now move the slider to 20.**"
        )
        _kind = "danger"
    elif prevalence.value >= 15:
        _msg = (
            f"Identical test. Sensitivity still 90, specificity still 95. Positive predictive "
            f"value is now **{trust:.0f} per cent**.\n\n"
            "This cuts both ways and the second direction is the dangerous one. Validate a "
            "model in a specialist clinic where prevalence is high and every metric looks "
            "excellent. Deploy it to general screening and it drowns in false positives while "
            "every offline test still passes, because your test set has the clinic's "
            "prevalence baked into it."
        )
        _kind = "success"
    else:
        _msg = (
            f"Positive predictive value is **{trust:.0f} per cent**. Compare the two ends, 1 in "
            "100 and 20 in 100. The test is identical at both."
        )
        _kind = "info"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Telling them apart from monitoring

    Nobody tells you which shift you have. You get a degrading model and whatever telemetry
    you set up in advance. Three measurements separate the three cases.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <table class="w5-table">
          <tr>
            <th>Measurement</th>
            <th>Covariate</th>
            <th>Concept</th>
            <th>Prior</th>
          </tr>
          <tr>
            <td>Input distribution against training, per feature: a
            <code>KS test</code> or population stability index</td>
            <td class="no">shifted</td>
            <td class="yes">unchanged</td>
            <td class="yes">unchanged</td>
          </tr>
          <tr>
            <td>Accuracy on a labelled slice the model has always had plenty of</td>
            <td class="yes">holds</td>
            <td class="no">drops</td>
            <td class="yes">holds</td>
          </tr>
          <tr>
            <td>Observed positive rate against the training base rate</td>
            <td class="yes">roughly stable</td>
            <td class="no">moves</td>
            <td class="no">moves</td>
          </tr>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The second row does most of the work, and it is the one teams most often cannot run,
    because it needs **labels on recent data**. That is usually the real constraint: input
    drift is free to measure, and accuracy drift needs somebody to go and find out what
    actually happened. Budget for that before you need it rather than after.

    Three teams describe what they see without naming the cause. Classify each.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    s1, s1_render, s1_sum = ask(
        "**1.** \"We price residential property. Training was mostly detached suburban houses. "
        "This quarter we are mostly being asked about one-bed city flats, which were about 2 "
        "per cent of training. We re-scored last year's suburban sales: errors unchanged.\"",
        {
            "Covariate shift": "cov",
            "Concept shift": "con",
            "Prior probability shift": "pri",
        },
        "cov",
        "The input distribution moved, and re-scoring the suburban sales demonstrates that "
        "P(Y|X) is intact. The model is extrapolating into a region where it has almost no "
        "training support. Importance weighting helps a little, but you cannot upweight your "
        "way out of 2 per cent coverage: no weight applied to almost no examples is still "
        "almost nothing. What this needs is flats in the training set.",
        key="s1",
    )
    s1
    return s1, s1_render, s1_sum


@app.cell(hide_code=True)
def _(s1, s1_render):
    s1_render(s1.value)
    return


@app.cell(hide_code=True)
def _(ask):
    s2, s2_render, s2_sum = ask(
        "**2.** \"Loan default model. The application distribution is statistically "
        "indistinguishable from last year on every feature we monitor. But applicants we score "
        "as low risk are defaulting at three times the rate they used to.\"",
        {
            "Covariate shift": "cov",
            "Concept shift": "con",
            "Prior probability shift": "pri",
        },
        "con",
        "Inputs unchanged and the model now wrong about rows it used to get right, so P(Y|X) "
        "itself moved. Note what that does to input-drift monitoring: it would have reported "
        "green the whole time. Reweighting historical data cannot recover the new relationship "
        "because the new relationship is not in it. This needs fresh labels and retraining, "
        "and until the loans mature you do not have them.",
        key="s2",
    )
    s2
    return s2, s2_render, s2_sum


@app.cell(hide_code=True)
def _(s2, s2_render):
    s2_render(s2.value)
    return


@app.cell(hide_code=True)
def _(ask):
    s3, s3_render, s3_sum = ask(
        "**3.** \"Our screening model was trained on general-population data with about 1 per "
        "cent prevalence. It now runs in a referral clinic. Within each class the feature "
        "distributions match training, and the likelihood of disease given a symptom profile is "
        "what it was. Roughly 20 per cent of arrivals have the condition.\"",
        {
            "Covariate shift": "cov",
            "Concept shift": "con",
            "Prior probability shift": "pri",
        },
        "pri",
        "P(X|Y) is stated to be unchanged and only P(Y) moved, which is prior shift by "
        "definition. It is also the cheapest to fix: with an estimate of the new prevalence "
        "you can move the decision threshold or rescale the predicted probabilities, without "
        "retraining anything. EM-based prior estimation will even recover the new base rate "
        "from unlabelled data.",
        key="s3",
    )
    s3
    return s3, s3_render, s3_sum


@app.cell(hide_code=True)
def _(s3, s3_render):
    s3_render(s3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### What each one needs

    | Shift | Remedy | Why it works, and where it stops |
    | - | - | - |
    | Covariate | Importance weighting by the density ratio, plus targeted collection in the new region | P(Y\|X) is intact, so correctly reweighted old data is still informative. It fails where training support is near zero. |
    | Concept | New labelled data and retraining, or online adaptation | The mapping changed. Reweighting old data reweights a relationship that no longer holds. There is no cheap version. |
    | Prior | Estimate the new base rate, then recalibrate or move the threshold | P(X\|Y) is unchanged, so the classes separate exactly as before. Only the optimal position of the boundary moved. |

    For all three, you only get to choose a remedy if you noticed. Input drift monitoring is
    cheap and catches covariate shift early. Accuracy on a labelled slice is expensive and is
    the only thing that catches concept shift at all.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 7: Your decision""")
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w5-question">
          <span class="lbl">The situation</span>
          <p>"The delivery-time estimator has been live eight months and it is drifting. It
          used to be within ten minutes; it is now out by half an hour and support is getting
          complaints. No errors, no deploys since launch, no schema changes. We have a month
          of recent deliveries logged, but nobody has joined them to actual arrival times
          yet."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "Retrain on the last month. It is the freshest data we have": "retrain",
        "Compare the recent input distribution against training, and re-score the old routes we do have labels for": "diagnose",
        "Add features. The model is clearly underspecified for the job now": "features",
        "Widen the output to a time window so we stop being measurably wrong": "widen",
    }
    decision_form = (
        mo.md("""
        {choice}

        {why}
        """)
        .batch(
            choice=mo.ui.radio(
                options=_choices,
                value=pick(_choices, _saved.get("choice")),
                disabled=locked,
                label="**What do you do first?**",
            ),
            why=mo.ui.text_area(
                value=_saved.get("why", ""),
                disabled=locked,
                placeholder="What you would measure, and what you would conclude from each possible result.",
                label="**Why?** This one is not marked, and you can change it as often as you like.",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_disabled=locked,
            submit_button_label="Submit my decision",
            bordered=True,
            validate=lambda v: (
                "Choose one of the four."
                if not v or v.get("choice") is None
                else "Write your reasoning, then submit."
                if not (v.get("why") or "").strip()
                else None
            ),
        )
    )
    decision_form
    return (decision_form,)


@app.cell(hide_code=True)
def _(decision_form, mo, saved):
    _answer = decision_form.value or saved.get("decision")
    mo.stop(
        not _answer,
        mo.callout(mo.md("Pick an answer, say why, then press **Submit my decision**."),
                   kind="warn"),
    )
    decision_choice = _answer["choice"]
    decision_why = _answer["why"].strip()
    return decision_choice, decision_why


@app.cell(hide_code=True)
def _(decision_choice, mo):
    _notes = {
        "retrain": (
            "It may well end up being the answer, but read the constraint again: the recent "
            "deliveries have no labels yet. Supervised retraining needs actual arrival times, "
            "so this is weeks away and somebody has to build that join first.\n\n"
            "There is also a failure mode worth naming. If the cause is that you have expanded "
            "into dense urban routes, retraining on a month of mostly-urban data gives you a "
            "model that is excellent there and worse everywhere else. You would have swapped "
            "one coverage gap for another and called it a fix."
        ),
        "diagnose": (
            "This is rows one and two of the monitoring table, and between them they identify "
            "the shift before you commit anybody's month. The input comparison is free and you "
            "can run it this afternoon. The old-routes check needs labels, but you have "
            "historical labels for those already, so it is a query rather than a project.\n\n"
            "Two outcomes, two different pieces of work. New routes look unfamiliar and old "
            "routes are still accurate: covariate shift, and you need coverage. Old routes have "
            "degraded too: something real changed. A depot moved, a courier contract, "
            "the traffic model. Only fresh labels will fix that."
        ),
        "features": (
            "The model was accurate for months, so underspecification is a hypothesis with "
            "evidence against it. Something external changed. Adding features before "
            "identifying what will usually work, in the worst way: you will find a feature "
            "that explains recent data, the metrics will improve, and you will never learn "
            "what happened. Next time you will be exactly where you are now, with one more "
            "feature to maintain."
        ),
        "widen": (
            "Legitimate as a holding action, and sometimes right for the customer: a window "
            "you can keep beats a point estimate you cannot. But it is a mitigation, not a "
            "diagnosis. The underlying error keeps growing, the window keeps widening, and the "
            "failure is now invisible to your own metrics because you redefined correct. Do it "
            "if you must, with a date on it and a diagnosis running underneath."
        ),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "All four are defensible and you are not marked on which you chose. The point is "
            "that \"the model got worse\" names a symptom, and the three shifts need three "
            "different months of work. Change your answer above if the note moved you."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(decision_choice, locked, mo, saved):
    _ = decision_choice
    _saved = saved.get("reflection") or {}
    reflect_form = (
        mo.md("{takeaway}")
        .batch(
            takeaway=mo.ui.text_area(
                value=_saved.get("takeaway", ""),
                disabled=locked,
                placeholder="I would measure ... weekly, and the reading that would make me act is ...",
                label="**Last one.** Name one quantity you would monitor weekly on a live model to catch shift early, and the reading that would make you act on it.",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_disabled=locked,
            submit_button_label="Finish the lab",
            bordered=True,
            validate=lambda v: (
                None if v and (v.get("takeaway") or "").strip()
                else "Write a sentence or two, then submit."
            ),
        )
    )
    reflect_form
    return (reflect_form,)


@app.cell(hide_code=True)
def _(mo, reflect_form, saved):
    _answer = reflect_form.value or saved.get("reflection")
    mo.stop(
        not _answer,
        mo.callout(mo.md("Answer the last question to finish the lab."), kind="warn"),
    )
    takeaway_text = _answer["takeaway"].strip()
    done = True
    return done, takeaway_text


@app.cell(hide_code=True)
def _(decision_form, gap, lab_sync, m1, m2, m3, odd, prevalence, q1, q2, q3, q4, s1, s2, s3):
    # Marked answers go through record_once, so the first answer is the one that
    # counts. Sliders and the written decision can change as often as the student likes.
    if lab_sync is not None:
        lab_sync.record_once(
            q1=q1.value, q2=q2.value, q3=q3.value, q4=q4.value,
            m1=m1.value, m2=m2.value, m3=m3.value,
            s1=s1.value, s2=s2.value, s3=s3.value,
        )
        lab_sync.record(odd=odd.value, gap=gap.value, prevalence=prevalence.value)
        if decision_form.value is not None:
            lab_sync.record(decision=decision_form.value)
    return


@app.cell(hide_code=True)
def _(lab_sync, reflect_form):
    # This form only exists once the decision is in, so it is recorded here.
    if lab_sync is not None and reflect_form.value is not None:
        lab_sync.record(reflection=reflect_form.value)
    return


@app.cell(hide_code=True)
def _(
    m1,
    m1_sum,
    m2,
    m2_sum,
    m3,
    m3_sum,
    q1,
    q1_sum,
    q2,
    q2_sum,
    q3,
    q3_sum,
    q4,
    q4_sum,
    s1,
    s1_sum,
    s2,
    s2_sum,
    s3,
    s3_sum,
):
    # One place that knows every marked answer, so the report, the score and the
    # dashboard cannot disagree.
    CHECKS = [
        ("Outliers: first move", q1_sum(q1.value)),
        ("Skewed data: which method", q2_sum(q2.value)),
        ("Outlier vs anomaly detection", q3_sum(q3.value)),
        ("Cost of complete-case deletion", q4_sum(q4.value)),
        ("Missingness: the lab test", m1_sum(m1.value)),
        ("Missingness: the destroyed post", m2_sum(m2.value)),
        ("Missingness: the star ratings", m3_sum(m3.value)),
        ("Shift: property pricing", s1_sum(s1.value)),
        ("Shift: loan defaults", s2_sum(s2.value)),
        ("Shift: the referral clinic", s3_sum(s3.value)),
    ]
    checks_right = sum(1 for _n, (_t, _ok) in CHECKS if _ok)
    checks_score = f"{checks_right}/{len(CHECKS)}"
    return CHECKS, checks_right, checks_score


@app.cell(hide_code=True)
def _(
    CHECKS,
    LAB_CSS,
    checks_score,
    decision_choice,
    decision_why,
    done,
    mo,
    odd,
    prevalence,
    takeaway_text,
    trust,
):
    _ = (LAB_CSS, done)
    _where = {
        "retrain": "Retrain on the last month",
        "diagnose": "Compare input distributions and re-score the old routes",
        "features": "Add features",
        "widen": "Widen the output to a time window",
    }

    def _mark(entry):
        _text, _ok = entry
        if _ok is None:
            return '<span class="cross">not answered</span>'
        _icon = '<span class="tick">right</span>' if _ok else '<span class="cross">wrong</span>'
        return f"{_text} &middot; {_icon}"

    _rows = "".join(
        f'<div class="row"><span class="k">{_name}</span>'
        f'<span class="v">{_mark(_entry)}</span></div>'
        for _name, _entry in CHECKS
    )
    mo.vstack([
        mo.md("## Your Week 5 report"),
        mo.Html(
            f"""
            <div class="w5-report">
              <div class="row">
                <span class="k">Marked checks</span>
                <span class="v"><span class="w5-score">{checks_score}</span></span>
              </div>
              <div class="row">
                <span class="k">Outlier value explored</span>
                <span class="v">{odd.value}</span>
              </div>
              <div class="row">
                <span class="k">Prevalence explored</span>
                <span class="v">{prevalence.value} in 100, giving a positive predictive value
                of {trust:.0f} per cent</span>
              </div>
              <div class="row">
                <span class="k">Delivery model, first move</span>
                <span class="v">{_where.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Reasoning</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">What you would monitor</span>
                <span class="v quote">{takeaway_text}</span>
              </div>
              {_rows}
            </div>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(done, get_given, locked, mo, pick, saved, set_given):
    _ = done
    QUIZ = [
        ("A temperature sensor normally reporting 20 to 30 degrees starts reporting 400. What "
         "should happen first?",
         {"Drop the row and carry on": "a",
          "Check whether the sensor has failed, because if it has, every later reading from it is suspect": "b",
          "Keep it; extreme values carry the most information": "c"},
         "b"),
        ("High earners are the ones leaving income blank, and you impute the observed mean. "
         "What have you introduced?",
         {"Random noise, which averages out across the dataset": "a",
          "Bias in a consistent direction, understating income for every imputed row": "b",
          "Nothing material; the mean is an unbiased estimator": "c"},
         "b"),
        ("Input distributions match training on every monitored feature, and the model is now "
         "wrong about cases it used to get right. Which shift, and what fixes it?",
         {"Prior shift; recalibrate using the new base rate": "a",
          "Covariate shift; apply importance weighting": "b",
          "Concept shift; nothing short of new labels and retraining": "c"},
         "c"),
    ]
    _saved = saved.get("quiz") or {}
    _given = get_given()

    def _lock(n):
        def handler(value):
            _k = "quiz" + str(n)
            if value is not None and get_given().get(_k, _saved.get(str(n))) is None:
                set_given(lambda d: dict(d, **{_k: value}))
        return handler

    quiz = mo.ui.array([
        mo.ui.radio(
            options=_options, label=f"**{_n}.** {_question}",
            value=pick(_options, _given.get("quiz" + str(_n), _saved.get(str(_n)))),
            disabled=locked or _given.get("quiz" + str(_n), _saved.get(str(_n))) is not None,
            on_change=_lock(_n),
        )
        for _n, (_question, _options, _right) in enumerate(QUIZ, 1)
    ])
    mo.vstack([
        mo.md("## Quiz"),
        mo.md("Three questions, one answer each, marked when you submit."),
        *[quiz[_i] for _i in range(len(QUIZ))],
    ], gap=1)
    return QUIZ, quiz


@app.cell(hide_code=True)
def _(CHECKS, QUIZ, checks_right, lab_sync, quiz):
    _quiz_right = sum(v == q[2] for q, v in zip(QUIZ, quiz.value))
    quiz_score = f"{_quiz_right}/{len(QUIZ)}"
    auto_score = f"{checks_right + _quiz_right}/{len(CHECKS) + len(QUIZ)}"
    if lab_sync is not None:
        lab_sync.record_once(**{str(n): v for n, v in enumerate(quiz.value, 1)})
        lab_sync.record(quiz={str(n): v for n, v in enumerate(quiz.value, 1)},
                        quiz_score=quiz_score, auto_score=auto_score)
    return auto_score, quiz_score


@app.cell(hide_code=True)
def _(done, lab_sync, locked, mo, quiz):
    _ = done
    _unanswered = sum(v is None for v in quiz.value)
    submit_button = mo.ui.run_button(
        label="Submit my work",
        kind="success",
        disabled=lab_sync is None or locked or _unanswered > 0,
        tooltip="Send your answers to your instructor",
    )
    mo.vstack([
        mo.md("## Submit your work"),
        mo.md(
            "Everything has been saving as you went. Press the button to hand the lab in. You "
            "can revise the written answers and submit again until your instructor locks the "
            "lab; the marked questions keep the answer you gave first."
            + (f" **Answer the {_unanswered} quiz question"
               f"{'s' if _unanswered > 1 else ''} above first.**" if _unanswered else "")
        ),
        submit_button,
    ])
    return (submit_button,)


@app.cell(hide_code=True)
async def _(
    auto_score,
    lab_status,
    lab_sync,
    locked,
    mo,
    quiz_score,
    reflect_form,
    saved,
    submit_button,
):
    # Runs when the button is pressed, and otherwise just says where things stand.
    if lab_sync is None:
        _msg, _kind = (
            "This copy of the lab is not connected to the course site, so it cannot be "
            "submitted from here.", "neutral")
    elif submit_button.value:
        _reply = await lab_sync.submit(
            reflection=reflect_form.value or saved.get("reflection"), finished=True)
        if _reply.get("ok"):
            _msg, _kind = (f"**Submitted.** Your instructor can see your work. "
                           f"Quiz: **{quiz_score}**. Marked answers overall: "
                           f"**{auto_score}**.", "success")
        elif _reply.get("locked"):
            _msg, _kind = ("**Not submitted.** Your instructor has locked this lab.", "danger")
        else:
            _msg, _kind = (
                f"**Not submitted:** {_reply.get('error', 'something went wrong')}. Your "
                "answers are still saved. Press **Submit my work** to try again.", "danger")
    elif lab_sync.last_submitted or lab_status.get("submitted"):
        _when = str(lab_sync.last_submitted or lab_status.get("submittedAt") or "")[:10]
        _msg, _kind = (
            f"**Submitted on {_when}.** Changed something since? Press **Submit my work** "
            "again.", "success")
    elif locked:
        _msg, _kind = ("Your instructor has locked this lab, so it can no longer be submitted.",
                       "warn")
    else:
        _msg, _kind = ("**Not submitted yet.** Press **Submit my work** when you are done.",
                       "warn")
    mo.callout(mo.md(_msg), kind=_kind)
    return


if __name__ == "__main__":
    app.run()
