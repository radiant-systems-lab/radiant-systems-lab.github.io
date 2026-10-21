import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 7 - Most of Your Data Is Not Teaching Anything")


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
        # Handed in means read-only: the server refuses any further writes,
        # so every control on the page is disabled to match.
        locked = bool(lab_status.get("locked") or lab_status.get("submitted"))
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
          .w7-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w7-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w7-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w7-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w7-hero p.sub code { background: #fff3cc; border: 1px solid #f2dfaa; padding: 0 5px;
                                border-radius: 4px; font-size: .92rem; }
          .w7-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w7-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w7-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w7-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w7-split { grid-template-columns: 1fr; } }
          .w7-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w7-split > .body p:last-child { margin-bottom: 0; }
          .w7-split code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                           font-size: .88rem; }

          .w7-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w7-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w7-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w7-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w7-aside li:last-child { margin-bottom: 0; }
          .w7-aside li::marker { color: #6a5314; font-weight: 800; }
          .w7-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w7-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w7-aside .meta div:last-child { margin-bottom: 0; }
          .w7-aside .meta dt { color: #6f6f6f; }
          .w7-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w7-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w7-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w7-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }
          .w7-question code { font-style: normal; background: #f4f4f4; padding: 1px 5px;
                              border-radius: 4px; font-size: .88rem; }

          .w7-note { color: #6f6f6f; font-size: .85rem; margin: 2px 0 0; line-height: 1.5; }

          .w7-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                     gap: 12px; margin: 14px 0; }
          .w7-stat { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff;
                     padding: 11px 13px; }
          .w7-stat .k { color: #6a5314; font-size: .72rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .w7-stat .v { display: block; color: #111; font-size: 1.45rem; font-weight: 800;
                        line-height: 1.2; margin-top: 2px; }
          .w7-stat .why { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 3px;
                          line-height: 1.4; }
          .w7-stat.green .v { color: #2e7d32; }
          .w7-stat.red .v { color: #c62828; }

          .w7-axis { position: relative; height: 96px; margin: 20px 0 6px;
                     border: 1px solid #e6e6e6; border-radius: 12px; background: #fff;
                     padding: 0; }
          .w7-axis .rule { position: absolute; left: 3%; right: 3%; top: 54px; height: 2px;
                           background: #e2e2e2; }
          .w7-axis .dot { position: absolute; top: 46px; width: 18px; height: 18px;
                          margin-left: -9px; border-radius: 50%; background: #fff;
                          border: 2px solid #c2c2c2; box-sizing: border-box; }
          .w7-axis .dot.on { background: #f1b82d; border-color: #9a7510;
                             box-shadow: 0 0 0 4px rgba(241, 184, 45, .22); }
          .w7-axis .tag { position: absolute; top: 20px; margin-left: -9px; width: 40px;
                          text-align: center; font-size: .78rem; font-weight: 800;
                          color: #9a9a9a; }
          .w7-axis .tag.on { color: #62490a; }
          .w7-axis .num { position: absolute; top: 70px; margin-left: -20px; width: 40px;
                          text-align: center; font-size: .7rem; color: #9a9a9a; }
          .w7-axis .ord { position: absolute; top: 2px; margin-left: -9px; width: 40px;
                          text-align: center; font-size: .66rem; font-weight: 800;
                          color: #6a5314; letter-spacing: .04em; }

          .w7-steps { display: flex; flex-direction: column; gap: 7px; margin: 16px 0; }
          .w7-step { display: grid; grid-template-columns: 34px 1fr 120px; gap: 12px;
                     align-items: center; border: 1px solid #e6e6e6; border-radius: 10px;
                     background: #fff; padding: 10px 14px; }
          @media (max-width: 640px) { .w7-step { grid-template-columns: 28px 1fr; } }
          .w7-step .n { display: flex; align-items: center; justify-content: center;
                        width: 26px; height: 26px; border-radius: 50%; background: #fff3cc;
                        border: 1px solid #f2dfaa; color: #62490a; font-size: .8rem;
                        font-weight: 800; }
          .w7-step .d { color: #2f2f2f; font-size: .91rem; line-height: 1.5; }
          .w7-step .r { text-align: right; font-size: .82rem; color: #6f6f6f; }
          @media (max-width: 640px) { .w7-step .r { display: none; } }

          .w7-stages { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
                       margin: 16px 0; }
          @media (max-width: 760px) { .w7-stages { grid-template-columns: 1fr; } }
          .w7-stage { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                      border-radius: 12px; background: #fff; padding: 13px 15px; }
          .w7-stage h4 { margin: 0 0 4px; font-size: .95rem; color: #111; }
          .w7-stage .when { color: #6a5314; font-size: .72rem; font-weight: 800;
                            letter-spacing: .05em; text-transform: uppercase;
                            display: block; margin-bottom: 8px; }
          .w7-stage ul { margin: 0; padding-left: 17px; }
          .w7-stage li { color: #3a3a3a; font-size: .85rem; line-height: 1.5;
                         margin-bottom: 5px; }
          .w7-stage li:last-child { margin-bottom: 0; }

          .w7-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w7-bar { display: grid; grid-template-columns: 210px 1fr 120px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w7-bar { grid-template-columns: 110px 1fr 86px; } }
          .w7-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w7-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 26px; overflow: hidden; }
          .w7-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w7-bar.good .fill { background: #7cb47f; }
          .w7-bar.bad .fill { background: #d98080; }
          .w7-bar.gold .fill { background: #f1b82d; }
          .w7-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }

          .w7-budget { display: flex; height: 44px; border-radius: 8px; overflow: hidden;
                       border: 1px solid #e6e6e6; margin: 14px 0 6px; background: #f6f6f6; }
          .w7-budget span { display: flex; align-items: center; justify-content: center;
                            color: #fff; font-size: .74rem; font-weight: 800;
                            overflow: hidden; white-space: nowrap; }
          .w7-budget .t { background: #4a6fa5; }
          .w7-budget .s { background: #c87f5a; }
          .w7-budget .f { background: #dcdcdc; color: #6f6f6f; }
          .w7-key { display: flex; flex-wrap: wrap; gap: 14px; margin: 0 0 12px; }
          .w7-key span { color: #4a4a4a; font-size: .8rem; display: flex;
                         align-items: center; gap: 6px; }
          .w7-key i { width: 11px; height: 11px; border-radius: 3px; display: inline-block; }

          table.w7-table { border-collapse: collapse; margin: 14px 0; font-size: .92rem;
                           width: 100%; }
          table.w7-table th, table.w7-table td { border: 1px solid #e6e6e6;
                                                 padding: 9px 13px; text-align: left;
                                                 vertical-align: top; }
          table.w7-table th { background: #fffdf5; color: #6a5314; font-size: .76rem;
                              text-transform: uppercase; letter-spacing: .04em; }
          table.w7-table td.num { text-align: right; font-variant-numeric: tabular-nums; }
          table.w7-table tr.on td { background: #fffdf5; font-weight: 700; }
          table.w7-table tr.off td { color: #9a9a9a; }
          table.w7-table code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                                font-size: .85rem; }
          table.w7-table .tick { color: #2e7d32; font-weight: 800; }
          table.w7-table .cross { color: #c62828; font-weight: 800; }

          .w7-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w7-report .row { display: grid; grid-template-columns: 200px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w7-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w7-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w7-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w7-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w7-report .tick { color: #2e7d32; font-weight: 800; }
          .w7-report .cross { color: #c62828; font-weight: 800; }
          .w7-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                              color: #333; font-style: italic; }
          .w7-score { display: inline-block; background: #fff3cc; border: 1px solid #f2dfaa;
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
        <div class="w7-hero">
          <p class="w7-eyebrow">CSC/EE 8001 &middot; Week 7</p>
          <h1>Most of Your Data Is Not Teaching Anything</h1>
          <p class="sub">You have 100,000 photos from doorbell cameras. You can only afford
          to train on 20,000 of them. And 60,000 of those photos are the same empty
          driveway, over and over.<br><br>
          So you have to delete 80,000 photos. Delete the right ones and you lose almost
          nothing. Delete the wrong ones and the model stops working. The hard part is that
          they all look like photos either way.</p>
          <div class="w7-chips">
            <span class="w7-chip">Why data got scarce</span>
            <span class="w7-chip">Keeping one of each kind</span>
            <span class="w7-chip">Keeping the hard ones</span>
            <span class="w7-chip">What to do with no labels</span>
            <span class="w7-chip-plain w7-chip">Checks are marked</span>
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
        <div class="w7-split">
          <div class="body">
            <p>For about ten years the plan was simple: get more data, get a better model.
            It worked. Nobody had to think much about <em>which</em> data.</p>
            <p>That plan has run out, and the reason is boring. Computers got cheap much
            faster than data did. GPUs get about ten times cheaper every three years. Good
            training data does not, because somebody has to go out and make it or find
            it.</p>
            <p>So now the shortage is on the other side. A company can buy enough computing
            power to read ten trillion words, then discover only five trillion good ones
            exist. We have lots of compute and not enough data. The question changed too.
            It used to be "where do we get more data?" Now it is "how do we get more out of
            the data we already have?"</p>
            <p>That sounds like a research question. Mostly it is a budgeting one. Every
            example you train on costs the same amount of compute. But they don't all teach
            the same amount. Some teach almost nothing, and you pay full price for them
            anyway.</p>
            <p>This lab is about spotting those. It is also about the bit people leave out:
            working out which examples to keep costs compute too, and sometimes it costs
            more than it saves.</p>
          </div>
          <aside class="w7-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Explain why having lots of compute and little data changes what you
              work on.</li>
              <li>Work out how much accuracy each GPU-hour is buying you.</li>
              <li>Run a real selection algorithm by hand, and say where it is blind.</li>
              <li>Give two very different reasons a model might get an example wrong.</li>
              <li>Work out whether the choosing cost more than it saved.</li>
              <li>Pick the right method when you are short of labels, or short of
              time.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 45 min</dd></div>
              <div><dt>Before this</dt><dd>Weeks 4 to 6</dd></div>
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
        <div class="w7-question">
          <span class="lbl">The question this lab answers</span>
          <p>"I can only afford to train on a fifth of my data. Which fifth do I keep, and
          did picking it cost me more than it saved?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: Why this is suddenly a problem""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is where the problem comes from. None of this is about machine learning. It is
    just about what is cheap and what is not.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <table class="w7-table">
          <thead><tr><th>Resource</th><th>Growth</th><th>Rate</th><th>Why</th></tr></thead>
          <tbody>
            <tr><td>GPU compute</td><td>Gets cheap fast</td><td>10&times; per 3 years</td>
                <td>We build the chips, and we keep getting better at it</td></tr>
            <tr><td>Training data</td><td>Grows slowly</td><td>2&times; per 5 years</td>
                <td>Somebody has to make it, then somebody has to find it</td></tr>
            <tr><td>Labelled data</td><td>Grows very slowly</td><td>1.5&times; per 5 years</td>
                <td>A human has to look at each one, and people don't get cheaper</td></tr>
            <tr><td>Made-up data</td><td>As much as you like</td><td>&mdash;</td>
                <td>But a model can't invent facts it doesn't already know</td></tr>
          </tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    You have probably seen the scaling-law graphs, the ones where accuracy keeps climbing
    as the dataset grows. People read those as "more data always helps". Look at the axis
    label though. It counts **different, good examples**. Copies don't count. Junk doesn't
    count.

    So a dataset of a million photos where 600,000 are the same driveway is not a
    million-photo dataset. It is a 400,000-photo dataset that costs a million photos to
    train on.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d1, d1_render, d1_sum = ask(
        "**Check 1.** Compute gets ten times cheaper every three years. Good data only "
        "doubles every five. Given that, what should you work on?",
        {
            "Go and collect more data, since data is the thing we are short of": "more",
            "Get more learning out of the data you already have": "value",
            "Buy more compute, since that is what the model actually runs on": "compute",
        },
        "value",
        "Collecting more data is the obvious answer, and it is the right answer when there "
        "is more data to collect. Often there is. If you work at a hospital and you have "
        "2,000 scans, go and get 10,000.\n\nBut the big labs have a different problem: they "
        "have already taken it. The good text, the labelled medical images, the annotated "
        "driving footage. There isn't a pile of it sitting somewhere waiting. So what you "
        "are short of isn't really data, it's *usefulness per example*. And that you can "
        "still fix with engineering.\n\nThe third answer is the trap. Compute is the thing "
        "you have plenty of. Spending more of it on photos of an empty driveway doesn't buy "
        "you anything.",
        key="d1",
    )
    d1
    return d1, d1_render, d1_sum


@app.cell(hide_code=True)
def _(d1, d1_render):
    d1_render(d1.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Putting a number on it

    Say you train the same model five times, on bigger and bigger slices of the same
    dataset. Here is what you get.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    _rows = [
        (10_000, 75.0, 1.0, None),
        (50_000, 85.0, 5.0, 2.50),
        (100_000, 89.0, 10.0, 0.80),
        (500_000, 92.0, 50.0, 0.075),
        (1_000_000, 93.0, 100.0, 0.020),
    ]
    _body = "".join(
        f"<tr><td class='num'>{_n:,}</td><td class='num'>{_acc:.0f}%</td>"
        f"<td class='num'>{_hrs:,.0f}</td>"
        f"<td class='num'>{'&mdash;' if _icr is None else f'{_icr:.3f}'}</td></tr>"
        for _n, _acc, _hrs, _icr in _rows
    )
    mo.Html(
        f"""
        <table class="w7-table">
          <thead><tr><th>Training examples</th><th>Validation accuracy</th>
            <th>GPU-hours</th><th>Accuracy points per GPU-hour, over the row above</th>
          </tr></thead>
          <tbody>{_body}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    That last column is the one to look at. It answers "what did the extra data actually
    buy me?" It has a name, the **information-compute ratio**, but it is just division:

    $$\text{ICR} = \frac{\text{accuracy you gained}}{\text{compute you spent}}$$

    Read down the column. Going from 10,000 photos to 50,000 buys you 2.5 points of
    accuracy for every GPU-hour. Good deal. Going from 500,000 to a million buys you 0.02
    points per GPU-hour. That is 125 times worse.

    Look at it the other way round. That last 500,000 photos cost you 50 GPU-hours and
    bought you **one point** of accuracy.

    People call this the **data tax**. Ten times the data, nine times the bill, two or
    three points of accuracy. And most datasets scraped off the web sit right there, in the
    flat part at the end, where you pay full price per photo and learn almost nothing.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d2, d2_render, d2_sum = ask(
        "**Check 2.** Someone tells you their carefully picked dataset has a really high "
        "ICR. How accurate will a model trained on it be?",
        {
            "Very accurate, because high ICR and high accuracy go together": "high",
            "You can't tell. ICR says how fast you learn, not how good you end up": "slope",
            "Not very, because a high ICR means it hasn't finished learning": "low",
        },
        "slope",
        "ICR tells you how *fast* you are learning per pound spent. It says nothing about "
        "where you finish. Those are two different questions.\n\nAn example of each. A tiny "
        "dataset of 400 carefully chosen examples on a hard problem can have a brilliant "
        "ICR: every single example teaches the model a lot. And then you run out of examples "
        "at 70% accuracy, because 400 examples is 400 examples. Great rate, bad "
        "destination.\n\nThe flat tail from the table is the opposite. Terrible rate, but it "
        "does get to 93% in the end, just expensively.\n\nSo: ICR is a speed. Accuracy is a "
        "destination. Mixing them up is how somebody ends up defending a 400-example "
        "dataset for a real product.",
        key="d2",
    )
    d2
    return d2, d2_render, d2_sum


@app.cell(hide_code=True)
def _(d2, d2_render):
    d2_render(d2.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Three places you can step in

    Everything else in this lab is one of three moves. They happen at different times, and
    you do them in this order rather than picking one.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w7-stages">
          <div class="w7-stage">
            <span class="when">1 &middot; Before training</span>
            <h4>Throw stuff out</h4>
            <ul>
              <li>Delete the copies</li>
              <li>Delete the junk</li>
              <li>Keep a well-chosen subset</li>
            </ul>
          </div>
          <div class="w7-stage">
            <span class="when">2 &middot; While training</span>
            <h4>Change the order</h4>
            <ul>
              <li>Easy examples first</li>
              <li>Ask a human about the confusing ones</li>
              <li>Let the model label the easy ones</li>
            </ul>
          </div>
          <div class="w7-stage">
            <span class="when">3 &middot; If you still have gaps</span>
            <h4>Make more</h4>
            <ul>
              <li>Flip, crop and recolour what you have</li>
              <li>Generate new examples</li>
              <li>Learn from unlabelled data first</li>
            </ul>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The order matters, and here is why. Suppose you skip step 1 and go straight to step 2.
    Now every clever thing you do in step 2 has to look at all 60,000 copies of the
    driveway, score them, rank them, and think about them. You pay for the copies twice:
    once to store and sort them, and again when you train.

    Delete them first. Everything after that is cheaper.

    ### How this differs from Weeks 4 and 5

    Weeks 4 and 5 were also about data, so it is worth being clear about the difference.
    Same photos, different question.

    | | Weeks 4 and 5 | This week |
    | - | - | - |
    | Asks | Is this data *correct*? | Is correct data *worth the compute*? |
    | Looks for | Broken fields, outliers, drift | Copies, boring examples, useful examples |
    | Measures | How much is wrong | How much you learn per pound |

    So a photo can be perfectly sharp, correctly labelled, nothing wrong with it at all,
    and still not be worth training on. That is a new idea. In Week 4 that photo was
    simply fine.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 2: The doorbell camera""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is the job for the rest of the lab.

    You work on a doorbell camera. When something moves, it takes a photo, and your model
    has to say which of three things it is seeing: a **person**, a **package**, or
    **nothing**. Getting "person" right is the one that matters, because that is the alert
    that wakes somebody up at 2am.

    Six months of cameras out in the world have given you this:
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w7-grid">
          <div class="w7-stat">
            <span class="k">Photos</span>
            <span class="v">100,000</span>
            <span class="why">from about 400 customers' doorbells</span>
          </div>
          <div class="w7-stat">
            <span class="k">Somebody has labelled</span>
            <span class="v">10,000</span>
            <span class="why">by hand, last year, until the money ran out</span>
          </div>
          <div class="w7-stat">
            <span class="k">Nobody has looked at</span>
            <span class="v">90,000</span>
            <span class="why">just photos; we don't know what is in them</span>
          </div>
          <div class="w7-stat red">
            <span class="k">Compute you are allowed</span>
            <span class="v">20 GPU-hrs</span>
            <span class="why">training on all 100,000 would take 100</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    One more thing, and it is the important one. You scroll through the photos for ten
    minutes and notice that about **60,000 of them are an empty driveway in daylight**.
    Not identical, exactly. One has a car parked in it. One was taken four minutes later so
    the shadow has moved. But as far as a model is concerned, they are the same photo
    60,000 times.

    So: you can keep 20,000. Before we do anything clever, say what you would do. Which
    80,000 would you delete?
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("hunch") or {}
    _choices = {
        "The 80,000 the model already gets right": "easy",
        "The 80,000 the model gets wrong": "hard",
        "80,000 picked at random, so what's left still looks like the original": "random",
        "80,000 picked so that what's left still has some of every kind of photo": "cover",
    }
    hunch_form = (
        mo.md("{choice}")
        .batch(
            choice=mo.ui.radio(
                options=_choices,
                value=pick(_choices, _saved.get("choice")),
                disabled=locked,
                label="**Your gut feeling, before we do this properly.** Not marked.",
            ),
        )
        .form(
            submit_button_disabled=locked,
            submit_button_label="That's my guess",
            bordered=True,
            validate=lambda v: None if v and v.get("choice") else "Pick one.",
        )
    )
    hunch_form
    return (hunch_form,)


@app.cell(hide_code=True)
def _(hunch_form, mo, saved):
    _answer = hunch_form.value or saved.get("hunch")
    mo.stop(
        not _answer,
        mo.callout(mo.md("Pick one and press **That's my guess**. Being wrong here is "
                         "genuinely the point — the rest of the lab lands better if you "
                         "have committed to something first."), kind="warn"),
    )
    hunch_choice = _answer["choice"]
    return (hunch_choice,)


@app.cell(hide_code=True)
def _(hunch_choice, mo):
    _notes = {
        "easy": (
            "Most people say this, and most of the time they are right. If the model "
            "already gets a photo right, it has nothing left to learn from it. Deleting "
            "those is the biggest easy win there is.\n\nIt does break eventually. If you "
            "delete *all* the easy photos and keep only the hard ones, the model loses its "
            "footing — it never sees a nice clear example of a person any more, only "
            "difficult ones. Accuracy drops off a cliff. You will see exactly where that "
            "happens in Part 5."
        ),
        "hard": (
            "This is backwards as a default, but it is a really useful mistake, and Part 4 "
            "is about it.\n\nHere is the problem. When a model gets a photo wrong, there "
            "are two possible reasons. Either it is a genuinely tricky photo and the model "
            "needs to see it, or somebody labelled it wrong and it is nonsense. A "
            "difficulty score looks exactly the same in both cases.\n\nSo deleting all the "
            "hard photos throws away the tricky ones you needed. And keeping *only* the "
            "hard photos collects every bad label in your dataset into one pile and trains "
            "on it."
        ),
        "random": (
            "The boring answer, and genuinely hard to beat. Keep it in mind as the thing "
            "every clever method has to actually beat.\n\nIts problem here is specific. "
            "Random picking keeps the mix the same. So if 60% of your photos are empty "
            "driveways, 60% of your 20,000 will be empty driveways too, which is 12,000 "
            "photos of nothing. You have faithfully preserved the thing that was wrong "
            "with the dataset."
        ),
        "cover": (
            "This is the best of the four for this dataset, and it is what Part 3 does.\n\n"
            "The trick is that it stops asking \"is this photo good?\" and asks \"what "
            "kinds of photo do I have, and have I kept at least one of each?\" One empty "
            "driveway is as good as 60,000 of them, so you keep one and move on.\n\nIt has "
            "one blind spot that will bite you, and it is worth knowing about before you "
            "trust it. Coming up shortly."
        ),
    }
    mo.vstack([
        mo.md("### On your guess"),
        mo.callout(mo.md(_notes[hunch_choice]), kind="info"),
    ])
    return


@app.cell(hide_code=True)
def _(ask):
    d3, d3_render, d3_sum = ask(
        "**Check 3.** You pick 20,000 of the 100,000 photos at random. Remember 60,000 of "
        "the originals are near-identical empty driveways. What have you ended up with?",
        {
            "A fair sample of the original, which is what you want": "ok",
            "About 12,000 empty driveways, because random picking keeps the same mix": "same",
            "Proportionally fewer driveways, because near-identical photos are less likely to be picked": "fewer",
        },
        "same",
        "20% of 60,000 is 12,000. So more than half your precious compute budget still goes "
        "on photos of an empty driveway.\n\nThe third answer is worth talking about, because "
        "it is a very natural mistake. Random picking has **no idea** that two photos look "
        "alike. It isn't looking at them. It rolls a dice for each photo independently. So a "
        "group of 60,000 similar photos gets picked in proportion to its size, exactly like "
        "any other group would.\n\nAnd the first answer is true, which is the annoying part. "
        "It *is* a fair sample. It faithfully represents a dataset that was already 60% "
        "rubbish. Being a fair sample of a bad dataset is not a win.",
        key="d3",
    )
    d3
    return d3, d3_render, d3_sum


@app.cell(hide_code=True)
def _(d3, d3_render):
    d3_render(d3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: Keep one of each kind""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    If the problem is that random picking keeps the same mix, then stop picking randomly.
    Instead, go looking for **one of each kind of photo**.

    Which needs us to answer a question first: how does a computer tell that two photos are
    "the same kind"? It can't look at them the way you did.

    ### Turning a photo into a number

    Here is the trick, and it is used everywhere. Take a neural network that somebody else
    already trained on millions of photos. Feed your photo in, but instead of reading its
    answer, read the numbers from one of its middle layers. You get a list of a few hundred
    numbers for each photo.

    The useful bit: **photos that look alike produce similar lists of numbers.** That is
    not magic, it is just what the network learned in order to do its original job. Those
    60,000 driveways all land on nearly the same numbers. A photo taken at night lands
    somewhere else entirely.

    People call that list of numbers an *embedding*. All you need from it is this: once a
    photo is a list of numbers, you can measure how far apart two photos are. And "far
    apart" now means "look different".

    ### The algorithm

    Now that distance means something, here is the whole method. It is called **k-center
    greedy**, which sounds worse than it is:

    1. Pick any photo to start.
    2. Find the photo that is **furthest away** from everything you've picked so far.
    3. Keep it.
    4. Repeat until you have as many as you can afford.

    That is it. Because you always grab the thing that is least like what you already have,
    you can't accidentally collect 60,000 driveways. The second one you pick is as different
    as possible from the first.

    The number to watch is the **worst distance**: take every photo in the dataset, measure
    how far it is from the nearest photo you kept, and look at the biggest one. That tells
    you how badly you've let the dataset down. Small is good.

    Below are seven photos. To keep it readable each one is a single number instead of a
    few hundred, so you can see the whole thing on one line. Photos with similar numbers
    look similar. Try it: pick a starting photo and how many to keep.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _starts = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    kc_start = mo.ui.radio(
        options=_starts,
        value=pick(_starts, saved.get("kc_start")) or "B",
        disabled=locked, label="Start from", inline=True,
    )
    kc_keep = mo.ui.slider(
        1, 7, value=saved.get("kc_keep", 3), step=1, disabled=locked,
        label="How many to keep", show_value=True,
    )
    mo.vstack([kc_start, kc_keep])
    return kc_keep, kc_start


@app.cell(hide_code=True)
def _(kc_keep, kc_start):
    # The lecture's seven frames. One dimension is a cartoon, but every property
    # that matters about k-center greedy survives the simplification.
    FRAMES = [
        ("A", 0.0, "Empty driveway, midday"),
        ("B", 0.1, "Empty driveway, midday"),
        ("C", 0.2, "Empty driveway, parked car"),
        ("D", 4.8, "Person walking past"),
        ("E", 5.0, "Person at the door"),
        ("F", 5.2, "Person walking away"),
        ("G", 9.8, "Night-time, shadow across the step"),
    ]

    def coverage(chosen):
        """The largest distance from any frame to its nearest chosen frame."""
        return max(min(abs(FRAMES[i][1] - FRAMES[j][1]) for j in chosen)
                   for i in range(len(FRAMES)))

    def k_center(start, k):
        """Greedy farthest-point selection. Returns the picks in order, each with
        the distance that justified it and the coverage radius afterwards."""
        chosen = [start]
        trace = [(start, None, coverage(chosen))]
        while len(chosen) < k:
            best, best_d = None, -1.0
            for i in range(len(FRAMES)):
                if i in chosen:
                    continue
                d = min(abs(FRAMES[i][1] - FRAMES[j][1]) for j in chosen)
                if d > best_d:
                    best, best_d = i, d
            chosen.append(best)
            trace.append((best, best_d, coverage(chosen)))
        return chosen, trace

    kc_chosen, kc_trace = k_center(kc_start.value, kc_keep.value)
    # The obvious lazy alternative: take the first k frames as they came off the
    # device. It is what you get by slicing a sorted file.
    kc_naive = list(range(kc_keep.value))
    kc_naive_cov = coverage(kc_naive)
    kc_scenes = len({FRAMES[i][2].split(",")[0] for i in kc_chosen})
    return (
        FRAMES,
        kc_chosen,
        kc_naive,
        kc_naive_cov,
        kc_scenes,
        kc_trace,
    )


@app.cell(hide_code=True)
def _(FRAMES, LAB_CSS, kc_chosen, mo):
    _ = LAB_CSS
    _span = 10.0
    _order = {idx: n for n, idx in enumerate(kc_chosen, 1)}
    _dots = ""
    for _i, (_name, _emb, _scene) in enumerate(FRAMES):
        _left = 3 + (_emb / _span) * 94
        _on = " on" if _i in _order else ""
        _ord = (f'<span class="ord" style="left:{_left}%">pick {_order[_i]}</span>'
                if _i in _order else "")
        _dots += (
            f'{_ord}'
            f'<span class="tag{_on}" style="left:{_left}%">{_name}</span>'
            f'<span class="dot{_on}" style="left:{_left}%"></span>'
            f'<span class="num" style="left:{_left}%">{_emb:.1f}</span>'
        )
    mo.Html(f'<div class="w7-axis"><span class="rule"></span>{_dots}</div>')
    return


@app.cell(hide_code=True)
def _(FRAMES, LAB_CSS, kc_trace, mo):
    _ = LAB_CSS
    _steps = ""
    for _n, (_idx, _d, _cov) in enumerate(kc_trace, 1):
        _name, _emb, _scene = FRAMES[_idx]
        _why = ("you started here" if _d is None
                else f"furthest from what you had, {_d:.1f} away")
        _steps += (
            f'<div class="w7-step"><span class="n">{_n}</span>'
            f'<span class="d"><strong>{_name}</strong> &middot; {_scene} &middot; '
            f'<span style="color:#6f6f6f">{_why}</span></span>'
            f'<span class="r">worst gap {_cov:.1f}</span></div>'
        )
    mo.Html(f'<div class="w7-steps">{_steps}</div>')
    return


@app.cell(hide_code=True)
def _(FRAMES, kc_chosen, kc_naive, kc_naive_cov, kc_scenes, kc_trace, mo):
    _names = ", ".join(FRAMES[i][0] for i in kc_chosen)
    _naive_names = ", ".join(FRAMES[i][0] for i in kc_naive)
    _radius = kc_trace[-1][2]
    _better = kc_naive_cov - _radius
    mo.callout(
        mo.md(
            f"Keeping **{len(kc_chosen)}** photos, the algorithm chose **{_names}**. The "
            f"worst gap is **{_radius:.1f}**, meaning every photo in the dataset has "
            f"something fairly similar in your subset. You got **{kc_scenes}** of the three "
            f"kinds of scene.\n\n"
            f"Now compare that to just taking the first {len(kc_naive)} photos off the "
            f"camera, which is what you get if you grab the top of the file. That gives you "
            f"**{_naive_names}**, and a worst gap of **{kc_naive_cov:.1f}**"
            + (f" &mdash; **{_better:.1f}** worse.\n\nSame number of photos. Same training "
               f"cost. But that model has never seen a person or a night-time photo in its "
               f"life. It will confidently tell you every photo is an empty driveway, and "
               f"it will be right 60% of the time."
               if _better > 0.05 else
               ".\n\nAt this size they're about the same, which is its own lesson: if you "
               "can afford to keep nearly everything, don't bother being clever.")
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Two things to try with the slider.

    **Watch how fast the gap closes.** Go from keeping 1 photo to keeping 3 and the worst
    gap drops from 9.7 to 0.2. Then go from 5 to 7 and almost nothing happens. That is the
    whole reason coresets work. The first few photos you pick do nearly all the useful work,
    and everything after that is the flat tail from Part 1 again.

    **Now change the starting photo.** Try A, then try G. You get different photos, but you
    still end up with one driveway, one person and the night shot. The algorithm fixes its
    own bad start, because whatever you began with, step 2 goes and grabs the opposite.

    It isn't perfect. Start from D or F, in the middle of the "person" group, and the worst
    gap settles at 0.4 instead of 0.2. Still fine, slightly worse. So in practice people
    run it from a few different starting photos and keep whichever run came out best. It
    costs nothing to do that.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d4, d4_render, d4_sum = ask(
        "**Check 4.** The algorithm hands you three photos, one of each kind. Now: your "
        "model absolutely has to spot people at night, and night photos are 0.4% of the "
        "dataset. What has the algorithm *not* promised you?",
        {
            "That it kept the photos the model finds hardest": "hard",
            "That any particular thing survived, because it was matching photos by how they look, not by what's in them": "class",
            "That training on the subset is cheaper than training on everything": "cheap",
            "That the right network was used to turn photos into numbers": "net",
        },
        "class",
        "The algorithm never saw a single label. It doesn't know what a person is. It was "
        "spreading out numbers, and nobody told it that night-time people are the thing that "
        "gets your company sued.\n\nIt can go wrong both ways:\n\n- A rare thing you care "
        "about might happen to produce numbers close to a common thing. The algorithm thinks "
        "it already has one of those, and drops it.\n- A big pile of corrupted photos "
        "produces unusual numbers. The algorithm thinks it has found an exciting new kind of "
        "photo and keeps loads of them.\n\nSo treat coverage as a sensible default, not a "
        "policy. The fix is easy: decide up front that you want at least 500 night photos, "
        "set those aside, and let the algorithm choose the rest.\n\nThe fourth answer is a "
        "genuinely good worry, and it is true that the choice of network matters a lot. It "
        "just isn't a thing the algorithm claimed to handle.",
        key="d4",
    )
    d4
    return d4, d4_render, d4_sum


@app.cell(hide_code=True)
def _(d4, d4_render):
    d4_render(d4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: Keep the hard ones instead""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Part 3 asked "what kind of photo is this?" Here is the other approach: ask "how badly
    does the model get this one wrong?"

    The recipe is cheap. Train a quick, rubbish model on everything for a few minutes. Don't
    use it for anything, just ask it to guess every photo. For each photo, measure how far
    its guess was from the right answer. Then keep the photos it was most wrong about.

    That gap between the guess and the truth has a name people use, **EL2N**, which stands
    for error L2 norm. Ignore the name. It means "how wrong was it", and the only thing
    you need to know is that bigger means more wrong.

    The logic: if the quick model already nails a photo, your real model will too, so
    there's nothing to learn there. If the quick model struggles, that is where the learning
    is.

    Here are our seven photos with their scores. Choose how many of the hardest to keep, and
    watch the last two columns.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    el2n_keep = mo.ui.slider(
        1, 7, value=saved.get("el2n_keep", 3), step=1, disabled=locked,
        label="Keep the hardest", show_value=True,
    )
    el2n_keep
    return (el2n_keep,)


@app.cell(hide_code=True)
def _(el2n_keep):
    # Scores from the lecture. The `bad` flag is the thing a difficulty score cannot
    # see: F is genuinely hard, G is simply mislabelled.
    SCORED = [
        ("A", 0.1, "Clear pedestrian, midday", False),
        ("B", 0.2, "Empty driveway", False),
        ("C", 0.3, "Package on the step", False),
        ("D", 0.8, "Pedestrian in shadow", False),
        ("E", 0.9, "Partially occluded pedestrian", False),
        ("F", 1.0, "Pedestrian at night", False),
        ("G", 1.5, "A dog, labelled 'person'", True),
    ]
    _ranked = sorted(range(len(SCORED)), key=lambda i: -SCORED[i][1])
    el2n_kept = set(_ranked[:el2n_keep.value])
    el2n_bad = sum(1 for i in el2n_kept if SCORED[i][3])
    el2n_noise = 100.0 * el2n_bad / len(el2n_kept)
    full_noise = 100.0 * sum(1 for s in SCORED if s[3]) / len(SCORED)
    return SCORED, el2n_bad, el2n_kept, el2n_noise, full_noise


@app.cell(hide_code=True)
def _(LAB_CSS, SCORED, el2n_kept, mo):
    _ = LAB_CSS
    _BAD = '<span class="cross">mislabelled</span>'
    _body = "".join(
        f"<tr class='{'on' if _i in el2n_kept else 'off'}'>"
        f"<td>{_n}</td><td class='num'>{_s:.1f}</td><td>{_scene}</td>"
        f"<td>{_BAD if _bad else 'label is correct'}</td>"
        f"<td>{'kept' if _i in el2n_kept else 'pruned'}</td></tr>"
        for _i, (_n, _s, _scene, _bad) in enumerate(SCORED)
    )
    mo.Html(
        f"""
        <table class="w7-table">
          <thead><tr><th>Frame</th><th>EL2N</th><th>What it is</th>
            <th>Ground truth</th><th>Your subset</th></tr></thead>
          <tbody>{_body}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, el2n_bad, el2n_keep, el2n_noise, full_noise, mo):
    _ = LAB_CSS
    _kind = "red" if el2n_noise > full_noise + 0.1 else "green"
    mo.Html(
        f"""
        <div class="w7-grid">
          <div class="w7-stat">
            <span class="k">Kept</span>
            <span class="v">{el2n_keep.value} of 7</span>
            <span class="why">the highest EL2N scores</span>
          </div>
          <div class="w7-stat">
            <span class="k">Bad labels in it</span>
            <span class="v">{el2n_bad}</span>
            <span class="why">of the one in the whole dataset</span>
          </div>
          <div class="w7-stat {_kind}">
            <span class="k">Label noise in your subset</span>
            <span class="v">{el2n_noise:.0f}%</span>
            <span class="why">against {full_noise:.0f}% in the full dataset</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(el2n_keep, el2n_noise, full_noise, mo):
    _ratio = el2n_noise / full_noise if full_noise else 1.0
    mo.callout(
        mo.md(
            f"Keeping the hardest **{el2n_keep.value}**, **{el2n_noise:.0f}%** of what you "
            f"train on has a wrong label. In the original dataset it was only "
            f"**{full_noise:.0f}%**. You have made the problem **{_ratio:.1f} times "
            f"worse**."
            + ("\n\nAnd this isn't bad luck with my made-up example. Think about what a "
               "wrongly labelled photo looks like to the quick model. It is a photo of a "
               "dog with the word 'person' attached. The model will never predict that "
               "correctly, because it isn't true. So it scores as *maximally hard* &mdash; "
               "it goes straight to the top of your ranking.\n\nWhich means sorting by "
               "difficulty is also, accidentally, sorting by badness of label. The harder "
               "you prune, the more of your dataset is junk."
               if _ratio > 1.2 else
               "\n\nNothing bad is happening yet, because you have kept nearly everything. "
               "Drag the slider down to 1 or 2 and watch what the ranking hands you.")
        ),
        kind="warn" if _ratio > 1.2 else "info",
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d5, d5_render, d5_sum = ask(
        "**Check 5.** One photo has the highest difficulty score in the whole dataset. "
        "What are the two things that could mean?",
        {
            "Either it's the most useful photo you own, or its label is wrong": "both",
            "Either it's the most useful photo you own, or it's a duplicate": "dup",
            "Either its label is wrong, or the quick model wasn't trained long enough": "proxy",
        },
        "both",
        "And the score can't tell you which. That is the whole problem. Both look identical: "
        "the model's guess was miles from the label. One of them is the photo your model "
        "most needs to see. The other is poison.\n\nThree ways to tell them apart, none of "
        "which are in the score:\n\n- **Ask two models.** A genuinely hard photo is hard for "
        "everybody. A mislabelled photo gets wrong in odd, inconsistent ways.\n- **Watch it "
        "over time.** If the model learns a photo, then forgets it, then learns it again, "
        "that's usually a bad label rather than a hard photo.\n- **Just look at them.** You "
        "only need to check the top of the list, so it's an hour of someone's afternoon, not "
        "a relabelling project.\n\nThe rule this gives you: **prune from the bottom, not the "
        "top.** Deleting the easiest photos is safe, because the worst case is you deleted "
        "something boring. Keeping only the hardest photos is dangerous, because the worst "
        "case is you kept only the mistakes.",
        key="d5",
    )
    d5
    return d5, d5_render, d5_sum


@app.cell(hide_code=True)
def _(d5, d5_render):
    d5_render(d5.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The one thing that has no downside

    Everything in this lab is a trade-off except this: **delete the duplicates.** Do it
    before anything else.

    It is the one free move available. Deleting a copy cannot cost you any accuracy, because
    whatever that photo had to teach is still sitting there in the original. And you save
    the full cost of training on it. Datasets scraped off the web are typically 30–50%
    near-duplicates. Our doorbell photos are worse than that.

    You do it in two passes:

    - **Exact copies.** Take a fingerprint of each file (an MD5 or SHA-256 hash) and throw
      away repeats. Basically free. Catches the photo that got uploaded twice, the file
      copied into two folders, the row inserted again when a request retried.
    - **Near copies.** A photo where one pixel changed has a completely different
      fingerprint, so the first pass misses it. Tools like MinHash group photos that are
      *roughly* alike into buckets, then you only compare within a bucket. More work, still
      cheap.

    And duplicates aren't only a waste of money. They quietly change what the model learns.
    A photo that appears 200 times gets 200 times the vote in every decision the model
    makes. You didn't choose that. The upload pipeline chose it for you.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d6, d6_render, d6_sum = ask(
        "**Check 6.** You carefully delete duplicates from your training photos. You leave "
        "the test set alone, because everyone knows you don't mess with the test set. What "
        "have you missed?",
        {
            "Nothing. Changing the test set would invalidate your results": "nothing",
            "Copies that sit in both sets, so test photos are also in your training data": "across",
            "The test set needs the savings too": "compute",
        },
        "across",
        "The duplicates don't care where you drew the line. If photo 4,812 is in your "
        "training set and a near-copy of it is in your test set, then you are testing the "
        "model on something it already memorised.\n\nHow much does this matter? About 8% "
        "overlap inflates your reported accuracy by roughly 5 points. That is more than most "
        "research papers claim as an improvement. So a model can ship at \"94% accurate\" "
        "and land in production at 89%, and nobody lied.\n\nThe first answer is the "
        "interesting one, because the instinct is right and aimed at the wrong thing. What "
        "ruins a test set is *picking* test examples based on how the model does on them. "
        "Removing a test photo because it's also in training isn't cheating, it's fixing a "
        "mistake.\n\nThe rule: deduplicate the whole lot **first**, then split into train and "
        "test. Never the other way round.",
        key="d6",
    )
    d6
    return d6, d6_render, d6_sum


@app.cell(hide_code=True)
def _(d6, d6_render):
    d6_render(d6.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: Did the choosing cost more than it saved?""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Now the bit the papers skip. **Choosing which photos to keep is not free.**

    Look back at what those two methods actually needed:

    - **k-center greedy** needed a number for all 100,000 photos. That means running every
      single photo through a neural network first. About 3.4 GPU-hours.
    - **EL2N** needed a quick model trained on everything before it could score anything.
      That's a small training run of its own. About 11 GPU-hours.

    Those hours come out of the same budget as the training they're supposed to save. So the
    real question is never "does this keep my accuracy up". It is:

    > Did I save more hours than I spent working out what to delete?

    Which depends on three things: how much you delete, which method you use, and how many
    times you'll train on the subset afterwards. Try all three.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    keep_pct = mo.ui.slider(
        5, 100, value=saved.get("keep_pct", 20), step=5, disabled=locked,
        label="How much of the 100,000 you keep (%)", show_value=True,
    )
    _methods = {
        "Pick at random (free)": "random",
        "Delete the duplicates (0.6 hrs)": "dedup",
        "One of each kind, as in Part 3 (3.4 hrs)": "kcenter",
        "Keep the hardest, as in Part 4 (11 hrs)": "el2n",
    }
    method = mo.ui.radio(
        options=_methods,
        value=pick(_methods, saved.get("method")) or "One of each kind, as in Part 3 (3.4 hrs)",
        disabled=locked, label="How you pick them",
    )
    runs = mo.ui.slider(
        1, 8, value=saved.get("runs", 1), step=1, disabled=locked,
        label="How many times you'll train on this subset", show_value=True,
    )
    mo.vstack([keep_pct, method, runs])
    return keep_pct, method, runs


@app.cell(hide_code=True)
def _(keep_pct, method, runs):
    # A cost model, not a measurement. The shapes are taken from the pruning
    # literature; the constants are invented so the arithmetic is legible. What it
    # is for is showing which term dominates and where the sign of the trade flips.
    FULL_HOURS = 100.0      # training once on all 100,000 frames
    FULL_ACC = 93.0         # what that gets you, from the table in Part 1
    DUP_SHARE = 0.45        # how much of this fleet's data is near-duplicate

    SELECT_HOURS = {
        "random": 0.0,      # a shuffle
        "dedup": 0.6,       # hashing is CPU work; the fuzzy pass dominates
        "kcenter": 3.4,     # one forward pass over 100k, plus distances
        "el2n": 11.0,       # a proxy model actually has to be trained
    }
    SELECT_NAME = {
        "random": "Picking at random",
        "dedup": "Deleting duplicates",
        "kcenter": "One of each kind",
        "el2n": "Keeping the hardest",
    }

    def retained(name, f):
        """Share of the full-data accuracy a subset of fraction f gets you."""
        if name == "random":
            return 1.0 - 0.12 * (1.0 - f) ** 2.0
        if name == "dedup":
            # Removing duplicates costs nothing until the duplicates run out; past
            # that you are deleting unique frames, and it degrades like random.
            if f >= 1.0 - DUP_SHARE:
                return 1.0
            short = (1.0 - DUP_SHARE - f) / (1.0 - DUP_SHARE)
            return 1.0 - 0.12 * short ** 2.0
        if name == "kcenter":
            return 1.0 - 0.06 * (1.0 - f) ** 1.6
        # EL2N is the best of them in the middle and the worst at the extreme: keep
        # only the hardest few per cent and you have kept the label noise and thrown
        # away the easy examples that anchor the rest of the boundary.
        collapse = max(0.0, 0.15 - f) * 1.2
        return 1.0 - 0.05 * (1.0 - f) ** 1.4 - collapse

    sel_name = method.value
    keep_f = keep_pct.value / 100.0
    train_hours = FULL_HOURS * keep_f * runs.value
    select_hours = SELECT_HOURS[sel_name]
    total_hours = train_hours + select_hours
    full_hours = FULL_HOURS * runs.value
    saved_hours = full_hours - total_hours

    acc = FULL_ACC * retained(sel_name, keep_f)
    points_lost = FULL_ACC - acc
    # The trade, stated as the thing an engineer has to sign off on.
    hours_per_point = (saved_hours / points_lost) if points_lost > 0.005 else None
    pays = saved_hours > 0
    return (
        FULL_ACC,
        FULL_HOURS,
        SELECT_NAME,
        acc,
        full_hours,
        hours_per_point,
        keep_f,
        pays,
        points_lost,
        saved_hours,
        sel_name,
        select_hours,
        total_hours,
        train_hours,
    )


@app.cell(hide_code=True)
def _(LAB_CSS, acc, mo, points_lost, saved_hours, total_hours):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w7-grid">
          <div class="w7-stat">
            <span class="k">Hours you spend</span>
            <span class="v">{total_hours:,.1f}</span>
            <span class="why">the training plus the choosing</span>
          </div>
          <div class="w7-stat {'green' if saved_hours > 0 else 'red'}">
            <span class="k">Hours you save</span>
            <span class="v">{saved_hours:+,.1f}</span>
            <span class="why">compared with just training on all of it</span>
          </div>
          <div class="w7-stat">
            <span class="k">Accuracy you get</span>
            <span class="v">{acc:,.1f}%</span>
            <span class="why">{points_lost:.2f} points worse than using everything</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, full_hours, mo, select_hours, total_hours, train_hours):
    _ = LAB_CSS
    _span = max(full_hours, total_hours)
    _t = 100.0 * train_hours / _span
    _s = 100.0 * select_hours / _span
    _f = max(0.0, 100.0 - _t - _s)

    def _seg(cls, width, text):
        if width < 0.5:
            return ""
        return (f'<span class="{cls}" style="width:{width}%">'
                f'{text if width > 11 else ""}</span>')

    mo.Html(
        f"""
        <div class="w7-budget">
          {_seg("t", _t, f"training {train_hours:,.1f} h")}
          {_seg("s", _s, f"choosing {select_hours:,.1f} h")}
          {_seg("f", _f, "hours you kept")}
        </div>
        <div class="w7-key">
          <span><i style="background:#4a6fa5"></i> training on what you kept</span>
          <span><i style="background:#c87f5a"></i> working out what to keep</span>
          <span><i style="background:#dcdcdc"></i> saved, out of {full_hours:,.0f} hours</span>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(FULL_ACC, FULL_HOURS, LAB_CSS, keep_f, mo, runs):
    # The same arithmetic for all four methods at the current keep rate, so the
    # comparison does not depend on remembering what the last setting showed.
    _ = LAB_CSS
    _sel = {"random": 0.0, "dedup": 0.6, "kcenter": 3.4, "el2n": 11.0}
    _label = {"random": "Pick at random", "dedup": "Delete duplicates",
              "kcenter": "One of each kind", "el2n": "Keep the hardest"}

    def _ret(name, f):
        if name == "random":
            return 1.0 - 0.12 * (1.0 - f) ** 2.0
        if name == "dedup":
            if f >= 0.55:
                return 1.0
            return 1.0 - 0.12 * ((0.55 - f) / 0.55) ** 2.0
        if name == "kcenter":
            return 1.0 - 0.06 * (1.0 - f) ** 1.6
        return 1.0 - 0.05 * (1.0 - f) ** 1.4 - max(0.0, 0.15 - f) * 1.2

    _rows = ""
    for _m in ("random", "dedup", "kcenter", "el2n"):
        _tot = FULL_HOURS * keep_f * runs.value + _sel[_m]
        _save = FULL_HOURS * runs.value - _tot
        _a = FULL_ACC * _ret(_m, keep_f)
        _lost = FULL_ACC - _a
        _verdict = ('<span class="tick">worth it</span>' if _save > 0
                    else '<span class="cross">cost more than it saved</span>')
        _rows += (
            f"<tr><td>{_label[_m]}</td><td class='num'>{_sel[_m]:.1f}</td>"
            f"<td class='num'>{_tot:,.1f}</td><td class='num'>{_save:+,.1f}</td>"
            f"<td class='num'>{_a:.1f}%</td><td class='num'>{_lost:.2f}</td>"
            f"<td>{_verdict}</td></tr>"
        )
    mo.Html(
        f"""
        <table class="w7-table">
          <thead><tr><th>Method</th><th>Hours choosing</th><th>Hours total</th>
            <th>Hours saved</th><th>Accuracy</th><th>Points given up</th><th></th></tr></thead>
          <tbody>{_rows}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(
    SELECT_NAME,
    hours_per_point,
    keep_pct,
    mo,
    pays,
    points_lost,
    runs,
    saved_hours,
    sel_name,
    select_hours,
):
    _trade = ("and it costs you no accuracy worth measuring. Free money."
              if hours_per_point is None else
              f"and every accuracy point you gave up bought you "
              f"**{hours_per_point:,.0f} GPU-hours**. Whether that is a good deal is your "
              f"call, not the algorithm's.")
    _amort = ("" if runs.value == 1 else
              f"\n\nAlso notice what happened when you set it to **{runs.value}** training "
              f"runs. The {select_hours:,.1f} hours of choosing get paid **once**, but the "
              f"saving happens every single run. This is why a team doing a big "
              f"hyperparameter sweep can afford a much fussier selection method than a team "
              f"training once and shipping.")
    mo.callout(
        mo.md(
            f"**{SELECT_NAME[sel_name]}**, keeping **{keep_pct.value}%**: "
            + (f"you save **{saved_hours:,.1f}** GPU-hours, {_trade}"
               if pays else
               f"this **costs you {-saved_hours:,.1f} hours more than just training on "
               f"everything**, and you still end up {points_lost:.2f} points less "
               f"accurate. Worst of both.\n\nThe reason is that the choosing costs "
               f"{select_hours:,.1f} hours no matter how much you keep. Keep almost "
               f"everything and there's barely any training left to save.")
            + _amort
        ),
        kind="success" if pays else "danger",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Two things in that table surprise people. Set the slider to 20%, then to 5%, and watch.

    **"Keep the hardest" is the best method at 20% and the worst at 5%** — worse even than
    picking at random. That flip is real, not an artefact of my made-up numbers.

    Here is why. Keeping the hardest photos works by throwing away the easy middle of each
    group and keeping the tricky edges, and that is a good trade right up until the middle
    is gone. Then the model has nothing but edge cases. It has never seen an obvious,
    unmistakable photo of a person. On top of that, the label noise from Part 4 is now a big
    chunk of what's left. So: **the more aggressively you prune, the more you should lean on
    "one of each kind" and the more you should deliberately keep some easy photos.**

    **"Delete duplicates" is free until it isn't.** Keep anything above 55% and you lose
    zero accuracy. Below 55% it starts falling off. The reason is simple: 45% of this
    dataset was duplicates, so at 55% you have deleted the last one. Keep deleting and you
    are now throwing away real photos at random, which is exactly what the random row does.

    Every method has a point like that, where the thing it was exploiting runs out. Finding
    yours tells you when to stop and move to the next stage.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Be honest: where do these numbers come from?": mo.md(
                """
                The *shapes* of these curves come from real published results on pruning.
                The exact constants I made up, so the arithmetic stays readable. Same deal
                as the memory budget in Week 6: good enough to show you which thing
                dominates and where a trade flips sign, not good enough to plan next
                quarter with. Here's what it ignores.

                - **Your time.** A duplicate-deletion pipeline is half a day of somebody's
                  attention before it is 0.6 GPU-hours. The salary usually costs more than
                  the compute.
                - **Stuff you already have.** If another team already ran all your photos
                  through a network last month, the 3.4 hours mostly vanish. Go and ask
                  before you spend it.
                - **Luck.** These are single numbers for things that actually vary a lot.
                  Picking 10% at random sometimes goes much worse than the average
                  suggests.
                - **Combining methods.** Delete the duplicates *and then* pick one of each
                  kind from what's left. That beats either on its own and costs about the
                  sum of the two. Nothing here lets you try that.
                - **Storage.** Sometimes GPU-hours aren't the problem at all, and what's
                  actually hurting is the bill for keeping 100,000 photos somewhere.
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d7, d7_render, d7_sum = ask(
        "**Check 7.** \"Keep the hardest\" costs 11 GPU-hours to work out, and it costs "
        "that whether you end up keeping 5% or 95%. When does it stop being worth it?",
        {
            "Never. Choosing is always cheaper than the training it replaces": "never",
            "When you keep so much that the training you saved is worth less than 11 hours": "high",
            "When the dataset is too small to have duplicates in it": "small",
        },
        "high",
        "Set the slider to 95% and look. You saved 5 hours of training and spent 11 working "
        "out what to delete. You are 6 hours down, and slightly *less* accurate than if "
        "you'd done nothing at all.\n\nThe thing to take away is the shape of it. **The cost "
        "of choosing is fixed. The saving depends on how much you delete.** So:\n\n- "
        "Expensive methods only make sense if you're deleting a lot.\n- Or if you'll reuse "
        "the subset. Train on it eight times and the 11 hours is paid once.\n- And it's why "
        "deleting duplicates always goes first. At 0.6 hours it pays for itself almost "
        "immediately, and it shrinks the pile that every later method has to chew through.",
        key="d7",
    )
    d7
    return d7, d7_render, d7_sum


@app.cell(hide_code=True)
def _(d7, d7_render):
    d7_render(d7.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 6: Changing your mind as you go""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Everything so far happened once, up front, before training started. But here is the
    thing: **whether a photo is useful depends on what the model currently knows.**

    A photo the model can't handle yet is worth showing it. The moment it learns that photo,
    the same photo is worth nothing. It has changed from useful to useless without changing
    at all.

    So instead of picking a subset once, you keep changing it as training goes on. There
    are three ways to do this, and the easiest way to keep them straight is to ask what
    you're short of.

    ### Short of time: show the easy ones first

    This is **curriculum learning**, and it is named after exactly what you think. You don't
    teach a child long division on day one.

    Score every photo by how hard it is, then start the model on the easy ones and bring in
    harder ones as it improves. Measuring difficulty is easy: just look at how confident
    the model is about the right answer.

    | Photo | How sure the model is | Difficulty |
    | - | - | - |
    | Clear pedestrian, daylight | 95% | 0.05 |
    | Pedestrian in shadow | 70% | 0.36 |
    | Pedestrian half hidden | 40% | 0.92 |
    | Pedestrian at night | 10% | 2.30 |

    Teach them in that order. The usual claim is that you reach your target accuracy 20–30%
    faster than feeding photos in randomly.

    Worth knowing: it doesn't always work. Sometimes random order wins. The variations
    mostly argue about *pacing* — how fast to introduce the hard stuff, and whether the
    model decides for itself or follows a schedule you set.

    ### Short of labels: that's the next two

    The other two are both about not having enough labels. **Active learning** has some
    money and spends it. **Semi-supervised learning** has no money and manages anyway.

    Those two are worth doing slowly, because they both compute the same number and then do
    the exact opposite thing with it.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Short of labels, with money: ask about the confusing ones

    Back to the doorbell. You have 10,000 labelled photos, 90,000 unlabelled, and budget to
    get 1,000 more labelled. Paying a human to label one photo costs somewhere between $5
    and $100 depending on how specialised the judgement is. So that budget is real money,
    and the question is which 1,000 photos to spend it on.

    The idea behind **active learning** is to let the model choose. Train it on the 10,000
    you have, then run it over the unlabelled pile. For every photo it gives you three
    percentages: how likely it thinks person, package, and nothing are. Where it is unsure,
    a human label would teach it a lot. Where it is confident, a human label tells it
    something it already knew.

    Here are five photos from the pile. But "unsure" turns out to have more than one
    meaning, so pick a definition and watch who gets chosen.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _strats = {
        "Its best guess is the weakest (least confidence)": "conf",
        "Its top two guesses are closest together (margin)": "margin",
        "It is spreading its bet most evenly (entropy)": "entropy",
        "Don't choose. Pick one at random": "random",
    }
    strategy = mo.ui.radio(
        options=_strats,
        value=pick(_strats, saved.get("strategy")) or
              "Its best guess is the weakest (least confidence)",
        disabled=locked, label="**Which photo counts as the one it's most unsure about?**",
    )
    strategy
    return (strategy,)


@app.cell(hide_code=True)
def _(strategy):
    import math as _math

    # Five frames from the unlabelled pool, as (person, package, empty). Chosen so
    # the three uncertainty measures do not agree, which is the point of the section.
    POOL = [
        ("f1", (0.40, 0.35, 0.25), "Something at the edge of the frame"),
        ("f2", (0.34, 0.33, 0.33), "Heavy rain, low light"),
        ("f3", (0.45, 0.45, 0.10), "A figure holding a box"),
        ("f4", (0.50, 0.25, 0.25), "Dusk, movement near the gate"),
        ("f5", (0.90, 0.05, 0.05), "A pedestrian on the path"),
    ]

    def scores(p):
        top = sorted(p, reverse=True)
        return {
            "conf": 1.0 - top[0],
            "margin": top[0] - top[1],
            "entropy": -sum(q * _math.log(q) for q in p if q > 0),
            "random": 0.0,
        }

    POOL_SCORES = [(name, probs, scene, scores(probs))
                   for name, probs, scene in POOL]
    # Least confidence and entropy want the largest score, margin the smallest.
    _key = strategy.value
    if _key == "random":
        query_order = [n for n, _p, _s, _sc in POOL_SCORES]
    elif _key == "margin":
        query_order = [n for n, _p, _s, _sc in
                       sorted(POOL_SCORES, key=lambda r: r[3]["margin"])]
    else:
        query_order = [n for n, _p, _s, _sc in
                       sorted(POOL_SCORES, key=lambda r: -r[3][_key])]
    query_pick = query_order[0]
    return POOL_SCORES, query_order, query_pick


@app.cell(hide_code=True)
def _(LAB_CSS, POOL_SCORES, mo, query_order, strategy):
    _ = LAB_CSS
    _rank = {n: i + 1 for i, n in enumerate(query_order)}
    _random = strategy.value == "random"
    _body = ""
    for _n, _p, _scene, _sc in POOL_SCORES:
        _r = _rank[_n]
        _body += (
            f"<tr class='{'on' if _r == 1 and not _random else ''}'>"
            f"<td><code>{_n}</code></td><td>{_scene}</td>"
            f"<td class='num'>{_p[0]:.2f} / {_p[1]:.2f} / {_p[2]:.2f}</td>"
            f"<td class='num'>{_sc['conf']:.2f}</td>"
            f"<td class='num'>{_sc['margin']:.2f}</td>"
            f"<td class='num'>{_sc['entropy']:.3f}</td>"
            f"<td class='num'>{'any' if _random else _r}</td></tr>"
        )
    mo.Html(
        f"""
        <table class="w7-table">
          <thead><tr><th>Photo</th><th>What's in it</th>
            <th>Model says person / package / nothing</th>
            <th>Weakest best guess</th><th>Closest top two</th><th>Most evenly spread</th>
            <th>Your pick order</th></tr></thead>
          <tbody>{_body}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, query_pick, strategy):
    _notes = {
        "conf": (
            f"This sends **{query_pick}** off to be labelled: the photo where the model's "
            "best guess is weakest. It is the simplest thing to compute and the easiest to "
            "explain to whoever controls the budget.\n\nIts weakness is that it only looks "
            "at one number, the top guess, and ignores everything underneath. So it can't "
            "tell the difference between a photo where the model is torn between two "
            "specific answers and one where it's vaguely lost about all three. Those are "
            "different problems."
        ),
        "margin": (
            f"This sends **{query_pick}** — and notice that's a *different photo* from the "
            "one the other two methods picked. Worth pausing on.\n\nMargin asks \"how close "
            "is this decision?\" So `f3` wins outright: the model is sitting at 45% person, "
            "45% package. It is perfectly torn, and one human label would settle it "
            "completely.\n\nNow look at where `f3` ranks under \"most evenly spread\": "
            "**fourth**. Because 45 / 45 / 10 isn't evenly spread at all — the model is "
            "quite sure it isn't nothing. Both methods are right, they're just answering "
            "different questions. If what you care about is a close call between two "
            "options, margin is your measure."
        ),
        "entropy": (
            f"This sends **{query_pick}**, and it is the only one of the three that looks "
            "at all three numbers rather than just the top one or two. Reach for it when "
            "you have lots of possible answers and a photo can be confusing in more than "
            "one way.\n\nWith only three classes it mostly agrees with \"weakest best "
            "guess\". The interesting disagreement is `f3`: this method ranks it fourth, "
            "margin ranks it first. Have a look at its numbers and work out why."
        ),
        "random": (
            "Not choosing at all, and here is the unglamorous finding from decades of "
            "research on this: **it's hard to beat.**\n\nEvery clever method above is making "
            "a bet that the model's own confidence is trustworthy. Early in training it "
            "isn't. And a model that is confidently wrong is invisible to all three of "
            "them — it will never flag the photos it's most badly mistaken about, because "
            "it doesn't know it's mistaken.\n\nRandom makes no bet, costs nothing, and gives "
            "you a labelled set that actually represents your data, which means you can "
            "measure things with it. If somebody shows you an active learning result "
            "without the random comparison at the same budget, they haven't shown you "
            "anything."
        ),
    }
    mo.callout(mo.md(_notes[strategy.value]), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The table above has five photos, which hides a problem you'd hit immediately in real
    life, where you have 90,000 photos and a budget for 1,000.

    Sort all 90,000 by how unsure the model is. Take the top 1,000. What you will very
    often get is **1,000 near-identical photos of the one thing the model finds confusing.**
    At $50 each, that's $50,000 spent asking the same question a thousand times. One label
    would have done.

    This is the Part 3 problem back again, so the fix is the Part 3 fix: sort by
    uncertainty, then pick **one of each kind** from the top of that list. Nearly all real
    active learning systems do both, in that order.

    One other method worth knowing by name. **Query by committee**: train five models
    instead of one, and ask about the photos they disagree with each other about. Five times
    the cost, and more reliable — it's much harder for five models to be confidently wrong
    together than for one.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Short of labels, with no money: use the model's own guesses

    Now change one thing. The budget is zero. You still have 90,000 unlabelled photos and a
    model that will happily give you percentages for all of them.

    **Pseudo-labelling** is the obvious move, once you hear it: where the model is already
    confident, just write its guess down as if it were the truth, and train on that. Pick a
    cut-off, say 85% sure. Anything above it gets a label. Anything below gets thrown away.

    And now notice what has happened. Active learning and pseudo-labelling look at **the
    very same number** and go in opposite directions. Move the cut-off and watch the last
    column.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    tau = mo.ui.slider(
        50, 99, value=saved.get("tau", 85), step=1, disabled=locked,
        label="How sure must it be before we believe it? (%)", show_value=True,
    )
    tau
    return (tau,)


@app.cell(hide_code=True)
def _(LAB_CSS, POOL_SCORES, mo, query_pick, tau):
    _ = LAB_CSS
    _t = tau.value / 100.0
    _classes = ("person", "package", "empty")
    _IN = '<span class="tick">believe it, train on it</span>'
    _WANTED = '<span class="cross">the one the human was going to label</span>'
    _body = ""
    for _n, _p, _scene, _sc in POOL_SCORES:
        _top = max(_p)
        _lab = _classes[_p.index(_top)]
        _ok = _top >= _t
        _body += (
            f"<tr class='{'on' if _ok else 'off'}'><td><code>{_n}</code></td>"
            f"<td class='num'>{_top:.2f}</td>"
            f"<td>{_lab if _ok else '&mdash;'}</td>"
            f"<td>{_IN if _ok else 'discarded'}</td>"
            f"<td>{_WANTED if _n == query_pick else ''}</td>"
            f"</tr>"
        )
    mo.Html(
        f"""
        <table class="w7-table">
          <thead><tr><th>Photo</th><th>How sure</th><th>Label we write down</th>
            <th>At a {tau.value}% cut-off</th><th></th></tr></thead>
          <tbody>{_body}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(POOL_SCORES, mo, query_pick, tau):
    _t = tau.value / 100.0
    _kept = [n for n, p, _s, _sc in POOL_SCORES if max(p) >= _t]
    mo.callout(
        mo.md(
            (f"At a **{tau.value}%** cut-off, **{len(_kept)}** of the five photos get "
             f"labelled by the model: {', '.join('`' + k + '`' for k in _kept)}."
             if _kept else
             f"At **{tau.value}%** nothing makes the cut. Set the bar high enough and this "
             "whole technique quietly does nothing, leaving you training on the 10,000 "
             "photos you already had.")
            + f"\n\nNow, `{query_pick}` is the photo your active learner wanted to spend "
              "$50 on. Is it in the list? "
            + ("Yes — and that should bother you. It got in *because* the model is "
               "confident, and the human was being asked about it because the model "
               "**isn't**. Something has gone wrong with your cut-off."
               if query_pick in _kept else
               "No, and it never could be. It's the photo the model is least sure about, "
               "so it will always be the last one in.")
            + "\n\n**And that's the whole relationship.** One number, two opposite ends:"
              "\n\n- Active learning takes the photos the model is **worst** at and pays a "
              "human, because that's where the mistakes are.\n- Pseudo-labelling takes the "
              "photos the model is **best** at and pays nobody, because that's where its "
              "guesses are safe enough to trust.\n\nSo the confusing photos are the valuable "
              "ones *and* the expensive ones. The easy photos are free *and* nearly "
              "worthless. Nothing about that is a coincidence — it's the same fact seen "
              "from two budgets."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The obvious objection

    You may already be uneasy about pseudo-labelling, and you should be. The model is
    training on its own opinions. If it is confidently wrong about something, that wrong
    answer becomes a training example, and now it is *more* confidently wrong. Whatever it
    was already biased about gets worse.

    Raising the cut-off limits the damage and also gives you less data. That's the trade,
    and there's no clever way out of it.

    ### The idea that fixes it

    Here is the trick that turns this from recycling into actually learning something new.

    Take an unlabelled photo. Rotate it slightly. Brighten it. Crop a corner off. You don't
    know what's in the photo — but you know **it's still the same thing**. A person doesn't
    stop being a person because you brightened the image.

    So you can demand that the model gives the same answer to both versions. And you can
    check that **without ever knowing the right answer.** That's a genuinely new source of
    information, squeezed out of unlabelled data, and it isn't circular: you're not asking
    the model to agree with its own past guesses, you're asking it to be consistent with
    itself right now.

    People call this **consistency regularisation**.

    ### FixMatch: both ideas together

    **FixMatch** is just those two ideas stapled together, and the result is neater than
    either one alone. For each unlabelled photo:

    1. Make an **easy** version. Flip it, nudge it a few pixels.
    2. Ask the model what it is. Take its best guess.
    3. **If it isn't confident enough, bin it.** (That's the slider above.)
    4. Make a **hard** version of the same photo. Crank the brightness, cut a chunk out,
       distort it.
    5. Train the model to give the hard version the same answer it gave the easy one.

    Walk through a real one. A photo has a pedestrian in it, and nobody has labelled it.

    - Easy version: the model says **97% person**. That clears a 95% cut-off, so we write
      down "person" and keep going.
    - Hard version, brightness pushed and half the figure hidden: the model says **60%
      person**. Much less sure.
    - So we nudge it: *you said 97% on the easy one, be more confident on the hard one
      too.*

    And that's the point. Step 3 stops the model learning from its own bad guesses. Step 4
    makes the good guesses actually worth learning from, because recognising a half-hidden
    pedestrian in bad light is a genuinely harder skill than recognising a clear one.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    d8, d8_render, d8_sum = ask(
        "**Check 8.** Active learning and FixMatch both sort the unlabelled photos by how "
        "confident the model is. What does each one do with that sorted list?",
        {
            "Both take the unsure ones; they just differ in who does the labelling": "both-unc",
            "Active learning takes the unsure end and pays a human; FixMatch takes the confident end and pays nobody": "opposite",
            "Both take the confident ones; active learning then double-checks them": "both-conf",
        },
        "opposite",
        "Opposite ends of one list, and it comes down to what each one is short of.\n\n"
        "Active learning has money. So it buys the photos the model **can't** do, because "
        "that's where a label changes something. FixMatch has no money. So it needs guesses "
        "that are safe, which means the photos the model **can** do — and it accepts that "
        "each one teaches very little.\n\nThe nice consequence: these two don't compete, "
        "they stack. Let the model label the confident end for free. Pay humans for the "
        "unsure end. Ignore the middle. You've now used your whole pile of photos and spent "
        "money only where it mattered.\n\nThe first answer is worth naming as a mistake, "
        "because it sounds right — both methods *do* care about confidence. But writing "
        "down a label for a photo the model is unsure about is exactly the thing the cut-off "
        "exists to prevent.",
        key="d8",
    )
    d8
    return d8, d8_render, d8_sum


@app.cell(hide_code=True)
def _(d8, d8_render):
    d8_render(d8.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The three of them, side by side

    | | Use it when | What it decides | What it costs you |
    | - | - | - | - |
    | Easy ones first | Training converges too slowly | What the model sees, and when | Scoring every photo once |
    | Ask a human | You have money for labels | Which photos a human looks at | Retraining after every round |
    | Model labels itself | You have no money for labels | Which of its guesses to believe | Two versions of every photo |

    Look at that last column, because it is the Part 5 lesson wearing a different hat. The
    expensive part of active learning **is not the labels**. It is that you have to retrain
    the model after every batch before you can ask it what to buy next. Ten rounds of
    active learning means ten training runs.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 7: Spend the money""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Right. Here is where you are:

    - 90,000 unlabelled photos, about two thirds of them empty daylight driveways.
    - Budget to get 1,000 of them labelled by a human.
    - And one known problem: **the model keeps missing people at night.** That is the
      failure that gets somebody hurt and the company sued.

    Pick how you spend the 1,000 labels, and say what you'd conclude from each outcome.
    This one goes in your report.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "The 1,000 photos the model is least sure about": "uncertain",
        "1,000 picked to cover every kind of photo, as in Part 3": "diverse",
        "1,000 at random": "random",
        "Spend nothing. Let the model label the confident ones and keep the money": "pseudo",
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
                label="**How do you spend the thousand labels?**",
            ),
            why=mo.ui.text_area(
                value=_saved.get("why", ""),
                disabled=locked,
                placeholder="I expect... If night-time misses go down, that tells me... "
                            "If they don't, that tells me...",
                label="**Why that one? And what would you conclude if it worked, or if it "
                      "didn't?** Not marked, and you can change it as often as you like.",
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
        "uncertain": (
            "The textbook answer, and it will probably beat random. But there are two traps "
            "here and you should see them coming.\n\n**Trap one.** Two thirds of your photos "
            "are the same driveway. So the \"most unsure\" list will be full of whatever the "
            "model finds slightly puzzling about *that one scene*. You could spend all "
            "1,000 labels asking the same question.\n\n**Trap two, and this is the bad one.** "
            "It doesn't target your actual problem. You need night-time people. This method "
            "only finds night photos if the model happens to be *unsure* about them. But a "
            "model that confidently calls a dark photo \"nothing\" is not unsure at all. "
            "**Confidently wrong is completely invisible to this method**, and confidently "
            "wrong is exactly your bug.\n\nBoth are fixable and cheap. Split the pile by "
            "time of day first. Then rank by uncertainty inside each group. Then spread the "
            "batch out using Part 3. That stack is roughly what real systems do."
        ),
        "diverse": (
            "A better fit for *this* dataset than pure uncertainty, and you can say why "
            "before running it: the thing wrong with this data is **too many copies**, not "
            "difficulty. Coverage attacks copies directly. It will not spend 900 labels on "
            "driveways.\n\nWhat you give up is that it doesn't know anything about labels or "
            "about your model. It will cheerfully buy labels for photos the model already "
            "handles perfectly, just because they look unusual. And as in Check 4, it has "
            "no idea that night-time people are what you're judged on — so set a quota for "
            "night photos first, then let it choose the rest.\n\nHonest summary: coverage is "
            "the right **first** move when your data is full of copies. Uncertainty is the "
            "right **second** move, once the copies are gone and the model's opinion is "
            "worth listening to."
        ),
        "random": (
            "Not the clever answer, and genuinely defensible. Here's the argument.\n\n"
            "Random gives you a *representative* set of labels, and that buys you two "
            "things nothing else does. You can find out what's actually in your unlabelled "
            "pile. And you get an honest way to measure the model.\n\nThat second one "
            "matters more than it sounds. Every clever method above deliberately picks "
            "weird, confusing photos. **You cannot measure your night-time accuracy on a "
            "set that was chosen for being confusing.** The number would mean nothing.\n\n"
            "The cost is that two thirds of your money goes on empty driveways.\n\nSo what "
            "most teams should actually do is split it: a few hundred at random so you can "
            "measure, the rest chosen cleverly so you can learn. Working out that you need "
            "both is worth more than picking the best single method."
        ),
        "pseudo": (
            "Free, tempting, and the one option that **cannot** fix the problem you were "
            "given.\n\nThink about which photos this collects. The ones the model is already "
            "confident about — which here means daylight driveways. So you train the model "
            "to be even better at daylight driveways. Your problem is that it doesn't know "
            "what a person at night looks like, and no amount of its own daytime opinions "
            "will ever tell it.\n\nIt can actively go backwards. Suppose the model "
            "confidently labels dark photos as \"nothing\". This method will now generate "
            "thousands of night photos labelled *nothing* and train on them. You have taught "
            "it that nothing happens at night. That is your exact bug, with a budget behind "
            "it.\n\nIt isn't a bad technique. It's the wrong technique for a known gap. Run "
            "it on the confident end *while* spending your money on the end the model is "
            "wrong about. And since the 1,000 labels are already approved, spending zero of "
            "them is a hard thing to justify to whoever approved them."
        ),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "Same point as Week 6: how you reasoned matters more than which one you picked. "
            "**A good plan is one where you can say in advance what each result would mean.**"
            "\n\nSo: suppose night-time misses drop by half. Was that because you bought "
            "night photos, or just because you added 1,000 labels of anything? If you can't "
            "tell those apart afterwards, you've spent the money and learnt nothing you can "
            "use next quarter."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### What you should actually do on day one

    None of the above, in fact. Before picking any method, go and measure the data. All five
    of these are a morning's work and any of them can change your whole plan.

    | Question | How you answer it | When to worry |
    | - | - | - |
    | How many of these are copies? | Fingerprint them all, then look for near-copies | Over 20%: delete them and start again |
    | Do copies span train and test? | Fingerprint both sets together, look for matches | Any at all — your accuracy number is wrong |
    | Is it all coming from a few cameras? | Count photos per camera, per hour of day | A handful dominating: your "coverage" is coverage of them |
    | How many labels are wrong? | Re-label 300 at random and compare | Over a few per cent: don't prune by difficulty |
    | Where is the model actually failing? | Accuracy per group, on a *representative* test set | Almost always somewhere you didn't expect |

    That last row is the one everybody skips, and it decides all the others. Every method in
    this lab is a way of spending a fixed budget on a specific gap. If you don't know what
    the gap is, you're guessing — you're just guessing with arithmetic attached, which feels
    better and isn't.
    """
    )
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
                placeholder="I would measure... and if it came back as... I would change "
                            "the plan, because...",
                label="**Last one.** Somebody hands you the 100,000 photos tomorrow "
                      "morning. Before you run any of this, what is the one thing you would "
                      "go and measure? And what result would make you change your plan?",
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
def _(
    d1,
    d2,
    d3,
    d4,
    d5,
    d6,
    d7,
    d8,
    decision_form,
    el2n_keep,
    hunch_form,
    kc_keep,
    kc_start,
    keep_pct,
    lab_sync,
    method,
    runs,
    strategy,
    tau,
):
    # Marked answers go through record_once, so the first answer is the one that
    # counts. Sliders and the written decision can change freely.
    if lab_sync is not None:
        lab_sync.record_once(
            d1=d1.value, d2=d2.value, d3=d3.value, d4=d4.value,
            d5=d5.value, d6=d6.value, d7=d7.value, d8=d8.value,
        )
        lab_sync.record(
            kc_start=kc_start.value, kc_keep=kc_keep.value,
            el2n_keep=el2n_keep.value, keep_pct=keep_pct.value,
            method=method.value, runs=runs.value,
            strategy=strategy.value, tau=tau.value,
        )
        if hunch_form.value is not None:
            lab_sync.record(hunch=hunch_form.value)
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
    d1,
    d1_sum,
    d2,
    d2_sum,
    d3,
    d3_sum,
    d4,
    d4_sum,
    d5,
    d5_sum,
    d6,
    d6_sum,
    d7,
    d7_sum,
    d8,
    d8_sum,
):
    # One place that knows every marked answer, so the report, the score and the
    # dashboard cannot disagree.
    CHECKS = [
        ("What to work on when data is scarce", d1_sum(d1.value)),
        ("A learning rate is not a destination", d2_sum(d2.value)),
        ("What random picking leaves you with", d3_sum(d3.value)),
        ("Where coverage is blind", d4_sum(d4.value)),
        ("Two reasons a photo scores as hard", d5_sum(d5.value)),
        ("Copies that span train and test", d6_sum(d6.value)),
        ("When choosing costs more than it saves", d7_sum(d7.value)),
        ("One number, two opposite ends", d8_sum(d8.value)),
    ]
    checks_right = sum(1 for _n, (_t, _ok) in CHECKS if _ok)
    checks_score = f"{checks_right}/{len(CHECKS)}"
    return CHECKS, checks_right, checks_score


@app.cell(hide_code=True)
def _(
    CHECKS,
    LAB_CSS,
    SELECT_NAME,
    acc,
    checks_score,
    decision_choice,
    decision_why,
    done,
    el2n_noise,
    kc_trace,
    keep_pct,
    mo,
    query_pick,
    saved_hours,
    sel_name,
    strategy,
    takeaway_text,
    tau,
):
    _ = (LAB_CSS, done)
    _what = {
        "uncertain": "Label the 1,000 the model is least sure about",
        "diverse": "Label 1,000 picked to cover every kind of photo",
        "random": "Label 1,000 at random",
        "pseudo": "Spend nothing; let the model label the confident ones",
    }
    _strat = {"conf": "weakest best guess", "margin": "closest top two",
              "entropy": "most evenly spread", "random": "no strategy, just random"}

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
        mo.md("## Your Week 7 report"),
        mo.Html(
            f"""
            <div class="w7-report">
              <div class="row">
                <span class="k">Marked checks</span>
                <span class="v"><span class="w7-score">{checks_score}</span></span>
              </div>
              <div class="row">
                <span class="k">Subset you picked</span>
                <span class="v">Kept {len(kc_trace)} of 7 photos, worst gap
                {kc_trace[-1][2]:.1f}. Keeping only the hardest left {el2n_noise:.0f} per
                cent wrong labels in what you'd train on</span>
              </div>
              <div class="row">
                <span class="k">What it cost</span>
                <span class="v">{SELECT_NAME[sel_name]}, keeping {keep_pct.value} per cent:
                {saved_hours:+,.1f} GPU-hours compared with training on everything, and
                {acc:.1f} per cent accuracy</span>
              </div>
              <div class="row">
                <span class="k">How you chose what to label</span>
                <span class="v">{_strat[strategy.value]}, which picked
                <code>{query_pick}</code>. Model labelled its own guesses above
                {tau.value} per cent</span>
              </div>
              <div class="row">
                <span class="k">How you spent the labels</span>
                <span class="v">{_what.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Reasoning</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">What you would measure first</span>
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
        ("The order was: delete copies, then pick a subset, then sort easy-to-hard. What "
         "does skipping the first step cost you?",
         {"Nothing, as long as the subset method is a good one": "a",
          "You pay twice, because every later step has to score and rank all the copies too": "b",
          "Only storage, since the later steps will drop the copies anyway": "c"},
         "b"),
        ("You have 90,000 unlabelled photos, plenty of compute, and no money at all for "
         "labelling. What can you still do?",
         {"Ask a human about the confusing ones, since that needs the fewest labels": "a",
          "Show the easy ones first, since that just reorders what you have": "b",
          "Let the model label its own confident guesses, since that costs nothing": "c"},
         "c"),
        ("Your model picks up the easy cases quickly, then crawls on the hard ones. What "
         "would you try?",
         {"Show it the easy ones first and bring in hard ones gradually": "a",
          "Pay humans to label the hard cases": "b",
          "Delete the duplicates, since slow training means redundant data": "c"},
         "a"),
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
def _(done, locked, mo):
    _ = done
    # Handing in cannot be undone, so it takes a tick as well as a press.
    confirm = mo.ui.checkbox(
        label="I have read my answers back and I know they cannot be changed after this",
        disabled=locked,
    )
    return (confirm,)


@app.cell(hide_code=True)
def _(confirm, done, lab_sync, locked, mo, quiz):
    _ = done
    _unanswered = sum(v is None for v in quiz.value)
    submit_button = mo.ui.run_button(
        label="Submit my work",
        kind="success",
        disabled=lab_sync is None or locked or _unanswered > 0
        or not confirm.value,
        tooltip="Send your answers to your instructor",
    )
    mo.vstack([
        mo.md("## Submit your work"),
        mo.md(
            "Everything has been saving as you went. Handing in is the last step and it is "
            "final: once the lab is in, nothing on this page can be changed, the written "
            "answers included. Read back through them first. If you hand in by mistake, ask "
            "your instructor to reopen the lab for you."
            + (f" **Answer the {_unanswered} quiz question"
               f"{'s' if _unanswered > 1 else ''} above first.**" if _unanswered else "")
        ),
        confirm,
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
                           f"**{auto_score}**. That is the lab in, so nothing on this "
                           f"page is saved from here on.", "success")
        elif _reply.get("submitted"):
            _msg, _kind = ("**Already handed in.** This lab went in earlier, so the "
                           "answers can no longer be changed.", "warn")
        elif _reply.get("locked"):
            _msg, _kind = ("**Not submitted.** Your instructor has locked this lab.", "danger")
        else:
            _msg, _kind = (
                f"**Not submitted:** {_reply.get('error', 'something went wrong')}. Your "
                "answers are still saved. Press **Submit my work** to try again.", "danger")
    elif lab_sync.last_submitted or lab_status.get("submitted"):
        _when = str(lab_sync.last_submitted or lab_status.get("submittedAt") or "")[:10]
        _msg, _kind = (
            f"**Submitted on {_when}.** Your answers are saved exactly as they were and "
            "cannot be changed now. If you need another go at it, ask your instructor to "
            "reopen the lab.", "success")
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
