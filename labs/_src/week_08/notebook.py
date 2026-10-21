import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 8 - The Photos You Need Don't Exist")


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
          .w8-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w8-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w8-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w8-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w8-hero p.sub code { background: #fff3cc; border: 1px solid #f2dfaa; padding: 0 5px;
                                border-radius: 4px; font-size: .92rem; }
          .w8-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w8-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w8-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w8-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w8-split { grid-template-columns: 1fr; } }
          .w8-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w8-split > .body p:last-child { margin-bottom: 0; }
          .w8-split code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                           font-size: .88rem; }

          .w8-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w8-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w8-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w8-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w8-aside li:last-child { margin-bottom: 0; }
          .w8-aside li::marker { color: #6a5314; font-weight: 800; }
          .w8-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w8-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w8-aside .meta div:last-child { margin-bottom: 0; }
          .w8-aside .meta dt { color: #6f6f6f; }
          .w8-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w8-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w8-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w8-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }

          .w8-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                     gap: 12px; margin: 14px 0; }
          .w8-stat { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff;
                     padding: 11px 13px; }
          .w8-stat .k { color: #6a5314; font-size: .72rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .w8-stat .v { display: block; color: #111; font-size: 1.45rem; font-weight: 800;
                        line-height: 1.2; margin-top: 2px; }
          .w8-stat .why { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 3px;
                          line-height: 1.4; }
          .w8-stat.green .v { color: #2e7d32; }
          .w8-stat.red .v { color: #c62828; }

          .w8-mix { display: flex; height: 52px; border-radius: 8px; overflow: hidden;
                    border: 1px solid #e6e6e6; margin: 16px 0 8px; }
          .w8-mix span { display: flex; align-items: center; justify-content: center;
                         color: #fff; font-size: .8rem; font-weight: 800;
                         overflow: hidden; white-space: nowrap; }
          .w8-mix .a { background: #4a6fa5; }
          .w8-mix .b { background: #c87f5a; }
          .w8-mix .sig { background: #7cb47f; }
          .w8-mix .noi { background: #9a9a9a; }

          .w8-flow { display: flex; flex-wrap: wrap; align-items: stretch; gap: 0;
                     margin: 18px 0; }
          .w8-flow .step { flex: 1 1 130px; border: 1px solid #e6e6e6; background: #fff;
                           border-radius: 10px; padding: 11px 13px; margin: 4px; }
          .w8-flow .step .n { color: #6a5314; font-size: .68rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w8-flow .step h5 { margin: 3px 0 5px; font-size: .9rem; color: #111; }
          .w8-flow .step p { margin: 0; color: #5a5a5a; font-size: .8rem; line-height: 1.45; }
          .w8-flow .step.drop { border-color: #f0c9c9; background: #fdf6f6; }
          .w8-flow .step.keep { border-color: #cfe4d0; background: #f7fbf7; }

          .w8-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w8-bar { display: grid; grid-template-columns: 180px 1fr 120px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w8-bar { grid-template-columns: 100px 1fr 84px; } }
          .w8-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w8-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 26px; overflow: hidden; }
          .w8-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w8-bar.good .fill { background: #7cb47f; }
          .w8-bar.bad .fill { background: #d98080; }
          .w8-bar.gold .fill { background: #f1b82d; }
          .w8-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }

          table.w8-table { border-collapse: collapse; margin: 14px 0; font-size: .92rem;
                           width: 100%; }
          table.w8-table th, table.w8-table td { border: 1px solid #e6e6e6;
                                                 padding: 9px 13px; text-align: left;
                                                 vertical-align: top; }
          table.w8-table th { background: #fffdf5; color: #6a5314; font-size: .76rem;
                              text-transform: uppercase; letter-spacing: .04em; }
          table.w8-table td.num { text-align: right; font-variant-numeric: tabular-nums; }
          table.w8-table tr.on td { background: #fffdf5; font-weight: 700; }
          table.w8-table tr.off td { color: #9a9a9a; }
          table.w8-table code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                                font-size: .85rem; }
          table.w8-table .tick { color: #2e7d32; font-weight: 800; }
          table.w8-table .cross { color: #c62828; font-weight: 800; }

          .w8-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w8-report .row { display: grid; grid-template-columns: 200px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w8-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w8-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w8-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w8-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w8-report .tick { color: #2e7d32; font-weight: 800; }
          .w8-report .cross { color: #c62828; font-weight: 800; }
          .w8-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                              color: #333; font-style: italic; }
          .w8-score { display: inline-block; background: #fff3cc; border: 1px solid #f2dfaa;
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
        <div class="w8-hero">
          <p class="w8-eyebrow">CSC/EE 8001 &middot; Week 8</p>
          <h1>The Photos You Need Don't Exist</h1>
          <p class="sub">Last week you deleted 80,000 photos and saved most of a week of
          GPU time. The doorbell still can't see people at night in the rain.<br><br>
          It never could. You only ever had 100 photos like that, and deleting things does
          not create the ones you are missing. This week you make them instead &mdash; and
          then find out what a made-up photo really costs.</p>
          <div class="w8-chips">
            <span class="w8-chip">When more data is the answer</span>
            <span class="w8-chip">Cheap tricks first</span>
            <span class="w8-chip">How image generators work</span>
            <span class="w8-chip">Why your GPU is idle</span>
            <span class="w8-chip-plain w8-chip">Checks are marked</span>
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
        <div class="w8-split">
          <div class="body">
            <p>Week 7 was about having too much data. You had 100,000 photos, could afford
            20,000, and the job was to work out which ones were worth keeping. Every
            technique was a way of <em>removing</em> things.</p>
            <p>This week is the opposite problem, and it needs the opposite tools. Some of
            the photos you need were never taken. No amount of clever deleting will produce
            a photo of a pedestrian in heavy rain at night, because that photo does not
            exist in your dataset to be kept.</p>
            <p>So you have to make one. Which immediately raises three questions that are
            more interesting than they sound. Can you fake it cheaply by messing with the
            photos you already have? If not, how do the generators that make images from
            scratch actually work? And since generating isn't free, how do you tell whether
            the whole exercise was worth it?</p>
            <p>Then, at the end, a plot twist. You will speed up your training by deleting
            three quarters of your data, and the job will take <strong>longer</strong>. That
            one is not a trick question.</p>
          </div>
          <aside class="w8-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Tell a "too much data" problem from a "missing data" problem, and pick
              the right tool.</li>
              <li>Mix two photos together and say what label the result should get.</li>
              <li>Explain how an image generator learns, without the maths.</li>
              <li>Work out what one <em>usable</em> fake photo costs you.</li>
              <li>Say why a realistic photo can still ruin a model.</li>
              <li>Find the bottleneck in a training pipeline and know what won't fix
              it.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 45 min</dd></div>
              <div><dt>Before this</dt><dd>Week 7</dd></div>
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
        <div class="w8-question">
          <span class="lbl">The question this lab answers</span>
          <p>"The examples my model needs were never collected. Do I go and photograph
          them, fake them, or generate them &mdash; and how do I know which was
          cheapest?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: Find out what is actually wrong""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Someone finally measured the doorbell model properly, by splitting the test set up
    instead of reporting one number. Here is what came back.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    _rows = [
        ("Pedestrian, daylight", 20000, 97),
        ("Pedestrian, night", 1000, 83),
        ("Pedestrian, night and heavy rain", 100, 62),
        ("Pedestrian, partly hidden", 500, 75),
    ]
    _body = ""
    for _scene, _n, _rec in _rows:
        _bad = _rec < 80
        _w = max(2, _rec)
        _body += (
            f"<tr class='{'on' if _bad else ''}'><td>{_scene}</td>"
            f"<td class='num'>{_n:,}</td>"
            f"<td><span style='display:inline-block;height:14px;border-radius:3px;"
            f"background:{'#d98080' if _bad else '#7cb47f'};width:{_w}%'></span></td>"
            f"<td class='num'>{_rec}%</td></tr>"
        )
    mo.Html(
        f"""
        <table class="w8-table">
          <thead><tr><th>What is in the photo</th><th>Real training photos</th>
            <th>How often the model spots it</th><th></th></tr></thead>
          <tbody>{_body}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Read the first and last columns together. The model is excellent at the thing it has
    20,000 examples of and poor at the thing it has 100 examples of. There is no mystery
    here, and that is what makes it useful: the number of photos and the accuracy go up and
    down together.

    Also notice what the overall accuracy would say. Daylight pedestrians are the
    overwhelming majority of real events, so the average comes out around 95% and looks
    fine. The 62% is invisible in it. That is the Week 4 lesson arriving again, and it is
    why nobody noticed this for six months.

    Now, before any technique: **what do you actually do about it?**
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("hunch") or {}
    _choices = {
        "Go out and photograph more rainy nights": "collect",
        "Take the daylight photos and darken them, add noise, make them look rainy": "augment",
        "Use an AI image generator to make rainy night photos": "generate",
        "Prune harder, as in Week 7, so training focuses on what is left": "prune",
    }
    hunch_form = (
        mo.md("{choice}")
        .batch(
            choice=mo.ui.radio(
                options=_choices,
                value=pick(_choices, _saved.get("choice")),
                disabled=locked,
                label="**Your gut feeling, before we look at any of these properly.** "
                      "Not marked.",
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
        mo.callout(mo.md("Pick one and press **That's my guess**. Three of these four are "
                         "reasonable and we will cost all of them out."), kind="warn"),
    )
    hunch_choice = _answer["choice"]
    return (hunch_choice,)


@app.cell(hide_code=True)
def _(hunch_choice, mo):
    _notes = {
        "collect": (
            "The honest answer, and the one everybody skips past too quickly. It gives you "
            "**real** photos with **real** labels, from your actual cameras, with your "
            "actual lens flare and compression artefacts. Nothing else in this lab can "
            "promise that.\n\nThe problem is simply that you don't control the weather. "
            "Rainy nights happen when they happen, and if you need 6,000 of them you may be "
            "waiting two winters. Then somebody has to label each one.\n\nKeep this option "
            "on the table though. It is the thing everything else has to beat, and in Part "
            "5 we will put a price on it."
        ),
        "augment": (
            "Right instinct, and it should genuinely be your first move because it costs "
            "almost nothing. Part 2 is about this.\n\nBut hold a specific doubt in mind as "
            "you go. Turning the brightness down on a daylight photo gives you a dark "
            "photo. It does not give you headlight reflections on wet tarmac, rain streaks "
            "that are blurrier the further away they are, or an umbrella covering half the "
            "person. Those things are not a brightness setting. They are a different scene."
        ),
        "generate": (
            "This is Parts 3 and 4, and it is the only option that can produce scenes your "
            "cameras have genuinely never captured.\n\nTwo things to watch for. It is not "
            "free, and the cost is in a surprising place &mdash; not the generating, as "
            "you'll see in Part 5. And a generated photo arrives with no label at all. "
            "Somebody still has to confirm there is actually a person in it, and where."
        ),
        "prune": (
            "This is the trap, and it is worth having fallen into because it is the main "
            "point of today.\n\nWeek 7's methods all answer the question \"which of my "
            "photos are worth keeping?\" Every one of them is a way of **removing** things. "
            "None of them can produce a rainy night photo, because you only have 100 and "
            "the information simply isn't in the dataset to be found.\n\nPruning fixes "
            "*redundancy*. You have a *coverage* problem. Different illness, different "
            "medicine."
        ),
    }
    mo.vstack([
        mo.md("### On your guess"),
        mo.callout(mo.md(_notes[hunch_choice]), kind="info"),
    ])
    return


@app.cell(hide_code=True)
def _(ask):
    e1, e1_render, e1_sum = ask(
        "**Check 1.** Your colleague suggests running Week 7's k-center method again, more "
        "aggressively, to focus training on the examples that matter. Will that raise the "
        "62%?",
        {
            "Yes, since it keeps the unusual photos and drops the repetitive ones": "yes",
            "No, because selection can only keep photos you already have, and you only have 100": "no",
            "Yes, but only if you also lower the learning rate": "lr",
        },
        "no",
        "Selection methods are all subtraction. The very best possible outcome is that it "
        "keeps all 100 of your rainy-night photos and throws away daylight ones. You would "
        "then be training on 100 rainy-night photos, which is exactly what you were doing "
        "before, and 62% is what 100 photos buys you.\n\nThe general shape is worth "
        "remembering, because the two problems look similar from a distance and need "
        "opposite responses:\n\n- **Too much data (Week 7).** You have what you need, buried "
        "in stuff you don't. Fix by removing.\n- **Missing data (this week).** You don't "
        "have what you need at all. Fix by adding.\n\nDiagnose before you reach for a tool. "
        "A pruning method pointed at a coverage problem will run happily, report a lovely "
        "saving, and change nothing.",
        key="e1",
    )
    e1
    return e1, e1_render, e1_sum


@app.cell(hide_code=True)
def _(e1, e1_render):
    e1_render(e1.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The comparison people get wrong

    Here is a mistake that sounds reasonable and quietly ruins the decision.

    In Week 7, success meant *doing less*: choosing 20,000 photos and finishing faster than
    training on all 100,000. Less compute, same accuracy. So the natural habit is to ask of
    any new method, "is this cheaper than what I was doing before?"

    Apply that habit here and generating data always looks terrible. Of course it costs
    more than not generating data. You are deliberately **adding** work in order to reach a
    quality you cannot currently reach at any price.

    The right comparison is between the options that would actually get you there:

    > **Which way of reaching 90% rainy-night recall costs least?**

    Collecting real photos is one way. Generating them is another. Cheap augmentation might
    be a third. They all get compared against each other, at the same target quality, and
    *not* against an imaginary world where you already had the data.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    e2, e2_render, e2_sum = ask(
        "**Check 2.** Your manager asks why they should approve 19 GPU-hours of image "
        "generation when the current training run only takes 8. What is wrong with that "
        "comparison?",
        {
            "Nothing. If generation costs more than current training it is not worth it": "fine",
            "The 8-hour run does not meet the requirement, so it is not an option you can actually choose": "target",
            "GPU-hours are the wrong unit; they should be compared in pounds": "units",
        },
        "target",
        "The 8-hour run produces a model with 62% rainy-night recall. If the requirement is "
        "90%, that run is not a cheaper way of succeeding, it is a cheap way of failing. "
        "You cannot compare the costs of two options when only one of them is an option."
        "\n\nSo fix the quality first, then compare costs. \"What is the cheapest way to "
        "reach 90%?\" has collecting real photos, generating them, and cheap augmentation "
        "all competing on even terms, and whichever wins is genuinely the answer.\n\nThe "
        "third option has a real point buried in it, and it will matter in Part 5: GPU-hours "
        "and human hours are both costs, and a method that is cheap in one can be ruinous "
        "in the other. But converting units doesn't rescue a comparison against something "
        "that doesn't work.",
        key="e2",
    )
    e2
    return e2, e2_render, e2_sum


@app.cell(hide_code=True)
def _(e2, e2_render):
    e2_render(e2.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 2: The cheap thing you should always try first""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Before generating anything, try the cheap trick: take photos you already have and
    change them. Flip them, crop them, shift the colours, add noise. You get a "new"
    training example for almost no compute, and crucially **you already know the label**,
    because a flipped pedestrian is still a pedestrian.

    That last point is the whole appeal. The expensive part of data is usually the labelling,
    and this skips it entirely.

    ### MixUp: a strange one that works

    Most augmentation is obvious. This one isn't, and it is worth understanding because it
    forces you to think about what a label actually is.

    **MixUp takes two different photos and fades between them.** Not two copies of the same
    photo. Two completely different ones. Photo A is a pedestrian, photo B is an empty
    driveway, and you blend them into a ghostly double exposure.

    Which raises the obvious question: what is the label of a photo that is 70% pedestrian?

    The answer is that you blend the label by exactly the same amount. Drag the slider.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    mix_lam = mo.ui.slider(
        0, 100, value=saved.get("mix_lam", 70), step=5, disabled=locked,
        label="How much of photo A (the pedestrian) is in the blend, %", show_value=True,
    )
    mix_lam
    return (mix_lam,)


@app.cell(hide_code=True)
def _(LAB_CSS, mix_lam, mo):
    _ = LAB_CSS
    _lam = mix_lam.value / 100.0
    _a, _b = 100.0 * _lam, 100.0 * (1 - _lam)

    def _seg(cls, w, text):
        return "" if w < 1 else (f'<span class="{cls}" style="width:{w}%">'
                                 f'{text if w > 18 else ""}</span>')

    mo.Html(
        f"""
        <div class="w8-mix">
          {_seg("a", _a, "photo A &middot; pedestrian")}
          {_seg("b", _b, "photo B &middot; empty driveway")}
        </div>
        <div class="w8-grid">
          <div class="w8-stat">
            <span class="k">The blended photo</span>
            <span class="v">{_lam:.2f} &middot; {1 - _lam:.2f}</span>
            <span class="why">{_a:.0f}% of A's pixels plus {_b:.0f}% of B's</span>
          </div>
          <div class="w8-stat">
            <span class="k">The label you train on</span>
            <span class="v">({_lam:.2f}, {1 - _lam:.2f})</span>
            <span class="why">person {_lam:.2f}, nothing {1 - _lam:.2f}</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mix_lam, mo):
    _lam = mix_lam.value / 100.0
    if mix_lam.value in (0, 100):
        _msg = (
            "At the ends nothing is being mixed, so you are simply training on one of the "
            "original photos with its original label. MixUp does nothing here. Drag towards "
            "the middle."
        )
    elif 40 <= mix_lam.value <= 60:
        _msg = (
            f"This is the interesting case. The label is **({_lam:.2f}, {1 - _lam:.2f})**, "
            "and you should stop and ask what that even means.\n\nIt is not \"a person\". It "
            "is not \"not a person\". It is an instruction to the model: *be exactly this "
            "unsure*. If the model shouts PERSON at 99% confidence on this image, it gets "
            "punished, even though there genuinely is most of a person in it.\n\nThat sounds "
            "perverse and it is the entire point. Models have a strong habit of being "
            "wildly overconfident on inputs halfway between two things they know. MixUp "
            "spends training time specifically in that gap, teaching the model to hedge "
            "where hedging is correct."
        )
    else:
        _msg = (
            f"The photo is **{100 * _lam:.0f}%** A, so the label is "
            f"**({_lam:.2f}, {1 - _lam:.2f})**. Both move together, always. That is the "
            "whole rule.\n\nNow drag it to the middle, where it gets strange."
        )
    mo.callout(mo.md(_msg), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    In practice you don't pick the blend by hand. You draw a random amount for every pair,
    usually biased towards the ends so most blends are mild and a few are extreme.

    MixUp costs essentially nothing, needs no new labels, and tends to give a small, free
    improvement. Which makes it a good example of the general rule: **do the cheap things
    before the expensive ones, and measure, because the cheap thing is sometimes enough.**
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    e3, e3_render, e3_sum = ask(
        "**Check 3.** A colleague wants to use MixUp on the text side of the product, "
        "blending two customer support messages the same way. Why does this not work?",
        {
            "Text models cannot take soft labels": "soft",
            "Halfway between two words is not a word, whereas halfway between two pixel values is a valid pixel": "discrete",
            "It works, but only for messages of the same length": "length",
        },
        "discrete",
        "Pixel brightness is continuous. 0.7 of one value plus 0.3 of another lands on a "
        "value that is perfectly valid and still looks like something. Blending is "
        "meaningful.\n\nWords aren't continuous. There is nothing 70% of the way between "
        "\"refund\" and \"delivery\" &mdash; the space between words is empty, not "
        "intermediate. You can average their numeric representations, but the result "
        "usually decodes to nonsense rather than to a plausible message.\n\nThis is a "
        "distinction worth keeping hold of beyond MixUp. **Continuous data can be "
        "interpolated; discrete data cannot.** It is why image augmentation is a toolbox of "
        "cheap geometric tricks while text augmentation leans on things like "
        "back-translation and paraphrasing &mdash; operations that stay inside the space of "
        "real sentences instead of trying to find the middle of two of them.",
        key="e3",
    )
    e3
    return e3, e3_render, e3_sum


@app.cell(hide_code=True)
def _(e3, e3_render):
    e3_render(e3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Where cheap augmentation runs out

    So: you have 100 real rainy-night photos and 20,000 daylight ones. You turn the
    brightness down on the daylight photos, add some noise, crop them about a bit.

    Have you made rainy-night training data?

    No, and it is worth being precise about why not. A real rainy night photo contains:

    - **Headlights reflecting off wet tarmac**, which puts bright streaks in places a
      darkened daylight photo has nothing at all.
    - **Rain that blurs with distance**, heavier-looking far away than near the lens.
    - **An umbrella**, covering the top half of the person you are trying to detect.
    - **Several light sources at once**, a porch lamp and a streetlight and a car, each
      throwing shadows in a different direction.

    None of those are adjustments to a daylight photo. They are a different arrangement of
    the world. Brightness is a knob; rain is a scene.

    That gap is why the next three parts exist. When you need a scene you have never
    photographed, you need something that can build one.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: How image generators actually work""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The models that make images from a text prompt are called **diffusion models**, and the
    idea behind them is genuinely simple once somebody tells you the trick. Most
    explanations don't, so here it is.

    ### The trick

    Making a photo from nothing is impossibly hard. So don't. Instead, learn to do a much
    easier job, over and over.

    Take a real photo. Add a little static to it. Now you have a pair: the noisy photo, and
    the exact static you added. Train a network on one question only:

    > Here is a slightly messy photo. **Which bits of it are the mess?**

    That's it. That's the whole training task.

    And here is why it is clever. **Nobody has to label anything.** You generated the
    static yourself, so you already know the right answer perfectly. No annotator, no
    bounding box, no "is this a person". You can do this to every photo on the internet.

    ### Why solving that gives you a generator

    Now think about what the network must learn in order to spot the static. To know that a
    pixel is wrong, it has to know what a right one would look like. It has to pick up that
    faces have two eyes roughly there, that arms attach at shoulders, that shadows fall away
    from lights, that tarmac is darker than sky.

    So you ask it to remove noise and it is forced to learn what real photos look like. The
    knowledge arrives as a side effect of the chore.

    Then you cheat. Hand it a picture of **pure static** and ask it to clean that up. It
    has never seen this one, so there is no "correct" answer underneath, but it does the
    only thing it knows: nudge this towards looking like a real photo. Do that fifty times
    in a row, each pass a little cleaner, and a photo of something that never existed
    assembles itself out of the noise.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w8-flow">
          <div class="step"><span class="n">Training &middot; 1</span>
            <h5>Real photo</h5><p>Any photo. No label needed.</p></div>
          <div class="step"><span class="n">Training &middot; 2</span>
            <h5>Add static</h5><p>You choose it, so you know it exactly.</p></div>
          <div class="step"><span class="n">Training &middot; 3</span>
            <h5>Guess the static</h5><p>Network's only job. Score it, correct it, repeat.</p></div>
          <div class="step keep"><span class="n">Making &middot; 1</span>
            <h5>Start from pure static</h5><p>No photo underneath at all.</p></div>
          <div class="step keep"><span class="n">Making &middot; 2</span>
            <h5>Clean it, 50 times</h5><p>Each pass slightly more photo-like.</p></div>
          <div class="step keep"><span class="n">Making &middot; 3</span>
            <h5>A new photo</h5><p>Of something that never happened.</p></div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Build one training example yourself

    Here is the recipe for mixing a clean photo with static, written down. It is one line
    and you can do it on a single pixel:

    $$x_t = \sqrt{\bar\alpha}\, x_0 \;+\; \sqrt{1-\bar\alpha}\, \epsilon$$

    Three things go in. $x_0$ is the real pixel. $\epsilon$ is the random static. And
    $\bar\alpha$ is the dial that says how much of the photo survives: at 1.00 you keep
    everything, at 0.00 you keep nothing but static.

    The square roots are there so the brightness stays sensible rather than the two parts
    adding up to something too strong. Don't worry about why.

    The sliders start on the lecture's worked example.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    alpha_bar = mo.ui.slider(
        1, 100, value=saved.get("alpha_bar", 64), step=1, disabled=locked,
        label="ᾱ  how much of the photo survives, %", show_value=True,
    )
    x0_val = mo.ui.slider(
        -100, 100, value=saved.get("x0_val", 100), step=10, disabled=locked,
        label="x₀  the real pixel (× 0.01)", show_value=True,
    )
    eps_val = mo.ui.slider(
        -200, 200, value=saved.get("eps_val", -100), step=10, disabled=locked,
        label="ε  the random static (× 0.01)", show_value=True,
    )
    mo.vstack([alpha_bar, x0_val, eps_val])
    return alpha_bar, eps_val, x0_val


@app.cell(hide_code=True)
def _(alpha_bar, eps_val, x0_val):
    import math as _math

    ab = alpha_bar.value / 100.0
    x0 = x0_val.value / 100.0
    eps = eps_val.value / 100.0
    sig_w = _math.sqrt(ab)              # how much signal survives
    noi_w = _math.sqrt(1.0 - ab)        # how much static goes in
    xt = sig_w * x0 + noi_w * eps
    return ab, eps, noi_w, sig_w, x0, xt


@app.cell(hide_code=True)
def _(LAB_CSS, ab, eps, mo, noi_w, sig_w, x0, xt):
    _ = LAB_CSS
    _s, _n = 100.0 * sig_w, 100.0 * noi_w
    _tot = _s + _n
    _sp, _np = 100.0 * _s / _tot, 100.0 * _n / _tot

    def _seg(cls, w, text):
        return "" if w < 1 else (f'<span class="{cls}" style="width:{w}%">'
                                 f'{text if w > 20 else ""}</span>')

    mo.Html(
        f"""
        <div class="w8-mix">
          {_seg("sig", _sp, "real photo")}
          {_seg("noi", _np, "static")}
        </div>
        <div class="w8-grid">
          <div class="w8-stat">
            <span class="k">Photo part</span>
            <span class="v">{sig_w:.3f} &times; {x0:+.2f}</span>
            <span class="why">&radic;{ab:.2f} = {sig_w:.3f}</span>
          </div>
          <div class="w8-stat">
            <span class="k">Static part</span>
            <span class="v">{noi_w:.3f} &times; {eps:+.2f}</span>
            <span class="why">&radic;{1 - ab:.2f} = {noi_w:.3f}</span>
          </div>
          <div class="w8-stat">
            <span class="k">The messy pixel the network sees</span>
            <span class="v">{xt:+.3f}</span>
            <span class="why">{sig_w * x0:+.3f} {'+' if noi_w * eps >= 0 else '&minus;'}
              {abs(noi_w * eps):.3f}</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(alpha_bar, eps, mo, sig_w, x0, xt):
    if alpha_bar.value >= 95:
        _msg = (
            f"Almost nothing has been done to it. The messy pixel is **{xt:+.3f}** and the "
            f"real one was **{x0:+.2f}**. Easy question for the network, so it learns very "
            "little from this example. Training samples a different amount of mess every "
            "time for exactly this reason."
        )
    elif alpha_bar.value <= 10:
        _msg = (
            f"Now it is nearly all static. The messy pixel is **{xt:+.3f}**, and the real "
            f"pixel has essentially vanished. The network cannot recover this one and isn't "
            "expected to.\n\nBut this is the state you *start from* when generating. Pure "
            "static, no photo underneath, and the network cleans it up anyway &mdash; "
            "towards whatever it has learned real photos look like."
        )
    else:
        _msg = (
            f"The pixel the network gets handed is **{xt:+.3f}**, from "
            f"**{sig_w:.3f} &times; {x0:+.2f}** of real photo plus some static."
        )
    _msg += (
        f"\n\n**And now the question that matters.** The network's job is to look at "
        f"{xt:+.3f} and tell you the static was **{eps:+.2f}**. Did anyone have to label "
        "this photo for that to be gradeable?\n\nNo. You *chose* the static. You can mark "
        "its homework perfectly without knowing, or caring, what the photo is of. That is "
        "why these models can be trained on billions of images: the training signal comes "
        "free with the data."
    )
    mo.callout(mo.md(_msg), kind="info")
    return


@app.cell(hide_code=True)
def _(ask):
    e4, e4_render, e4_sum = ask(
        "**Check 4.** To train a diffusion model on a photo, what does a human have to "
        "write down about that photo first?",
        {
            "A class label, so the model knows what it is learning to draw": "class",
            "Nothing. The training answer is the static, which the pipeline chose itself": "nothing",
            "A bounding box around the main object": "box",
        },
        "nothing",
        "This is the property that made these models possible at the scale they exist at. "
        "The thing being predicted is the static, and the static was generated by the "
        "training code three lines earlier. The answer key writes itself.\n\nSo the usual "
        "bottleneck vanishes. Every other model in this course needs somebody to say what "
        "each example is; this one needs a hard drive full of photos and nothing else. "
        "That is how you get a model trained on billions of images.\n\nWorth separating "
        "from a related fact, though: text prompts. Text-to-image models *do* use "
        "captions, which are a kind of label, and they mostly come scraped off the web "
        "alongside the image rather than from annotators. The underlying noise-prediction "
        "training still needs nothing at all.",
        key="e4",
    )
    e4
    return e4, e4_render, e4_sum


@app.cell(hide_code=True)
def _(e4, e4_render):
    e4_render(e4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: Making it affordable, and making it do what you asked""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Two problems with what we just built. It is slow, and it does whatever it likes.

    ### Problem one: it is slow

    Generating one photo means cleaning up static fifty times, and every one of those is a
    full pass through a large network. Compare that to flipping an image, which is free.

    Worse, look at how much data each pass has to chew through. A 512&times;512 colour
    photo is:

    $$512 \times 512 \times 3 = 786{,}432 \text{ numbers}$$

    The fix is to stop working on photos. First, squash the photo down with a separate
    network trained to compress and then restore images. A typical squashed version is
    64&times;64 with 4 channels:

    $$64 \times 64 \times 4 = 16{,}384 \text{ numbers}$$

    $$\frac{786{,}432}{16{,}384} = 48\times \text{ fewer numbers}$$

    Now do all fifty cleanup passes on the small version, and only expand it back to a real
    photo once at the very end. This is called **latent diffusion**, and it is why these
    models run on a normal graphics card instead of a datacentre.

    One caveat, and your lecturer flagged it deliberately: **48&times; fewer numbers is not
    48&times; faster.** Runtime depends on how the network is built, how memory moves, how
    many cleanup steps you run and what the final expansion costs. It is a large speed-up.
    It is not that number.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    e5, e5_render, e5_sum = ask(
        "**Check 5.** Working on the squashed version means handling 48 times fewer "
        "numbers. What can you safely conclude about speed?",
        {
            "Generation will be about 48 times faster": "48",
            "It will be a lot faster, but 48 is a ratio of array sizes and not a measured speed-up": "unknown",
            "Nothing, because the compression itself costs more than it saves": "worse",
        },
        "unknown",
        "The 48 is honest arithmetic about array sizes, and array size is only one of the "
        "things that sets runtime. Also in play: how the network's layers scale with input "
        "size (some parts scale much worse than linearly), how much time is spent moving "
        "memory rather than computing, how many cleanup steps your sampler takes, and the "
        "one-off cost of expanding the result back into a photo.\n\nThe habit this is "
        "training is the useful bit, and it is the same one from Week 6 when you counted "
        "operations in a layer and found they didn't predict the runtime: **a count of "
        "numbers is not a measurement of time.** Quoting one as the other is the most common "
        "way performance claims go wrong, and it usually isn't deliberate.\n\nThe third "
        "answer is wrong but points somewhere real. Compression isn't free, which is "
        "precisely why you do it once at each end rather than inside the loop that runs "
        "fifty times.",
        key="e5",
    )
    e5
    return e5, e5_render, e5_sum


@app.cell(hide_code=True)
def _(e5, e5_render):
    e5_render(e5.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Problem two: it does whatever it likes

    What we have built so far makes *a* plausible photo. You need a *specific* one. So
    alongside the messy image, you also feed the network a description of what you want,
    and it learns to take that into account while cleaning up:

    > "a pedestrian crossing a residential driveway at night in heavy rain"

    That is **conditional** generation, and it is most of what you do with these models.

    But a sentence is a loose specification, and this is where it starts to matter for your
    actual job. You asked for a pedestrian. You will reliably get a rainy night driveway.
    You might get a pedestrian on the wrong side of the frame. Facing away. Standing where
    a car should be. Or no pedestrian at all, because the model decided the scene looked
    complete without one.

    For a detection model, where the person *is* in the frame is the entire point. A
    sentence cannot pin that down.

    So you give it the geometry directly, alongside the words: a stick-figure skeleton in
    the pose you want, an outline sketch, or a depth map saying what is near and far. The
    best-known way of bolting this onto an existing generator is called **ControlNet**.

    Which helps a great deal and still does not finish the job, and that brings us to the
    part everyone underestimates.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: A convincing photo is not a training example""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is the thing to take away from this whole lab.

    You generate a rainy-night driveway with a pedestrian in it. It looks great. You could
    not tell it from a real photo.

    **It is still not training data.** To train a detector you need to know exactly where
    the person is, as a box or an outline. And you don't. You asked for a person; you did
    not receive a receipt confirming one is present, let alone its coordinates.

    You cannot reuse the pose skeleton you fed in, either, which is the trap that catches
    people. The generated person will not line up with it exactly &mdash; a coat changes
    the silhouette, an umbrella hides a shoulder, the model nudges a leg. Use the skeleton's
    box and you have a box that is slightly wrong on every single example, and a detector
    trained on thousands of slightly wrong boxes learns to put its boxes slightly wrong.

    That failure is nastier than a visibly broken image, because broken images get noticed.
    This one looks perfect all the way to production.

    So every generated candidate has to be checked, by another model or by a person:

    1. Is the thing I asked for actually in the picture?
    2. Where is it, precisely?
    3. Is the scene usable, or did it come out mangled?

    Some fail. The share that survive is your **acceptance rate**, and it is the number
    that decides whether any of this was affordable.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    need_valid = mo.ui.slider(
        1000, 20000, value=saved.get("need_valid", 6000), step=500, disabled=locked,
        label="Usable photos you need", show_value=True,
    )
    accept_pct = mo.ui.slider(
        5, 100, value=saved.get("accept_pct", 60), step=5, disabled=locked,
        label="Of what you generate, how much passes checking, %", show_value=True,
    )
    gen_secs = mo.ui.slider(
        1, 40, value=saved.get("gen_secs", 8), step=1, disabled=locked,
        label="GPU seconds to generate one candidate (× 0.1)", show_value=True,
    )
    val_secs = mo.ui.slider(
        5, 300, value=saved.get("val_secs", 50), step=5, disabled=locked,
        label="Seconds of human time to check one candidate (× 0.1)", show_value=True,
    )
    mo.vstack([need_valid, accept_pct, gen_secs, val_secs])
    return accept_pct, gen_secs, need_valid, val_secs


@app.cell(hide_code=True)
def _(accept_pct, gen_secs, need_valid, val_secs):
    # Costs are illustrative. What they are for is showing which term grows fastest
    # as the acceptance rate falls, which is the thing people misjudge.
    GPU_POUNDS_PER_HOUR = 2.50
    HUMAN_POUNDS_PER_HOUR = 18.00
    REAL_PHOTO_POUNDS = 1.50      # what an annotator charges to label one real frame

    accept = accept_pct.value / 100.0
    n_generated = need_valid.value / accept
    t_gen_h = n_generated * (gen_secs.value / 10.0) / 3600.0
    t_val_h = n_generated * (val_secs.value / 10.0) / 3600.0
    t_total_h = t_gen_h + t_val_h
    wasted = n_generated - need_valid.value

    # Generating is GPU time; checking is a person looking at every candidate,
    # which is why the two halves are priced differently.
    cost_synth = t_gen_h * GPU_POUNDS_PER_HOUR + t_val_h * HUMAN_POUNDS_PER_HOUR
    cost_real = need_valid.value * REAL_PHOTO_POUNDS
    per_usable_synth = cost_synth / need_valid.value
    cheaper_by = cost_real / cost_synth if cost_synth > 0 else 0.0
    screening_dominates = t_val_h > t_gen_h
    return (
        REAL_PHOTO_POUNDS,
        accept,
        cheaper_by,
        cost_real,
        cost_synth,
        n_generated,
        per_usable_synth,
        screening_dominates,
        t_gen_h,
        t_total_h,
        t_val_h,
        wasted,
    )


@app.cell(hide_code=True)
def _(LAB_CSS, mo, n_generated, need_valid, per_usable_synth, t_total_h, wasted):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w8-grid">
          <div class="w8-stat">
            <span class="k">You must generate</span>
            <span class="v">{n_generated:,.0f}</span>
            <span class="why">to end up with {need_valid.value:,} usable ones</span>
          </div>
          <div class="w8-stat red">
            <span class="k">Thrown away</span>
            <span class="v">{wasted:,.0f}</span>
            <span class="why">generated, checked, and binned</span>
          </div>
          <div class="w8-stat">
            <span class="k">Hours of work</span>
            <span class="v">{t_total_h:,.1f}</span>
            <span class="why">GPU time plus somebody's afternoon</span>
          </div>
          <div class="w8-stat">
            <span class="k">Cost per usable photo</span>
            <span class="v">&pound;{per_usable_synth:,.2f}</span>
            <span class="why">the number that actually matters</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo, t_gen_h, t_total_h, t_val_h):
    _ = LAB_CSS
    _span = max(t_total_h, 0.001)
    _g = 100.0 * t_gen_h / _span
    _v = 100.0 * t_val_h / _span

    def _seg(cls, w, text):
        return "" if w < 1 else (f'<span class="{cls}" style="width:{w}%">'
                                 f'{text if w > 22 else ""}</span>')

    mo.Html(
        f"""
        <div class="w8-mix">
          {_seg("sig", _g, f"generating &middot; {t_gen_h:,.1f} GPU-hrs")}
          {_seg("b", _v, f"checking &middot; {t_val_h:,.1f} human-hrs")}
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(
    REAL_PHOTO_POUNDS,
    accept,
    cheaper_by,
    cost_real,
    cost_synth,
    mo,
    n_generated,
    need_valid,
    per_usable_synth,
    screening_dominates,
    t_gen_h,
    t_val_h,
    wasted,
):
    _accept_note = (
        f"Start with the acceptance rate. At **{accept * 100:.0f}%** you have to generate "
        f"**{n_generated:,.0f}** candidates to end up with {need_valid.value:,}, so "
        f"**{wasted:,.0f}** get made, inspected and binned. You pay in full for every one "
        "of those. Drag it down to 20%, which is an ordinary number for a fussy prompt, and "
        "watch what happens."
    )
    _screen_note = (
        f"\n\nNow look at where the hours went. Checking took **{t_val_h:,.1f}** hours of "
        f"somebody's attention against **{t_gen_h:,.1f}** of GPU time. **The expensive part "
        "of making fake data is not making it.** The generator is a few pence an hour; the "
        "person confirming there is really a pedestrian in frame, and where, is not."
        if screening_dominates else
        f"\n\nRight now generating ({t_gen_h:,.1f} h of GPU) outweighs checking "
        f"({t_val_h:,.1f} h of human time). Push the checking slider up. Confirming a "
        "bounding box properly takes a person five to thirty seconds, and that is the "
        "number that usually decides whether this was affordable."
    )
    _vs = (
        f"\n\n**Against the real thing.** Your generated photos work out at "
        f"**£{per_usable_synth:,.2f}** each, all in. Paying an annotator to label a real "
        f"collected frame is about £{REAL_PHOTO_POUNDS:.2f} &mdash; so "
        f"£{cost_synth:,.0f} versus £{cost_real:,.0f} for the {need_valid.value:,} you "
        f"need, roughly **{cheaper_by:,.0f}&times; cheaper**."
        "\n\nWhich is a real advantage and is also why the argument never ends on price. "
        "Generated photos are cheap and *might not work*; real photos are dear and "
        "definitely do. And the £1.50 only buys the labelling &mdash; it assumes somebody "
        "already captured 6,000 rainy nights, which is the bit you actually can't buy."
    )
    mo.callout(mo.md(_accept_note + _screen_note + _vs), kind="info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Be honest: where do these numbers come from?": mo.md(
                """
                The generation speed and acceptance rate are plausible, not measured.
                Real diffusion throughput swings wildly with the hardware, the resolution,
                the model and how many cleanup steps the sampler takes, and acceptance
                rates depend enormously on how fussy your prompt is and how strict your
                checking is. The £2.50 per GPU-hour and £12 per labelled photo are
                round numbers for the shape of the argument.

                Things the calculator still leaves out:

                - **Storage and moving data.** Tens of thousands of generated images have
                  to live somewhere and be shipped to the training job.
                - **Retries.** A prompt that accepts at 20% usually gets rewritten a few
                  times first, and each attempt costs a batch.
                - **Your time.** Building the checking pipeline is days of work before it
                  is any GPU-hours at all.
                - **The generator's own training.** You are using a pretrained model, so
                  someone else paid for that, and it was enormous. It is fair to exclude
                  from your project's budget and worth knowing it exists.
                """
            )
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    e6, e6_render, e6_sum = ask(
        "**Check 6.** You generate a rainy-night scene using a pose skeleton, and the image "
        "is convincing. Why can't you just reuse that skeleton's bounding box as the label?",
        {
            "You can. The skeleton is exactly what the model was told to draw": "reuse",
            "The generated person won't line up with the skeleton exactly, so every box is slightly wrong": "drift",
            "Bounding boxes cannot be computed from skeletons at all": "cannot",
        },
        "drift",
        "The skeleton is a request, not a guarantee. The model drapes a coat on the figure, "
        "hands it an umbrella, shifts a leg to make the pose look natural. The result is a "
        "plausible person near where you asked, with a silhouette that is not the one you "
        "specified.\n\nNow think about what that does in bulk. Every box is wrong by a "
        "little, and mostly wrong in the *same direction*, since the model has consistent "
        "habits. Train on thousands of those and the detector doesn't learn to be vague, it "
        "learns your generator's specific bias and applies it to real photos.\n\nAnd this "
        "failure is quiet. A mangled image gets spotted the moment somebody scrolls through "
        "the folder. A beautiful image with a box eight pixels off looks fine, passes "
        "review, and degrades the model anyway. **The thing that needs checking is the "
        "label, not the picture.**",
        key="e6",
    )
    e6
    return e6, e6_render, e6_sum


@app.cell(hide_code=True)
def _(e6, e6_render):
    e6_render(e6.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The gap between made-up and real

    One more way this goes wrong, and it is the one that survives all your checking.

    Your generated photos can be individually perfect and still, taken together, not look
    like the world. Real doorbell footage has motion blur when someone walks quickly, JPEG
    compression blocks, a slightly dirty lens, a sensor that goes grainy in low light, and
    rain that behaves like actual water. Generated photos have the generator's habits
    instead: a certain style it favours, textures it repeats, reflections that look right
    but obey no particular physics.

    So a model can get very good at your fake rainy nights and stay bad at real ones. This
    is the **domain gap**, and the dangerous part is that your metrics will look wonderful
    while it happens, because you are measuring on the same fake photos you trained on.

    There is one rule that saves you, and it is not optional:

    > **Measure on real, held-out photos. Always. However few you have.**

    Those 100 real rainy-night frames you started with? Do not train on all of them. Hold
    some back, and let those be the judge. A hundred real test photos tell you more than
    ten thousand fake ones.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    e7, e7_render, e7_sum = ask(
        "**Check 7.** You add 6,000 generated rainy-night photos. Accuracy on a held-out "
        "slice of generated photos goes from 61% to 94%. What have you learned?",
        {
            "The synthetic data worked; rainy-night performance improved by 33 points": "works",
            "Almost nothing about the real problem, because both sets came from the same generator": "nothing",
            "The model is overfitting and you should add more generated photos": "more",
        },
        "nothing",
        "You have shown the model can handle your generator's output. Which it should, "
        "since the training and test photos share a maker, a style and the same habits. "
        "That is closer to a memory test than an evaluation.\n\nThe real question is what "
        "happens on actual footage from actual doorbells on actual rainy nights, and the "
        "only thing that answers it is actual footage. Even a small amount. Hold back 30 of "
        "your 100 real frames and measure on those; a 30-photo real test set is crude and "
        "noisy and still worth more than 6,000 fake ones, because it is the only one "
        "measuring the thing you are being paid to fix.\n\nThis is the Week 4 lesson once "
        "more, in a new costume: **the number went up** and **the system got better** are "
        "two separate claims, and only one of them is about your users.",
        key="e7",
    )
    e7
    return e7, e7_render, e7_sum


@app.cell(hide_code=True)
def _(e7, e7_render):
    e7_render(e7.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### How to test this fairly

    Which means the experiment has to be set up so the answer means something. Four runs,
    everything else held fixed:

    | Run | What you train on | What it tells you |
    | - | - | - |
    | **A** | Real photos only | The baseline. Without this nothing else has meaning |
    | **B** | Real + cheap augmentation | Could you have got away with Part 2 and gone home? |
    | **C** | Real + generated | Does generation add anything augmentation couldn't? |
    | **D** | Real + both | Do they stack, or overlap? |

    Run **B** is the one people leave out, and leaving it out is how a team spends three
    weeks on a diffusion pipeline to get an improvement that brightness jitter would have
    given them in an afternoon.

    Keep the model, the test set, the seeds and the training budget identical across all
    four. Report rainy-night recall specifically, not overall accuracy. And measure all of
    it on real held-out photos.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 6: Why your GPU is idle anyway""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Change of subject, and it is the part of this lab most likely to be worth money to you
    directly.

    Everything so far has been about *which* examples to train on. None of it matters if
    your expensive GPU is sitting there doing nothing, and it very often is.

    Training is a production line. Photos are read off disk, decoded from JPEG, augmented,
    batched, then handed to the GPU. Four stages, and like any production line, **it runs at
    the speed of the slowest stage.** A GPU that can chew through 800 images a second fed by
    a pipeline that delivers 300 runs at 300, and spends the rest of its life waiting.

    $$\text{actual speed} = \min(\text{how fast data arrives},\; \text{how fast the GPU works})$$

    There is a cheap trick for this, called **echoing**: when an image has been read and
    decoded, don't use it once and throw it away. Use it a few times, applying different
    random augmentation to each copy, so you get several different training views for one
    expensive read.

    Have a play. Watch all three numbers, especially the third.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    r_input = mo.ui.slider(
        50, 1200, value=saved.get("r_input", 300), step=50, disabled=locked,
        label="Images per second your pipeline can read and decode", show_value=True,
    )
    r_gpu = mo.ui.slider(
        200, 1600, value=saved.get("r_gpu", 800), step=100, disabled=locked,
        label="Images per second your GPU can train on", show_value=True,
    )
    echo = mo.ui.slider(
        1, 6, value=saved.get("echo", 1), step=1, disabled=locked,
        label="Echo: times each decoded image is reused", show_value=True,
    )
    mo.vstack([r_input, r_gpu, echo])
    return echo, r_gpu, r_input


@app.cell(hide_code=True)
def _(echo, r_gpu, r_input):
    views_available = r_input.value * echo.value
    r_effective = min(views_available, r_gpu.value)
    gpu_busy = 100.0 * r_effective / r_gpu.value
    # The point of the whole section: echoing multiplies views, never unique images.
    unique_rate = min(r_input.value, r_gpu.value / echo.value) if echo.value else 0
    input_bound = views_available < r_gpu.value
    return gpu_busy, input_bound, r_effective, unique_rate, views_available


@app.cell(hide_code=True)
def _(LAB_CSS, gpu_busy, input_bound, mo, r_effective, unique_rate):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w8-grid">
          <div class="w8-stat">
            <span class="k">Training views per second</span>
            <span class="v">{r_effective:,.0f}</span>
            <span class="why">what the GPU actually receives</span>
          </div>
          <div class="w8-stat {'red' if gpu_busy < 70 else 'green'}">
            <span class="k">GPU busy</span>
            <span class="v">{gpu_busy:,.0f}%</span>
            <span class="why">the rest is it waiting for data</span>
          </div>
          <div class="w8-stat">
            <span class="k">Bottleneck</span>
            <span class="v">{'Reading' if input_bound else 'GPU'}</span>
            <span class="why">{'the GPU is starved' if input_bound
                                else 'the GPU is the limit, as it should be'}</span>
          </div>
          <div class="w8-stat gold">
            <span class="k">Different photos per second</span>
            <span class="v">{unique_rate:,.0f}</span>
            <span class="why">new information, not repeats</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(echo, gpu_busy, input_bound, mo, r_effective, r_gpu, r_input, unique_rate):
    _head = (
        f"Reading at **{r_input.value:,}/s**, GPU capable of **{r_gpu.value:,}/s**, each "
        f"image reused **{echo.value}&times;**. The GPU gets **{r_effective:,.0f}** views "
        f"per second and is busy **{gpu_busy:.0f}%** of the time."
    )
    if echo.value == 1 and input_bound:
        _body = (
            f"\n\nSo **{100 - gpu_busy:.0f}%** of your GPU rental is being spent waiting "
            "for JPEGs to decode. Buying a GPU twice as fast would change nothing at all "
            "&mdash; it would wait twice as efficiently.\n\nNow push the echo slider up."
        )
    elif input_bound:
        _body = (
            f"\n\nEchoing has lifted the GPU from starving to **{gpu_busy:.0f}%** busy, and "
            "the reading stage never got any faster. You are getting more work out of "
            "hardware you were already paying for. Keep going until it stops helping."
        )
    else:
        _body = (
            f"\n\nThe GPU is now the bottleneck, which is where you want it: you are paying "
            f"for compute and using all of it.\n\n**But look at the last number.** Different "
            f"photos per second: **{unique_rate:,.0f}**. Push echo higher and it does not "
            "improve. It gets *worse*, because the GPU's fixed capacity is being spent on "
            "repeats instead of new material.\n\nThat is the catch, and it is the reason "
            "this question is worth asking carefully. Echoing buys you **utilisation**, not "
            "**learning**. The fifth copy of an image teaches far less than a fifth image "
            "would. A pipeline at 100% busy can still reach a target accuracy more slowly "
            "than one at 60%, if what it is busy with is the same photo over and over."
        )
    mo.callout(mo.md(_head + _body), kind="success" if gpu_busy >= 70 else "warn")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Deleting 75% of your data and making training slower

    Now the promised plot twist, and it is a real effect that catches good engineers.

    You take Week 7's advice. You prune a million photos down to 250,000, and you measure
    both runs over ten passes through the data.

    | | All the data | The pruned quarter |
    | - | - | - |
    | Photos per pass | 1,000,000 | 250,000 |
    | Speed it actually sustains | 1,000/s | **200/s** |
    | Time per pass | 1,000s | 1,250s |
    | **Ten passes** | **10,000s** | **12,500s** |

    Three quarters less data. Twenty-five per cent **more** time.

    The culprit is that middle row. Your original photos sat on disk in big sequential
    files, and reading those is what disks and networks are good at: ask for a chunk, get a
    chunk. Your pruned subset is 250,000 photos scattered all through those files. Now every
    read is a seek to a different place, and the clever prefetching that was hiding the disk
    latency has nothing to work with.

    Fewer photos, worse access pattern, slower pipeline.

    The fix is dull and completely effective: **after choosing your subset, write it out
    again as a fresh set of sequential files.** One pass over the data, once, and you get
    the sequential read speed back on a dataset a quarter the size. Then it really is
    faster.

    The lesson generalises beyond this example. A change that reduces the *amount* of work
    can increase the *time* by changing how the work is laid out. Count your examples all
    you like; you still have to measure the clock.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    e8, e8_render, e8_sum = ask(
        "**Check 8.** Your pipeline delivers 300 images/s and your GPU can take 800. "
        "Finance offers you a GPU twice as fast. What happens to your training time?",
        {
            "It roughly halves, since the GPU does the heavy lifting": "half",
            "Nothing, because the pipeline still delivers 300/s and that is what sets the pace": "nothing",
            "It improves by about 37.5%, in line with current utilisation": "util",
        },
        "nothing",
        "You would go from a GPU idle 62% of the time to one idle 81% of the time, at "
        "roughly twice the hourly rate. The production line still runs at the speed of its "
        "slowest stage, and you have just made the fast stage faster.\n\nWhat would actually "
        "help costs far less: more decoding workers, a cheaper image format, decoding on "
        "the GPU, caching the decoded data, or storing the dataset in big sequential files "
        "instead of many small ones.\n\nThe habit worth taking from this is the one from "
        "Week 6, and it is probably the most portable thing in this course. **Find the "
        "bottleneck before you spend anything.** An upgrade aimed at a stage that was never "
        "the limit buys you nothing, and it is an easy mistake to make because the "
        "expensive component feels like it must be the important one.",
        key="e8",
    )
    e8
    return e8, e8_render, e8_sum


@app.cell(hide_code=True)
def _(e8, e8_render):
    e8_render(e8.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 7: Three engineers, one budget""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Everything from both weeks, in one decision.

    The doorbell is good in daylight and bad on rainy nights. **The product requirement is
    90% rainy-night recall**, and you are currently at 62%. Three people on your team each
    want to do something different, and you can fund one of them this quarter.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w8-flow">
          <div class="step"><span class="n">Engineer A</span>
            <h5>Prune the daylight photos</h5>
            <p>Week 7's k-center. Drop the redundant daylight shots so training stops
            wasting time on them.</p></div>
          <div class="step"><span class="n">Engineer B</span>
            <h5>Generate rainy nights</h5>
            <p>Conditional diffusion plus a checking pipeline, to build the examples that
            were never photographed.</p></div>
          <div class="step"><span class="n">Engineer C</span>
            <h5>Fix the data pipeline</h5>
            <p>Caching, more decode workers, sequential files. Same dataset, better
            hardware utilisation.</p></div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    They each run a pilot. Here is what comes back, measured on **real** held-out photos.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    _rows = [
        ("A: pruning only", "96%", 65, "8 GPU-hrs"),
        ("B: generated + real", "95.5%", 91, "19 GPU-hrs"),
        ("C: better pipeline only", "96%", 75, "10 GPU-hrs"),
    ]
    _rows_html = ""
    _YES = '<span class="tick">meets the requirement</span>'
    _NO = '<span class="cross">does not meet it</span>'
    for _name, _acc, _rec, _cost in _rows:
        _ok = _rec >= 90
        _rows_html += (
            f"<tr class='{'on' if _ok else 'off'}'><td>{_name}</td>"
            f"<td class='num'>{_acc}</td><td class='num'>{_rec}%</td>"
            f"<td class='num'>{_cost}</td><td>{_YES if _ok else _NO}</td></tr>"
        )
    mo.Html(
        f"""
        <table class="w8-table">
          <thead><tr><th>Approach</th><th>Overall accuracy</th>
            <th>Rainy-night recall</th><th>Cost</th><th></th></tr></thead>
          <tbody>{_rows_html}</tbody>
        </table>
        """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "A: pruning, because it is cheapest and overall accuracy is highest": "prune",
        "B: generated data, because it is the only one that meets the requirement": "generate",
        "C: the pipeline work, because it is cheap and the gain is real": "pipeline",
        "C first, then B, because a faster pipeline makes B's experiments cheaper": "combo",
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
                label="**Which do you fund?**",
            ),
            why=mo.ui.text_area(
                value=_saved.get("why", ""),
                disabled=locked,
                placeholder="I would fund... because... The thing that would change my "
                            "mind is...",
                label="**Why? And what single measurement would tell you that you chose "
                      "wrong?** Not marked, and you can change it as often as you like.",
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
        "prune": (
            "The highest overall accuracy and the lowest cost, and it is the wrong call, "
            "for the reason this whole course keeps circling back to.\n\n96% overall with "
            "65% on rainy nights means the average is being carried by daylight, which is "
            "most events. The 35% of rainy-night pedestrians it misses are not a rounding "
            "error in a dashboard; they are the cases the product exists to catch. "
            "Optimising the average here optimises away the thing that matters.\n\nAnd "
            "pruning never addressed this problem. It made training cheaper. The model is "
            "still bad at night, because nobody gave it any more night."
        ),
        "generate": (
            "Right, and the reasoning is the part worth keeping. It is the most expensive "
            "option, 19 GPU-hours against 8, and it has the *lowest* overall accuracy of "
            "the three. On both of the numbers an instinct reaches for first, it loses."
            "\n\nIt is also the only one that does the job. The requirement is 90% "
            "rainy-night recall. A and C are not cheaper ways of meeting it; they do not "
            "meet it. There is one option on the table and the question is only whether you "
            "can afford it.\n\nThis is Check 2 arriving with real numbers. Fix the quality "
            "bar first, then shop on price among the things that clear it. The half-point "
            "of overall accuracy is a genuine cost and it is worth paying."
        ),
        "pipeline": (
            "A real improvement, genuinely cheap, and it does not solve your problem. 75% "
            "is better than 65% and it is not 90%.\n\nWorth understanding why it helped at "
            "all, because it is instructive: a faster pipeline means more training in the "
            "same wall-clock time, so the model squeezed more out of the 100 rainy-night "
            "photos it had. But the ceiling is set by those 100 photos, and efficiency "
            "cannot lift it. You can get to the ceiling faster. You cannot get through "
            "it.\n\nDo this work. Do it because it makes everything else cheaper, including "
            "B. Just don't file it as a fix for night-time recall."
        ),
        "combo": (
            "The answer a good engineer gives, and the one worth arguing about, so let's "
            "argue.\n\nThe logic is sound: C is cheap and makes every later experiment "
            "faster, so doing it first reduces the cost of B. Sequencing cheap "
            "infrastructure ahead of expensive experiments is usually right.\n\nThe "
            "objection is the clock. You are at 62% against a requirement of 90%, and C "
            "does not move you towards it. If the requirement has a date on it, you have "
            "spent some of your quarter making your tooling nicer while the actual gap sat "
            "where it was. B takes weeks: building the prompts, the checking pipeline, the "
            "validation.\n\nSo: start B now, and let C happen alongside it, because they "
            "touch different parts of the system and C's benefit lands on B's experiments "
            "while B is still running. If you genuinely must pick one, pick the one that "
            "clears the bar."
        ),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "The move underneath all four answers is the same one: **work out what is "
            "actually broken before you choose a tool.** Engineer A's method fixes "
            "redundancy. Engineer C's fixes throughput. Only B's fixes coverage, and "
            "coverage was what was broken.\n\nAll three are good techniques. Two of them "
            "were aimed at the wrong thing."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### One more thing: when expensive setup is worth it

    A footnote that decides a lot of real arguments.

    Engineer A's pruning costs 6 hours of scoring, then saves 4 hours on every training run
    (16 hours down to 12). Run once and you have spent 18 hours instead of 16, so you lost.
    Run it four times, as you would during a hyperparameter sweep, and it is 6 + 4&times;12
    = 54 hours against 4&times;16 = 64. You won.

    The break-even is just the setup cost divided by the per-run saving:

    $$n > \frac{6}{16 - 12} = 1.5$$

    So from the **second** run onward. The same arithmetic applies to Engineer B: screening
    6,000 generated photos is a one-off, and that dataset then serves every future training
    run.

    Which is why "is this worth it?" has no answer until somebody says how many times you
    are going to run it.
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
                placeholder="I would check... first, because if it came back as... then...",
                label="**Last one.** You've funded Engineer B. Before anybody generates a "
                      "single image, name one thing you would put in place, and say what "
                      "it protects you from.",
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
    accept_pct,
    alpha_bar,
    decision_form,
    e1,
    e2,
    e3,
    e4,
    e5,
    e6,
    e7,
    e8,
    echo,
    eps_val,
    gen_secs,
    hunch_form,
    lab_sync,
    mix_lam,
    need_valid,
    r_gpu,
    r_input,
    val_secs,
    x0_val,
):
    # Marked answers go through record_once, so the first answer is the one that
    # counts. Sliders and the written decision can change freely.
    if lab_sync is not None:
        lab_sync.record_once(
            e1=e1.value, e2=e2.value, e3=e3.value, e4=e4.value,
            e5=e5.value, e6=e6.value, e7=e7.value, e8=e8.value,
        )
        lab_sync.record(
            mix_lam=mix_lam.value, alpha_bar=alpha_bar.value,
            x0_val=x0_val.value, eps_val=eps_val.value,
            need_valid=need_valid.value, accept_pct=accept_pct.value,
            gen_secs=gen_secs.value, val_secs=val_secs.value,
            r_input=r_input.value, r_gpu=r_gpu.value, echo=echo.value,
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
    e1,
    e1_sum,
    e2,
    e2_sum,
    e3,
    e3_sum,
    e4,
    e4_sum,
    e5,
    e5_sum,
    e6,
    e6_sum,
    e7,
    e7_sum,
    e8,
    e8_sum,
):
    # One place that knows every marked answer, so the report, the score and the
    # dashboard cannot disagree.
    CHECKS = [
        ("Deleting cannot create what is missing", e1_sum(e1.value)),
        ("Comparing against something that fails", e2_sum(e2.value)),
        ("Why blending words does not work", e3_sum(e3.value)),
        ("Training a generator needs no labels", e4_sum(e4.value)),
        ("Fewer numbers is not a speed", e5_sum(e5.value)),
        ("The label is what needs checking", e6_sum(e6.value)),
        ("Testing on your own fake data", e7_sum(e7.value)),
        ("Upgrading the stage that was not the limit", e8_sum(e8.value)),
    ]
    checks_right = sum(1 for _n, (_t, _ok) in CHECKS if _ok)
    checks_score = f"{checks_right}/{len(CHECKS)}"
    return CHECKS, checks_right, checks_score


@app.cell(hide_code=True)
def _(
    CHECKS,
    LAB_CSS,
    accept,
    checks_score,
    cost_real,
    decision_choice,
    decision_why,
    done,
    echo,
    gpu_busy,
    mix_lam,
    mo,
    n_generated,
    need_valid,
    per_usable_synth,
    t_total_h,
    takeaway_text,
    unique_rate,
    xt,
):
    _ = (LAB_CSS, done)
    _what = {
        "prune": "Fund Engineer A, pruning",
        "generate": "Fund Engineer B, generated data",
        "pipeline": "Fund Engineer C, the pipeline",
        "combo": "Fund C first, then B",
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
        mo.md("## Your Week 8 report"),
        mo.Html(
            f"""
            <div class="w8-report">
              <div class="row">
                <span class="k">Marked checks</span>
                <span class="v"><span class="w8-score">{checks_score}</span></span>
              </div>
              <div class="row">
                <span class="k">Blending and noise</span>
                <span class="v">A MixUp blend of {mix_lam.value} per cent gives the label
                ({mix_lam.value / 100:.2f}, {1 - mix_lam.value / 100:.2f}). Your noise
                settings produced a pixel of {xt:+.3f}</span>
              </div>
              <div class="row">
                <span class="k">Cost of fake photos</span>
                <span class="v">To get {need_valid.value:,} usable ones at a
                {accept * 100:.0f} per cent pass rate you generate {n_generated:,.0f}, over
                {t_total_h:,.1f} hours of GPU and human time. That is
                &pound;{per_usable_synth:,.2f} each, against &pound;{cost_real:,.0f} to
                have the real ones labelled</span>
              </div>
              <div class="row">
                <span class="k">Your training pipeline</span>
                <span class="v">GPU busy {gpu_busy:.0f} per cent at an echo of
                {echo.value}, with {unique_rate:,.0f} genuinely different photos reaching
                it per second</span>
              </div>
              <div class="row">
                <span class="k">What you funded</span>
                <span class="v">{_what.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Reasoning</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">What you would put in place first</span>
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
        ("Your model is weak on a rare scene you have very few photos of. Which of these "
         "can raise the ceiling on how well it could possibly do?",
         {"Pruning the common scenes so training focuses on the rare one": "a",
          "Adding examples of the rare scene, whether photographed or generated": "b",
          "Making the data pipeline faster so it trains for more steps": "c"},
         "b"),
        ("Scoring and choosing a subset costs 6 hours once, and saves 4 hours on every "
         "training run. When does it start paying off?",
         {"Immediately, since each run is cheaper": "a",
          "From the second run, because 6 divided by 4 is 1.5": "b",
          "Never, since the setup cost is larger than the per-run saving": "c"},
         "b"),
        ("Your GPU reports 100% busy after you turned on echoing, but the model is taking "
         "more steps to reach the target accuracy than before. What is going on?",
         {"The GPU is throttling and needs better cooling": "a",
          "Busy is not the same as learning; it is processing repeats of the same photos": "b",
          "The echo factor is too low and should be raised further": "c"},
         "b"),
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
