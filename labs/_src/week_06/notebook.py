import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 6 - Reading a Training Run")


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
          .w6-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w6-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w6-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w6-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w6-hero p.sub code { background: #fff3cc; border: 1px solid #f2dfaa; padding: 0 5px;
                                border-radius: 4px; font-size: .92rem; }
          .w6-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w6-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w6-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w6-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w6-split { grid-template-columns: 1fr; } }
          .w6-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w6-split > .body p:last-child { margin-bottom: 0; }
          .w6-split code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                           font-size: .88rem; }

          .w6-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w6-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w6-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w6-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w6-aside li:last-child { margin-bottom: 0; }
          .w6-aside li::marker { color: #6a5314; font-weight: 800; }
          .w6-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w6-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w6-aside .meta div:last-child { margin-bottom: 0; }
          .w6-aside .meta dt { color: #6f6f6f; }
          .w6-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w6-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w6-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w6-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }
          .w6-question code { font-style: normal; background: #f4f4f4; padding: 1px 5px;
                              border-radius: 4px; font-size: .88rem; }

          .w6-note { color: #6f6f6f; font-size: .85rem; margin: 2px 0 0; line-height: 1.5; }

          .w6-runs { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
                     margin: 16px 0; }
          @media (max-width: 900px) { .w6-runs { grid-template-columns: 1fr 1fr; } }
          @media (max-width: 520px) { .w6-runs { grid-template-columns: 1fr; } }
          .w6-run { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                    border-radius: 12px; background: #fff; padding: 13px 14px; }
          .w6-run h4 { margin: 0 0 9px; font-size: .95rem; color: #111; }
          .w6-run ul { margin: 0; padding-left: 17px; }
          .w6-run li { color: #3a3a3a; font-size: .85rem; line-height: 1.5;
                       margin-bottom: 5px; }
          .w6-run code { background: #fdecec; color: #c62828; padding: 1px 5px;
                         border-radius: 4px; font-size: .79rem; }

          .w6-stack { display: flex; flex-direction: column; gap: 7px; margin: 18px 0; }
          .w6-layer { display: grid; grid-template-columns: 160px 1fr; gap: 14px;
                      align-items: center; border: 1px solid #e6e6e6; border-radius: 10px;
                      background: #fff; padding: 11px 15px; }
          @media (max-width: 640px) { .w6-layer { grid-template-columns: 1fr; gap: 3px; } }
          .w6-layer .n { color: #6a5314; font-size: .78rem; font-weight: 800;
                         letter-spacing: .05em; text-transform: uppercase; }
          .w6-layer .d { color: #3a3a3a; font-size: .89rem; line-height: 1.5; }
          .w6-layer .d code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                              font-size: .84rem; }
          .w6-layer.top { border-left: 5px solid #f1b82d; }
          .w6-layer.bottom { border-left: 5px solid #9a9a9a; background: #fafafa; }

          .w6-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                     gap: 12px; margin: 14px 0; }
          .w6-stat { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff;
                     padding: 11px 13px; }
          .w6-stat .k { color: #6a5314; font-size: .72rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .w6-stat .v { display: block; color: #111; font-size: 1.45rem; font-weight: 800;
                        line-height: 1.2; margin-top: 2px; }
          .w6-stat .why { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 3px;
                          line-height: 1.4; }
          .w6-stat.green .v { color: #2e7d32; }
          .w6-stat.red .v { color: #c62828; }

          .w6-budget { display: flex; height: 44px; border-radius: 8px; overflow: hidden;
                       border: 1px solid #e6e6e6; margin: 14px 0 6px; background: #f6f6f6; }
          .w6-budget span { display: flex; align-items: center; justify-content: center;
                            color: #fff; font-size: .74rem; font-weight: 800;
                            overflow: hidden; white-space: nowrap; }
          .w6-budget .p { background: #4a6fa5; }
          .w6-budget .g { background: #7cb47f; }
          .w6-budget .o { background: #f1b82d; color: #4a3708; }
          .w6-budget .a { background: #c87f5a; }
          .w6-budget .w { background: #9a9a9a; }
          .w6-key { display: flex; flex-wrap: wrap; gap: 14px; margin: 0 0 12px; }
          .w6-key span { color: #4a4a4a; font-size: .8rem; display: flex;
                         align-items: center; gap: 6px; }
          .w6-key i { width: 11px; height: 11px; border-radius: 3px; display: inline-block; }

          .w6-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w6-bar { display: grid; grid-template-columns: 200px 1fr 130px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w6-bar { grid-template-columns: 110px 1fr 90px; } }
          .w6-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w6-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 26px; overflow: hidden; }
          .w6-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w6-bar.good .fill { background: #7cb47f; }
          .w6-bar.bad .fill { background: #d98080; }
          .w6-bar.gold .fill { background: #f1b82d; }
          .w6-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }

          table.w6-table { border-collapse: collapse; margin: 14px 0; font-size: .92rem;
                           width: 100%; }
          table.w6-table th, table.w6-table td { border: 1px solid #e6e6e6;
                                                 padding: 9px 13px; text-align: left;
                                                 vertical-align: top; }
          table.w6-table th { background: #fffdf5; color: #6a5314; font-size: .76rem;
                              text-transform: uppercase; letter-spacing: .04em; }
          table.w6-table code { background: #f4f4f4; padding: 1px 5px; border-radius: 4px;
                                font-size: .85rem; }

          .w6-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w6-report .row { display: grid; grid-template-columns: 200px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w6-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w6-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w6-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w6-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w6-report .tick { color: #2e7d32; font-weight: 800; }
          .w6-report .cross { color: #c62828; font-weight: 800; }
          .w6-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                              color: #333; font-style: italic; }
          .w6-score { display: inline-block; background: #fff3cc; border: 1px solid #f2dfaa;
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
        <div class="w6-hero">
          <p class="w6-eyebrow">CSC/EE 8001 &middot; Week 6</p>
          <h1>Reading a Training Run</h1>
          <p class="sub">Twenty-four gigabytes of GPU. Seven gigabytes of weights. The
          forward pass completes, then the run dies with <code>CUDA out of memory</code>
          inside <code>loss.backward()</code>. Nothing in that error says where the other
          seventeen gigabytes went. By the end of this lab you can work it out, and design
          the experiment that proves it.</p>
          <div class="w6-chips">
            <span class="w6-chip">The training stack</span>
            <span class="w6-chip">FLOPs and bytes</span>
            <span class="w6-chip">Memory budget</span>
            <span class="w6-chip-plain w6-chip">Checks are marked</span>
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
        <div class="w6-split">
          <div class="body">
            <p>Notice how little that error told you. The allocator reported that a request
            for some number of bytes could not be satisfied. That is a fact about the last
            millisecond of the run, not about the cause, and 7 GB of weights cannot explain a
            24 GB failure on its own.</p>
            <p>Most training problems are shaped like this. A run that does not crash, keeps
            the GPU warm and brings the loss down is not evidence of much: the same
            description fits a run using an eighth of the card you are renting, a run two
            hundred tokens of sequence length from falling over, a run whose gradients are
            about to overflow FP16, and a run that is learning nothing at all.</p>
            <p>None of them announce themselves. They arrive as a vague complaint three weeks
            later. It is slow, or it ran out of memory, or the eval numbers are rubbish.</p>
            <p>So the work is getting from a complaint to a number you can measure, and
            knowing which number. <code>nvidia-smi</code> and
            <code>torch.cuda.max_memory_allocated()</code> will answer most of what is in
            this lab, but only if you know what to ask them.</p>
          </div>
          <aside class="w6-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Classify four symptoms into resource, throughput, numerical and
              correctness failures.</li>
              <li>Use the execution stack to turn a symptom into a hypothesis about one
              layer.</li>
              <li>Count MACs and FLOPs for a layer, and say why that does not predict its
              runtime.</li>
              <li>Account for training memory in five terms and say which one dominates.</li>
              <li>Design an OOM experiment whose outcome rules something out either way.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 45 min</dd></div>
              <div><dt>Before this</dt><dd>Weeks 1 to 5</dd></div>
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
        <div class="w6-question">
          <span class="lbl">The question this lab answers</span>
          <p>"Training is slow and it keeps running out of memory. What do I measure
          first?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: Four runs, four different problems""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Run A below is the one from the first page. Three others sit beside it, and all four
    start, allocate memory, use the GPU and produce numbers. If your only check is "did it
    start", all four pass.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w6-runs">
          <div class="w6-run">
            <h4>Run A</h4>
            <ul>
              <li>Starts normally</li>
              <li>Memory climbs through the first step</li>
              <li><code>CUDA out of memory</code></li>
              <li>Dies inside <code>loss.backward()</code></li>
            </ul>
          </div>
          <div class="w6-run">
            <h4>Run B</h4>
            <ul>
              <li><code>nvidia-smi</code> shows 25% utilisation</li>
              <li>Memory at 60%</li>
              <li>Completes successfully</li>
              <li>Takes four times the estimate</li>
            </ul>
          </div>
          <div class="w6-run">
            <h4>Run C</h4>
            <ul>
              <li>Loss falls for ~2,000 steps</li>
              <li>Then becomes <code>nan</code></li>
              <li>Every later step is <code>nan</code></li>
            </ul>
          </div>
          <div class="w6-run">
            <h4>Run D</h4>
            <ul>
              <li>Utilisation steady at 90%</li>
              <li>Loss flat from step 50</li>
              <li>Accuracy at chance</li>
            </ul>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("Sort them. One answer each.")
    return


@app.cell(hide_code=True)
def _(ask):
    RUN_KINDS = {
        "Resource: it needs more memory than the device has": "mem",
        "Throughput: the hardware is idle waiting for work": "speed",
        "Numerical: the arithmetic has left the range of the format": "num",
        "Correctness: it is executing perfectly and not learning": "learn",
    }
    r1, r1_render, r1_sum = ask(
        "**Run A.** Memory climbs, then `CUDA out of memory` inside `loss.backward()`.",
        RUN_KINDS, "mem",
        "A resource failure, and the location is the useful part. Forward completed, so "
        "everything forward needed fitted. Whatever broke is tied to backward: the "
        "activations forward saved for the gradient computation, and backward's own "
        "workspace. We come back to this run at the end of the lab.",
        key="r1",
    )
    r1
    return RUN_KINDS, r1, r1_render, r1_sum


@app.cell(hide_code=True)
def _(r1, r1_render):
    r1_render(r1.value)
    return


@app.cell(hide_code=True)
def _(RUN_KINDS, ask):
    r2, r2_render, r2_sum = ask(
        "**Run B.** 25 per cent utilisation, 60 per cent memory, four times slower than "
        "estimated.",
        RUN_KINDS, "speed",
        "A throughput problem, and 25 per cent utilisation is the whole story: the GPU is not "
        "struggling, it is waiting. The usual culprits are the input pipeline (too few "
        "dataloader workers, decoding on the main process, reading many small files), "
        "synchronous host-device copies, or a model decomposed into so many small kernels "
        "that launch overhead dominates the arithmetic.\n\nOne caveat worth carrying: "
        "`nvidia-smi` utilisation means 'at least one kernel was resident', not 'the "
        "arithmetic units were busy'. A run doing nothing but tiny elementwise kernels can "
        "read 100 per cent.",
        key="r2",
    )
    r2
    return r2, r2_render, r2_sum


@app.cell(hide_code=True)
def _(r2, r2_render):
    r2_render(r2.value)
    return


@app.cell(hide_code=True)
def _(RUN_KINDS, ask):
    r3, r3_render, r3_sum = ask(
        "**Run C.** Loss falls for 2,000 steps, then goes to `nan` and never recovers.",
        RUN_KINDS, "num",
        "A numerical failure. Something overflowed or divided by zero, and once a `nan` "
        "exists it propagates through every operation that touches it, including into the "
        "weights at the next optimiser step, which is why there is no recovery.\n\nIn "
        "FP16 the usual cause is that the exponent range runs out: max finite value around "
        "65,504, and gradients underflow to zero well before that at the other end. Loss "
        "scaling exists for exactly this. BF16 trades mantissa bits for FP32's exponent "
        "range and largely removes the problem. Gradient clipping bounds the other end.",
        key="r3",
    )
    r3
    return r3, r3_render, r3_sum


@app.cell(hide_code=True)
def _(r3, r3_render):
    r3_render(r3.value)
    return


@app.cell(hide_code=True)
def _(RUN_KINDS, ask):
    r4, r4_render, r4_sum = ask(
        "**Run D.** 90 per cent utilisation, loss flat from step 50, accuracy at chance.",
        RUN_KINDS, "learn",
        "A correctness failure, and the hardest of the four to be told about, because every "
        "infrastructure dashboard says this run is healthy. The GPU is fully occupied doing "
        "arithmetic that does not reduce the loss.\n\nThe shortlist is short and worth "
        "memorising: labels misaligned with inputs by a shuffle or an off-by-one; learning "
        "rate orders of magnitude wrong; parameters never passed to the optimiser or left "
        "with `requires_grad=False`; `model.eval()` never switched back so dropout and "
        "batchnorm behave wrongly; loss computed on a detached tensor. All of them execute "
        "perfectly.",
        key="r4",
    )
    r4
    return r4, r4_render, r4_sum


@app.cell(hide_code=True)
def _(r4, r4_render):
    r4_render(r4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 2: The execution stack""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    You write a model. The GPU does not run a model. Five layers sit between the two, and
    every training problem lives in one of them.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w6-stack">
          <div class="w6-layer top">
            <span class="n">Model</span>
            <span class="d">What you wrote. Layer types, dimensions, optimiser, loss.</span>
          </div>
          <div class="w6-layer">
            <span class="n">Operations</span>
            <span class="d">What that becomes once autograd has traced it: matrix multiplies,
            softmaxes, layer norms, elementwise ops, in a specific order, each with a
            backward counterpart.</span>
          </div>
          <div class="w6-layer">
            <span class="n">Tensors</span>
            <span class="d">The buffers those operations read and write. Three properties
            matter: shape, dtype, and which device they live on.</span>
          </div>
          <div class="w6-layer">
            <span class="n">Kernels</span>
            <span class="d">The GPU code that implements each operation: a cuBLAS GEMM,
            a fused attention kernel, a hand-written elementwise loop. Performance varies by
            an order of magnitude between implementations of the same operation.</span>
          </div>
          <div class="w6-layer bottom">
            <span class="n">Hardware</span>
            <span class="d">Finite memory, finite bandwidth, finite arithmetic throughput,
            and it can only work on data that has already arrived.</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The reason to draw it is that errors surface at the bottom and originate anywhere.

    `CUDA out of memory` is raised by the allocator, so it feels like a hardware fact. All it
    actually says is that a request for N bytes could not be satisfied. Why the request was
    that size is a question about the model (parameter count), the operations (an attention
    matrix of size $B \times H \times S \times S$), or the tensors (keeping activations alive
    for backward). The allocator is the messenger.

    "Training is slow" is the same shape. It is a complaint, not a diagnosis. The diagnostic
    question is *where is the time going*, and the first fork is whether the GPU is busy. If
    it is idle, look upward at what is failing to feed it. If it is busy, ask whether the work
    is arithmetic you need or overhead you could remove.

    Today covers the first three layers: what are we computing, how much arithmetic is that,
    and what has to be stored.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    c1, c1_render, c1_sum = ask(
        "A colleague says \"training is slow\". What have they given you?",
        {
            "A hardware problem; the GPU is too small for this model": "a",
            "A symptom consistent with several layers of the stack, which the next measurement has to narrow down": "b",
            "A batch size problem": "c",
        },
        "b",
        "Slow is what was observed. The candidates are: the model needs far more arithmetic "
        "than anyone estimated; it decomposes into kernels too small to amortise launch "
        "overhead; it moves large tensors through memory for little arithmetic; the kernels "
        "chosen are poor; or the GPU is idle waiting on the input pipeline. Five different "
        "pieces of work. The first measurement that separates them is simply whether the GPU "
        "is busy.",
        key="c1",
    )
    c1
    return c1, c1_render, c1_sum


@app.cell(hide_code=True)
def _(c1, c1_render):
    c1_render(c1.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: What a linear layer costs""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    A linear layer computes $y = \sigma(Wx + b)$. Treat it as a workload rather than an
    equation: how much arithmetic does it generate, and how much data does it need?

    With $n$ inputs and $m$ outputs, $W$ is $m \times n$. One output unit is a dot product of
    length $n$: $n$ multiplications and $n$ additions. A multiply-and-add together is counted
    as one **MAC**. So:

    - one unit: $n$ MACs
    - the layer: $m \times n$ MACs
    - the layer on a batch of $B$: $B \times m \times n$ MACs

    FLOPs are conventionally about twice the MAC count, since the multiply and the add are
    counted separately. Conventions differ and it does not matter; what matters is how the
    number scales with the dimensions.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, saved):
    n_in = mo.ui.slider(
        256, 8192, value=saved.get("n_in", 4096), step=256, disabled=locked,
        label="Inputs (n)", show_value=True,
    )
    m_out = mo.ui.slider(
        256, 8192, value=saved.get("m_out", 4096), step=256, disabled=locked,
        label="Outputs (m)", show_value=True,
    )
    b_size = mo.ui.slider(
        1, 256, value=saved.get("b_size", 32), step=1, disabled=locked,
        label="Batch (B)", show_value=True,
    )
    mo.vstack([n_in, m_out, b_size])
    return b_size, m_out, n_in


@app.cell(hide_code=True)
def _(b_size, m_out, n_in):
    macs = b_size.value * m_out.value * n_in.value
    flops = 2 * macs
    weights = m_out.value * n_in.value + m_out.value      # one bias per output
    weight_mb_32 = weights * 4 / 1e6
    weight_mb_16 = weights * 2 / 1e6
    return flops, macs, weight_mb_16, weight_mb_32, weights


@app.cell(hide_code=True)
def _(LAB_CSS, flops, macs, mo, weight_mb_16, weight_mb_32, weights):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w6-grid">
          <div class="w6-stat">
            <span class="k">MACs</span>
            <span class="v">{macs / 1e6:,.0f}M</span>
            <span class="why">B &times; m &times; n, forward only</span>
          </div>
          <div class="w6-stat">
            <span class="k">FLOPs</span>
            <span class="v">{flops / 1e9:,.2f}G</span>
            <span class="why">twice the MACs by the usual convention</span>
          </div>
          <div class="w6-stat">
            <span class="k">Parameters</span>
            <span class="v">{weights / 1e6:,.1f}M</span>
            <span class="why">m &times; n weights plus m biases</span>
          </div>
          <div class="w6-stat">
            <span class="k">Weights in memory</span>
            <span class="v">{weight_mb_32:,.0f} MB</span>
            <span class="why">FP32; {weight_mb_16:,.0f} MB at 2 bytes</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(b_size, flops, mo, weight_mb_32, weights):
    mo.callout(
        mo.md(
            f"One line of Python, one `torch.nn.Linear`, and underneath it "
            f"**{flops / 1e9:,.2f} billion** floating-point operations and "
            f"**{weights / 1e6:,.1f} million** parameters occupying **{weight_mb_32:,.0f} MB** "
            "before training has stored anything of its own.\n\n"
            f"The batch slider is at **{b_size.value}**. Raising it scales the arithmetic "
            "linearly, and it scales the intermediate tensors that have to stay resident "
            "linearly too. The second effect is the one that causes out-of-memory errors, and "
            "it is Part 5."
        ),
        kind="info",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Why the FLOP count does not predict the runtime

    A modern data-centre GPU does tens of teraFLOPs per second. A billion FLOPs is therefore
    a fraction of a millisecond of arithmetic, provided the arithmetic units never
    have to wait.

    They usually wait. Every operation has to read its inputs from memory and write its output
    back, and memory bandwidth is finite. The ratio that decides which limit binds is
    **arithmetic intensity**: FLOPs performed per byte moved.

    Compare two operations on the same tensors:

    - A **matrix multiply** of two $4096 \times 4096$ matrices reads about 134 MB and performs
      about 137 GFLOPs. Roughly 1,000 FLOPs per byte. There is plenty of arithmetic to hide
      the memory traffic behind, so this is **compute-bound** and will approach the hardware's
      peak throughput.
    - A **GELU** applied elementwise to one of those matrices reads 67 MB, writes 67 MB and
      performs a handful of operations per element. Under 1 FLOP per byte. The arithmetic
      units are idle almost the whole time waiting on memory, so this is **memory-bound** and
      its runtime is set entirely by bandwidth.

    This is why kernel fusion matters so much in practice: three memory-bound elementwise
    operations in a row read and write the same tensor three times, and fusing them into one
    kernel does the same arithmetic with a third of the traffic. It is also why
    FlashAttention is faster without reducing the FLOP count at all, because it avoids
    materialising the $S \times S$ attention matrix in high-bandwidth memory.

    Plotting achieved FLOPs against arithmetic intensity gives you the **roofline** model: a
    sloped region where bandwidth limits you and a flat region where arithmetic does.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    c2, c2_render, c2_sum = ask(
        "Two operations each perform about a billion FLOPs. One takes 3 ms, the other 40 ms. "
        "Most likely explanation?",
        {
            "One of the FLOP counts is wrong": "a",
            "The slow one has much lower arithmetic intensity, so it is bandwidth-bound and spends its time waiting on memory": "b",
            "The fast one ran on a better GPU": "c",
        },
        "b",
        "Arithmetic is cheap on a GPU; feeding it is not. An operation doing few FLOPs per "
        "byte read spends most of its time on memory traffic, with the arithmetic units idle "
        "in the middle of a run that looks fully utilised. Elementwise operations, "
        "normalisations and small matrix multiplies all land here, which is why fusing them "
        "is usually the biggest single speedup available.",
        key="c2",
    )
    c2
    return c2, c2_render, c2_sum


@app.cell(hide_code=True)
def _(c2, c2_render):
    c2_render(c2.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: Why training needs more memory than inference""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    A model that runs happily at inference can need many times the memory to train, and the
    reason is backward.

    At inference, an intermediate tensor can be freed the moment the next operation has
    consumed it. Nothing will ask for it again, which is what `torch.no_grad()` tells the
    framework it is allowed to assume.

    During training it will be asked for again. The gradient of a matrix multiply with respect
    to $W$ is $\frac{\partial L}{\partial y} x^\top$, which needs $x$, the input from the
    forward pass. So autograd keeps $x$ alive from the moment forward produces it until backward
    reaches that node, which is most of the step.

    The tensors are not larger. They live longer, and peak memory is what the allocator cares
    about.

    This is why you can hit an out-of-memory error without touching the model. Raise the batch
    size or the sequence length and every saved activation grows with it.

    **Activation checkpointing** is the direct trade against this: discard most saved
    activations and recompute them during backward from a few retained checkpoints. Memory
    drops substantially, at a cost of roughly 30 per cent extra compute. Time for space, as an
    explicit choice.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    c3, c3_render, c3_sum = ask(
        "Why does training need far more memory than inference on the same model?",
        {
            "Training uses a wider numeric format": "a",
            "Backward needs values produced during forward, so they stay alive instead of being freed after use": "b",
            "Training loads the dataset into GPU memory": "c",
        },
        "b",
        "At inference an intermediate can be freed as soon as it is consumed. In training, "
        "autograd needs forward values to compute gradients, so they stay resident until "
        "backward reaches them. Same tensors, much longer lifetimes, much higher peak. "
        "Activation checkpointing trades that memory back for recomputation.",
        key="c3",
    )
    c3
    return c3, c3_render, c3_sum


@app.cell(hide_code=True)
def _(c3, c3_render):
    c3_render(c3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: The five-term memory budget""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    "The model is 8 GB and the GPU has 24 GB, so why did it run out of memory?" Because the
    weights are one of five claims on that 24 GB:

    > parameters + gradients + optimiser state + saved activations + workspace

    Which term dominates is not fixed. In a small model trained on long sequences the
    activations are most of it; in a large model on short sequences the optimiser state is.
    And it is the **peak** that matters, not the average, because the allocator fails at the
    worst instant.

    Build one. Hidden size and depth set the parameter count; batch and sequence length do
    not change the model at all.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    # The model's shape. Parameter count follows from it rather than being set
    # separately, so the thing being budgeted is always a model that could exist.
    hidden = mo.ui.slider(
        1024, 8192, value=saved.get("hidden", 2048), step=1024, disabled=locked,
        label="Hidden size (H)", show_value=True,
    )
    layers = mo.ui.slider(
        4, 64, value=saved.get("layers", 16), step=4, disabled=locked,
        label="Layers", show_value=True,
    )
    _precisions = {"FP32, 4 bytes": 4, "FP16 or BF16, 2 bytes": 2}
    precision = mo.ui.radio(
        options=_precisions,
        value=pick(_precisions, saved.get("precision")) or "FP32, 4 bytes",
        disabled=locked, label="Parameter and activation dtype",
    )
    _opts = {
        "SGD, no state": 0,
        "SGD with momentum, 1 extra per parameter": 1,
        "Adam, 2 extra per parameter": 2,
    }
    optimiser = mo.ui.radio(
        options=_opts,
        value=pick(_opts, saved.get("optimiser")) or "Adam, 2 extra per parameter",
        disabled=locked, label="Optimiser",
    )
    mo.vstack([hidden, layers, precision, optimiser])
    return hidden, layers, optimiser, precision


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    # How you run it. None of these change the model by a single parameter.
    batch = mo.ui.slider(
        1, 32, value=saved.get("batch", 4), step=1, disabled=locked,
        label="Batch (B)", show_value=True,
    )
    seq_len = mo.ui.slider(
        512, 8192, value=saved.get("seq_len", 1024), step=512, disabled=locked,
        label="Sequence length (S)", show_value=True,
    )
    _gpus = {"16 GB": 16, "24 GB": 24, "40 GB": 40, "80 GB": 80}
    gpu_gb = mo.ui.radio(
        options=_gpus, value=pick(_gpus, saved.get("gpu_gb")) or "24 GB",
        disabled=locked, label="Device memory",
    )
    mo.vstack([batch, seq_len, gpu_gb])
    return batch, gpu_gb, seq_len


@app.cell(hide_code=True)
def _(batch, gpu_gb, hidden, layers, optimiser, precision, seq_len):
    # First-order estimates. Good enough to show which term dominates, which is the
    # only thing they are for. The accordion below lists what they leave out.
    GB = 1e9                 # decimal GB, so the sums match the lecture's arithmetic
    PER_LAYER = 12           # a transformer block is roughly 12 x H x H parameters
    SAVED_PER_LAYER = 4      # rough count of tensors each block keeps for backward
    WORKSPACE_GB = 1.0       # flat allowance for temporary buffers and fragmentation

    params = PER_LAYER * hidden.value * hidden.value * layers.value
    param_gb = params * precision.value / GB
    grad_gb = params * precision.value / GB
    # Optimiser state is normally kept in FP32 even in a mixed-precision run, which is
    # why moving the dtype to 2 bytes does not halve this term.
    opt_gb = params * 4 * optimiser.value / GB
    act_gb = (batch.value * seq_len.value * hidden.value * layers.value
              * SAVED_PER_LAYER * precision.value) / GB
    work_gb = WORKSPACE_GB

    total_gb = param_gb + grad_gb + opt_gb + act_gb + work_gb
    budget_gb = float(gpu_gb.value)
    fits = total_gb <= budget_gb
    headroom = budget_gb - total_gb
    return (
        act_gb,
        budget_gb,
        fits,
        grad_gb,
        headroom,
        opt_gb,
        param_gb,
        params,
        total_gb,
        work_gb,
    )


@app.cell(hide_code=True)
def _(LAB_CSS, mo, params):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w6-grid">
          <div class="w6-stat">
            <span class="k">A model that shape has</span>
            <span class="v">{params / 1e9:,.2f}B</span>
            <span class="why">parameters, at roughly 12 &times; H &times; H per block</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, act_gb, grad_gb, mo, opt_gb, param_gb, total_gb, work_gb):
    _ = LAB_CSS
    _parts = [("p", "parameters", param_gb), ("g", "gradients", grad_gb),
              ("o", "optimiser state", opt_gb), ("a", "activations", act_gb),
              ("w", "workspace", work_gb)]
    _segs = ""
    for _cls, _name, _v in _parts:
        _pct = _v / total_gb * 100 if total_gb else 0
        _label = f"{_pct:.0f}%" if _pct >= 7 else ""
        _segs += f'<span class="{_cls}" style="width:{_pct:.2f}%">{_label}</span>'
    _key = "".join(
        f'<span><i style="background:{_c}"></i>{_n} &middot; {_v:.1f} GB</span>'
        for (_cls, _n, _v), _c in zip(
            _parts, ["#4a6fa5", "#7cb47f", "#f1b82d", "#c87f5a", "#9a9a9a"])
    )
    mo.Html(f'<div class="w6-budget">{_segs}</div><div class="w6-key">{_key}</div>')
    return


@app.cell(hide_code=True)
def _(LAB_CSS, budget_gb, fits, headroom, mo, total_gb):
    _ = LAB_CSS
    _pct = min(100.0, total_gb / budget_gb * 100) if budget_gb else 0
    mo.Html(
        f"""
        <div class="w6-bars">
          <div class="w6-bar {'good' if fits else 'bad'}">
            <span class="t">Peak memory required</span>
            <span class="track"><span class="fill" style="width:{_pct:.1f}%"></span></span>
            <span class="n">{total_gb:.1f} GB</span>
          </div>
        </div>
        <p class="w6-note">The bar fills at {budget_gb:.0f} GB.
        {format(headroom, '.1f') + ' GB spare.'
         if fits else 'Over by ' + format(-headroom, '.1f') + ' GB.'}</p>
        """
    )
    return


@app.cell(hide_code=True)
def _(act_gb, fits, headroom, mo, opt_gb, param_gb, total_gb):
    _biggest = max([("the parameters", param_gb),
                    ("the optimiser state", opt_gb),
                    ("the saved activations", act_gb)], key=lambda p: p[1])
    if not fits:
        _msg = (
            f"Over budget by {-headroom:.1f} GB. Before changing anything, read which term is "
            f"responsible: the largest single consumer is **{_biggest[0]}** at "
            f"{_biggest[1]:.1f} GB of {total_gb:.1f} GB.\n\n"
            "That determines the fix. Activations dominating means batch size, sequence "
            "length and checkpointing are your levers and the model can stay as it is. "
            "Optimiser state dominating means a different optimiser or sharding buys more "
            "than any amount of batch-size tuning."
        )
        _kind = "danger"
    else:
        _msg = (
            f"Fits, with {headroom:.1f} GB spare of {total_gb:.1f} GB used. Largest single "
            f"consumer: **{_biggest[0]}** at {_biggest[1]:.1f} GB.\n\n"
            "Two things worth trying. Double the sequence length twice and watch where it "
            "breaks, with the model untouched. Then switch the dtype to 2 bytes and notice "
            "that the optimiser term does not move."
        )
        _kind = "success"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "The five terms in detail, and what this estimate leaves out": mo.md(
            r"""
**Parameters.** One value each, in whatever dtype you chose. Fixed once the architecture is.

**Gradients.** One per trainable parameter, normally the same dtype. Assume it doubles the
parameter cost unless you are freezing most of the model or using LoRA, where only the
adapter parameters get gradients.

**Optimiser state.** The term people forget, and often the largest. SGD keeps nothing;
momentum keeps one buffer; Adam keeps two (the first and second moment estimates, `exp_avg`
and `exp_avg_sq`). These are normally kept in FP32 regardless of your training dtype, which
is why switching to BF16 does not halve this term.

The commonly quoted figure follows from this: for FP32 Adam, 4 bytes of weight + 4 of
gradient + 8 of optimiser state = 16 bytes per parameter. A billion parameters is about 16 GB
before a single activation exists. Mixed precision does not reduce it as much as people
expect, because it adds an FP32 master copy of the weights.

**Activations.** The only term determined by how you run the model rather than what it is.
For one tensor it is just elements × bytes. Sequence length bites hardest, and in attention
it can bite quadratically: a naive implementation materialises a $B \times \text{heads} \times
S \times S$ matrix, which at S = 8192 is enormous. FlashAttention avoids materialising it,
which is why the quadratic term often does not appear in practice any more.

**Workspace.** Temporary buffers that kernels need, plus fragmentation. Worth knowing that
`torch.cuda.memory_allocated()` and `memory_reserved()` differ: the caching allocator holds
onto freed blocks, so you can get an OOM with gigabytes "free" if nothing is a contiguous
block of the right size.

**What this calculator leaves out.** Mixed precision's FP32 master weights. ZeRO and FSDP
sharding, which split optimiser state, gradients and parameters across devices. Activation
checkpointing. Gradient accumulation, which gives you a large effective batch at the
activation cost of a small one. Every one of those changes the sums.

Do not memorise sixteen bytes per parameter. Memorise **which five things to count**, then go
and measure the real ones.
            """
        ),
    })
    return


@app.cell(hide_code=True)
def _(ask):
    c4, c4_render, c4_sum = ask(
        "A run has been stable for weeks. You change nothing in the model, double the sequence "
        "length, and it now runs out of memory. Which term grew?",
        {
            "Parameters, because longer sequences need a larger model": "a",
            "Saved activations, because every intermediate tensor scales with sequence length": "b",
            "Optimiser state, because there is more to optimise": "c",
        },
        "b",
        "Parameters, gradients and optimiser state are all determined by the architecture, and "
        "the architecture did not change. Activations scale with batch × sequence length × "
        "hidden size × layers, so doubling S at least doubles that term, and more than "
        "doubles it if attention materialises an S × S matrix. This is why an out-of-memory error can appear from a "
        "config change that touches no model code.",
        key="c4",
    )
    c4
    return c4, c4_render, c4_sum


@app.cell(hide_code=True)
def _(c4, c4_render):
    c4_render(c4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 6: Run A, properly""")
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w6-question">
          <span class="lbl">The run from the first page, in full</span>
          <p>"24 GB device. Weights occupy 7 GB. The forward pass completes every time. The
          run dies with <code>CUDA out of memory</code> inside <code>loss.backward()</code>,
          at the same point every time, on the first iteration."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    You now have the five terms, so the two facts in that description can do their work.

    **Seven GB cannot explain a 24 GB failure.** Something consumed the other seventeen, and
    it was not the weights.

    **Forward completed.** Everything forward needed fitted. The failure is specific to
    backward, which points at the two terms that exist only because you are training: the
    activations forward saved, and backward's own workspace.

    That is a hypothesis. Now choose an experiment, and commit in advance to what each outcome
    would mean.
    """
    )
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "Halve the batch size and rerun": "batch",
        "Switch Adam for SGD to free the optimiser state": "optim",
        "Move to a larger device": "gpu",
        "Reduce the model size until it fits": "model",
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
                label="**Your first experiment?**",
            ),
            why=mo.ui.text_area(
                value=_saved.get("why", ""),
                disabled=locked,
                placeholder="What you expect, and what you would conclude if it worked and if it did not.",
                label="**Why that one, and what does each outcome rule out?** Not marked; change it as often as you like.",
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
        "batch": (
            "The cheapest experiment that separates the hypotheses, and it matches the "
            "evidence. Activation memory scales with batch size; parameters, gradients and "
            "optimiser state do not. So the result is informative either way.\n\n"
            "If halving fixes it, the dominant term scales with batch size, which is "
            "overwhelmingly saved activations, and you now have a real choice between "
            "gradient accumulation and activation checkpointing. If it barely moves, you have "
            "learned something equally useful: it is not activations, so look at optimiser "
            "state and backward workspace instead."
        ),
        "optim": (
            "It will free real memory, but look at the timing again. Optimiser state for Adam "
            "is lazily allocated at the first `step()`, which this run never reaches. So it "
            "may well get the run going without telling you why, and you will not know whether "
            "you fixed the cause or just bought headroom.\n\n"
            "There is a cost too: changing optimiser changes how the model trains, not only "
            "how much memory it needs. If you want the memory without the training change, "
            "8-bit Adam or sharding the optimiser state are better trades."
        ),
        "gpu": (
            "It will probably work, and occasionally it is the right call: some runs are "
            "simply too large for the hardware and the cheapest fix is hardware. But you will "
            "have spent money without learning which term was responsible, and the next person "
            "to raise the sequence length will be in exactly this position on the larger "
            "device. Price it after the diagnosis, not instead of one."
        ),
        "model": (
            "This treats the 7 GB of weights as the cause of a 24 GB failure, and the "
            "arithmetic says otherwise: seventeen GB went somewhere else. Shrinking the model "
            "reduces parameters, gradients and optimiser state together, so it may well work, "
            "but it is the most expensive way to find out and it costs you model quality to "
            "fix something the model was not responsible for."
        ),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "The shape of the question matters more than the answer: **a good experiment is "
            "one where you can state beforehand what each outcome rules out.** Changing three "
            "things at once until the error stops does stop the error, and teaches you "
            "nothing."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### One detail in the brief that changes everything

    It fails **on the first iteration**. If instead memory had crept up every iteration, that
    is a different problem with a much more specific cause: something is being retained that
    should have been released.

    The classic version is accumulating the loss for logging without detaching it:
    `total += loss` instead of `total += loss.item()`. The tensor keeps a reference to its
    whole computation graph, so every step's graph stays alive and memory grows linearly with
    step count. Others: caching hidden states across steps without `detach()`, appending
    predictions to a list for later evaluation, holding a reference to a batch after the step.

    A run that fails at a fixed point is a budget that is too small. A run that fails later
    each time is a leak. They need different work.

    ### Then measure rather than guess

    Before reaching for a fix:

    | What to ask | How |
    | - | - |
    | What was the peak, and when? | `torch.cuda.max_memory_allocated()`, reset per phase with `reset_peak_memory_stats()` |
    | Allocated versus reserved? | `torch.cuda.memory_summary()`, where a large gap means fragmentation rather than demand |
    | Which tensors and what shapes? | `torch.cuda.memory._record_memory_history()`, then the PyTorch memory visualiser |
    | Where is the time going? | `torch.profiler` with `record_shapes=True` |

    Then put those numbers against the five terms and see which one you mis-estimated.
    That move, from vague runtime symptom to measurable resource question, is the whole lab.
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
                placeholder="I would measure ... and a reading of ... would point me at ...",
                label="**Last one.** Take Run B, at 25 per cent utilisation. Name one thing you would measure, and say what reading would point you at a specific layer of the stack.",
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
    b_size,
    batch,
    c1,
    c2,
    c3,
    c4,
    decision_form,
    gpu_gb,
    hidden,
    lab_sync,
    layers,
    m_out,
    n_in,
    optimiser,
    precision,
    r1,
    r2,
    r3,
    r4,
    seq_len,
):
    # Marked answers go through record_once, so the first answer is the one that
    # counts. Sliders and the written decision can change freely.
    if lab_sync is not None:
        lab_sync.record_once(
            r1=r1.value, r2=r2.value, r3=r3.value, r4=r4.value,
            c1=c1.value, c2=c2.value, c3=c3.value, c4=c4.value,
        )
        lab_sync.record(
            n_in=n_in.value, m_out=m_out.value, b_size=b_size.value,
            precision=precision.value, optimiser=optimiser.value,
            batch=batch.value, seq_len=seq_len.value,
            hidden=hidden.value, layers=layers.value, gpu_gb=gpu_gb.value,
        )
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
    c1,
    c1_sum,
    c2,
    c2_sum,
    c3,
    c3_sum,
    c4,
    c4_sum,
    r1,
    r1_sum,
    r2,
    r2_sum,
    r3,
    r3_sum,
    r4,
    r4_sum,
):
    # One place that knows every marked answer, so the report, the score and the
    # dashboard cannot disagree.
    CHECKS = [
        ("Run A: out of memory in backward", r1_sum(r1.value)),
        ("Run B: 25 per cent utilisation", r2_sum(r2.value)),
        ("Run C: loss goes to nan", r3_sum(r3.value)),
        ("Run D: busy and not learning", r4_sum(r4.value)),
        ("\"Training is slow\"", c1_sum(c1.value)),
        ("Same FLOPs, different runtime", c2_sum(c2.value)),
        ("Training vs inference memory", c3_sum(c3.value)),
        ("Longer sequences: which term", c4_sum(c4.value)),
    ]
    checks_right = sum(1 for _n, (_t, _ok) in CHECKS if _ok)
    checks_score = f"{checks_right}/{len(CHECKS)}"
    return CHECKS, checks_right, checks_score


@app.cell(hide_code=True)
def _(
    CHECKS,
    LAB_CSS,
    act_gb,
    budget_gb,
    checks_score,
    decision_choice,
    decision_why,
    done,
    fits,
    flops,
    mo,
    opt_gb,
    params,
    takeaway_text,
    total_gb,
):
    _ = (LAB_CSS, done)
    _what = {
        "batch": "Halve the batch size",
        "optim": "Switch Adam for SGD",
        "gpu": "Move to a larger device",
        "model": "Reduce the model size",
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
        mo.md("## Your Week 6 report"),
        mo.Html(
            f"""
            <div class="w6-report">
              <div class="row">
                <span class="k">Marked checks</span>
                <span class="v"><span class="w6-score">{checks_score}</span></span>
              </div>
              <div class="row">
                <span class="k">Layer you built</span>
                <span class="v">{flops / 1e9:,.2f} GFLOPs for one forward pass</span>
              </div>
              <div class="row">
                <span class="k">Budget you left</span>
                <span class="v">{params / 1e9:,.2f}B parameters needing {total_gb:.1f} GB on a
                {budget_gb:.0f} GB device, which {'fits' if fits else 'does not fit'}.
                Activations {act_gb:.1f} GB, optimiser state {opt_gb:.1f} GB</span>
              </div>
              <div class="row">
                <span class="k">First experiment</span>
                <span class="v">{_what.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Reasoning</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">What you would measure</span>
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
        ("A run fails with `CUDA out of memory`. What does that tell you about where the "
         "problem originated?",
         {"It is a hardware limitation, since the error came from the device": "a",
          "Nothing on its own. The allocator is where it surfaced; the cause could be at any layer above": "b",
          "It is in the kernels, since they request the allocations": "c"},
         "b"),
        ("Which of the five memory terms is determined by how you run the model rather than by "
         "what the model is?",
         {"Parameters": "a",
          "Optimiser state": "b",
          "Saved activations": "c"},
         "c"),
        ("Memory climbs a little on every iteration until the run dies. What does that pattern "
         "point at?",
         {"A batch size slightly too large for the device": "a",
          "Something retained across steps, such as a loss accumulated without detaching it": "b",
          "Adam allocating more state as training proceeds": "c"},
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
