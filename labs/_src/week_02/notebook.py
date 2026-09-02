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
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 15 min</dd></div>
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
    size
    return MODELS, size


@app.cell(hide_code=True)
def _(MODELS, size):
    HOMES = [
        # name, where, memory it has (MB), read speed (GB/s), must answer within (ms)
        ("Data centre", "a rack of accelerators", 80_000.0, 2039.0, 500.0),
        ("Local server", "a machine in the building", 8_000.0, 200.0, 100.0),
        ("Phone", "in someone's pocket", 1_500.0, 50.0, 50.0),
        ("Microcontroller", "inside a device", 0.5, 0.2, 10.0),
    ]

    params_m = float(size.value)
    # Four bytes for every number in the model. This is the space it takes up.
    model_mb = params_m * 4.0
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
    return describe, model_mb, params_m, results


@app.cell(hide_code=True)
def _(LAB_CSS, describe, mo, model_mb, params_m, results):
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
              f"That takes up **{_size(model_mb)}**."),
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
    mo.md(r"""## Part 3: Your decision""")
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
                <span class="v">{params_m:g} million numbers, {describe}</span>
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
            </div>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(
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
    takeaway_text,
):
    _ = done
    _a1 = q1_sum(q1.value)
    _a2 = q2_sum(q2.value)

    def _word(ok):
        return "not answered" if ok is None else ("correct" if ok else "not correct")

    submission = {
        "lab": "CSC/EE 8001 - Week 2",
        "model_size_millions": params_m,
        "where_i_would_run_it": decision_choice,
        "why": decision_why,
        "what_runs_out_first": takeaway_text,
        "check_1_why_a_microcontroller": {"answer": _a1[0], "correct": _a1[1]},
        "check_2_what_stops_a_phone": {"answer": _a2[0], "correct": _a2[1]},
    }

    report_text = chr(10).join([
        "CSC/EE 8001 - Week 2",
        "=" * 40,
        "",
        "MODEL I LEFT IT ON",
        f"  {params_m:g} million numbers",
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
