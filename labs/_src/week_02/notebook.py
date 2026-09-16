import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 2 - Where Does It Actually Run")


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
    def ask(prompt, options, correct, explain, key):
        """A quick check you can answer as many times as you like.

        Returns (radio, render, summarise). Pass radio.value to render(); the
        report uses summarise() to include the answer at the end of the lab.
        """
        labels = {value: label for label, value in options.items()}
        BREAK = chr(10) + chr(10)

        radio = mo.ui.radio(options=options, label=prompt,
                            value=pick(options, saved.get(key)), disabled=locked)

        def render(value):
            if value is None:
                return mo.callout(mo.md("Pick an answer and I will explain it."), kind="neutral")
            ok = value == correct
            body = ("**Correct.** " if ok else "**Not quite.** ") + explain[value]
            if not ok:
                body += BREAK + f"The answer is *{labels[correct]}*."
            return mo.callout(mo.md(body), kind="success" if ok else "warn")

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
          .w2-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w2-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w2-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w2-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w2-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w2-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w2-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w2-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w2-split { grid-template-columns: 1fr; } }
          .w2-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w2-split > .body p:last-child { margin-bottom: 0; }

          .w2-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w2-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w2-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w2-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w2-aside li:last-child { margin-bottom: 0; }
          .w2-aside li::marker { color: #6a5314; font-weight: 800; }
          .w2-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w2-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w2-aside .meta div:last-child { margin-bottom: 0; }
          .w2-aside .meta dt { color: #6f6f6f; }
          .w2-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w2-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w2-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w2-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }

          .w2-homes { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
                      margin: 16px 0; }
          @media (max-width: 900px) { .w2-homes { grid-template-columns: 1fr 1fr; } }
          @media (max-width: 560px) { .w2-homes { grid-template-columns: 1fr; } }
          .w2-home { border: 1px solid #e6e6e6; border-top: 5px solid #dcdcdc;
                     border-radius: 12px; background: #fff; padding: 14px 15px; }
          .w2-home.ok  { border-top-color: #2e7d32; }
          .w2-home.bad { border-top-color: #c62828; background: #fefafa; }
          .w2-home h4 { margin: 0 0 2px; font-size: 1rem; color: #111; }
          .w2-home .where { color: #6f6f6f; font-size: .78rem; margin: 0 0 10px; }
          .w2-home dl { margin: 0; font-size: .84rem; }
          .w2-home dt { color: #6f6f6f; margin-top: 7px; }
          .w2-home dd { margin: 1px 0 0; color: #111; font-weight: 700; }
          .w2-home .verdict { margin-top: 11px; padding-top: 9px;
                              border-top: 1px solid #f0f0f0; font-size: .86rem;
                              font-weight: 800; }
          .w2-home.ok  .verdict { color: #2e7d32; }
          .w2-home.bad .verdict { color: #c62828; }
          .w2-home .why { display: block; font-weight: 400; color: #6f6f6f;
                          font-size: .8rem; margin-top: 2px; line-height: 1.4; }

          .w2-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w2-report .row { display: grid; grid-template-columns: 190px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w2-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w2-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w2-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w2-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w2-report .tick { color: #2e7d32; font-weight: 800; }
          .w2-report .cross { color: #c62828; font-weight: 800; }
          .w2-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                              color: #333; font-style: italic; }

          .w2-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w2-bar { display: grid; grid-template-columns: 150px 1fr 100px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w2-bar { grid-template-columns: 110px 1fr 78px; } }
          .w2-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w2-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 28px; overflow: hidden; }
          /* A span is inline by default, so it ignores height and percentage width.
             Both of these have to be blocks or the bar renders empty. */
          .w2-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w2-bar.win .fill { background: #f1b82d; }
          .w2-bar.win .t { color: #111; font-weight: 700; }
          .w2-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }
          .w2-total { border-top: 1px solid #eee; margin-top: 12px; padding-top: 10px;
                      display: flex; justify-content: space-between; font-size: .95rem; }
          .w2-total b { color: #111; }
        </style>
        """
    )
    LAB_CSS
    return (LAB_CSS,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w2-hero">
          <p class="w2-eyebrow">CSC/EE 8001 &middot; Week 2</p>
          <h1>Where Does It Actually Run?</h1>
          <p class="sub">A model has to live on a real machine somewhere. This lab is about
          two questions you have to answer before it can: will it fit, and once it fits, how
          long does it take to reply?</p>
          <div class="w2-chips">
            <span class="w2-chip">Four kinds of machine</span>
            <span class="w2-chip">What fits where</span>
            <span class="w2-chip-plain w2-chip">Nothing here is marked</span>
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
        <div class="w2-split">
          <div class="body">
            <p>Start with what a model actually is, physically, once training is finished.</p>
            <p><strong>It is a very long list of numbers.</strong> That is genuinely all. When
            someone says "a model with 25 million parameters", they mean there are 25 million
            numbers written down. Show it a photo and the computer does arithmetic with those
            numbers until an answer falls out the other end.</p>
            <p>That matters here for one reason. Numbers take up room, and they have to be
            somewhere the computer can reach quickly. So before a model can run anywhere, two
            things have to be true. <strong>The list has to fit</strong>, and <strong>the
            computer has to be able to read through it fast enough</strong> that whoever asked
            is still waiting.</p>
            <p>This lab is those two questions, in that order.</p>
          </div>
          <aside class="w2-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Work out on paper whether a model will fit on a given machine.</li>
              <li>Say what to do when it does not.</li>
              <li>Break the time it takes to answer into three parts, and find the slow one.</li>
              <li>Explain why that answer changes when you send more work at once.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 30 min</dd></div>
              <div><dt>Before this</dt><dd>Week 1</dd></div>
              <div><dt>Marked?</dt><dd>no, the quiz is</dd></div>
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
        <div class="w2-question">
          <span class="lbl">The question this lab answers</span>
          <p>"I have a model and a machine. Will it fit, and will it be quick enough?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: The machine it has to live on""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The list of numbers has to sit in the computer's **memory**. Not on its hard disk, which is
    too slow to be useful here, but in the fast working memory the processor can reach directly.

    How much of that memory you get depends entirely on the machine, and machines vary far more
    than most people expect. Almost everything you build ends up on one of these four.

    | Where | Answers in | Electricity | Memory it has |
    | - | - | - | - |
    | **A data centre** | 100 to 500 ms | 3 to 5 megawatts | terabytes |
    | **A local server** | 10 to 100 ms | 100 to 200 watts | gigabytes |
    | **A phone** | 5 to 50 ms | 3 to 5 watts | gigabytes, but you only get a slice |
    | **A microcontroller** | 1 to 10 ms | 50 to 100 milliwatts | kilobytes |

    Look at the electricity column twice. The top row is **megawatts**, about what a small town
    uses. The bottom row is **milliwatts**, less than a hearing aid. Nine zeros between them.
    Memory does the same thing: terabytes down to kilobytes.

    Why so far apart? Because of what each one is plugged into. The data centre is on the mains,
    in a building built to carry the heat away. The little chip is running off a battery that
    someone has to get a ladder out to change, and they would rather do that every two years
    than every two weeks.

    Now look at the speed column, which runs the other way. The machine with almost nothing has
    to answer the **fastest**.

    That is not a mistake either. When you ask a data centre something, you are a person at the
    end of a network, and people will wait half a second without minding. The little chip is not
    answering a person. It is inside a door that is closing, or a motor that is turning, and
    those do not wait. It also has nobody to hand the job to. The phone can ask a server, the
    server can ask a data centre, and the chip stuck on the wall can ask nobody.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q1, q1_render, q1_sum = ask(
        "**Quick check.** A data centre has a thousand times more of everything. Why would anyone put a model on a microcontroller instead?",
        {
            "Microcontrollers are faster at maths": "a",
            "Because the data centre is not there: no network, no time to wait, no battery to spare": "b",
            "It is cheaper to train the model that way": "c",
            "Microcontrollers are more accurate on small datasets": "d",
        },
        "b",
        {
            "a": ("The opposite, by a wide margin. A microcontroller does roughly a billionth of "
                  "the sums per second that a rack in a data centre does."),
            "b": ("Sending the work somewhere else costs a network round trip, and a lot of "
                  "things cannot wait or have nowhere to send it. A doorbell in a house with bad "
                  "wifi still has to work."),
            "c": ("Training almost never happens on the small device. It happens in the data "
                  "centre, and only the finished model is sent down."),
            "d": ("Accuracy is a property of the model and the data it learned from, not of the "
                  "chip it later runs on."),
        },
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
    mo.md(r"""## Part 2: Will it fit?""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Now the first of the two questions. Given a model and a machine, will the list of numbers
    fit in the memory that machine has?

    You can work this out on paper, and it is worth seeing how simple it is.

    Each number in the list normally takes up **four bytes**. So a model with 25 million numbers
    takes 25 million times four, which is 100 million bytes, or about **100 MB**. Compare that
    against the memory of the machine, and you have your answer.

    The cards below do exactly that sum for four machines at once. They also check the second
    question, how long the machine takes to read the whole list, but leave that for now. Drag
    the slider and watch which machines stay open to you.

    /// admonition | Each card is one example chip, not a whole category
    Chips in the same row differ wildly. An Arduino Uno has **2 KB** of memory. The ESP32 in a
    smart plug has about **520 KB**. That is 250 times, inside one row, and a model that runs
    happily on one will not load at all on the other.

    So "will it run on a microcontroller" has no answer. **"Will it run on this chip"** does.
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    MODELS = [
        (0.05, "a wake word spotter, the thing listening for 'hey'"),
        (0.5, "a tiny image classifier"),
        (3.5, "MobileNet, built for phones"),
        (25.0, "ResNet-50, the workhorse image model"),
        (110.0, "BERT base, a small language model"),
        (350.0, "BERT large"),
        (1500.0, "GPT-2"),
        (7000.0, "a 7 billion parameter chat model"),
    ]
    size = mo.ui.slider(
        steps=[m[0] for m in MODELS],
        value=saved.get("size", 3.5),
        disabled=locked,
        label="Model size, in millions of numbers",
        show_value=True,
    )
    _precisions = {
        "4 bytes each, full precision": 4.0,
        "2 bytes each, half": 2.0,
        "1 byte each, quantised": 1.0,
    }
    precision = mo.ui.radio(
        options=_precisions,
        value=pick(_precisions, saved.get("precision")) or "4 bytes each, full precision",
        disabled=locked,
        inline=True,
        label="How much space each number takes",
    )
    mo.vstack([size, precision])
    return MODELS, precision, size


@app.cell(hide_code=True)
def _(MODELS, precision, size):
    HOMES = [
        # name, where, memory it has (MB), read speed (GB/s), must answer within (ms)
        ("Data centre", "one big accelerator", 80_000.0, 2039.0, 500.0),
        ("Local server", "a workstation card", 8_000.0, 200.0, 100.0),
        ("Phone", "what one app is allowed", 1_500.0, 50.0, 50.0),
        ("Microcontroller", "an ESP32, roughly", 0.5, 0.2, 10.0),
    ]

    params_m = float(size.value)
    bytes_each = float(precision.value)
    # Space taken up is simply how many numbers there are times how big each one is.
    model_mb = params_m * bytes_each
    describe = dict(MODELS).get(params_m, "")

    results = []
    for _name, _where, _mem, _bw, _budget in HOMES:
        fits = model_mb <= _mem
        # One answer means reading every number once, so time is size divided by read speed.
        read_ms = (model_mb / 1024.0) / _bw * 1000.0
        in_time = read_ms <= _budget
        results.append({
            "name": _name, "where": _where, "mem": _mem, "budget": _budget,
            "fits": fits, "read_ms": read_ms, "in_time": in_time,
            "ok": fits and in_time,
            "over": model_mb / _mem if _mem else float("inf"),
        })
    return bytes_each, describe, model_mb, params_m, results


@app.cell(hide_code=True)
def _(LAB_CSS, bytes_each, describe, mo, model_mb, params_m, results):
    _ = LAB_CSS

    def _size(mb):
        if mb >= 1024:
            return f"{mb / 1024:.1f} GB"
        if mb >= 1:
            return f"{mb:.0f} MB"
        return f"{mb * 1024:.0f} KB"

    def _time(ms):
        if ms >= 1:
            return f"{ms:.1f} ms"
        if ms >= 0.001:
            return f"{ms * 1000:.0f} microseconds"
        return "well under a microsecond"

    _cards = ""
    for r in results:
        if r["ok"]:
            verdict = "Runs here"
            why = f"reads in {_time(r['read_ms'])}, budget is {r['budget']:.0f} ms"
        elif not r["fits"]:
            verdict = "Will not fit"
            why = f"{r['over']:.0f} times bigger than the memory available"
        else:
            verdict = "Too slow here"
            why = f"needs {_time(r['read_ms'])} to read, budget is {r['budget']:.0f} ms"
        _cards += f"""
        <div class="w2-home {'ok' if r['ok'] else 'bad'}">
          <h4>{r['name']}</h4>
          <p class="where">{r['where']}</p>
          <dl>
            <dt>Memory it has</dt><dd>{_size(r['mem'])}</dd>
            <dt>Must answer within</dt><dd>{r['budget']:.0f} ms</dd>
          </dl>
          <div class="verdict">{verdict}<span class="why">{why}</span></div>
        </div>
        """

    mo.vstack([
        mo.md(f"**{params_m:g} million numbers**, which is {describe}. "
              f"At {bytes_each:g} bytes each that takes up **{_size(model_mb)}**."),
        mo.Html(f'<div class="w2-homes">{_cards}</div>'),
    ])
    return


@app.cell(hide_code=True)
def _(mo, results):
    _open = [r["name"] for r in results if r["ok"]]
    if len(_open) == 4:
        _msg, _kind = "**Every machine on the list can run this one.**", "success"
    elif _open:
        _msg, _kind = (
            f"**Still fine on:** {', '.join(_open)}. The rest have run out of something.",
            "info",
        )
    else:
        _msg, _kind = (
            "**Nowhere on this list can run it.** That is a real situation, and the answer is "
            "either a smaller model or a bigger machine than anything here.",
            "danger",
        )
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "What you should have noticed": mo.md(
                """
**Places drop out from the bottom, and they drop out early.** The microcontroller is gone
before you reach anything most people would call a big model. MobileNet was built to be small
and to run on phones, and it is still about 28 times too big for a microcontroller.

**Memory runs out long before speed does.** Read the red cards again. They nearly all say "will
not fit", not "too slow". Once something fits, it is usually quick enough. People buy faster
chips when what actually stopped them was space.

**The model never changed.** Same numbers, same order, the whole way along. All that changed was
where you asked it to live. Last week that point came at you through time. This week it comes
through space.

**The top runs out too.** A 7 billion number model is 27 GB. Only the data centre can hold it.
That is why the chat tools you use every day answer over a network instead of running on your
laptop.
"""
            ),
            "Why reading the model is what takes the time": mo.md(
                """
To produce one answer, the machine has to read every number in the model at least once. It
cannot skip any: they all contribute.

So the time has a floor set by something very ordinary, which is how fast that machine can pull
data out of its memory. A data centre accelerator moves about 2,000 gigabytes a second. A phone
manages perhaps 50. A microcontroller, a fraction of one.

That gives you a quick sum you can do in your head before writing any code:

> **time to read the model = size of the model divided by how fast the machine reads**

For ResNet-50 at 100 MB on a data centre accelerator, that is about 0.05 milliseconds. On a
phone, about 2 milliseconds. Both comfortably inside their budgets, which is why that model is
everywhere.

This is rough. It ignores the sums themselves, and it assumes one answer at a time. But it gets
you close enough in about ten seconds, and close enough is usually all you need to decide.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q2, q2_render, q2_sum = ask(
        "**Quick check.** A model will not run on your phone. Looking at the cards above, what is most often the reason?",
        {
            "The phone is not fast enough at doing the sums": "a",
            "The model is simply too big to fit in the memory the phone gives an app": "b",
            "The phone is not accurate enough": "c",
            "The model was trained on the wrong kind of hardware": "d",
        },
        "b",
        {
            "a": ("Sometimes, but it is rarely what stops you first. Look at how many red cards "
                  "said 'will not fit' rather than 'too slow'."),
            "b": ("Space runs out before speed does, almost every time. That is why so much of "
                  "this course is about making models smaller rather than machines faster."),
            "c": ("Accuracy belongs to the model, not the phone. The same model gives the same "
                  "answers wherever it manages to run."),
            "d": ("Where a model was trained has no bearing on whether it fits somewhere later. "
                  "Training happens once, in a data centre, on hardware nobody deploys to."),
        },
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
    mo.md(r"""## Part 3: What to do when it does not fit""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    You will have found sizes where some of the cards go red. That happens constantly in real
    work, and the machine is usually not something you get to change. It is the camera already
    screwed to the wall, or the phone your users already own.

    So the model has to get smaller. And there is a way to do that which does not touch the
    model's design at all.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Storing the same number in less space

    Remember the sum from Part 2: size is the count of numbers times four bytes each.

    There are two ways to make that smaller, and only one of them is easy. You could use fewer
    numbers, which means designing a different model and retraining it. Or you could **keep
    every number and store each one in less space**.

    Four bytes is simply the default. It holds a number to far more decimal places than most
    models need. Round each one off a little and it fits in **two bytes**. Round harder and it
    fits in **one**.

    The list stays exactly as long. Nothing is deleted. But the whole thing halves, then halves
    again. Go back to the slider in Part 2 and switch between the three settings.

    | How each number is stored | A 110 million number model | What it costs you |
    | - | - | - |
    | 4 bytes, full precision | 440 MB | nothing, this is the original |
    | 2 bytes, half | 220 MB | usually almost no accuracy |
    | 1 byte, quantised | 110 MB | a little accuracy, sometimes none |

    This is called **quantisation**, and it is the first thing anyone reaches for. It is close
    to free at 2 bytes. At 1 byte you start paying, and how much you pay depends on the model
    and on what it is being asked to do.

    It is also not unlimited. Four times smaller is roughly where this particular trick runs
    out, and a 7 billion number model that needs 27 GB is still 6.8 GB after it. Real
    deployments stack other techniques on top, which is what several later weeks are about.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w2-question">
          <span class="lbl">Worth knowing</span>
          <p>"A GPT-4 class model is about 1.8 trillion numbers. Even at two bytes each that is
          roughly 3.6 terabytes. A phone has about 8 gigabytes. That is a gap of some 450
          times, and no amount of rounding closes it."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q3, q3_render, q3_sum = ask(
        "**Quick check.** You halve the space each number takes. What happens to the model?",
        {
            "It has half as many numbers in it": "a",
            "It keeps every number, but each is stored less precisely, so the whole thing is half the size": "b",
            "It runs twice as fast but stays the same size": "c",
            "It has to be retrained from scratch": "d",
        },
        "b",
        {
            "a": ("Nothing is removed. Every number is still there, which is why the model still "
                  "behaves in almost the same way."),
            "b": ("The list is the same length; each entry is just kept more roughly. Half the "
                  "space, and usually very little accuracy lost at two bytes."),
            "c": ("It usually does speed things up too, because there is less to fetch. But the "
                  "main thing it changes is size, and size is what decides whether it fits at "
                  "all."),
            "d": ("Usually not. It is normally applied to a model that has already been trained, "
                  "which is a large part of why it is the first thing people try."),
        },
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
    mo.md(r"""## Part 4: Fitting is not the same as being fast enough""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    That was the first question settled. The model fits. Now the second one, which is the
    harder half: somebody has asked it something, and they are waiting. How long do they wait?

    Here is the part people skip. To produce one single answer, the computer has to **read every
    number in the model**. All of them. It cannot use some and ignore the rest, because they all
    contribute to the answer.

    So reading is not free, and on a big model it is not quick either.

    A useful way to picture the whole thing is making a sandwich. You walk to the fridge and get
    the things out. You make the sandwich. And there is a little faff around it, washing your
    hands, finding a plate. Three steps, and the time is all three added up.

    A computer answering a question does exactly those three.

    **It fetches.** It pulls the model's numbers out of memory. Memory is the fridge, and the
    walk is not instant.

    **It does the sums.** Multiplying and adding, millions of times over. This is the bit
    everyone pictures when they imagine a computer working, and it is often not the slow bit.

    **And there is a little setup.** Starting the job off, waiting for parts of it to line up.
    Usually a few milliseconds.

    > **time = fetching + doing the sums + setup**

    Now, why does anyone bother writing that down?

    Because of this. Suppose fetching takes ten seconds and the sums take one. You go out and
    buy a computer that does sums twice as fast. What actually improves? Almost nothing. You
    still spend ten seconds walking to the fridge.

    **So before spending anything on making something faster, work out which of the three you
    are stuck on.** The next part is you doing that.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <p style="color:#3a3a3a; line-height:1.7;"><strong>Working out each one.</strong>
        Both of the first two are the same kind of sum you already know: how much, divided by how
        fast.</p>
        <ul style="color:#3a3a3a; line-height:1.75; font-size:1rem;">
          <li><strong>Fetching.</strong> How many bytes, divided by how many bytes a second the
              machine can pull from memory. 40 megabytes at 100 megabytes a second is 0.4
              seconds. Exactly like 40 miles at 100 miles an hour.</li>
          <li><strong>The sums.</strong> How many operations, divided by how many the machine
              does per second. One warning: no chip ever runs at the speed printed on the box.
              If yours manages 60 per cent of it, use 60 per cent.</li>
          <li><strong>Setup.</strong> Just a number someone measured. A few milliseconds.</li>
        </ul>
        <div class="w2-question">
          <span class="lbl">One check that catches most mistakes</span>
          <p>"All three have to come out in seconds. If yours do not, something has gone wrong
          before you got to the answer."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: Working out which of the three is the slow one""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is a request arriving at a service, with all three numbers worked out for you as you
    change them.

    About the machine: it pulls **100 megabytes a second** out of memory, and every request
    carries a fixed **5 milliseconds** of setup however small the job is.

    The three sliders describe the job you hand it. The first two are the sums from before, both
    of them just *how much, divided by how fast*. Move them and watch where the time goes.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    bytes_mb = mo.ui.slider(
        5, 200, value=saved.get("bytes_mb", 40), step=5, disabled=locked,
        label="How much it has to fetch (megabytes)", show_value=True,
    )
    ops_gf = mo.ui.slider(
        0.5, 20.0, value=saved.get("ops_gf", 2.0), step=0.5, disabled=locked,
        label="How many sums it has to do (billions)", show_value=True,
    )
    machine_gf = mo.ui.slider(
        4, 48, value=saved.get("machine_gf", 12), step=2, disabled=locked,
        label="How many sums the machine really manages per second (billions)",
        show_value=True,
    )
    mo.vstack([bytes_mb, ops_gf, machine_gf])
    return bytes_mb, machine_gf, ops_gf


@app.cell(hide_code=True)
def _(bytes_mb, machine_gf, ops_gf):
    BANDWIDTH_MBPS = 100.0
    OVERHEAD_MS = 5.0

    t_data = float(bytes_mb.value) / BANDWIDTH_MBPS * 1000.0
    t_compute = float(ops_gf.value) / float(machine_gf.value) * 1000.0
    t_over = OVERHEAD_MS
    t_total = t_data + t_compute + t_over

    terms = [
        ("Fetching", t_data, f"{bytes_mb.value:g} MB to fetch, at {BANDWIDTH_MBPS:g} MB a second"),
        ("Doing the sums", t_compute,
         f"{ops_gf.value:g} billion sums, at {machine_gf.value:g} billion a second"),
        ("Setup", t_over, "the same every time"),
    ]
    biggest = max(terms, key=lambda x: x[1])[0]

    # What a machine twice as fast would actually buy you.
    t_total_2x = t_data + (t_compute / 2.0) + t_over
    saved_pct = (t_total - t_total_2x) / t_total * 100.0
    return biggest, saved_pct, t_total, t_total_2x, terms


@app.cell(hide_code=True)
def _(LAB_CSS, biggest, mo, t_total, terms):
    _ = LAB_CSS
    _widest = max(t[1] for t in terms) or 1.0
    _rows = ""
    for _label, _ms, _detail in terms:
        _pct = _ms / _widest * 100.0
        _win = " win" if _label == biggest else ""
        _rows += f"""
        <div class="w2-bar{_win}">
          <span class="t">{_label}<br><span style="color:#8a8a8a;font-size:.78rem">{_detail}</span></span>
          <span class="track"><span class="fill" style="width:{_pct:.1f}%"></span></span>
          <span class="n">{_ms:.0f} ms</span>
        </div>
        """
    mo.Html(
        f"""
        <div class="w2-bars">{_rows}</div>
        <div class="w2-total"><span>How long that person waits</span><b>{t_total:.0f} ms</b></div>
        """
    )
    return


@app.cell(hide_code=True)
def _(biggest, mo, saved_pct, t_total, t_total_2x):
    mo.vstack([
        mo.callout(
            mo.md(f"**{biggest}** is the biggest of the three. That is the one holding "
                  f"you up, and the only one worth paying to fix."),
            kind="info",
        ),
        mo.md(
            f"Say you buy a machine that does sums **twice as fast**. The wait goes from "
            f"**{t_total:.0f} ms** down to **{t_total_2x:.0f} ms**. You paid twice as much "
            f"and got **{saved_pct:.0f} per cent**."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "What to take from that": mo.md(
                """
Where the sliders started, the three numbers were **400**, **167** and **5** milliseconds.

Fetching took more than twice as long as the sums. So for most of that request, the computer had
already finished its maths and was sitting there waiting for data to arrive. Back at the fridge.

Now look at what the upgrades buy you.

- A processor **twice as fast** cuts 167 down to 83. You save 84 ms out of 572. About **15 per
  cent**.
- Memory **twice as fast** cuts 400 down to 200. You save 200 ms out of 572. About **35 per
  cent**.

Same money. One of them is more than twice as good, and it is not the one most people reach for.

**So: find the biggest of the three before you spend anything.** That is really all this is for.

Try dragging the sums slider up to 20 billion. Now the sums are the big number, and the fast
processor becomes the right buy. Neither component is better than the other. It depends entirely
on the job you are giving it.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q4, q4_render, q4_sum = ask(
        "**Quick check.** Your request spends 400 ms moving bytes and 167 ms computing. Your budget buys one upgrade. Which?",
        {
            "A processor twice as fast": "a",
            "Memory twice as fast": "b",
            "Both, split evenly": "c",
            "Neither: reduce the overhead instead": "d",
        },
        "b",
        {
            "a": ("This is the reflex, and it buys about 15 per cent. You would be paying to "
                  "speed up the part that was already waiting around."),
            "b": ("Halving the 400 ms term takes 200 ms off a 572 ms request, roughly 35 per "
                  "cent. Three times the improvement, for the same money."),
            "c": ("Splitting a budget across both gets you less than putting all of it on the "
                  "term that dominates. Diagnose first, then spend."),
            "d": ("The overhead is 5 ms of 572. Even removing it entirely is under one per cent."),
        },
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
    mo.md(r"""## Part 6: The slow step can change, without you changing the model""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    You can now find the slow step. The last thing to know is that the answer is not fixed. It
    moves, and you are the one who moves it.

    Back to the sandwiches.

    Making one sandwich: you walk to the fridge, get everything out, make it, put it back. Most
    of your time went on walking.

    Making eight: you still walk to the fridge **once**. That walk is now shared between all
    eight, so per sandwich it hardly counts. What takes the time now is buttering and cutting,
    and you have to do that eight times over.

    **Same fridge, same walk, same sandwich. Different answer about what is slowing you down.**

    Computers do precisely this, and it is why "that model is slow because of memory" is not a
    fact you can look up anywhere.

    To see it, there is one detail Part 2 left out. A model does not only need room for its own
    numbers. While it runs it also scribbles down working-out at each step, the way you would on
    paper, then throws it away. For ResNet-50, a common image model:

    - its own numbers come to about **97.5 MB**, and those are fetched **once**, no matter how
      many images you send through together
    - the working-out is about **20 MB for every image**, so that part grows

    The sums come to about **7.7 billion for every image**, so those grow too.

    Send eight images at once and you do eight times the sums. But you do not fetch eight times
    the bytes, because the 97.5 MB was fetched once and shared between them. That is the walk to
    the fridge, and it is what shifts the balance.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    batch = mo.ui.slider(
        steps=[1, 2, 3, 4, 8, 16, 32, 64],
        value=saved.get("batch", 1),
        disabled=locked,
        label="How many images you send at once",
        show_value=True,
    )
    batch
    return (batch,)


@app.cell(hide_code=True)
def _(batch):
    WEIGHTS_MB = 97.5
    ACT_MB = 20.0
    FLOPS_PER_IMAGE = 7.7e9
    MACHINE_DEMANDS = 153.0     # what this accelerator needs per byte to stay busy

    b = int(batch.value)
    fetched_mb = WEIGHTS_MB + ACT_MB * b
    ops = FLOPS_PER_IMAGE * b
    supplied = ops / (fetched_mb * 1e6)          # sums the job offers per byte fetched
    ceiling = FLOPS_PER_IMAGE / (ACT_MB * 1e6)  # where it flattens out, however big the batch
    compute_bound = supplied > MACHINE_DEMANDS
    return (
        MACHINE_DEMANDS,
        b,
        ceiling,
        compute_bound,
        fetched_mb,
        ops,
        supplied,
    )


@app.cell(hide_code=True)
def _(LAB_CSS, MACHINE_DEMANDS, compute_bound, fetched_mb, mo, ops, supplied):
    _ = LAB_CSS
    _scale = max(supplied, MACHINE_DEMANDS) * 1.1
    mo.Html(
        f"""
        <div class="w2-bars">
          <div class="w2-bar{' win' if compute_bound else ''}">
            <span class="t">Sums the job offers<br><span style="color:#8a8a8a;font-size:.78rem">
            {ops / 1e9:.1f} billion sums for every {fetched_mb:.0f} MB fetched</span></span>
            <span class="track"><span class="fill"
              style="width:{supplied / _scale * 100:.1f}%"></span></span>
            <span class="n">{supplied:.0f}</span>
          </div>
          <div class="w2-bar{'' if compute_bound else ' win'}">
            <span class="t">Sums the machine wants<br><span style="color:#8a8a8a;font-size:.78rem">
            to avoid sitting idle</span></span>
            <span class="track"><span class="fill"
              style="width:{MACHINE_DEMANDS / _scale * 100:.1f}%"></span></span>
            <span class="n">{MACHINE_DEMANDS:.0f}</span>
          </div>
        </div>
        <p style="color:#6f6f6f;font-size:.85rem;margin:2px 0 0">Both bars count sums per byte
        fetched. If the job offers fewer than the machine wants, the machine finishes early and
        waits around.</p>
        """
    )
    return


@app.cell(hide_code=True)
def _(b, compute_bound, mo, supplied):
    if compute_bound:
        _msg = (f"With {b} image{'s' if b > 1 else ''} at a time, the job hands over "
                f"{supplied:.0f} sums for every byte fetched. The machine only wanted 153, so "
                f"it has plenty to get on with. **Now the sums are what take the time.**")
        _kind = "success"
    else:
        _msg = (f"With {b} image{'s' if b > 1 else ''} at a time, the job only hands over "
                f"{supplied:.0f} sums for every byte fetched, and the machine wanted 153. "
                f"**It finishes early and waits.** Most of the time goes on fetching.")
        _kind = "warn"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(ceiling, mo):
    mo.accordion(
        {
            "What just happened": mo.md(
                f"""
First, what the two numbers on the bars mean.

The top one belongs to the job: how many sums it hands over for every byte fetched. Send more
images at once and this number changes.

The bottom one belongs to the machine: how many sums it can get through for every byte it can
fetch. For this one that is **153**, and it never changes.

Compare the two and you have your answer. If the job offers fewer sums per byte than the machine
wants, the machine finishes early and waits. If it offers more, the machine is what is holding
you up.

Now watch what happened.

**One image.** The job offers 66 sums per byte. The machine wanted 153. It is bored. Most of the
time goes on fetching.

**Four images.** They cross over.

**Eight images.** The job now offers 239. The machine has plenty to do, and the sums become the
slow part.

Nothing about the model changed. Same numbers inside it, same card underneath it. **All you
changed was how many images you sent at once.** So if someone asks you whether ResNet-50 is
limited by memory or by computing, the honest answer is "it depends how you run it", and how you
run it is your choice.

**It does stop helping, though.** Push the slider to 64 and the number barely moves. The highest
it can ever go is about **{ceiling:.0f}**. Once the working-out is much bigger than the model's
own numbers, there is no fridge trip left to share out. That limit comes from how the model is
built, and no batch size gets past it.

So why do people run 512 images at once? Not for this. That was settled by about four. They do
it to stop the machine sitting idle between jobs, which is the throughput problem from Week 1.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q5, q5_render, q5_sum = ask(
        "**Quick check.** Is ResNet-50 compute-bound or memory-bound?",
        {
            "Compute-bound, it is a convolutional network": "a",
            "Memory-bound, it has to read all its weights": "b",
            "The question is malformed: it depends on the batch size and the machine": "c",
            "It depends only on which machine you run it on": "d",
        },
        "c",
        {
            "a": ("You just watched it be memory-bound at one image. The architecture does not "
                  "decide this on its own."),
            "b": ("True at batch 1, false by batch 8. Same model, same card, only the batch "
                  "changed."),
            "c": ("A model does not carry a regime around with it. It is bound by whichever term "
                  "is larger in the setup you are actually running, and batch size moves that."),
            "d": ("The machine is half of it. The other half is how you feed it, which is why "
                  "the batch slider changed the verdict without touching the hardware."),
        },
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
    mo.md(r"""## Part 7: Putting it to work""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w2-question">
          <span class="lbl">The situation</span>
          <p>"We are putting a camera on every door of the building. It should notice when a
          parcel is left and tell someone. There are three hundred doors, the wifi is
          unreliable, and the cameras run on batteries we would rather not change every
          month."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "Send every frame to a data centre and do the work there": "cloud",
        "Put a small server in the building and send frames to that": "edge",
        "Run a small model on each camera and send only what it finds": "device",
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
                label="**Where would you run it?**",
            ),
            why=mo.ui.text_area(
                value=_saved.get("why", ""),
                disabled=locked,
                placeholder="What made you pick that, and what would change your mind?",
                label="**Why?**",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_disabled=locked,
            submit_button_label="Submit my decision",
            bordered=True,
            validate=lambda v: (
                "Choose one of the three."
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
    mo.stop(
        not (decision_form.value or saved.get("decision")),
        mo.callout(mo.md("Pick an answer, say why, then press **Submit my decision**."), kind="warn"),
    )
    decision_choice = (decision_form.value or saved.get("decision"))["choice"]
    decision_why = (decision_form.value or saved.get("decision"))["why"].strip()
    return decision_choice, decision_why


@app.cell(hide_code=True)
def _(decision_choice, mo):
    _notes = {
        "cloud": ("Defensible if the wifi were good, and here it is not. Three hundred cameras "
                  "sending video all day is a lot of bandwidth, and every dropped connection is "
                  "a door that stops working. It also drains the batteries fastest, because "
                  "sending data over a radio costs more energy than almost anything else the "
                  "camera does."),
        "edge": ("A reasonable middle. The building's own network is more dependable than the "
                 "internet connection, and one decent machine can serve all three hundred "
                 "doors. You still pay to send video from every camera, so the batteries still "
                 "suffer, and you now own a server that somebody has to look after."),
        "device": ("The usual answer for this shape of problem, and the batteries are the "
                   "reason. A camera that only wakes the radio when it has actually seen "
                   "something sends almost nothing. The cost is that the model has to be small "
                   "enough to fit on the camera, which as you saw is a hard limit and not a "
                   "preference."),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "There is no single right answer here, which is deliberate. All three are used in "
            "real buildings. What matters is whether you can say which limit pushed you, and "
            "what would have to be true for you to choose differently."
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
                placeholder="The thing that would stop me first is... because...",
                label="**Last one.** For the option you chose, which runs out first: memory, time, or battery? Say why.",
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
    mo.stop(
        not (reflect_form.value or saved.get("reflection")),
        mo.callout(mo.md("Answer the last question to finish."), kind="warn"),
    )
    takeaway_text = (reflect_form.value or saved.get("reflection"))["takeaway"].strip()
    done = True
    return done, takeaway_text


@app.cell(hide_code=True)
def _(
    bytes_each,
    decision_choice,
    decision_why,
    describe,
    done,
    mo,
    params_m,
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
        "cloud": "A data centre",
        "edge": "A server in the building",
        "device": "On each camera",
    }

    mo.vstack([
        mo.md("## Your Week 2 report"),
        mo.Html(
            f"""
            <div class="w2-report">
              <div class="row">
                <span class="k">Model you left it on</span>
                <span class="v">{params_m:g} million numbers at {bytes_each:g} bytes each, {describe}</span>
              </div>
              <div class="row">
                <span class="k">Where you would run it</span>
                <span class="v">{_where.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Why</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">What runs out first</span>
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
def _(done, lab_sync, locked, mo):
    _ = done
    submit_button = mo.ui.run_button(
        label="Submit my work",
        kind="success",
        disabled=lab_sync is None or locked,
        tooltip="Send your answers to your instructor",
    )
    mo.vstack([
        mo.md("## Submit your work"),
        mo.md(
            "Your answers have been saving as you went. When you are happy with them, "
            "press the button to hand the lab in. You can change answers and submit "
            "again until your instructor locks the lab."
        ),
        submit_button,
    ])
    return (submit_button,)


@app.cell(hide_code=True)
async def _(lab_status, lab_sync, locked, mo, reflect_form, saved, submit_button):
    # Runs when the button is pressed, and otherwise just says where things stand.
    if lab_sync is None:
        _msg, _kind = (
            "This copy of the lab is not connected to the course site, so it cannot be "
            "submitted from here.", "neutral")
    elif submit_button.value:
        _reply = await lab_sync.submit(
            reflection=reflect_form.value or saved.get("reflection"), finished=True)
        if _reply.get("ok"):
            _msg, _kind = ("**Submitted.** Your instructor can see your work.", "success")
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
def _(done, mo):
    _ = done
    mo.vstack([
        mo.md("### Check yourself"),
        mo.accordion({
            "Someone says a model is 'too big for the phone'. Too big for what, exactly?":
                mo.md(
                    "For the memory the phone is willing to give one app, which is a slice of "
                    "the total rather than all of it. A model stores four bytes for every "
                    "number in it, so a 25 million number model occupies about 100 MB before "
                    "it has done anything at all. The phone in this lab allowed 1.5 GB, which "
                    "sounds generous until you try to put a language model in it."
                ),
            "Why is a microcontroller expected to answer faster than a data centre?":
                mo.md(
                    "Because it is usually attached to something happening in the real world, "
                    "and it has nowhere to pass the work to. A doorbell, a motor, a hearing "
                    "aid. The data centre gets a longer budget precisely because a person is "
                    "waiting on a network connection, and a person will tolerate a few hundred "
                    "milliseconds."
                ),
            "You need to run a model somewhere it does not fit. What are your options?":
                mo.md(
                    "Make the model smaller, or move to a bigger machine. Those are genuinely "
                    "the only two, and most of the second half of this course is about the "
                    "first one, because the second is often not available to you. Making it "
                    "smaller has its own cost, which is usually accuracy, and deciding how much "
                    "of that to spend is an engineering judgement rather than a formula."
                ),
            "Why does sending data cost more battery than computing on the device?":
                mo.md(
                    "Radios are expensive. Pushing a signal out into the air takes far more "
                    "energy than moving numbers around inside a chip, and the further it has to "
                    "reach, the worse it gets. This is why the camera answer in Part 3 leans "
                    "towards doing the work on the device: not because the chip is good, but "
                    "because staying quiet is cheap."
                ),
        }),
    ])
    return


@app.cell(hide_code=True)
def _(
    batch,
    bytes_mb,
    decision_form,
    lab_sync,
    machine_gf,
    ops_gf,
    precision,
    q1,
    q2,
    q3,
    q4,
    q5,
    size,
):
    # Answers that are on the page from the start. A form's value is None until
    # it is submitted in this visit, so it is only recorded once it has one.
    if lab_sync is not None:
        lab_sync.record(q1=q1.value, q2=q2.value, q3=q3.value, q4=q4.value, q5=q5.value, size=size.value, precision=precision.value, bytes_mb=bytes_mb.value, ops_gf=ops_gf.value, machine_gf=machine_gf.value, batch=batch.value)
        if decision_form.value is not None:
            lab_sync.record(decision=decision_form.value)
    return

@app.cell(hide_code=True)
def _(lab_sync, reflect_form):
    # The last question only exists once the decision is in.
    if lab_sync is not None:
        if reflect_form.value is not None:
            lab_sync.record(reflection=reflect_form.value)
    return



if __name__ == "__main__":
    app.run()
