import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 4 - Right Nearly Every Time, and Useless")


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
def _(locked, mo, pick, saved):
    def ask(prompt, options, correct, because, key):
        """A quick check. One answer, then the reason the right one is right.

        `because` explains the correct answer in plain words. Wrong answers are
        not picked apart one by one; the student just gets the explanation.
        """
        labels = {value: label for label, value in options.items()}
        BREAK = chr(10) + chr(10)

        radio = mo.ui.radio(options=options, label=prompt,
                            value=pick(options, saved.get(key)), disabled=locked)

        def render(value):
            if value is None:
                return mo.callout(mo.md("Pick an answer and I will tell you why."),
                                  kind="neutral")
            ok = value == correct
            head = "**That is it.** " if ok else f"**The answer is:** *{labels[correct]}*."
            return mo.callout(mo.md(head + BREAK + because),
                              kind="success" if ok else "warn")

        def summarise(value):
            if value is None:
                return "not answered", None
            return labels[value], value == correct

        return radio, render, summarise
    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    LAB_CSS = mo.Html(
        """
        <style>
          .w4-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w4-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w4-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w4-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w4-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w4-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w4-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w4-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w4-split { grid-template-columns: 1fr; } }
          .w4-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w4-split > .body p:last-child { margin-bottom: 0; }

          .w4-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w4-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w4-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w4-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w4-aside li:last-child { margin-bottom: 0; }
          .w4-aside li::marker { color: #6a5314; font-weight: 800; }
          .w4-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w4-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w4-aside .meta div:last-child { margin-bottom: 0; }
          .w4-aside .meta dt { color: #6f6f6f; }
          .w4-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w4-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w4-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w4-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }

          .w4-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w4-bar { display: grid; grid-template-columns: 210px 1fr 120px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w4-bar { grid-template-columns: 120px 1fr 90px; } }
          .w4-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w4-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 26px; overflow: hidden; }
          .w4-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w4-bar.good .fill { background: #7cb47f; }
          .w4-bar.bad .fill { background: #d98080; }
          .w4-bar.gold .fill { background: #f1b82d; }
          .w4-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }
          .w4-note { color: #6f6f6f; font-size: .85rem; margin: 2px 0 0; line-height: 1.5; }

          .w4-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
                      margin: 16px 0; }
          @media (max-width: 900px) { .w4-cards { grid-template-columns: 1fr 1fr; } }
          @media (max-width: 520px) { .w4-cards { grid-template-columns: 1fr; } }
          .w4-card { border: 1px solid #e6e6e6; border-top: 5px solid #dcdcdc;
                     border-radius: 12px; background: #fff; padding: 13px 14px; }
          .w4-card.ok { border-top-color: #2e7d32; }
          .w4-card.bad { border-top-color: #c62828; background: #fefafa; }
          .w4-card h4 { margin: 0 0 2px; font-size: .95rem; color: #111; }
          .w4-card .where { color: #6f6f6f; font-size: .78rem; margin: 0 0 9px; }
          .w4-card .big { display: block; font-size: 1.5rem; font-weight: 800; color: #111;
                          line-height: 1.15; }
          .w4-card .small { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 3px;
                            line-height: 1.4; }

          .w4-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                     gap: 12px; margin: 14px 0; }
          .w4-stat { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff;
                     padding: 11px 13px; }
          .w4-stat .k { color: #6a5314; font-size: .72rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .w4-stat .v { display: block; color: #111; font-size: 1.45rem; font-weight: 800;
                        line-height: 1.2; margin-top: 2px; }
          .w4-stat .why { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 3px; }
          .w4-stat.green .v { color: #2e7d32; }
          .w4-stat.red .v { color: #c62828; }

          table.w4-matrix { border-collapse: collapse; margin: 14px 0; font-size: .92rem; }
          table.w4-matrix th, table.w4-matrix td { border: 1px solid #e6e6e6;
                                                   padding: 9px 14px; text-align: center; }
          table.w4-matrix th { background: #fffdf5; color: #6a5314; font-size: .78rem;
                               text-transform: uppercase; letter-spacing: .04em; }
          table.w4-matrix td.hit { background: #edf7ee; font-weight: 800; }
          table.w4-matrix td.miss { background: #fdecec; font-weight: 800; }

          .w4-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w4-report .row { display: grid; grid-template-columns: 190px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w4-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w4-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w4-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w4-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w4-report .tick { color: #2e7d32; font-weight: 800; }
          .w4-report .cross { color: #c62828; font-weight: 800; }
          .w4-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                              color: #333; font-style: italic; }
        </style>
        """
    )
    LAB_CSS
    return (LAB_CSS,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w4-hero">
          <p class="w4-eyebrow">CSC/EE 8001 &middot; Week 4</p>
          <h1>Right Nearly Every Time, and Useless</h1>
          <p class="sub">A model can be right ninety-nine times out of a hundred and still be
          worth nothing. This lab is about the data underneath it: who is in it, who is
          missing, and why the score on your screen can look wonderful while the thing you
          built does not work.</p>
          <div class="w4-chips">
            <span class="w4-chip">Who is in your data</span>
            <span class="w4-chip">Rare things</span>
            <span class="w4-chip">Scores that lie</span>
            <span class="w4-chip-plain w4-chip">Nothing here is marked</span>
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
        <div class="w4-split">
          <div class="body">
            <p>So far the labs have been about the machine. Will the model fit on it, how long
            does it take to answer, and what happens to the plan when the answer is no.</p>
            <p>This week we go the other way, to the thing the model is made of.</p>
            <p><strong>A model is not really written. It is grown from data.</strong> Whatever
            is in that data is what the model learns, including the gaps. Nobody chose those
            gaps on purpose. They got in because of how the data was collected, and they stay
            in because nothing about them looks broken.</p>
            <p>That is the hard part, and it is worth saying plainly before we start. When code
            is wrong, it stops. When data is wrong, everything keeps running. The model trains,
            the tests pass, the score goes up, and the system quietly gets a group of people
            wrong for a month before anyone notices.</p>
          </div>
          <aside class="w4-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Say why a broken piece of data does not make anything crash.</li>
              <li>Work out who is missing from a dataset, and what that costs later.</li>
              <li>Tell the difference between a rare thing and a small number of examples.</li>
              <li>Read accuracy, precision and recall, and say which one your problem needs.</li>
              <li>Pick where to set the line between alerting and staying quiet.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 45 min</dd></div>
              <div><dt>Before this</dt><dd>Weeks 1 to 3</dd></div>
              <div><dt>Marked?</dt><dd>no, the quiz at the end is</dd></div>
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
        <div class="w4-question">
          <span class="lbl">The question this lab answers</span>
          <p>"My model scores well. How do I know it is any good?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: The data is the program""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is a way of looking at this that will save you a lot of confusion later.

    In ordinary software, the code is the thing you write and the program is what comes out.
    In machine learning, **the data is the thing you write** and the model is what comes out.
    Training is just the step in between, the way compiling is.

    Follow that through and it says something uncomfortable. Deleting a row of data is like
    deleting a line of code. Changing how a field is recorded is like changing what a function
    does. Nobody would do either of those without a second pair of eyes. With data, people do
    it every week and tell nobody.

    Now the difference that actually bites.

    **Broken code stops. Broken data does not.** A typo in code gives you a red error and a
    line number. Bad data gives you a model that trains normally, scores normally, ships
    normally, and is wrong about one group of people.

    Here is one that really happened.

    A team had postcodes in their data. Somewhere upstream, another team changed that field
    from a number to text. Sounds harmless. But `07102` had been stored as a number, so the
    leading zero was never there, and it came out as `7102`.

    Every row was still perfectly valid. `7102` is a fine piece of text. Nothing to complain
    about, so nothing complained.

    The model had never seen `7102` before. It treated a whole region as something unknown and
    started turning those people down. No error. No alert. Nothing in the logs.

    Work by researchers at Google on exactly this kind of fault found it takes around **four
    weeks** before anyone notices, and by then the bad values have been copied into other
    tables and several newer models have trained on them.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q1, q1_render, q1_sum = ask(
        "**Quick check.** Why did nothing break when 07102 turned into 7102?",
        {
            "The team had not written enough tests": "a",
            "Because the value was still perfectly valid; nothing was checking what it meant": "b",
            "The model was too small to notice": "c",
            "The change was made on a weekend": "d",
        },
        "b",
        "Checks look at shape, not meaning. Is it text? Yes. Is anything missing? No. "
        "Both answers are fine, and both are useless here, because the question that "
        "mattered was whether the postcode still pointed at the same place. Ordinary "
        "software gets caught by the computer itself; data has to be caught by a check "
        "somebody chose to write.",
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
    mo.accordion(
        {
            "So what do you do about it": mo.md(
                """
You write down what the data is supposed to look like, and you check every batch against it
before it is allowed in. Postcodes are five digits. Ages are between 0 and 120. This camera
sends pictures 2048 pixels wide. Roughly one in a hundred of these transactions is fraud.

The first few are easy and catch the stupid mistakes. The last one is the interesting one,
because it catches the day the world changes rather than the day the code changes.

There is also a habit worth building, and it is free. **Look at your data.** Open it. Sort it.
Look at the largest values, the smallest, the most common. People who do this find things in
ten minutes that a month of tuning would never have found.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 2: Who is actually in your data""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Most datasets are not collected. They are **whatever was easy to get**.

    Language models are trained on what was lying around on the internet. Review data comes
    from the people who bothered to write a review. Self-driving car data mostly comes from
    California and Arizona, because that is where the test fleets are, which means very little
    of it is rain and almost none of it is snow.

    Read that last one again, because it is the whole point of this part.

    > **The system is least trained exactly where it is most likely to fail.**

    Nobody decided that. It is just what happens when you take the data that is easy instead of
    the data you need. And no amount of work on the model fixes it, because the examples are
    not there to learn from.

    Below is a year of driving, and you get to pick 1,000 clips from it to label. The three
    buttons are the three ways this actually goes in real teams.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _picks = {
        "Take the 1,000 newest clips from the test fleet in Phoenix": "easy",
        "Pick 1,000 at random from the whole year": "random",
        "Take 250 from each kind of driving on purpose": "even",
    }
    coverage = mo.ui.radio(
        options=_picks,
        value=pick(_picks, saved.get("coverage")) or "Take the 1,000 newest clips from the test fleet in Phoenix",
        disabled=locked,
        label="**How do you choose the 1,000 clips to label?**",
    )
    coverage
    return (coverage,)


@app.cell(hide_code=True)
def _(coverage):
    # A year of driving, and how often each kind of weather actually happens.
    CONDITIONS = [
        # name, share of real driving, clips you get under each choice
        ("Clear daylight", 0.78, {"easy": 985, "random": 780, "even": 250}),
        ("Night", 0.15, {"easy": 15, "random": 150, "even": 250}),
        ("Heavy rain", 0.05, {"easy": 0, "random": 50, "even": 250}),
        ("Snow", 0.02, {"easy": 0, "random": 20, "even": 250}),
    ]

    def miss_rate(clips):
        """Roughly how often the car misses something, given what it was shown."""
        if clips == 0:
            return 0.60
        return max(0.03, 0.90 / (clips ** 0.5))

    choice = coverage.value
    rows = []
    for _name, _share, _clips in CONDITIONS:
        n = _clips[choice]
        rows.append({"name": _name, "share": _share, "clips": n, "miss": miss_rate(n)})
    overall = sum(r["share"] * r["miss"] for r in rows)
    worst = max(rows, key=lambda r: r["miss"])
    return choice, overall, rows, worst


@app.cell(hide_code=True)
def _(LAB_CSS, mo, overall, rows):
    _ = LAB_CSS
    _cards = ""
    for r in rows:
        _bad = r["miss"] > 0.15
        _cards += f"""
        <div class="w4-card {'bad' if _bad else 'ok'}">
          <h4>{r['name']}</h4>
          <p class="where">{r['share'] * 100:.0f} per cent of real driving</p>
          <span class="big">{r['clips']}</span>
          <span class="small">clips to learn from</span>
          <span class="big" style="margin-top:8px;color:{'#c62828' if _bad else '#2e7d32'}">
            {r['miss'] * 100:.0f}%</span>
          <span class="small">of things missed here</span>
        </div>
        """
    mo.vstack([
        mo.Html(f'<div class="w4-cards">{_cards}</div>'),
        mo.Html(
            f"""
            <div class="w4-grid">
              <div class="w4-stat {'red' if overall > 0.1 else 'green'}">
                <span class="k">Missed overall</span>
                <span class="v">{overall * 100:.1f}%</span>
                <span class="why">weighted by how often each kind of driving happens</span>
              </div>
            </div>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(choice, mo, overall, worst):
    if choice == "easy":
        _msg = (f"**This is the one that gets shipped.** The overall number looks respectable "
                f"at {overall * 100:.1f} per cent missed, because almost all driving is clear "
                f"daylight and the car is good at that. But it has never seen rain or snow, and "
                f"in those it misses **{worst['miss'] * 100:.0f} per cent** of what matters. "
                f"You will not find this out from the score. You find it out in February.")
        _kind = "danger"
    elif choice == "random":
        _msg = (f"**Honest, and still thin where it counts.** A random sample looks like the "
                f"real world, so common driving is well covered and the overall number is "
                f"{overall * 100:.1f} per cent. The trouble is that rare weather is rare in the "
                f"sample too: only 20 snow clips, and the car misses "
                f"{worst['miss'] * 100:.0f} per cent of what happens in the worst of them.")
        _kind = "warn"
    else:
        _msg = (f"**Deliberately uneven, and much safer.** You spent clips where the car is "
                f"weak instead of where it was already fine. Clear daylight got worse, because "
                f"you gave it fewer examples. Rain and snow got far better. Overall: "
                f"{overall * 100:.1f} per cent missed, and nothing on the list is a disaster.")
        _kind = "success"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "The names for these three": mo.md(
                """
Every one of these has a proper name, and you will hear all three.

**Convenience sampling** is the first one: take what is easy to reach. Almost all data in
machine learning is this, including the famous datasets. It is not automatically wrong. It is
wrong when the easy data is a different shape from the real world, which it usually is.

**Simple random sampling** is the second: everything has the same chance of being picked. It
is honest and it is the baseline everything else is compared against. Its weakness is exactly
what you saw: if something is rare in the world, it is just as rare in your sample.

**Stratified sampling** is the third: split the world into groups first, then take from each
group on purpose. You use it when you care about the small groups, which in safety work is
always.

There is a fourth worth knowing by name. **Cluster sampling** is picking a few whole groups
and taking everyone inside them: choose three cities, take every driver in them. It is cheaper
to collect, but people in the same city resemble each other, so a thousand rows from three
cities tells you much less than a thousand rows from everywhere.

One sentence to keep from all of this: **stratified means each group should be similar inside;
cluster means each group should be as varied inside as the world is.** People get that
backwards every year.
"""
            ),
            "When somebody says just collect more data": mo.md(
                """
More of the same data mostly buys you very little.

If your data was collected in a lopsided way, collecting ten times more of it in the same way
gives you ten times more of the same lopsided data. You become more confident about a number
that was never the right number. Meanwhile the cost goes up in a straight line.

The useful version of "collect more data" is always specific: more of **what**, from **where**,
covering **which** situations you currently cannot handle. That is a sampling decision, which
is where this section started.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q2, q2_render, q2_sum = ask(
        "**Quick check.** A team says their driving data is fine because it was picked at random from a year of real driving. What is still missing?",
        {
            "Nothing, random is the gold standard": "a",
            "Enough examples of the rare conditions, because rare in the world means rare in the sample too": "b",
            "More clips of clear daylight driving": "c",
            "A bigger model to learn from the same clips": "d",
        },
        "b",
        "Random sampling copies the world, including how little of it is snow. That is "
        "exactly right for measuring how the car does on an average day, and not enough "
        "for teaching it the days that hurt. If you care about the rare case, you have to "
        "go and get more of it on purpose, and then remember that your sample no longer "
        "looks like the world.",
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
    mo.md(r"""## Part 3: Rare is not the same as few""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Now to the thing that makes most of these systems hard: **the thing you care about hardly
    ever happens.**

    Fraud is about one or two transactions in a thousand. Serious disease in a screening
    programme is rarer than that. Machine faults, intrusions, bad reactions to a drug. In every
    one of them, the rare case is the entire reason anyone is building the system.

    People describe this with a ratio, like "999 to 1", and the ratio is the less useful half
    of the story. What decides whether you can build anything is **how many examples of the
    rare thing you actually have**.

    - 1,000 to 1, with ten million fraud cases in hand: fine. Plenty to learn from.
    - 10 to 1, with forty fraud cases in hand: not fine. Forty is almost nothing.

    The second one has a far kinder ratio and is the far worse position to be in.

    Move the two sliders and watch the number that matters, which is the one on the right.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    rows_labelled = mo.ui.slider(
        steps=[1000, 5000, 20000, 100000, 500000, 2000000],
        value=saved.get("rows", 20000),
        disabled=locked,
        label="How many rows you can afford to label",
        show_value=True,
    )
    _rates = {
        "1 in 10 (common)": 0.1,
        "1 in 100": 0.01,
        "1 in 1,000 (fraud)": 0.001,
        "1 in 10,000 (rare disease)": 0.0001,
    }
    prevalence = mo.ui.radio(
        options=_rates,
        value=pick(_rates, saved.get("prevalence")) or "1 in 1,000 (fraud)",
        disabled=locked,
        label="How often the thing you care about happens",
    )
    mo.vstack([rows_labelled, prevalence])
    return prevalence, rows_labelled


@app.cell(hide_code=True)
def _(prevalence, rows_labelled):
    labelled = int(rows_labelled.value)
    rate = float(prevalence.value)
    positives = labelled * rate
    # Rough rule of thumb from practice, not a law of nature.
    if positives < 50:
        verdict = ("Not enough", "bad",
                   "Fewer than about fifty examples and there is nothing to learn from. "
                   "No method fixes this. Go and find more of them.")
    elif positives < 500:
        verdict = ("Thin", "warn",
                   "Enough to start, not enough to trust. Expect the model to be unstable: "
                   "retrain it on a different week of data and it changes its mind.")
    else:
        verdict = ("Workable", "ok",
                   "Enough examples of the rare thing to actually learn its shape. The "
                   "lopsided ratio is now a training problem, and those have known fixes.")
    return labelled, positives, rate, verdict


@app.cell(hide_code=True)
def _(LAB_CSS, labelled, mo, positives, rate, verdict):
    _ = LAB_CSS
    _colour = {"bad": "red", "warn": "", "ok": "green"}[verdict[1]]
    mo.vstack([
        mo.Html(
            f"""
            <div class="w4-grid">
              <div class="w4-stat">
                <span class="k">Rows you label</span>
                <span class="v">{labelled:,}</span>
                <span class="why">and pay for, one by one</span>
              </div>
              <div class="w4-stat">
                <span class="k">Ratio</span>
                <span class="v">{round(1 / rate):,}:1</span>
                <span class="why">the number people quote</span>
              </div>
              <div class="w4-stat {_colour}">
                <span class="k">Examples of the rare thing</span>
                <span class="v">{positives:,.0f}</span>
                <span class="why">the number that decides everything</span>
              </div>
            </div>
            """
        ),
        mo.callout(mo.md(f"**{verdict[0]}.** {verdict[2]}"),
                   kind={"bad": "danger", "warn": "warn", "ok": "success"}[verdict[1]]),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Why this is the first thing to check": mo.md(
                """
Because it decides which problem you are actually having.

If you have forty fraud cases, you do not have a modelling problem. You have a data
collection problem, and every clever trick below is a distraction. Go and get more cases:
buy labels, dig through history, borrow from a related product, pay an expert to label a week
of transactions properly.

If you have fifty thousand fraud cases sitting inside fifty million transactions, now the
lopsidedness is a real training problem, and the rest of this lab is about what to do.

It takes one line of code to find out which of those two you are in, and people skip it
constantly.
"""
            ),
        }
    )
    return
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: Ninety per cent right, and no use to anyone""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is the trap this whole lab is named after.

    A thousand people are screened. One hundred of them have cancer, nine hundred do not. Now
    consider a program that is one line long:

    ```python
    print("normal")
    ```

    It says everybody is fine. It never looks at anything. It is right nine hundred times out
    of a thousand, so its accuracy is **90 per cent**, and it misses every single cancer.

    That is the thing to sit with. Your model has to beat that before it has done anything at
    all, and beating it on accuracy is easy while being useful is not.

    So accuracy is out. What do we use instead? Two questions, and they are ordinary questions
    once you say them in plain words.

    **Of the people who really had cancer, how many did we catch?** That is **recall**. High
    recall means few people get sent home wrongly.

    **Of the people we raised the alarm about, how many really had it?** That is **precision**.
    High precision means few people get a frightening phone call for nothing.

    Set the two sliders below and watch what happens to those numbers, and to accuracy, which
    barely moves.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    caught = mo.ui.slider(
        0, 100, value=saved.get("caught", 10), step=5, disabled=locked,
        label="Of the 100 real cancers, how many the model catches", show_value=True,
    )
    alarms = mo.ui.slider(
        0, 300, value=saved.get("alarms", 10), step=5, disabled=locked,
        label="How many healthy people it also flags (out of 900)", show_value=True,
    )
    mo.vstack([caught, alarms])
    return alarms, caught


@app.cell(hide_code=True)
def _(alarms, caught):
    tp = int(caught.value)              # cancers caught
    fn = 100 - tp                       # cancers missed
    fp = int(alarms.value)              # healthy people wrongly flagged
    tn = 900 - fp                       # healthy people correctly left alone

    accuracy = (tp + tn) / 1000
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / 100
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    baseline = 0.90                     # what print("normal") gets
    return accuracy, baseline, f1, fn, fp, precision, recall, tn, tp


@app.cell(hide_code=True)
def _(LAB_CSS, accuracy, baseline, f1, fn, fp, mo, precision, recall, tn, tp):
    _ = LAB_CSS
    mo.vstack([
        mo.Html(
            f"""
            <table class="w4-matrix">
              <tr><th></th><th>Really has cancer</th><th>Really healthy</th></tr>
              <tr><th>Model says cancer</th>
                  <td class="hit">{tp} caught</td><td class="miss">{fp} false alarms</td></tr>
              <tr><th>Model says normal</th>
                  <td class="miss">{fn} missed</td><td class="hit">{tn} correctly left alone</td></tr>
            </table>
            <div class="w4-grid">
              <div class="w4-stat {'green' if accuracy > baseline else 'red'}">
                <span class="k">Accuracy</span>
                <span class="v">{accuracy * 100:.0f}%</span>
                <span class="why">print("normal") gets {baseline * 100:.0f}%</span>
              </div>
              <div class="w4-stat">
                <span class="k">Recall</span>
                <span class="v">{recall * 100:.0f}%</span>
                <span class="why">of real cancers caught</span>
              </div>
              <div class="w4-stat">
                <span class="k">Precision</span>
                <span class="v">{precision * 100:.0f}%</span>
                <span class="why">of alarms that were real</span>
              </div>
              <div class="w4-stat">
                <span class="k">F1</span>
                <span class="v">{f1 * 100:.0f}%</span>
                <span class="why">the two above, rolled into one</span>
              </div>
            </div>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(accuracy, baseline, fn, mo, precision, recall):
    if accuracy <= baseline and recall < 0.5:
        _msg, _kind = (
            f"**Beaten by one line of code.** At {accuracy * 100:.0f} per cent you are level "
            f"with or behind `print(\"normal\")`, and you are sending {fn} people with cancer "
            f"home. This is the shape of a real model that looks fine on a dashboard.", "danger")
    elif recall >= 0.85 and precision >= 0.4:
        _msg, _kind = (
            f"**This is what you want.** {recall * 100:.0f} per cent of cancers caught, and "
            f"{precision * 100:.0f} per cent of your alarms are real. Notice the accuracy "
            f"hardly moved from the useless version. It was never the number telling you "
            f"anything.", "success")
    elif recall >= 0.85:
        _msg, _kind = (
            f"**Catching nearly everything, at a price.** {recall * 100:.0f} per cent of "
            f"cancers found, but only {precision * 100:.0f} per cent of your alarms are real, "
            f"so most people you frighten are fine. Whether that trade is right depends on "
            f"what happens after the alarm.", "warn")
    else:
        _msg, _kind = (
            f"**Still missing {fn} of 100.** Accuracy says {accuracy * 100:.0f} per cent, "
            f"which sounds like a pass. Recall says {recall * 100:.0f} per cent, which is the "
            f"number a patient would care about.", "warn")
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Two models, same accuracy, completely different lives": mo.md(
                """
This is the example from the lecture, and it is worth having in your head as a picture.

| | Cancers caught | False alarms | Accuracy | Precision | Recall |
| - | - | - | - | - | - |
| Model A | 10 of 100 | 10 | 90% | 50% | 10% |
| Model B | 90 of 100 | 90 | 90% | 50% | 90% |

Same accuracy. Same precision. One of them finds ninety cancers, the other finds ten. If you
were choosing between them on the number most people report, you could not tell them apart.

Recall is the number that separates them, and in screening it is the one that matters.

**F1** is the two numbers squeezed into one, and it is handy for ranking a pile of models
quickly. Be careful with it, though: it treats a miss and a false alarm as equally bad, and
almost no real problem works that way.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q3, q3_render, q3_sum = ask(
        "**Quick check.** Which number tells you whether people with the disease are being sent home?",
        {
            "Accuracy": "a",
            "Precision": "b",
            "Recall": "c",
            "The size of the training set": "d",
        },
        "c",
        "Recall asks: of everyone who really had it, how many did we catch? The ones we "
        "did not catch are the people sent home. Precision is the other side of the coin, "
        "and answers a different worry: of the people we alarmed, how many were really ill. "
        "Accuracy mixes both together with a huge number of healthy people and hides both.",
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
    mo.md(r"""## Part 5: Which mistake would you rather make?""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    You cannot have both. Push recall up and precision falls, every time. So the real question
    is never "which is better", it is **which mistake does less harm here**, and that is a
    question about the world, not about the model.

    Three of them, quickly.

    **A contagious illness.** Miss one and it spreads to other people. A false alarm costs one
    more test. Catch everything: go for recall.

    **Predicting who will commit a crime.** A false alarm is a real person accused of something
    they have not done. Be sure before you speak: precision.

    **A tool that flags bugs in code.** If it cries wolf, developers switch it off, and a tool
    nobody runs catches nothing. Precision, for a reason that is about people rather than
    statistics.

    Notice that the third one has no lives in it and still comes out the same way. The question
    is always what happens next, to whom, and who pays for it.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q4, q4_render, q4_sum = ask(
        "**Quick check.** A hospital is screening everyone for an illness that is easy to treat early and deadly if missed. A positive result means one more test. Where should the emphasis go?",
        {
            "Precision: do not worry people without good reason": "a",
            "Recall: catch every case, and accept some unnecessary tests": "b",
            "Accuracy: keep the overall number as high as possible": "c",
            "It does not matter, they trade off anyway": "d",
        },
        "b",
        "Compare what each mistake costs. A false alarm costs one extra test and a bad "
        "afternoon. A miss costs a life that could have been saved. When the two sides are "
        "that lopsided, you buy recall and pay for it in false alarms. Note that this flips "
        "later in the same hospital: once someone is being confirmed rather than screened, "
        "precision matters more, because now the next step is treatment.",
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
    mo.md(r"""## Part 6: The line you draw yourself""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    One more thing people do not realise they are choosing.

    A model does not really say yes or no. It gives a number between 0 and 1, a sort of
    confidence. Somebody then draws a line and says: above this, raise the alarm. That line is
    called the **threshold**, and the usual value of 0.5 was not chosen by anyone who thought
    about your problem. It is just the middle.

    Move the line down and you catch more real cases and cause more false alarms. Move it up
    and you cause fewer false alarms and miss more real cases. **This is a dial you own, and
    it costs nothing to turn.**

    Here is a screening programme at full size. One million people, and one hundred of them are
    really ill. Try the dial.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    threshold = mo.ui.slider(
        0, 100, value=saved.get("threshold", 0), step=5, disabled=locked,
        label="Where you draw the line (0 = alarm on the faintest hint, 100 = only when almost certain)",
        show_value=True, full_width=True,
    )
    threshold
    return (threshold,)


@app.cell(hide_code=True)
def _(threshold):
    import math

    REAL_CASES = 100
    HEALTHY = 1_000_000

    t = float(threshold.value)
    # A well behaved model: raising the bar loses a few real cases and a lot of false alarms.
    recall_t = 0.99 * math.exp(-0.012 * t)
    false_rate = 0.02 * math.exp(-0.060 * t)

    found = round(REAL_CASES * recall_t)
    false_alarms = round(HEALTHY * false_rate)
    missed = REAL_CASES - found
    precision_t = found / (found + false_alarms) if (found + false_alarms) else 0.0
    per_real = (false_alarms / found) if found else float("inf")
    return REAL_CASES, false_alarms, found, missed, per_real, precision_t, t


@app.cell(hide_code=True)
def _(LAB_CSS, false_alarms, found, missed, mo, per_real, precision_t):
    _ = LAB_CSS
    _scale = 20000.0
    mo.vstack([
        mo.Html(
            f"""
            <div class="w4-grid">
              <div class="w4-stat {'green' if found >= 80 else 'red'}">
                <span class="k">Real cases found</span>
                <span class="v">{found} of 100</span>
                <span class="why">{missed} {'person' if missed == 1 else 'people'} sent home ill</span>
              </div>
              <div class="w4-stat {'red' if false_alarms > 1000 else 'green'}">
                <span class="k">False alarms</span>
                <span class="v">{false_alarms:,}</span>
                <span class="why">healthy people told to come back in</span>
              </div>
              <div class="w4-stat">
                <span class="k">Alarms that are real</span>
                <span class="v">{precision_t * 100:.1f}%</span>
                <span class="why">{per_real:,.0f} false alarms for every real case</span>
              </div>
              <div class="w4-stat">
                <span class="k">AUC</span>
                <span class="v">0.98</span>
                <span class="why">does not move, wherever you put the line</span>
              </div>
            </div>
            <div class="w4-bars">
              <div class="w4-bar bad">
                <span class="t">False alarms</span>
                <span class="track"><span class="fill"
                  style="width:{min(false_alarms / _scale * 100, 100):.1f}%"></span></span>
                <span class="n">{false_alarms:,}</span>
              </div>
              <div class="w4-bar good">
                <span class="t">Real cases found</span>
                <span class="track"><span class="fill"
                  style="width:{found / 100 * 100:.1f}%"></span></span>
                <span class="n">{found}</span>
              </div>
            </div>
            <p class="w4-note">The two bars are not on the same scale. They cannot be: one tops
            out at a hundred and the other runs into the tens of thousands. That gap is the
            whole problem with rare things.</p>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(false_alarms, found, missed, mo, per_real):
    if per_real > 50:
        _msg, _kind = (
            f"**Nobody can work with this.** You find {found} of the 100 real cases, and to do "
            f"it you send {false_alarms:,} healthy people for more tests. That is about "
            f"{per_real:,.0f} false alarms for every real case. The clinic would stop using it "
            f"in a week, and then it catches nothing at all.", "danger")
    elif found < 50:
        _msg, _kind = (
            f"**Quiet, and not doing its job.** Only {false_alarms:,} false alarms, which the "
            f"clinic is happy about, but {missed} of the 100 ill people were told they were "
            f"fine.", "warn")
    else:
        _msg, _kind = (
            f"**This is roughly the useful range.** {found} of 100 real cases found, "
            f"{false_alarms:,} false alarms, about {per_real:,.0f} for each real case. Whether "
            f"that is acceptable is a decision for the people who staff the clinic, not for "
            f"you. Your job is to show them the choice in these terms.", "success")
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Why the AUC number did not move, and why that matters": mo.md(
                """
You will hear people judge a model by its **AUC**, usually somewhere around 0.97, and treat
that as the answer. Here is what it actually is.

Slide the threshold from one end to the other, write down the pair of numbers you get at each
setting, and draw them as a curve. AUC is the area under that curve: one number summarising
every possible setting at once. That is why it did not change when you moved the slider. You
were moving along the curve, not changing it.

And now the trap, which is specific to rare things.

One axis of that curve is the share of healthy people wrongly flagged. With a million healthy
people, flagging a thousand of them is 0.1 per cent, which draws as almost nothing. The curve
hugs the corner. The AUC comes out at 0.98 and everybody relaxes.

Meanwhile the clinic has a thousand false alarms and a hundred real cases, so nine out of ten
alarms are wrong. The number that shows this is precision, and AUC has quietly divided it away
by a million healthy people.

So when the thing you care about is rare, look at precision against recall instead. Same idea,
same sweep of the threshold, but the enormous pile of healthy people is left out of the
arithmetic, and the picture stops flattering you.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q5, q5_render, q5_sum = ask(
        "**Quick check.** A fraud model reports an AUC of 0.98. Why is your next question not \"great, ship it?\"",
        {
            "AUC above 0.95 is always overfitting": "a",
            "Because with millions of honest transactions, a tiny false alarm rate still means a huge pile of alerts, and AUC hides that": "b",
            "AUC only works for images": "c",
            "Because AUC changes when you move the threshold": "d",
        },
        "b",
        "AUC divides false alarms by the number of honest transactions, and that number is "
        "enormous. One alarm in a thousand honest transactions looks like nothing on the "
        "curve and is thousands of alerts a day for the team reading them. Ask instead: at "
        "the setting we would actually run, how many alerts a day, and what share of them "
        "are real?",
        key="q5",
    )
    q5
    return q5, q5_render, q5_sum


@app.cell(hide_code=True)
def _(q5, q5_render):
    q5_render(q5.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 7: Making the data less lopsided, without fooling yourself""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Suppose you do have enough real examples, and the ratio is still brutal. There are three
    usual moves, and they are all simple.

    **Throw away some of the common class.** You had fifty million honest transactions; keep
    two million. You lose some information, but honest transactions mostly repeat each other,
    and training gets much faster.

    **Copy the rare class.** Duplicate the fraud cases until there are more of them. No new
    information arrives, and a flexible model will happily memorise the copies.

    **Make new rare examples.** This is **SMOTE**. Take a fraud case, find another fraud case
    that looks similar, and invent a new one somewhere on the line between them. Unlike
    copying, this fills in a bit of the space around your real examples instead of stacking
    them higher.

    **Or change what mistakes cost.** Leave the data alone and tell the training process that
    missing a fraud hurts twenty times more than a false alarm. The model then leans towards
    catching them. This is **cost-sensitive learning**, and it is often the tidiest option,
    because it puts your real priorities in one place instead of hiding them in a resampling
    step.

    Now the mistake. It is the most common serious mistake in this whole area, and it is easy
    to make.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _when = {
        "Balance the whole dataset first, then split into train and test": "before",
        "Split first, then balance only the training part": "after",
    }
    resample = mo.ui.radio(
        options=_when,
        value=pick(_when, saved.get("resample")) or "Balance the whole dataset first, then split into train and test",
        disabled=locked,
        label="**When do you do the balancing?**",
    )
    resample
    return (resample,)


@app.cell(hide_code=True)
def _(mo, resample):
    if resample.value == "before":
        _msg = (
            "**This is the trap, and the score will not warn you.**" + chr(10) + chr(10)
            + "You made new fraud examples out of real ones, then shuffled everything and cut "
            "it in two. So a real case went into training and a near-copy of it went into the "
            "test set. The model has effectively seen the test paper." + chr(10) + chr(10)
            + "Your test score comes out at something like **0.98**, you present it, and the "
            "live system runs at about **0.71**. Nothing failed. The number was simply never "
            "measuring what you thought.")
        _kind = "danger"
    else:
        _msg = (
            "**Right, and it will feel worse.**" + chr(10) + chr(10)
            + "The test set is untouched real data, still as lopsided as the world is. Your "
            "score comes out around **0.71**, and that is the number that survives contact "
            "with production." + chr(10) + chr(10)
            + "The rule fits in one line: **split first, then do anything you like to the "
            "training half.** Never let a made-up example, or a copy of a real one, end up on "
            "the other side of that line.")
        _kind = "success"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Where SMOTE stops helping": mo.md(
                """
It is a good tool and it is not magic.

The line between two fraud cases can pass straight through honest territory, so the case you
invent in the middle may not be fraud at all. You have just taught the model something untrue.

It also depends on the middle of two examples meaning something. For a few numeric columns,
fine. For images, text, or anything with hundreds of dimensions, the halfway point between two
examples is usually nothing at all.

The people who invented it suggest throwing away some of the common class first, and then
filling in the rare one. And they wrote it for straightforward yes-or-no problems with numeric
columns, which is not every problem you will meet.
"""
            ),
            "How to choose between these in practice": mo.md(
                """
Roughly in this order, and stop as soon as it works.

1. **Move the threshold.** Free, instant, reversible, and it often gets you most of the way.
   Do this before anything else.
2. **Change what mistakes cost** in training. One number, written down where the next person
   can find it.
3. **Throw away some of the common class**, if training is slow and the common class is
   repetitive.
4. **Invent new rare examples** last, carefully, and only inside the training half.

Notice that the first two do not touch your data at all. Most teams reach for step four first,
which is backwards.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 8: Putting it to work""")
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w4-question">
          <span class="lbl">The situation</span>
          <p>"We handle two million card payments a day. About one in a thousand is fraud, and
          we have eighteen months of confirmed cases, so roughly twenty thousand of them. Our
          model reports an AUC of 0.97. The fraud team is four people, and they can look at
          about three hundred alerts a day between them. Right now they get four thousand, so
          they ignore most of it. What do we do?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Before you choose, notice what you already know. Twenty thousand real examples is plenty,
    so this is not a data collection problem. The AUC is not the issue either, and neither is
    the model. Four people can read three hundred alerts a day, and they are being handed four
    thousand.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "Raise the threshold until about 300 alerts a day come out, and see what that costs in missed fraud": "threshold",
        "Use SMOTE to balance the classes and retrain": "smote",
        "Collect more fraud examples before doing anything else": "collect",
        "Hire more analysts so the team can read all four thousand": "hire",
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
                placeholder="What made you pick that, and what would you need to see to change your mind?",
                label="**Why?**",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_label="Submit my decision",
            submit_button_disabled=locked,
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
        mo.callout(mo.md("Pick an answer, say why, then press **Submit my decision**."), kind="warn"),
    )
    decision_choice = _answer["choice"]
    decision_why = _answer["why"].strip()
    return decision_choice, decision_why


@app.cell(hide_code=True)
def _(decision_choice, mo):
    _notes = {
        "threshold": ("The right first move, and it costs nothing. The team can read three "
                      "hundred, so build the system that gives them three hundred, and find "
                      "out what that does to the fraud you catch. You may lose less than you "
                      "fear, because the strongest alerts are where most of the real fraud "
                      "is. And you will finally have the conversation in the right terms: "
                      "this many alerts, this much fraud caught, this much missed."),
        "smote": ("Reasonable instinct, wrong problem. Inventing more fraud examples helps "
                  "when you do not have enough to learn from. You have twenty thousand. "
                  "Nothing here says the model cannot tell fraud from honest payments; the "
                  "complaint is that four people are handed four thousand alerts. Balancing "
                  "the training data does not change how many alerts come out the other end."),
        "collect": ("This is the right answer to a different situation. With forty fraud "
                    "cases, stop everything and go get more. With twenty thousand and "
                    "eighteen months of history, more of the same will not change what the "
                    "team sees tomorrow."),
        "hire": ("Sometimes genuinely correct, and worth pricing rather than dismissing. But "
                 "price it honestly: reading all four thousand needs roughly four times the "
                 "team, every year, forever. Turning the threshold dial costs one afternoon. "
                 "Try the free thing first, then hire if the numbers still say you should."),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "The thing to take from this is the shape of it. The complaint was about the "
            "model, and the fix was about what the people downstream can actually do. Almost "
            "every question in this lab turns out that way once you ask who is on the other "
            "end of the answer."
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
                placeholder="The number I would stop trusting is... because...",
                label="**Last one.** Name one number you have reported in the past, or seen reported, that you would now ask a harder question about. What is the question?",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_label="Finish the lab",
            submit_button_disabled=locked,
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
        mo.callout(mo.md("Answer the last question to finish."), kind="warn"),
    )
    takeaway_text = _answer["takeaway"].strip()
    done = True
    return done, takeaway_text


@app.cell(hide_code=True)
def _(
    decision_choice,
    decision_why,
    done,
    labelled,
    mo,
    positives,
    q1,
    q1_sum,
    q2,
    q2_sum,
    q3,
    q3_sum,
    q4,
    q4_sum,
    q5,
    q5_sum,
    recall,
    takeaway_text,
):
    _ = done

    def _check(summary):
        text, ok = summary
        if ok is None:
            return "<em>not answered</em>"
        mark = '<span class="tick">right</span>' if ok else '<span class="cross">wrong</span>'
        return f"{text} ({mark})"

    _where = {
        "threshold": "Move the threshold to fit the team",
        "smote": "Balance the classes with SMOTE",
        "collect": "Collect more fraud examples first",
        "hire": "Hire more analysts",
    }

    mo.vstack([
        mo.md("## Your Week 4 report"),
        mo.Html(
            f"""
            <div class="w4-report">
              <div class="row">
                <span class="k">Rare things</span>
                <span class="v">you left it at {labelled:,} labelled rows, which is
                {positives:,.0f} examples of the rare case</span>
              </div>
              <div class="row">
                <span class="k">Cancer screening</span>
                <span class="v">your model caught {recall * 100:.0f} per cent of real cases</span>
              </div>
              <div class="row">
                <span class="k">The fraud team</span>
                <span class="v">{_where.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Why</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">A number you would question</span>
                <span class="v quote">{takeaway_text}</span>
              </div>
              <div class="row">
                <span class="k">Quick check 1</span>
                <span class="v">{_check(q1_sum(q1.value))}</span>
              </div>
              <div class="row">
                <span class="k">Quick check 2</span>
                <span class="v">{_check(q2_sum(q2.value))}</span>
              </div>
              <div class="row">
                <span class="k">Quick check 3</span>
                <span class="v">{_check(q3_sum(q3.value))}</span>
              </div>
              <div class="row">
                <span class="k">Quick check 4</span>
                <span class="v">{_check(q4_sum(q4.value))}</span>
              </div>
              <div class="row">
                <span class="k">Quick check 5</span>
                <span class="v">{_check(q5_sum(q5.value))}</span>
              </div>
            </div>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(done, locked, mo, pick, saved):
    _ = done
    QUIZ = [
        ("A postcode field changes from a number to text and leading zeros vanish. "
         "What happens to the system?",
         {"It crashes on the next run": "a",
          "It keeps working and gets one region quietly wrong": "b",
          "Training refuses to start": "c"},
         "b"),
        ("You have 40 confirmed fraud cases in total. What should you do first?",
         {"Use SMOTE to make more of them": "a",
          "Go and get more real cases; 40 is not enough to learn from": "b",
          "Lower the threshold": "c"},
         "b"),
        ("When do you balance the classes?",
         {"Before splitting, so both halves are balanced": "a",
          "After splitting, on the training half only": "b",
          "It makes no difference": "c"},
         "b"),
    ]
    _saved = saved.get("quiz") or {}
    quiz = mo.ui.array([
        mo.ui.radio(options=_options, label=f"**{_n}.** {_question}",
                    value=pick(_options, _saved.get(str(_n))), disabled=locked)
        for _n, (_question, _options, _right) in enumerate(QUIZ, 1)
    ])
    mo.vstack([
        mo.md("## Quick quiz"),
        mo.md("Three questions on what this lab showed. Saved and scored when you submit."),
        *[quiz[_i] for _i in range(len(QUIZ))],
    ], gap=1)
    return QUIZ, quiz


@app.cell(hide_code=True)
def _(QUIZ, lab_sync, quiz):
    quiz_score = f"{sum(v == q[2] for q, v in zip(QUIZ, quiz.value))}/{len(QUIZ)}"
    if lab_sync is not None:
        lab_sync.record(quiz={str(n): v for n, v in enumerate(quiz.value, 1)},
                        quiz_score=quiz_score)
    return (quiz_score,)


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
            "Your answers have been saving as you went. When you are happy with them, "
            "press the button to hand the lab in. You can change answers and submit "
            "again until your instructor locks the lab."
            + (f" **Answer the {_unanswered} quiz question"
               f"{'s' if _unanswered > 1 else ''} above first.**" if _unanswered else "")
        ),
        submit_button,
    ])
    return (submit_button,)


@app.cell(hide_code=True)
async def _(
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
                           f"Quiz: **{quiz_score}**.", "success")
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


@app.cell(hide_code=True)
def _(
    alarms,
    caught,
    coverage,
    decision_form,
    lab_sync,
    prevalence,
    q1,
    q2,
    q3,
    q4,
    q5,
    resample,
    rows_labelled,
    threshold,
):
    # Everything on the page from the start. A form's value is None until it is
    # submitted in this visit, so it is only recorded once it has one.
    if lab_sync is not None:
        lab_sync.record(
            q1=q1.value, q2=q2.value, q3=q3.value, q4=q4.value, q5=q5.value,
            coverage=coverage.value, rows=rows_labelled.value, prevalence=prevalence.value,
            caught=caught.value, alarms=alarms.value, threshold=threshold.value,
            resample=resample.value,
        )
        if decision_form.value is not None:
            lab_sync.record(decision=decision_form.value)
    return


@app.cell(hide_code=True)
def _(lab_sync, reflect_form):
    # The last question only exists once the decision is in.
    if lab_sync is not None and reflect_form.value is not None:
        lab_sync.record(reflection=reflect_form.value)
    return


@app.cell(hide_code=True)
def _(done, mo):
    _ = done
    mo.vstack([
        mo.md("### Check yourself"),
        mo.accordion({
            "Why does a broken piece of data not make anything crash?":
                mo.md(
                    "Because nothing in the machine knows what the data is supposed to mean. "
                    "A postcode that lost its leading zero is still a valid piece of text, so "
                    "every check passes and training runs normally. The only thing that can "
                    "catch it is a check somebody wrote on purpose, saying what good data "
                    "looks like: five digits, this range, roughly this mix."
                ),
            "Your data was collected the easy way. What has that cost you?":
                mo.md(
                    "Coverage of exactly the situations you are worst at. Test fleets drive "
                    "where the weather is good, so there is little rain and no snow, and that "
                    "is where the car is least able to cope. No model choice fixes it, "
                    "because the examples are not there. The fix is to go and get the data "
                    "you are missing, on purpose."
                ),
            "Why is the ratio less useful than the count?":
                mo.md(
                    "Because learning needs examples, not proportions. A thousand to one is "
                    "comfortable if that means ten million rare cases. Ten to one is hopeless "
                    "if it means forty. Count first: under about fifty, no technique saves "
                    "you and the job is to go and collect more."
                ),
            "A model is 99 per cent accurate. What do you ask next?":
                mo.md(
                    "What does the do-nothing answer score? If one per cent of cases are "
                    "fraud, then always saying honest scores 99 per cent. Then ask the two "
                    "real questions: of the fraud that happened, how much did we catch, and "
                    "of the alarms we raised, how many were real."
                ),
            "Why does moving the threshold count as engineering?":
                mo.md(
                    "Because it is the cheapest change with the largest effect on what the "
                    "people downstream experience. It costs one line and can be undone in a "
                    "minute. It decides how many alerts a day a team of four receives, and "
                    "whether they keep reading them at all."
                ),
            "Why must balancing happen after the split?":
                mo.md(
                    "Because copies and invented examples made before the split land on both "
                    "sides of it. The model then sees near-copies of the test data during "
                    "training, and the score you report is measuring memory rather than "
                    "ability. Split first; do what you like to the training half."
                ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
