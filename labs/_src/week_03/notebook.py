import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 3 - The Constraint You Found Too Late")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import json
    import numpy as np
    return json, mo, np


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
          .w3-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .w3-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .w3-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .w3-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }
          .w3-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .w3-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .w3-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .w3-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .w3-split { grid-template-columns: 1fr; } }
          .w3-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .w3-split > .body p:last-child { margin-bottom: 0; }

          .w3-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .w3-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .w3-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .w3-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .w3-aside li:last-child { margin-bottom: 0; }
          .w3-aside li::marker { color: #6a5314; font-weight: 800; }
          .w3-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                            padding-top: 11px; padding-left: 24px; }
          .w3-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .w3-aside .meta div:last-child { margin-bottom: 0; }
          .w3-aside .meta dt { color: #6f6f6f; }
          .w3-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .w3-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .w3-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .w3-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }

          /* The five stages, shown as a row that loops back on itself. */
          .w3-stages { display: flex; flex-wrap: wrap; gap: 8px; align-items: stretch;
                       margin: 16px 0 6px; }
          .w3-stage { flex: 1 1 150px; border: 1px solid #e6e6e6; border-top: 5px solid #dcdcdc;
                      border-radius: 10px; background: #fff; padding: 11px 13px; }
          .w3-stage .n { color: #9a9a9a; font-size: .7rem; font-weight: 800;
                         letter-spacing: .06em; }
          .w3-stage .s { display: block; color: #111; font-size: .93rem; font-weight: 700;
                         margin-top: 2px; line-height: 1.3; }
          .w3-stage .tag { display: block; margin-top: 7px; font-size: .74rem;
                           font-weight: 800; letter-spacing: .04em; text-transform: uppercase;
                           color: #9a9a9a; }
          .w3-stage.hit { border-top-color: #f1b82d; background: #fffdf5; }
          .w3-stage.hit .tag { color: #6a5314; }
          .w3-stage.origin { border-top-color: #c62828; background: #fefafa; }
          .w3-stage.origin .tag { color: #c62828; }
          .w3-loop { margin: 0; color: #6f6f6f; font-size: .85rem; text-align: center;
                     border-top: 1px dashed #dcdcdc; padding-top: 8px; }

          /* Horizontal bars, reused for the budget gauge and the drift readout. */
          .w3-bars { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
          .w3-bar { display: grid; grid-template-columns: 170px 1fr 110px;
                    align-items: center; gap: 12px; }
          @media (max-width: 640px) { .w3-bar { grid-template-columns: 110px 1fr 86px; } }
          .w3-bar .t { color: #4a4a4a; font-size: .87rem; line-height: 1.3; }
          .w3-bar .track { display: block; background: #f4f4f4; border: 1px solid #ececec;
                           border-radius: 6px; height: 28px; overflow: hidden;
                           position: relative; }
          /* A span is inline by default, so it ignores height and percentage width.
             Both of these have to be blocks or the bar renders empty. */
          .w3-bar .fill { display: block; height: 100%; background: #c9c9c9; }
          .w3-bar.good .fill { background: #7cb47f; }
          .w3-bar.bad .fill  { background: #d98080; }
          .w3-bar .limit { position: absolute; top: 0; bottom: 0; width: 2px;
                           background: #111; }
          .w3-bar .n { text-align: right; font-weight: 800; font-size: .9rem; color: #111; }
          .w3-note { color: #6f6f6f; font-size: .85rem; margin: 2px 0 0; line-height: 1.5; }

          /* Two-column compare, used for system-versus-requirement. */
          .w3-two { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
          @media (max-width: 760px) { .w3-two { grid-template-columns: 1fr; } }
          .w3-col { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                    border-radius: 12px; background: #fff; padding: 14px 16px; }
          .w3-col h4 { margin: 0 0 4px; font-size: 1rem; color: #111; }
          .w3-col p.lead { margin: 0 0 10px; color: #6f6f6f; font-size: .84rem; }
          .w3-col ul { margin: 0; padding-left: 20px; }
          .w3-col li { color: #2f2f2f; font-size: .89rem; line-height: 1.5; margin-bottom: 6px; }
          .w3-col li:last-child { margin-bottom: 0; }

          /* The hand-off checklist verdict. */
          .w3-parts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;
                      margin: 14px 0; }
          @media (max-width: 820px) { .w3-parts { grid-template-columns: 1fr 1fr; } }
          .w3-part { border: 1px solid #e6e6e6; border-left: 5px solid #dcdcdc;
                     border-radius: 10px; background: #fafafa; padding: 11px 13px; }
          .w3-part.on { border-left-color: #2e7d32; background: #fff; }
          .w3-part h5 { margin: 0 0 3px; font-size: .9rem; color: #111; }
          .w3-part p { margin: 0; color: #6f6f6f; font-size: .8rem; line-height: 1.45; }
          .w3-part.on p { color: #3a3a3a; }

          /* The weekly workflow, drawn as a DAG. */
          .w3-dag { display: flex; flex-wrap: wrap; align-items: center; gap: 6px;
                    margin: 12px 0; }
          .w3-dag .pair { display: flex; flex-direction: column; gap: 6px; flex: 1 1 150px;
                          align-self: stretch; }
          .w3-arrow { align-self: center; color: #c4c4c4; font-weight: 800; font-size: 1.1rem; }
          .w3-node { flex: 1 1 150px; border: 1px solid #e6e6e6; border-left: 5px solid #c9c9c9;
                     border-radius: 10px; background: #fff; padding: 9px 11px; }
          .w3-node .id { color: #9a9a9a; font-size: .7rem; font-weight: 800; }
          .w3-node .lab { display: block; color: #111; font-size: .86rem; font-weight: 700;
                          line-height: 1.3; margin-top: 1px; }
          .w3-node .st { display: block; margin-top: 6px; font-size: .73rem; font-weight: 800;
                         letter-spacing: .03em; text-transform: uppercase; color: #8a8a8a; }
          .w3-node.ran    { border-left-color: #2e7d32; }
          .w3-node.ran .st { color: #2e7d32; }
          .w3-node.failed { border-left-color: #c62828; background: #fefafa; }
          .w3-node.failed .st { color: #c62828; }
          .w3-node.skipped { background: #fafafa; }
          .w3-node.stale  { border-left-color: #d98f00; background: #fffdf5; }
          .w3-node.stale .st { color: #8a5c00; }
          .w3-runhead { margin: 14px 0 0; font-size: .76rem; font-weight: 800;
                        letter-spacing: .06em; text-transform: uppercase; color: #6a5314; }

          /* The server-health panel in the monitoring part. */
          .w3-status { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
                       margin: 14px 0; }
          @media (max-width: 720px) { .w3-status { grid-template-columns: 1fr; } }
          .w3-stat { border: 1px solid #e6e6e6; border-radius: 10px; background: #fff;
                     padding: 12px 14px; }
          .w3-stat .k { color: #6f6f6f; font-size: .74rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .w3-stat .v { display: block; color: #111; font-size: 1.3rem; font-weight: 800;
                        line-height: 1.25; margin-top: 3px; }
          .w3-stat .why { display: block; color: #6f6f6f; font-size: .78rem; margin-top: 4px; }
          .w3-stat.green .v { color: #2e7d32; }
          .w3-stat.red .v { color: #c62828; }

          .w3-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                       border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                       box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .w3-report .row { display: grid; grid-template-columns: 190px 1fr; gap: 16px;
                            padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                            align-items: baseline; }
          .w3-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) { .w3-report .row { grid-template-columns: 1fr; gap: 3px; } }
          .w3-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                          letter-spacing: .06em; text-transform: uppercase; }
          .w3-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .w3-report .tick { color: #2e7d32; font-weight: 800; }
          .w3-report .cross { color: #c62828; font-weight: 800; }
          .w3-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
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
        <div class="w3-hero">
          <p class="w3-eyebrow">CSC/EE 8001 &middot; Week 3</p>
          <h1>The Constraint You Found Too Late</h1>
          <p class="sub">Four months of work, a model that scores 95 per cent, and a tablet
          it was never going to fit on. This lab is about why that happens, what it costs to
          undo, and how the stages of a project are supposed to stop it.</p>
          <div class="w3-chips">
            <span class="w3-chip">Stages and the loop</span>
            <span class="w3-chip">Constraints travelling backwards</span>
            <span class="w3-chip">Failures that never crash</span>
            <span class="w3-chip-plain w3-chip">Nothing here is marked</span>
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
        <div class="w3-split">
          <div class="body">
            <p>Week 2 ended on a hard edge. A model either fits on the machine you have or it
            does not, and if it does not, you make the model smaller or you get a bigger
            machine.</p>
            <p>That sounds like a decision you make at the end, once the model exists. It is
            not. <strong>The moment you agree to make the model smaller, you have changed what
            the training run has to produce, which changes what counts as a good enough
            result, which can change what data you needed in the first place.</strong> A
            decision taken on the last day of the project reaches all the way back to the
            first one.</p>
            <p>This week is about that reach. Where the stages of an ML project are, which
            direction trouble travels along them, and what each stage has to hand the next one
            so that a problem gets caught by a machine instead of by a customer.</p>
          </div>
          <aside class="w3-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Name the five stages, and say what makes them a loop rather than a line.</li>
              <li>Trace a deployment constraint backwards to the stages that have to absorb it.</li>
              <li>Say what one stage owes the next, and what breaks when it is not handed over.</li>
              <li>Explain how a system can fail while every log line says it is healthy.</li>
              <li>Say what a scheduler does that a timer cannot.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 45 min</dd></div>
              <div><dt>Before this</dt><dd>Weeks 1 and 2</dd></div>
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
        <div class="w3-question">
          <span class="lbl">The question this lab answers</span>
          <p>"The model is finished and it does not fit. Whose problem is that, and when did
          it become one?"</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: Four months, and a number nobody asked for""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    A team spends four months building a classifier that reads photographs of the back of the
    eye and flags diabetic retinopathy. It is good work. On the test set it scores **95 per
    cent accuracy**, with an AUC of **0.98**. Those are numbers you would be pleased to put in
    a paper.

    They built it the way everyone builds these now. Take a large pretrained vision model,
    fine-tune it on fundus photographs, and run it at high resolution, because the lesions
    that matter are a few pixels across and disappear if you shrink the image. The backbone
    they picked has about **a billion parameters**.

    Last week's sum tells you what that weighs. A billion numbers at four bytes each is
    **4 GB**, before the model has done anything at all.

    The plan is to put it on a tablet and give it to rural clinics, where there is no
    ophthalmologist within a hundred miles and a screening tool would genuinely change what
    happens to people. The clinics have tablets already. The programme bought them in bulk,
    two years ago, at the price you pay when you are buying three hundred of something.

    Then the deployment engineer opens the file.

    > "Those tablets have 2 GB of memory, and Android keeps most of it. One app gets about
    > **512 MB** before the system starts killing whatever is using the most. Your model needs
    > 4 GB."

    That is not a near miss. It is **eight times over**, and no amount of care in the serving
    code closes it.

    Now, two questions, and the gap between them is what this course is about.

    - **Is the model good?** Yes. Unambiguously. The metrics are real and the work was sound.
    - **Is the system good?** No. It cannot run. Nobody will ever be screened by it.

    Both statements are true at once, and that is the uncomfortable part. Nothing in the
    modelling work was done badly. The failure is in the **order the questions were asked**.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q1, q1_render, q1_sum = ask(
        "**Quick check.** At what point in the project should the 512 MB limit have started affecting decisions?",
        {
            "At deployment, which is when the tablet was actually available to test on": "a",
            "During evaluation, as one more metric to report alongside accuracy": "b",
            "Before any data was collected, because it decides what counts as a good model": "c",
            "It should not: get the accuracy first, then find hardware that can run it": "d",
        },
        "c",
        {
            "a": ("That is when it *was* found, and that is the whole problem. By then four "
                  "months of choices had already been made on the assumption that size did "
                  "not matter."),
            "b": ("Better, but still late. By evaluation the architecture is fixed and the "
                  "training data is collected. You would be measuring a constraint you can no "
                  "longer cheaply satisfy."),
            "c": ("The tablet was known from the start. A model that cannot fit on it was "
                  "never a candidate, so 'good' should have meant 'accurate *and* under 512 "
                  "MB' from the first day."),
            "d": ("Sometimes you genuinely get to choose the hardware. Here you do not: the "
                  "clinics have the tablets they have, and 'buy three hundred new tablets' is "
                  "a different project with a different budget."),
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
    mo.md(r"""## Part 2: The five stages, and why they are a circle""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Before going further, here is the map. Almost every ML project, whatever it is for, moves
    through the same five stages.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    _stages = [
        ("01", "Data collection", "what the system learns from"),
        ("02", "Model development", "turning that into a model"),
        ("03", "Evaluation", "deciding whether it is good enough"),
        ("04", "Deployment", "putting it where people use it"),
        ("05", "Monitoring", "watching it once it is out there"),
    ]
    _cards = "".join(
        f"""
        <div class="w3-stage">
          <span class="n">{_n}</span>
          <span class="s">{_name}</span>
          <span class="tag">{_note}</span>
        </div>
        """
        for _n, _name, _note in _stages
    )
    mo.Html(
        f"""
        <div class="w3-stages">{_cards}</div>
        <p class="w3-loop">and monitoring feeds straight back into data collection &#8630;</p>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Two words get used for this, and they are not the same thing.

    The **pipeline**, or workflow, is the five stages: the sequence of things that have to
    happen.

    The **lifecycle** is what you get when you notice that the arrow out of monitoring goes
    back to the start. Monitoring tells you the model has gone stale, so you collect fresh
    data, so you train again, so you evaluate again, so you deploy again. It never stops while
    the system is alive.

    > **Workflow is the stages. Lifecycle is going round the stages, again and again.**

    Which means there is a way to write down what the system actually depends on, and it is
    worth staring at for a second:

    $$\text{System performance} = f(\text{Data},\; \text{Algorithm},\; \text{Machine},\; \text{Monitoring})$$

    Not $f(\text{Algorithm})$. The machine is in there, sitting as an equal next to the model,
    which is exactly why a perfect model on the wrong tablet scores zero as a system.

    And because it is one function of four arguments, **you cannot optimise the arguments one
    at a time.** Improving the algorithm while ignoring the machine is not progress towards a
    working system. It is progress towards a nicer number in a notebook.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: Trouble travels backwards""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Back to the tablet. The constraint arrived at the **deployment** stage, but it cannot be
    fixed there: no amount of clever loading fits 4 GB into 512 MB. So it has to travel
    upstream until it reaches a stage that can actually absorb it. That travelling is called
    **constraint propagation**, and watching it happen is the point of this part.

    Below are four ways to make the model smaller. Each one shrinks it, each one costs
    accuracy, and each one reopens some stage of the project that you thought was finished.

    Two things have to be true before you can ship:

    - the model must be **at or under 512 MB**, which is a fact about the tablet
    - accuracy must stay **at or above 90 per cent**, which is a decision the clinicians made,
      because a screening tool that misses disease is worse than no screening tool

    Tick fixes until both are satisfied. It is harder than it looks.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    fix_quant = mo.ui.checkbox(
        label="**Quantise** the weights, 4 bytes down to 1 &nbsp;&middot;&nbsp; 4&times; smaller, costs 4.0 points"
    )
    fix_prune = mo.ui.checkbox(
        label="**Prune** 30 per cent of the connections &nbsp;&middot;&nbsp; 1.4&times; smaller, costs 1.5 points"
    )
    fix_arch = mo.ui.checkbox(
        label="**Swap the architecture** for a compact one &nbsp;&middot;&nbsp; 8&times; smaller, costs 3.0 points"
    )
    fix_res = mo.ui.checkbox(
        label="**Halve the input resolution** &nbsp;&middot;&nbsp; 1.8&times; smaller, costs 6.5 points"
    )
    mo.vstack([
        mo.md("**Pick the fixes you would apply.**"),
        fix_quant, fix_prune, fix_arch, fix_res,
    ])
    return fix_arch, fix_prune, fix_quant, fix_res


@app.cell(hide_code=True)
def _(fix_arch, fix_prune, fix_quant, fix_res):
    BASE_MB = 4000.0        # a billion parameters at four bytes each
    BUDGET_MB = 512.0       # what the tablet has free
    BASE_ACC = 95.0         # test accuracy the team reported
    ACC_FLOOR = 90.0        # what the clinicians will accept for screening

    # name, chosen, size multiplier, accuracy points given up, stages it reopens
    FIXES = [
        ("Quantise to 1 byte", fix_quant.value, 0.25, 4.0,
         {"Model development", "Evaluation"},
         "The training run itself is untouched, but every number is now stored more roughly, "
         "so the model has to be re-checked before anyone trusts it."),
        ("Prune 30 per cent", fix_prune.value, 0.70, 1.5,
         {"Model development", "Evaluation"},
         "Connections are removed and the remainder is fine-tuned, so this is a return to "
         "training, then a return to evaluation."),
        ("Compact architecture", fix_arch.value, 0.12, 3.0,
         {"Data collection", "Model development", "Evaluation"},
         "You are abandoning the billion-parameter backbone for one built to run on a phone. "
         "It expects differently prepared inputs, so the preparation code and the stored "
         "dataset are rebuilt, and the whole thing is trained again from the beginning."),
        ("Half resolution", fix_res.value, 0.55, 6.5,
         {"Data collection", "Model development", "Evaluation"},
         "You are throwing away pixels before the model ever sees them. The dataset is "
         "regenerated, the model is retrained on it, and the small lesions get harder to see."),
    ]

    chosen = [f for f in FIXES if f[1]]

    size_mb = BASE_MB
    accuracy = BASE_ACC
    reopened = {"Deployment"}       # where the constraint was found in the first place
    for _n, _on, _mult, _cost, _stages, _note in chosen:
        size_mb *= _mult
        accuracy -= _cost
        reopened |= _stages

    fits = size_mb <= BUDGET_MB
    accurate = accuracy >= ACC_FLOOR
    shippable = fits and accurate
    return (
        ACC_FLOOR,
        BASE_ACC,
        BASE_MB,
        BUDGET_MB,
        FIXES,
        accuracy,
        accurate,
        chosen,
        fits,
        reopened,
        shippable,
        size_mb,
    )


@app.cell(hide_code=True)
def _(
    ACC_FLOOR,
    BASE_ACC,
    BASE_MB,
    BUDGET_MB,
    LAB_CSS,
    accuracy,
    accurate,
    fits,
    mo,
    size_mb,
):
    _ = LAB_CSS

    # Both bars are drawn against a fixed span so they do not rescale as you tick
    # boxes; a bar that redraws its own axis hides the thing you are looking for.
    _size_span = BASE_MB
    _size_pct = min(size_mb / _size_span * 100.0, 100.0)
    _budget_pct = BUDGET_MB / _size_span * 100.0

    _acc_lo, _acc_hi = 75.0, 100.0
    _acc_pct = max(min((accuracy - _acc_lo) / (_acc_hi - _acc_lo) * 100.0, 100.0), 0.0)
    _floor_pct = (ACC_FLOOR - _acc_lo) / (_acc_hi - _acc_lo) * 100.0

    def _mb(v):
        return f"{v:,.0f} MB"

    mo.vstack([
        mo.Html(
            f"""
            <div class="w3-bars">
              <div class="w3-bar {'good' if fits else 'bad'}">
                <span class="t">Size on the tablet<br><span style="color:#8a8a8a;font-size:.78rem">
                started at {_mb(BASE_MB)}, budget is {BUDGET_MB:.0f} MB</span></span>
                <span class="track">
                  <span class="fill" style="width:{_size_pct:.1f}%"></span>
                  <span class="limit" style="left:{_budget_pct:.1f}%"></span>
                </span>
                <span class="n">{_mb(size_mb)}</span>
              </div>
              <div class="w3-bar {'good' if accurate else 'bad'}">
                <span class="t">Accuracy left<br><span style="color:#8a8a8a;font-size:.78rem">
                started at {BASE_ACC:.0f}%, floor is {ACC_FLOOR:.0f}%</span></span>
                <span class="track">
                  <span class="fill" style="width:{_acc_pct:.1f}%"></span>
                  <span class="limit" style="left:{_floor_pct:.1f}%"></span>
                </span>
                <span class="n">{accuracy:.1f}%</span>
              </div>
            </div>
            <p class="w3-note">The black line on each bar is the limit. The size bar has to end
            left of it; the accuracy bar has to end right of it.</p>
            """
        ),
    ])
    return


@app.cell(hide_code=True)
def _(accuracy, accurate, fits, mo, shippable, size_mb):
    if shippable:
        _msg = (f"**This one ships.** {size_mb:.0f} MB on a 512 MB tablet, and {accuracy:.1f} "
                f"per cent against a floor of 90. Now look at which stages you had to reopen "
                f"to get here.")
        _kind = "success"
    elif not fits and not accurate:
        _msg = (f"**Neither limit is met.** Still {size_mb:.0f} MB, and accuracy is down to "
                f"{accuracy:.1f} per cent. You are paying for shrinkage without getting enough "
                f"of it.")
        _kind = "danger"
    elif not fits:
        _msg = (f"**Still too big.** {size_mb:.0f} MB against 512 MB. The accuracy is fine, so "
                f"you have room to spend more of it.")
        _kind = "warn"
    else:
        _msg = (f"**It fits, and it is no longer good enough.** {size_mb:.0f} MB is inside the "
                f"budget, but {accuracy:.1f} per cent is below the floor the clinicians set. "
                f"A screening tool that misses disease is not a smaller success, it is a "
                f"different kind of failure.")
        _kind = "warn"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo, reopened):
    _ = LAB_CSS
    _stages = [
        ("01", "Data collection"),
        ("02", "Model development"),
        ("03", "Evaluation"),
        ("04", "Deployment"),
        ("05", "Monitoring"),
    ]
    _cards = ""
    for _n, _name in _stages:
        if _name == "Deployment":
            _cls, _tag = "origin", "where it was found"
        elif _name in reopened:
            _cls, _tag = "hit", "has to be redone"
        else:
            _cls, _tag = "", "untouched"
        _cards += f"""
        <div class="w3-stage {_cls}">
          <span class="n">{_n}</span>
          <span class="s">{_name}</span>
          <span class="tag">{_tag}</span>
        </div>
        """
    mo.vstack([
        mo.md("**What your choice reopens**"),
        mo.Html(f'<div class="w3-stages">{_cards}</div>'),
    ])
    return


@app.cell(hide_code=True)
def _(chosen, mo):
    mo.stop(not chosen, mo.callout(mo.md("Tick a fix to see what it drags back upstream."), kind="neutral"))
    _lines = chr(10).join(f"- **{_n}.** {_note}" for _n, _on, _m, _c, _s, _note in chosen)
    mo.md("**Why those stages:**" + chr(10) + chr(10) + _lines)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "What you should have noticed": mo.md(
                """
**Quantisation alone is not enough, and it is the first thing everyone tries.** It is the
cheapest fix on the list and it takes 4 GB down to 1 GB, which is still twice the budget. An
eight-fold gap is not a rounding problem. You cannot store your way out of it.

**Only two of the sixteen combinations actually ship**, and both of them include swapping the
architecture:

| What you tick | Size | Accuracy | Ships? |
| - | - | - | - |
| Compact architecture, on its own | 480 MB | 92.0% | yes |
| Compact architecture and pruning | 336 MB | 90.5% | yes |
| Quantise and compact architecture | 120 MB | 88.0% | no, below the floor |
| Quantise, on its own | 1,000 MB | 91.0% | no, twice the budget |
| Everything at once | 46 MB | 80.0% | no, and by a long way |

**The fix that works is the one that reaches furthest back.** Swapping the architecture
reopens data collection, because a different model wants differently prepared inputs. That is
not a coincidence. The constraint was violated by *eight times*, and a violation that large
can only be absorbed by a stage early enough to still be making real choices.

**Ticking everything makes it worse.** Four fixes leave you with a 46 MB model that is right
80 per cent of the time. It fits beautifully and no clinician should ever use it. Shrinking is
not the goal; shipping something worth shipping is.

**None of this was modelling work.** Nobody found a better architecture or a cleverer loss.
The entire exercise was spending accuracy to buy memory, at exchange rates set by hardware
that was sitting in the clinics the whole time.
"""
            ),
            "So what should the team have done in month one": mo.md(
                """
Written the tablet into the definition of the problem, before a single image was collected.

In practice that means the first stage of the project produces a sentence like: *"a screening
model, at least 90 per cent accurate, running in under 512 MB and answering within two seconds
on the tablets the clinics already own."* Every one of those is checkable. Every one of them
rules out work that was never going to survive.

With that sentence written down, the compact architecture is where you start rather than where
you end up, the data pipeline is built once for the inputs that model needs, and the four
months produce something that can be deployed on the day it is finished.

The work is not obviously harder. It is the same work in a different order.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q2, q2_render, q2_sum = ask(
        "**Quick check.** Quantising took the model from 4 GB to 1 GB and it still did not fit. What does that tell you?",
        {
            "Quantisation was applied incorrectly": "a",
            "The tablet needs more memory, so the hardware has to change": "b",
            "A gap that large has to be absorbed by an earlier stage, which means redesigning and retraining": "c",
            "Accuracy should be lowered further until the size comes down": "d",
        },
        "c",
        {
            "a": ("Four times smaller is what quantisation gives you, and that is what it "
                  "gave. It did its job; its job was just not big enough."),
            "b": ("That is the one option the story removed. The clinics own the tablets, and "
                  "replacing three hundred of them is a different project with a different "
                  "budget."),
            "c": ("Late fixes have small, fixed exchange rates. An eight-fold miss needs a "
                  "stage that is still free to make real choices, and the only stages like "
                  "that are upstream."),
            "d": ("Accuracy is not a dial that produces megabytes. Each fix has its own fixed "
                  "size effect, and ticking all four left a model too weak to use."),
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
    mo.md(r"""## Part 4: When two constraints cannot both be satisfied""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Sometimes propagation does not converge. You shrink the model to fit, and the shrinking
    breaks the thing the model was for.

    Take a different system: a camera on a delivery truck watching fresh produce for spoilage.
    The obvious way to make it cheap enough to run is to halve the input resolution. Do that,
    and the small mould spots, which are the entire point, stop being visible at all.

    Now you have a **constraint conflict**. Every fix that satisfies one requirement violates
    another, and no amount of further propagation escapes it.

    There are exactly two kinds of response, and confusing them is how projects stall.
    """
    )
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w3-two">
          <div class="w3-col">
            <h4>1. Change the system</h4>
            <p class="lead">Keep every requirement. Build something cleverer.</p>
            <ul>
              <li>Find the region worth looking at first, and only run the real model there</li>
              <li>Use a tiny trigger model that wakes the big one occasionally</li>
              <li>Add a hardware accelerator to the device</li>
              <li>Change the architecture rather than the input</li>
            </ul>
          </div>
          <div class="w3-col">
            <h4>2. Change the requirement</h4>
            <p class="lead">Ask whether the requirement was ever real.</p>
            <ul>
              <li>Loosen the deadline if nothing physical depends on it</li>
              <li>Look at events rather than at every single frame</li>
              <li>Send the hard cases to a server when there is signal</li>
              <li>Put a person in the loop for the uncertain ones</li>
            </ul>
          </div>
        </div>
        <p class="w3-note">The second column is not giving up. Requirements are written by
        people, often early, often by guess. "Thirty frames a second" is a camera setting
        somebody copied, not a fact about how quickly a tomato rots.</p>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The engineering judgement is which column you are in, and you owe everyone an honest
    answer. A requirement that came from physics, like a door that is already closing, cannot
    be renegotiated. A requirement that came from a default setting can, and should be, before
    anybody spends six weeks building around it.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 5: What one stage owes the next""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    So constraints travel, and stages reopen each other. That is manageable if each stage hands
    the next one something complete. It is chaos if it does not.

    The way to stop the chaos is to agree, in advance, what a stage has to produce before it is
    allowed to call itself finished. Think of it as a **contract**: inputs, outputs, and things
    that must be true.

    | Stage | What it hands over | What must be true |
    | - | - | - |
    | **Problem** | Measurable goals and the deployment target | Every success criterion is a number |
    | **Data** | A versioned dataset with a schema and validation rules | It looks like what production will send |
    | **Model** | A reproducible artefact | It meets the metric *and* the compute budget |

    Look at the last row. "A reproducible artefact" is doing a lot of work, and the most common
    way to break the model contract is to hand over a weights file and think you are done.

    Below are the four pieces the model stage actually owes. Tick what you would hand over.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    part_weights = mo.ui.checkbox(value=True, label="**Weights** &nbsp;&middot;&nbsp; the trained numbers")
    part_code = mo.ui.checkbox(label="**Inference code** &nbsp;&middot;&nbsp; preprocessing and the forward pass")
    part_env = mo.ui.checkbox(label="**Environment** &nbsp;&middot;&nbsp; library versions, drivers, the container")
    part_config = mo.ui.checkbox(label="**Configuration** &nbsp;&middot;&nbsp; hyperparameters and runtime flags")
    mo.vstack([
        mo.md("**What goes in the hand-over?**"),
        part_weights, part_code, part_env, part_config,
    ])
    return part_code, part_config, part_env, part_weights


@app.cell(hide_code=True)
def _(LAB_CSS, mo, part_code, part_config, part_env, part_weights):
    _ = LAB_CSS
    PARTS = [
        ("Weights", part_weights.value, "The learned numbers. On their own they are a file "
         "nobody can interpret."),
        ("Inference code", part_code.value, "How an image becomes a tensor, and the exact "
         "forward pass. Resizing with a different library shifts every pixel slightly."),
        ("Environment", part_env.value, "Framework version, CUDA version, the container. "
         "Different maths libraries give different last decimal places."),
        ("Configuration", part_config.value, "Hyperparameters, thresholds, runtime flags. "
         "The decision threshold alone changes what gets flagged."),
    ]
    _cards = "".join(
        f"""
        <div class="w3-part {'on' if _on else ''}">
          <h5>{_name}</h5>
          <p>{_note if _on else 'Not handed over.'}</p>
        </div>
        """
        for _name, _on, _note in PARTS
    )
    mo.Html(f'<div class="w3-parts">{_cards}</div>')
    return (PARTS,)


@app.cell(hide_code=True)
def _(PARTS, mo):
    _missing = [_n for _n, _on, _ in PARTS if not _on]
    _consequence = {
        "Weights": "there is no model at all, only a description of one",
        "Inference code": ("production writes its own preprocessing, resizes with a different "
                           "library, and every prediction shifts a little"),
        "Environment": ("production installs whatever version is current, the maths differs in "
                        "the last decimal place, and borderline cases flip"),
        "Configuration": ("nobody knows what threshold was used, so production picks 0.5 and "
                          "the false-negative rate quietly changes"),
    }
    if not _missing:
        _msg = ("**All four.** This is the thing the deployment team can actually run, and the "
                "thing you can rebuild in a year when somebody asks why it made a particular "
                "call. Tools like MLflow exist to package exactly these four together, and a "
                "container image seals the environment half of it.")
        _kind = "success"
    else:
        _bits = chr(10).join(f"- Without **{_m.lower()}**, {_consequence[_m]}." for _m in _missing)
        _msg = ("**Incomplete hand-over.**" + chr(10) + chr(10) + _bits + chr(10) + chr(10)
                + "And here is the part that makes this dangerous: **none of these throw an "
                  "error.** The service starts, returns predictions, and logs nothing unusual. "
                  "The numbers are just quietly different from the ones you evaluated.")
        _kind = "warn"
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "What this looks like in code": mo.md(
                """
The version that breaks is short, which is why it is so common:

```python
model = DiabeticRetinopathyCNN()
train_loop(model)
torch.save(model.state_dict(), "/shared/models/latest_weights.pt")
```

One file, dropped in a shared folder. It does not record which framework version produced it,
which preprocessing the images went through, or what threshold the evaluation used. Six weeks
later someone loads it in production against a slightly different install and gets slightly
different answers, with no error to trace.

The version that holds records all four pieces as one unit:

```python
with mlflow.start_run():
    mlflow.log_params({"learning_rate": 0.001, "batch_size": 32, "threshold": 0.42})
    mlflow.log_metric("auc", 0.98)
    mlflow.pyfunc.log_model(
        artifact_path="dr_model",
        python_model=DiabeticRetinopathyModel(),   # carries its own preprocessing
    )
```

and seals the environment alongside it:

```dockerfile
FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn8-runtime
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache-dir
```

You do not need to know these tools yet. The point is that the contract is what matters, and
the tools exist because people kept breaking it.
"""
            ),
            "The same idea, one stage earlier: the data contract": mo.md(
                """
Data preparation eats most of the time on a real project, and it has its own contract. Three
things get checked, and all three are checked **at the moment data arrives**, not after
training has already used it.

**Schema.** Are the fields the right type, is anything missing, are the images the resolution
they are supposed to be? A clinic technician changes a camera setting, the resolution drops,
and nothing complains.

**Distribution.** Do the values look like what production will actually send? A dataset can be
perfectly well-formed and still be from the wrong population.

**Provenance.** Which camera, which operator, which site produced each sample? Without this you
cannot answer "is the problem coming from one clinic?", which is the first question worth
asking when something goes wrong.

Written as code, a gate is unglamorous and about eight lines:

```python
Contract = pa.DataFrameSchema({
    "image_id":      pa.Column(str, unique=True, nullable=False),
    "camera_model":  pa.Column(str, checks=pa.Check.isin(["Fundus-X10", "Fundus-V5"])),
    "resolution_w":  pa.Column(int, checks=pa.Check.geq(2048)),   # trap low-res inputs
    "mean_intensity": pa.Column(float, checks=pa.Check.between(10.0, 245.0)),
})
```

Without it, corrupt data flows into training, the model learns from it, and the pipeline
reports success at every step. That is a **data cascade**: one bad input at the top, and no
error anywhere on the way down.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q3, q3_render, q3_sum = ask(
        "**Quick check.** A team hands over only a weights file. Production loads it and serves predictions with no errors. What is the risk?",
        {
            "The service will be slower than it was in testing": "a",
            "Predictions will differ from the ones that were evaluated, with nothing to signal it": "b",
            "The model will refuse to load on different hardware": "c",
            "There is no real risk, since the weights are the model": "d",
        },
        "b",
        {
            "a": ("Speed is not the issue. The service runs at a perfectly normal speed while "
                  "giving you different answers."),
            "b": ("Preprocessing, library versions and thresholds all move the output a "
                  "little, and none of them raise an exception. The system looks healthy and "
                  "is not the system you tested."),
            "c": ("It usually loads fine. That is the problem: a loud failure would be much "
                  "easier to deal with than a quiet one."),
            "d": ("The weights are only one of four pieces. Without the other three you cannot "
                  "reproduce the behaviour you measured, which means you cannot honestly claim "
                  "the evaluation applies."),
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
    mo.md(r"""## Part 6: The failure that never crashes""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The model is deployed and the contracts held. One stage is left, and it is the one people
    skip, because it does not feel like building anything.

    Here is the whole problem in one sentence: **a model going wrong does not look like
    software going wrong.**

    When ordinary software breaks, something throws, a status code changes, an alert fires. The
    normal monitoring you already know about catches it.

    When a model breaks, the server returns `200 OK`, the response has the right shape, and the
    numbers inside it are junk. Nothing throws, because nothing is broken in the sense that
    code understands. The world simply moved away from the data the model learned on.

    Suppose one of the clinics upgrades its scanner. The new one is better, and its images are
    brighter. Every single thing the deployment team monitors stays green.

    Drag the slider and watch what the server reports, and what is actually happening.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    shift = mo.ui.slider(
        0, 40, value=0, step=2,
        label="How much brighter the new scanner's images are (mean pixel intensity)",
        show_value=True,
    )
    shift
    return (shift,)


@app.cell(hide_code=True)
def _(np, shift):
    # Two samples: what the model was trained on, and what the new scanner sends.
    # A fixed seed keeps the reading stable while only the slider moves it.
    _rng = np.random.default_rng(8018)
    N = 200
    baseline = _rng.normal(128.0, 12.0, N)
    current = _rng.normal(128.0 + float(shift.value), 12.0, N)

    # Two-sample Kolmogorov-Smirnov statistic, written out rather than imported:
    # the largest gap between the two samples' cumulative distributions.
    _all = np.sort(np.concatenate([baseline, current]))
    _cdf_a = np.searchsorted(np.sort(baseline), _all, side="right") / N
    _cdf_b = np.searchsorted(np.sort(current), _all, side="right") / N
    ks_stat = float(np.max(np.abs(_cdf_a - _cdf_b)))

    # The usual 5 per cent threshold for two samples of size N each.
    ks_critical = 1.36 * np.sqrt((N + N) / (N * N))
    drifted = ks_stat > ks_critical

    # Accuracy is not observed in production; this is what it would be if anyone measured.
    true_accuracy = max(95.0 - 0.9 * float(shift.value), 50.0)
    return baseline, current, drifted, ks_critical, ks_stat, true_accuracy


@app.cell(hide_code=True)
def _(LAB_CSS, drifted, ks_critical, ks_stat, mo, true_accuracy):
    _ = LAB_CSS
    mo.Html(
        f"""
        <div class="w3-status">
          <div class="w3-stat green">
            <span class="k">What the server reports</span>
            <span class="v">200 OK</span>
            <span class="why">0 errors, response shape correct, latency normal</span>
          </div>
          <div class="w3-stat {'red' if true_accuracy < 90 else 'green'}">
            <span class="k">What is actually true</span>
            <span class="v">{true_accuracy:.1f}% correct</span>
            <span class="why">nobody in production is measuring this</span>
          </div>
          <div class="w3-stat {'red' if drifted else 'green'}">
            <span class="k">Distribution check</span>
            <span class="v">{'DRIFT' if drifted else 'stable'}</span>
            <span class="why">largest gap {ks_stat:.3f}, alarm above {ks_critical:.3f}</span>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(drifted, mo, true_accuracy):
    if not drifted and true_accuracy >= 94.0:
        _msg, _kind = (
            "Nothing has changed yet. Both panels agree, which is the only time they ever do "
            "without you having to think about it.", "info",
        )
    elif drifted:
        _msg, _kind = (
            f"**The distribution check has fired and the server has not noticed anything.** "
            f"That single comparison is the difference between finding out today and finding "
            f"out when a clinic complains. Accuracy is at {true_accuracy:.1f} per cent and no "
            f"log line anywhere says so.", "warn",
        )
    else:
        _msg, _kind = (
            "The shift is real but still small enough that the check tolerates it. Thresholds "
            "are a judgement: set it tighter and you get woken up for nothing, looser and you "
            "find out late.", "info",
        )
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "What that check actually is": mo.md(
                """
It compares two sets of numbers and asks how far apart their shapes are.

Line up the values the model was trained on. Line up the values arriving now. Walk along both
at once, keeping track of what fraction of each sample you have passed. The **largest gap
between those two running fractions** is the whole statistic. That is the
Kolmogorov-Smirnov two-sample test, and the notebook computes it above in four lines of
numpy, with no statistics library involved.

Then you need a line to compare it against. For two samples of size $n$ each, the conventional
5 per cent threshold is

$$D_{\\text{crit}} = 1.36 \\sqrt{\\frac{2n}{n^2}}$$

which for 200 samples each comes to about 0.136. Above that, a difference this large would be
surprising if nothing had changed, so something probably changed.

**Three things worth keeping.**

It compares **inputs**, not correctness. In production you almost never know the right answer
at the time, and usually not for weeks or months. Watching the inputs is the thing you can do
today.

It tells you something moved, not what to do. Drift is a prompt to go and look, and roughly
half the time the honest conclusion is that the change is harmless.

It closes the loop. A drift alarm is the arrow from monitoring back to data collection, and it
is the only part of the lifecycle that can start itself.
"""
            ),
            "What naive monitoring looks like": mo.md(
                """
```python
def predict_and_log(request):
    try:
        features = extract_payload(request)
        prediction = production_model(features)
        logging.info(f"Status: 200 | Output shape: {prediction.shape}")
        return prediction
    except Exception as e:
        logging.error(f"Status: 500 | Error: {e}")
```

Read what is being recorded. Whether the code threw, and what shape came out. Both of those
stay perfectly healthy while a scanner upgrade quietly halves the model's accuracy.

This is not bad code. It is the right monitoring for a web service, applied to something that
is not only a web service. The missing line is one that looks at the *values* going in and
compares them with what the model was trained on.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q4, q4_render, q4_sum = ask(
        "**Quick check.** A clinic upgrades its scanner. Error rate stays at zero, latency is unchanged, accuracy has dropped by fifteen points. What catches this?",
        {
            "The exception handler, once the bad inputs cause a crash": "a",
            "The latency dashboard, since the new images are larger": "b",
            "A check that compares incoming values against the training distribution": "c",
            "Nothing can catch it; you wait for users to report it": "d",
        },
        "c",
        {
            "a": ("There is nothing to catch. Brighter images are still valid images, so the "
                  "code runs cleanly all the way through."),
            "b": ("Latency is about how long the work takes, not whether the answers are "
                  "right. It would sit perfectly flat through all of this."),
            "c": ("That comparison is the only signal available, because the correct answers "
                  "are not known at prediction time. Watch the inputs, since they arrive "
                  "immediately."),
            "d": ("That is what happens without a distribution check, and it is why this "
                  "matters. Waiting for complaints means months of wrong answers first."),
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
    mo.md(r"""## Part 7: Going round the loop, every week, without you""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Drift fires, so you retrain. Next month it fires again. This is the lifecycle, and doing it
    by hand does not scale past about two people.

    So it gets automated, and here is the shape almost every ML workflow takes:

    1. Pull last week's data from the warehouse
    2. Extract features from it
    3. Train model A, and train model B
    4. Compare A and B on the test set
    5. Deploy whichever won

    Two things about that list matter for how you run it.

    **The steps depend on each other.** Step 4 is meaningless unless 3 finished. Step 5 is
    actively dangerous unless 4 finished.

    **Step 5 depends on an outcome, not just on completion.** What gets deployed depends on
    what the comparison said. That is a **conditional** dependency, and it is where the simple
    tools stop being enough.

    Drawn out, the dependencies form a graph with arrows and no cycles: a **directed acyclic
    graph**, which everyone calls a DAG. Directed because order matters, acyclic because a loop
    would never finish. Every workflow tool you will meet asks you to describe your work as
    one.

    Now the interesting part. Below, choose a step to fail, and compare what happens under a
    plain timer against what happens under something that understands the graph.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    failure = mo.ui.radio(
        options={
            "Nothing fails": "none",
            "Step 1 fails: the warehouse export is late": "1",
            "Step 2 fails: a feature column changed type": "2",
            "Step 3a fails: model A runs out of memory": "3a",
            "Step 4 fails: the test set is missing": "4",
        },
        value="Nothing fails",
        label="**Which step fails tonight?**",
    )
    failure
    return (failure,)


@app.cell(hide_code=True)
def _(failure):
    STEPS = [
        ("1", "Pull last week's data"),
        ("2", "Extract features"),
        ("3a", "Train model A"),
        ("3b", "Train model B"),
        ("4", "Compare A and B"),
        ("5", "Deploy the winner"),
    ]
    DEPS = {"1": [], "2": ["1"], "3a": ["2"], "3b": ["2"], "4": ["3a", "3b"], "5": ["4"]}

    def _downstream(start):
        """Every step that depends on `start`, directly or through others."""
        out, changed = {start}, True
        while changed:
            changed = False
            for _step, _parents in DEPS.items():
                if _step not in out and any(p in out for p in _parents):
                    out.add(_step)
                    changed = True
        return out

    failed = failure.value
    if failed == "none":
        affected = set()
    else:
        affected = _downstream(failed) - {failed}

    # A scheduler knows the graph, so it stops. Cron knows only the clock, so every
    # later job still starts on time, using whatever files happen to be on disk.
    sched_state = {
        _id: ("failed" if _id == failed else "skipped" if _id in affected else "ran")
        for _id, _ in STEPS
    }
    cron_state = {
        _id: ("failed" if _id == failed else "stale" if _id in affected else "ran")
        for _id, _ in STEPS
    }
    return STEPS, affected, cron_state, failed, sched_state


@app.cell(hide_code=True)
def _(LAB_CSS, STEPS, cron_state, mo, sched_state):
    _ = LAB_CSS
    WORDS = {
        "ran": "ran", "failed": "failed",
        "skipped": "never started", "stale": "ran on last week's files",
    }

    def _dag(state):
        # 3a and 3b are the two training runs and sit side by side in the graph.
        def _node(_id, _label):
            _st = state[_id]
            return (f'<div class="w3-node {_st}"><span class="id">{_id}</span>'
                    f'<span class="lab">{_label}</span>'
                    f'<span class="st">{WORDS[_st]}</span></div>')

        _by_id = dict(STEPS)
        _arrow = '<span class="w3-arrow">&rarr;</span>'
        return (
            '<div class="w3-dag">'
            + _node("1", _by_id["1"]) + _arrow
            + _node("2", _by_id["2"]) + _arrow
            + '<div class="pair">' + _node("3a", _by_id["3a"]) + _node("3b", _by_id["3b"]) + '</div>'
            + _arrow + _node("4", _by_id["4"]) + _arrow + _node("5", _by_id["5"])
            + '</div>'
        )

    mo.Html(
        f"""
        <p class="w3-runhead">With a scheduler, which knows the graph</p>
        {_dag(sched_state)}
        <p class="w3-runhead">With cron, which knows only the time</p>
        {_dag(cron_state)}
        """
    )
    return


@app.cell(hide_code=True)
def _(affected, failed, mo):
    if failed == "none":
        _msg, _kind = (
            "**Everything runs, and both look identical.** They always do on a good night. "
            "Pick a step to fail, because the difference only shows up on a bad one.", "info",
        )
    elif "5" in affected:
        _msg, _kind = (
            f"**The scheduler stops. Cron deploys a model anyway.** Step {failed} failed, so "
            f"{len(affected)} later step{'s' if len(affected) > 1 else ''} had nothing valid "
            f"to work with. The scheduler knows that and refuses to start them. Cron starts "
            f"them on time regardless, they read whatever files are still sitting on disk from "
            f"last week, and something gets deployed. Everything exits zero.", "danger",
        )
    else:
        _msg, _kind = (
            f"**Step {failed} failed at the very end.** Nothing downstream was waiting on it, "
            f"so both behave the same here. That is luck, not design.", "warn",
        )
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Timers, schedulers, orchestrators: which is which": mo.md(
                """
Three words that get used interchangeably and should not be.

**cron** runs a command at a time you specify, and tells you whether it exited zero. That is
the entire feature set. It has no idea that step 4 needs step 3, so it cannot wait, cannot
retry sensibly, and cannot stop the rest of the chain when something upstream fails.

**A scheduler** is cron that understands dependencies. Give it the DAG and it works out what
can start, holds back what cannot, retries what is worth retrying, and stops the branch when
something fails for good. It also thinks about **resources**: this job needs 8 GB and two CPUs,
so it waits for a machine with 8 GB and two CPUs and queues it there. Slurm is the one you will
meet on a university cluster, where you write down the job name, the memory and the core count
and it finds you a slot.

**An orchestrator** answers a different question. The scheduler decides *when* a job runs and
*what it needs*; the orchestrator decides *where the machines come from*. If there is more work
than machines, it starts more machines. Kubernetes is the one everybody means by this.

They stack: a scheduler usually runs on top of an orchestrator. The reason the words blur is
that the real tools all reach a little into each other's territory.
"""
            ),
            "The tools you will hear named": mo.md(
                """
All of these are ways to write down a DAG and have something run it. The differences are real
but small next to the fact that they all do the same job.

**Airflow** came first, in 2014, and is still everywhere. Workflows are written in Python,
which was a deliberate stand against configuration files. Its age shows in three places: the
whole workflow is packaged as one unit, so two steps cannot easily have different requirements;
workflows cannot take parameters, so running the same pipeline with a different learning rate
means writing a second pipeline; and the graph is fixed before it runs, so it cannot create a
step per record when it does not know how many records there are.

**Argo** fixed the container problem. Every step runs in its own container, workflows take
parameters, and the graph can change as it runs. The cost is YAML, which gets long, and a hard
dependency on Kubernetes, which means you cannot easily run the same thing on your laptop.

**Prefect** fixed the parameters problem while staying in Python, and is pleasant to use, but
containers are not its first concern.

**Kubeflow** and **Metaflow** aim at the gap between your laptop and production: write it once,
run it small locally and large on the cluster.

**MLflow** is a different animal and often confused with these. It is not a workflow runner. It
tracks experiments, stores metrics and parameters, and packages models, which is the artefact
side of Part 5 rather than the scheduling side of Part 7.

You do not need to choose one today. You need to recognise that "Airflow" or "Argo" is an
answer to "how do we run the DAG", and not an answer to "what should the DAG be".
"""
            ),
            "Where all this actually runs": mo.md(
                """
Underneath the workflow tools sit four layers, and it is worth knowing the names because
people will say them as if you already do.

**Storage.** Where the data lives. For ML this usually means object storage, which is buckets
and objects rather than folders and files: S3 in the cloud, or something like MinIO if you are
running your own. It has to cope with very large numerical arrays, with data types from tables
to images to audio, with versions of both datasets and models, and with a surprising volume of
intermediate junk like checkpoints and gradients.

**Compute.** The machines. Measured in memory and in operations per second, and rented by the
hour, which is why cloud compute suits ML so well: experiments come in bursts, and you pay for
the burst rather than for a data centre that idles the rest of the year.

**Resource management.** The schedulers and orchestrators from this part.

**ML platform.** The shared tools every project in a company ends up needing: somewhere to
store models, somewhere to store features, somewhere to watch them. These usually get built
once by whichever team needed them first, and then everybody else adopts them.

How much of this you need depends entirely on scale. One model for one app needs none of it.
A company handling terabytes a day with a hundred data scientists needs all four, and will
argue about them constantly.
"""
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q5, q5_render, q5_sum = ask(
        "**Quick check.** Your five steps run on cron, one per hour. Tonight, feature extraction fails. What happens at 3am when the deploy job fires?",
        {
            "Cron skips it, because the earlier job failed": "a",
            "Cron retries feature extraction first, then continues": "b",
            "It runs on schedule using last week's leftover files, and deploys something": "c",
            "It waits until feature extraction succeeds": "d",
        },
        "c",
        {
            "a": ("cron does not know one job has anything to do with another. It knows the "
                  "time, and at 3am it is 3am."),
            "b": ("Retrying on failure needs someone to know that a failure happened and that "
                  "it mattered. That is a scheduler's job, not a timer's."),
            "c": ("This is the whole argument for schedulers. Every job exits zero, the "
                  "pipeline looks successful, and a model trained on stale features is now "
                  "live."),
            "d": ("Waiting for something means knowing what to wait for. cron has no concept "
                  "of one job depending on another."),
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
    mo.md(r"""## Part 8: Putting it to work""")
    return


@app.cell(hide_code=True)
def _(LAB_CSS, mo):
    _ = LAB_CSS
    mo.Html(
        """
        <div class="w3-question">
          <span class="lbl">The situation</span>
          <p>"Our trucks carry fresh produce through areas with no signal for hours. We want a
          camera in the trailer that spots spoilage and alerts the driver. We have four hundred
          trucks, so the board in each one has to be cheap: a small ARM computer, 1 GB of
          memory, no accelerator. The camera gives us 4K at thirty frames a second. The data
          science team has handed us a model that is 99 per cent accurate, takes 2 GB, and
          needs 400 ms per frame on that board. They developed it on a cloud GPU."</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Before choosing, notice what is actually broken, and by how much.

    | What was promised | What the model does | Over by |
    | - | - | - |
    | 33 ms per frame, which is what thirty a second means | 400 ms per frame | 12 times |
    | 1 GB of memory on the board | 2 GB | 2 times |

    The timing is the bad one, and it is bad enough that no amount of shrinking reaches it. On
    top of that the board cannot be changed cheaply and the network is not there at all.

    So one of the four requirements has to give, and which one you pick says what you think the
    system is for.
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
                    "Change the system: a tiny model checks each frame, the big one only looks at suspicious regions": "system",
                    "Change the requirement: check one frame a second instead of thirty, because produce spoils over hours": "requirement",
                    "Change the machine: pay for a better processor in every truck": "machine",
                },
                label="**What would you do?**",
            ),
            why=mo.ui.text_area(
                placeholder="Which requirement did you decide was negotiable, and what makes you think so?",
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
        "system": ("The engineer's answer, and it works: a cheap model on every frame, the "
                   "expensive one only where something looks wrong. Be honest about the cost "
                   "though. You now have two models, two sets of weights to keep in step, and "
                   "a new failure mode where the cheap model misses something and the "
                   "expensive one never gets asked. The 2 GB problem is also still sitting "
                   "there, so this has to be combined with making the big model fit."),
        "requirement": ("The cheapest fix available, and the one most teams argue about "
                        "longest. Nobody chose thirty frames a second because spoilage needs "
                        "it; it is what the camera does by default. Produce rots over hours, "
                        "so one frame a second is already 3,600 looks an hour at the same "
                        "thing. That single sentence buys you 1,000 ms per frame against a "
                        "400 ms model, and the entire timing problem disappears without a "
                        "line of code. Memory is still a real problem and still needs Week "
                        "2's answers."),
        "machine": ("Sometimes correct, and worth pricing rather than dismissing. But count "
                    "the fleet. Whatever the better board costs, multiply it by four hundred, "
                    "then add fitting it, maintaining it, and the extra power it draws in a "
                    "vehicle. And to close a twelve-fold timing gap you are not looking at a "
                    "slightly better board. It also leaves the underlying problem untouched: "
                    "a model developed on a cloud GPU with no target hardware in mind will do "
                    "this again next year."),
    }
    mo.vstack([
        mo.md("### On your answer"),
        mo.callout(mo.md(_notes[decision_choice]), kind="info"),
        mo.md(
            "All three are used in real systems, and the exercise was never about picking the "
            "right one. It was about noticing that **the thirty frames a second was a "
            "requirement nobody had checked**, and that a requirement is a thing you are "
            "allowed to question before you spend six weeks building around it."
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
                placeholder="The stage that has to be redone is... because...",
                label="**Last one.** Name one stage *upstream* of your fix that now has to be redone, and say what specifically changes in it.",
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
    accuracy,
    chosen,
    decision_choice,
    decision_why,
    done,
    mo,
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
    reopened,
    shippable,
    size_mb,
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
        "system": "Change the system, with a cheap trigger model",
        "requirement": "Change the requirement, one frame a second",
        "machine": "Change the machine, a better processor per truck",
    }
    _fix_names = ", ".join(_n for _n, *_ in chosen) or "none"
    _stage_names = ", ".join(sorted(reopened - {"Deployment"})) or "none beyond deployment"
    _verdict = "ships" if shippable else "does not ship"

    mo.vstack([
        mo.md("## Your Week 3 report"),
        mo.Html(
            f"""
            <div class="w3-report">
              <div class="row">
                <span class="k">Fixes you applied</span>
                <span class="v">{_fix_names}</span>
              </div>
              <div class="row">
                <span class="k">Where that left you</span>
                <span class="v">{size_mb:.0f} MB at {accuracy:.1f} per cent, which {_verdict}</span>
              </div>
              <div class="row">
                <span class="k">Stages reopened</span>
                <span class="v">{_stage_names}</span>
              </div>
              <div class="row">
                <span class="k">The truck decision</span>
                <span class="v">{_where.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Why</span>
                <span class="v quote">{decision_why}</span>
              </div>
              <div class="row">
                <span class="k">What has to be redone</span>
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
    accuracy,
    chosen,
    decision_choice,
    decision_why,
    done,
    json,
    mo,
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
    reopened,
    shippable,
    size_mb,
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

    _fixes = [_n for _n, *_ in chosen]
    _stages = sorted(reopened)

    submission = {
        "lab": "CSC/EE 8001 - Week 3",
        "fixes_applied": _fixes,
        "final_size_mb": round(size_mb, 1),
        "final_accuracy_pct": round(accuracy, 1),
        "ships": shippable,
        "stages_reopened": _stages,
        "truck_decision": decision_choice,
        "why": decision_why,
        "stage_to_redo": takeaway_text,
        "check_1_when_the_constraint_should_bite": {"answer": _a1[0], "correct": _a1[1]},
        "check_2_why_quantising_was_not_enough": {"answer": _a2[0], "correct": _a2[1]},
        "check_3_weights_only_handover": {"answer": _a3[0], "correct": _a3[1]},
        "check_4_what_catches_drift": {"answer": _a4[0], "correct": _a4[1]},
        "check_5_cron_versus_scheduler": {"answer": _a5[0], "correct": _a5[1]},
    }

    report_text = chr(10).join([
        "CSC/EE 8001 - Week 3",
        "=" * 40,
        "",
        "FIXES I APPLIED",
        "  " + (", ".join(_fixes) or "none"),
        "",
        "WHERE THAT LEFT ME",
        f"  {size_mb:.0f} MB at {accuracy:.1f} per cent "
        f"({'ships' if shippable else 'does not ship'})",
        "",
        "STAGES REOPENED",
        "  " + ", ".join(_stages),
        "",
        "THE TRUCK DECISION",
        f"  {decision_choice}",
        "",
        "WHY",
        f"  {decision_why}",
        "",
        "WHAT HAS TO BE REDONE",
        f"  {takeaway_text}",
        "",
        "QUICK CHECKS",
        "  When the memory constraint should have started to matter",
        f"    {_a1[0]}  [{_word(_a1[1])}]",
        "  Why quantising alone did not close the gap",
        f"    {_a2[0]}  [{_word(_a2[1])}]",
        "  What is missing when only weights are handed over",
        f"    {_a3[0]}  [{_word(_a3[1])}]",
        "  What catches a silent accuracy drop",
        f"    {_a4[0]}  [{_word(_a4[1])}]",
        "  What cron does when an earlier job fails",
        f"    {_a5[0]}  [{_word(_a5[1])}]",
    ])

    mo.accordion({
        "A copy of what you did": mo.vstack([
            mo.hstack(
                [
                    mo.download(data=report_text.encode("utf-8"),
                                filename="week3_report.txt", label="Download my report"),
                    mo.download(data=json.dumps(submission, indent=2).encode("utf-8"),
                                filename="week3_report.json", label="Download as JSON"),
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
            "What is the difference between the workflow and the lifecycle?":
                mo.md(
                    "The workflow is the five stages: data collection, model development, "
                    "evaluation, deployment, monitoring. The lifecycle is going round them "
                    "repeatedly, because monitoring feeds back into data collection. A "
                    "project that treats the five as a line finishes once and then rots. A "
                    "project that treats them as a circle has somewhere for a drift alarm to "
                    "go."
                ),
            "Why can a constraint discovered at deployment not usually be fixed at deployment?":
                mo.md(
                    "Because deployment has almost no freedom left. The architecture is "
                    "chosen, the data is collected, the model is trained. All that is "
                    "available there are small fixed-ratio tricks like quantisation. If the "
                    "gap is larger than those tricks, the constraint has to travel back to a "
                    "stage that still has real choices to make, and in this lab the only "
                    "combinations that worked were the ones that reached back as far as data "
                    "collection."
                ),
            "Someone hands you a weights file and says the model is done. What do you ask for?":
                mo.md(
                    "The inference code, including preprocessing; the environment, meaning "
                    "library versions and drivers, usually as a container; and the "
                    "configuration, meaning hyperparameters and thresholds. Without all four "
                    "you cannot reproduce the behaviour that was measured, so the evaluation "
                    "you were shown does not describe what production will do. Nothing about "
                    "this failure is loud, which is exactly why you have to ask up front."
                ),
            "Why is monitoring an ML system different from monitoring a web service?":
                mo.md(
                    "A web service fails loudly: it throws, it returns a 500, latency spikes. "
                    "A model fails silently: the code runs, the response has the right shape, "
                    "and the values in it are wrong because the world moved. Standard "
                    "monitoring catches none of that, so you watch the input distribution "
                    "instead, since the inputs arrive immediately and the correct answers "
                    "often never do."
                ),
            "Why does a workflow need a scheduler rather than a timer?":
                mo.md(
                    "Because the steps depend on each other and one of them depends on an "
                    "outcome rather than on completion. A timer runs each job when its clock "
                    "says so, whether or not the job it needed has produced anything, which "
                    "is how a model trained on stale features ends up deployed with every "
                    "exit code at zero. A scheduler takes the DAG, holds back what cannot "
                    "start, retries what is worth retrying, and stops the branch when "
                    "something genuinely failed."
                ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
