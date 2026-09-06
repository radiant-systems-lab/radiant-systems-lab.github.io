import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 2 - Where Does It Actually Run")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json
    return json, mo


@app.cell(hide_code=True)
def _(mo):
    def ask(prompt, options, correct, explain):
        """A quick check you can answer as many times as you like.

        Returns (radio, render, summarise). Pass radio.value to render(); the
        report uses summarise() to include the answer at the end of the lab.
        """
        labels = {value: label for label, value in options.items()}
        BREAK = chr(10) + chr(10)

        radio = mo.ui.radio(options=options, label=prompt)

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
          .w2-bar .track { background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 28px; overflow: hidden; }
          .w2-bar .fill { height: 100%; background: #dcdcdc; }
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
          <p class="sub">Last week the thing that stopped you was time. This week it is space.
          The same model can be perfectly sensible in one place and physically impossible a
          few centimetres away.</p>
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
            <p>People say a model is "deployed" as though that were one thing. It is not. A
            model can end up running in a data centre the size of a warehouse, or on a chip
            smaller than your thumbnail, and those two jobs have almost nothing in common.</p>
            <p>What is surprising is how far apart they are. Not twice as different. Not ten
            times. The gap between the biggest and smallest place you might put a model is
            about a <strong>billion</strong> times, in both memory and electricity.</p>
            <p>That is the whole lab. Once you have felt that gap, a lot of decisions that
            looked arbitrary start looking obvious.</p>
          </div>
          <aside class="w2-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Name the four places a model normally runs and what limits each one.</li>
              <li>Work out whether a given model can fit somewhere before you try.</li>
              <li>Say which thing runs out first: memory, time, or power.</li>
              <li>Work out whether moving bytes or doing arithmetic is the real bottleneck.</li>
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
          <p>"I have a model. Can this particular machine actually run it?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: Four places a model can live""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Almost everything you will build ends up in one of four places. They are usually described
    as a spectrum, from enormous and plugged into the grid, down to tiny and running off a coin
    cell.

    | Where | Answers in | Electricity | Memory it has |
    | - | - | - | - |
    | **A data centre** | 100 to 500 ms | 3 to 5 megawatts | terabytes |
    | **A local server** | 10 to 100 ms | 100 to 200 watts | gigabytes |
    | **A phone** | 5 to 50 ms | 3 to 5 watts | gigabytes, but you only get a slice |
    | **A microcontroller** | 1 to 10 ms | 50 to 100 milliwatts | kilobytes |

    Read the electricity column again. The top row is **megawatts**, roughly what a small town
    draws. The bottom row is **milliwatts**, less than a hearing aid. Same column, nine zeros
    apart. Memory is the same story: terabytes at the top, kilobytes at the bottom.

    And notice the direction of the speed column. The machine with the least power is expected
    to answer the **fastest**. That is not a mistake. A microcontroller is usually sitting
    inside something physical that is happening right now, and it has nowhere to send the work.
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
                  "the arithmetic per second that a data centre rack does."),
            "b": ("Sending the work somewhere else costs a network round trip, and a lot of "
                  "things cannot wait or have nowhere to send it. A doorbell in a house with bad "
                  "wifi still has to work."),
            "c": ("Training almost never happens on the small device. It happens in the data "
                  "centre, and only the finished model is sent down."),
            "d": ("Accuracy is a property of the model and the data it learned from, not of the "
                  "chip it later runs on."),
        },
    )
    q1
    return q1, q1_render, q1_sum


@app.cell(hide_code=True)
def _(q1, q1_render):
    q1_render(q1.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 2: Try it""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here are four real machines and a set of real models. Drag the slider and watch which homes
    stay open to you.

    Two things decide it. **Does the model fit in the memory that machine has**, and **can it be
    read fast enough** to answer in time. That second one matters more than people expect: to
    produce one answer, the machine has to read every single number in the model, so a bigger
    model is slower for a reason that has nothing to do with cleverness.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
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
        value=3.5,
        label="Model size, in millions of numbers",
        show_value=True,
    )
    precision = mo.ui.radio(
        options={
            "4 bytes each, full precision": 4.0,
            "2 bytes each, half": 2.0,
            "1 byte each, quantised": 1.0,
        },
        value="4 bytes each, full precision",
        inline=True,
        label="How much space each number takes",
    )
    mo.vstack([size, precision])
    return MODELS, precision, size


@app.cell(hide_code=True)
def _(MODELS, precision, size):
    HOMES = [
        # name, where, memory it has (MB), read speed (GB/s), must answer within (ms)
        ("Data centre", "a rack of accelerators", 80_000.0, 2039.0, 500.0),
        ("Local server", "a machine in the building", 8_000.0, 200.0, 100.0),
        ("Phone", "in someone's pocket", 1_500.0, 50.0, 50.0),
        ("Microcontroller", "inside a device", 0.5, 0.2, 10.0),
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
**The homes close from the bottom up, and they close early.** The microcontroller is out
before you reach a model most people would call small. A 3.5 million number model, which is
already stripped down and built for phones, is about 28 times too big for it.

**Memory runs out long before speed does.** Look at how the cards fail. Almost every red card
says "will not fit", not "too slow". Once something fits, it is usually fast enough. This is
worth remembering, because people reach for faster chips when the thing that actually stopped
them was space.

**Nothing about the model changed.** It is the same numbers in the same order the whole way
along. What changed is where you asked it to live. Last week the same point arrived through
time; this week it arrives through space.

**And the top does not stay open forever either.** The 7 billion number model is 28 GB. That
fits in a data centre and nowhere else on this list, which is exactly why the chat models you
use every day are somewhere else, answering over a network, rather than on your laptop.
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

The sum is rough. It ignores the actual arithmetic, and it assumes one answer at a time. But it
gets you the right order of magnitude in ten seconds, and the right order of magnitude is
usually the decision.
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
            "The phone's processor is not fast enough at arithmetic": "a",
            "The model is simply too big to fit in the memory the phone gives an app": "b",
            "The phone is not accurate enough": "c",
            "The model was trained on the wrong kind of hardware": "d",
        },
        "b",
        {
            "a": ("Sometimes, but it is rarely what stops you first. Notice how many of the red "
                  "cards said 'will not fit' rather than 'too slow'."),
            "b": ("Space runs out before speed does, almost every time. That is why so much of "
                  "this course is about making models smaller rather than machines faster."),
            "c": ("Accuracy belongs to the model, not the phone. The same model gives the same "
                  "answers wherever it manages to run."),
            "d": ("Where a model was trained has no bearing on whether it fits somewhere later. "
                  "Training happens once, in a data centre, on hardware nobody deploys to."),
        },
    )
    q2
    return q2, q2_render, q2_sum


@app.cell(hide_code=True)
def _(q2, q2_render):
    q2_render(q2.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: When it does not fit""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Suppose the machine is fixed. It is the camera you already bought, or the phone your users
    already own. You cannot make it bigger. The model does not fit. Now what?

    There are only two moves available, and one of them is usually not.

    You can **get a bigger machine**, which is often out of the question: you are not going to
    ship everyone a new phone. Or you can **make the model smaller**, which is where nearly all
    the engineering effort goes.

    The bluntest way to make a model smaller has nothing to do with the model at all. It is
    just arithmetic about how you store numbers.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Storing the same number in less space

    A model is a long list of numbers. By default each one is kept to high precision and takes
    **four bytes**. But nothing forces that. You can round them off and keep each in **two
    bytes**, or **one**.

    Do that and the model halves, then halves again, without removing a single number from it.
    Go back to the slider above and switch between the three settings. Watch homes reopen.

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
            "It becomes twice as fast at arithmetic but the same size": "c",
            "It has to be retrained from scratch": "d",
        },
        "b",
        {
            "a": ("Nothing is removed. Every number is still there, which is why the model still "
                  "behaves in almost the same way."),
            "b": ("The list is the same length; each entry is just kept more roughly. Half the "
                  "space, and usually very little accuracy lost at two bytes."),
            "c": ("It often does speed things up, because there is less to read from memory. But "
                  "the headline effect is size, and size is what decides whether it fits."),
            "d": ("Usually not. It is normally applied to a model that has already been trained, "
                  "which is a large part of why it is the first thing people try."),
        },
    )
    q3
    return q3, q3_render, q3_sum


@app.cell(hide_code=True)
def _(q3, q3_render):
    q3_render(q3.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: What a task's time is actually made of""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    So far the question has been whether a model fits. Now assume it does. How long does it
    take to produce one answer?

    It turns out to be three things, and you add them up.

    **Moving the bytes.** Everything the machine needs has to travel from memory to the part
    that does the arithmetic. That takes however many bytes you need, divided by how fast the
    machine can move them.

    **Doing the arithmetic.** Count the operations, divide by how many the machine gets through
    per second. With one honest correction: no machine ever reaches its advertised speed. If it
    only manages 60 per cent of what is printed on the box, use 60 per cent.

    **Everything else.** Launching the work, waiting for things to synchronise, the general tax
    of being a computer. Usually small, occasionally not.

    That is the whole method:

    > **time = bytes to move / how fast it moves them + operations / how fast it computes + overhead**

    Nothing clever. What makes it useful is that it tells you *which of the three is the
    problem*, and therefore which one is worth spending money on.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="w2-question">
          <span class="lbl">Before you go on</span>
          <p>"Every one of those three has to come out in seconds. If your units do not resolve
          to seconds, you have made a mistake somewhere."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: Find out what is actually slowing it down""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is a request arriving at a service. The machine moves **100 MB per second** and there
    is a fixed **5 ms** of overhead on every request.

    Work out where the time goes.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    bytes_mb = mo.ui.slider(
        5, 200, value=40, step=5,
        label="Bytes this request has to move (MB)", show_value=True,
    )
    ops_gf = mo.ui.slider(
        0.5, 20.0, value=2.0, step=0.5,
        label="Arithmetic it has to do (billions of operations)", show_value=True,
    )
    machine_gf = mo.ui.slider(
        4, 48, value=12, step=2,
        label="What the machine actually manages (billion operations per second)",
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
        ("Moving the bytes", t_data, f"{bytes_mb.value:g} MB at {BANDWIDTH_MBPS:g} MB/s"),
        ("Doing the arithmetic", t_compute,
         f"{ops_gf.value:g} billion at {machine_gf.value:g} billion/s"),
        ("Everything else", t_over, "fixed overhead"),
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
        <div class="w2-total"><span>Total for one request</span><b>{t_total:.0f} ms</b></div>
        """
    )
    return


@app.cell(hide_code=True)
def _(biggest, mo, saved_pct, t_total, t_total_2x):
    mo.vstack([
        mo.callout(
            mo.md(f"**{biggest}** is the biggest of the three. That is your bottleneck."),
            kind="info",
        ),
        mo.md(
            f"Now suppose you buy a machine with **twice the arithmetic speed**. The total goes "
            f"from **{t_total:.0f} ms** to **{t_total_2x:.0f} ms**. That is "
            f"**{saved_pct:.0f} per cent** faster, for double the money."
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "What to take from that": mo.md(
                """
Leave the sliders where they started and the three terms come out at **400 ms**, **167 ms** and
**5 ms**. Moving the bytes takes more than twice as long as the arithmetic. The machine finishes
computing and then sits there waiting for data.

Buying twice the arithmetic speed in that situation improves the total by about **15 per cent**.
Not nothing, but you doubled your spend to shave a seventh off. If you had doubled the memory
speed instead, you would have taken 200 ms off a 572 ms request.

**The rule this gives you: only upgrading the biggest term buys you much.** Money spent on any
other term is mostly wasted, and the arithmetic above is how you find out which is which before
you spend it.

Drag the arithmetic slider up to 20 billion operations and watch the verdict change. Same
method, different answer, and now the expensive GPU is exactly the right purchase.
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
    )
    q4
    return q4, q4_render, q4_sum


@app.cell(hide_code=True)
def _(q4, q4_render):
    q4_render(q4.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 6: The bottleneck is not a property of the model""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    People say things like "transformers are memory-bound" and "convolutional networks are
    compute-bound" as though it were a fact about the architecture. It is not, and here is the
    counter-example.

    First, a correction to something Part 2 quietly glossed over. **A model in memory is not
    just its weights.** Running it also produces intermediate results at every layer, and those
    are usually the bigger number. For ResNet-50 the weights are about **97.5 MB**, loaded once
    however many images you push through, and the intermediates are about **20 MB per image**.

    So the bytes you move are `97.5 + 20 x images`. The arithmetic is `7.7 billion x images`.

    Notice the two grow at different rates. Double the images and you double the arithmetic
    exactly, but you do not double the bytes, because the weights are paid for once and then
    shared. Drag the slider and watch what that does.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    batch = mo.ui.slider(
        steps=[1, 2, 3, 4, 8, 16, 32, 64],
        value=1,
        label="Images sent through together",
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
    d_vol_mb = WEIGHTS_MB + ACT_MB * b
    ops = FLOPS_PER_IMAGE * b
    supplied = ops / (d_vol_mb * 1e6)          # operations per byte the workload offers
    ceiling = FLOPS_PER_IMAGE / (ACT_MB * 1e6)  # where it flattens out, however big the batch
    compute_bound = supplied > MACHINE_DEMANDS
    return (
        MACHINE_DEMANDS,
        b,
        ceiling,
        compute_bound,
        d_vol_mb,
        ops,
        supplied,
    )


@app.cell(hide_code=True)
def _(LAB_CSS, MACHINE_DEMANDS, compute_bound, d_vol_mb, mo, ops, supplied):
    _ = LAB_CSS
    _scale = max(supplied, MACHINE_DEMANDS) * 1.1
    mo.Html(
        f"""
        <div class="w2-bars">
          <div class="w2-bar{' win' if compute_bound else ''}">
            <span class="t">The work offers<br><span style="color:#8a8a8a;font-size:.78rem">
            {ops / 1e9:.1f} billion operations over {d_vol_mb:.0f} MB</span></span>
            <span class="track"><span class="fill"
              style="width:{supplied / _scale * 100:.1f}%"></span></span>
            <span class="n">{supplied:.0f}</span>
          </div>
          <div class="w2-bar{'' if compute_bound else ' win'}">
            <span class="t">The machine needs<br><span style="color:#8a8a8a;font-size:.78rem">
            to keep its arithmetic busy</span></span>
            <span class="track"><span class="fill"
              style="width:{MACHINE_DEMANDS / _scale * 100:.1f}%"></span></span>
            <span class="n">{MACHINE_DEMANDS:.0f}</span>
          </div>
        </div>
        <p style="color:#6f6f6f;font-size:.85rem;margin:2px 0 0">Both numbers are operations per
        byte. If the work offers less than the machine needs, the machine runs out of data and
        waits.</p>
        """
    )
    return


@app.cell(hide_code=True)
def _(b, compute_bound, mo, supplied):
    if compute_bound:
        _msg = (f"At {b} image{'s' if b > 1 else ''} the work offers {supplied:.0f} operations "
                f"per byte, more than the machine needs. **The arithmetic is now the "
                f"bottleneck.**")
        _kind = "success"
    else:
        _msg = (f"At {b} image{'s' if b > 1 else ''} the work offers only {supplied:.0f} "
                f"operations per byte. **The machine is starved**, finishing its arithmetic and "
                f"waiting for bytes.")
        _kind = "warn"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(ceiling, mo):
    mo.accordion(
        {
            "What just happened": mo.md(
                f"""
**One image:** the work offers 66 operations per byte, the machine wants 153. It starves. The
time is dominated by moving bytes.

**Four images:** they cross over. Three is still just short.

**Eight images:** 239 offered against 153 needed. The machine is fed, and now the arithmetic is
what takes the time.

Same model. Same card. Same numbers inside the model, unchanged. **Only the batch size moved**,
and the bottleneck swapped ends. So "is ResNet-50 compute-bound or memory-bound?" is not a
question with an answer. It is bound by whichever term is bigger *in the situation you are
actually running it*, and you get to move that.

**It does stop, though.** Push the slider to 64 and the number barely grows any more. The
ceiling is about **{ceiling:.0f}** operations per byte, and no batch size gets past it, because
once the intermediates dwarf the weights there is no fixed cost left to spread out. That ceiling
belongs to the architecture.

So why does anyone run batches of 512? Not to change the regime, which was settled by about
batch 4. For throughput: to amortise the fixed overhead and keep the machine busy. Which is a
different argument, and the one you met in Week 1.
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
    )
    q5
    return q5, q5_render, q5_sum


@app.cell(hide_code=True)
def _(q5, q5_render):
    q5_render(q5.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 7: Your decision""")
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
def _(mo):
    decision_form = (
        mo.md("""
        {choice}

        {why}
        """)
        .batch(
            choice=mo.ui.radio(
                options={
                    "Send every frame to a data centre and do the work there": "cloud",
                    "Put a small server in the building and send frames to that": "edge",
                    "Run a small model on each camera and send only what it finds": "device",
                },
                label="**Where would you run it?**",
            ),
            why=mo.ui.text_area(
                placeholder="What made you pick that, and what would change your mind?",
                label="**Why?**",
                full_width=True,
                rows=4,
            ),
        )
        .form(
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
def _(decision_form, mo):
    mo.stop(
        decision_form.value is None,
        mo.callout(mo.md("Pick an answer, say why, then press **Submit my decision**."), kind="warn"),
    )
    decision_choice = decision_form.value["choice"]
    decision_why = decision_form.value["why"].strip()
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
def _(decision_choice, mo):
    _ = decision_choice
    reflect_form = (
        mo.md("{takeaway}")
        .batch(
            takeaway=mo.ui.text_area(
                placeholder="The thing that would stop me first is... because...",
                label="**Last one.** For the option you chose, which runs out first: memory, time, or battery? Say why.",
                full_width=True,
                rows=4,
            ),
        )
        .form(
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
def _(mo, reflect_form):
    mo.stop(
        reflect_form.value is None,
        mo.callout(mo.md("Answer the last question to finish."), kind="warn"),
    )
    takeaway_text = reflect_form.value["takeaway"].strip()
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
def _(
    bytes_each,
    decision_choice,
    decision_why,
    done,
    json,
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
    _a1 = q1_sum(q1.value)
    _a2 = q2_sum(q2.value)
    _a3 = q3_sum(q3.value)
    _a4 = q4_sum(q4.value)
    _a5 = q5_sum(q5.value)

    def _word(ok):
        return "not answered" if ok is None else ("correct" if ok else "not correct")

    submission = {
        "lab": "CSC/EE 8001 - Week 2",
        "model_size_millions": params_m,
        "bytes_per_number": bytes_each,
        "where_i_would_run_it": decision_choice,
        "why": decision_why,
        "what_runs_out_first": takeaway_text,
        "check_1_why_a_microcontroller": {"answer": _a1[0], "correct": _a1[1]},
        "check_2_what_stops_a_phone": {"answer": _a2[0], "correct": _a2[1]},
        "check_3_halving_the_bytes": {"answer": _a3[0], "correct": _a3[1]},
        "check_4_which_upgrade": {"answer": _a4[0], "correct": _a4[1]},
        "check_5_bound_by_what": {"answer": _a5[0], "correct": _a5[1]},
    }

    report_text = chr(10).join([
        "CSC/EE 8001 - Week 2",
        "=" * 40,
        "",
        "MODEL I LEFT IT ON",
        f"  {params_m:g} million numbers at {bytes_each:g} bytes each",
        "",
        "WHERE I WOULD RUN IT",
        f"  {decision_choice}",
        "",
        "WHY",
        f"  {decision_why}",
        "",
        "WHAT RUNS OUT FIRST",
        f"  {takeaway_text}",
        "",
        "QUICK CHECKS",
        "  Why put a model on a microcontroller",
        f"    {_a1[0]}  [{_word(_a1[1])}]",
        "  What stops a model running on a phone",
        f"    {_a2[0]}  [{_word(_a2[1])}]",
        "  What halving the bytes per number does",
        f"    {_a3[0]}  [{_word(_a3[1])}]",
        "  Which upgrade to buy",
        f"    {_a4[0]}  [{_word(_a4[1])}]",
        "  Whether a model has a fixed bottleneck",
        f"    {_a5[0]}  [{_word(_a5[1])}]",
    ])

    mo.accordion({
        "A copy of what you did": mo.vstack([
            mo.hstack(
                [
                    mo.download(data=report_text.encode("utf-8"),
                                filename="week2_report.txt", label="Download my report"),
                    mo.download(data=json.dumps(submission, indent=2).encode("utf-8"),
                                filename="week2_report.json", label="Download as JSON"),
                ],
                justify="start",
                gap=1,
            ),
            mo.md("```" + chr(10) + report_text + chr(10) + "```"),
        ]),
    })
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


if __name__ == "__main__":
    app.run()
