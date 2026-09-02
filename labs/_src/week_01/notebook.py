import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week 1 - Why the Model Is Not the System")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import math
    import json
    import numpy as np
    from urllib.parse import quote
    return json, math, mo, np, quote


@app.cell(hide_code=True)
def _():
    # ---------------------------------------------------------------------------
    # WHERE STUDENTS HAND THIS IN.
    #
    # Leave HANDIN_URL empty and the lab simply asks them to download the report
    # and upload it wherever you normally collect work. Nothing breaks.
    #
    # To collect answers automatically instead:
    #   1. Build a form in Microsoft Forms (a Quiz if you want it auto-marked).
    #   2. Open it, choose "Collect responses", then "Get pre-filled URL".
    #   3. Fill every question in with the placeholder word shown below, generate
    #      the link, and paste the whole thing here.
    #
    # Placeholders the lab will substitute, spelled exactly like this:
    #   GUESSHERE       what they guessed
    #   REASONHERE      why they guessed it
    #   BATCHHERE       the batch size they settled on
    #   WAITHERE        the wait their choice produces
    #   DECISIONHERE    ship / ship with a second machine / do not ship
    #   WHYHERE         their reasoning for that decision
    #   STOPPEDHERE     what they said actually decided whether it could ship
    # ---------------------------------------------------------------------------
    HANDIN_URL = ""
    return (HANDIN_URL,)


@app.cell(hide_code=True)
def _(mo):
    def one_shot(prompt, options, correct, explain):
        """Build a multiple choice question that can only be answered once.

        Students get a single attempt on purpose. If they could keep changing the
        answer until the box turned green, the question would measure nothing and
        they would learn nothing from getting it wrong.

        Returns (form, render). Pass the latched answer to render(): None shows the
        question, anything else shows their answer and the explanation, with no way
        back to the options.
        """
        labels = {value: label for label, value in options.items()}
        BREAK = chr(10) + chr(10)          # a blank line, i.e. a new paragraph

        form = (
            mo.md("{choice}")
            .batch(choice=mo.ui.radio(options=options, label=prompt))
            .form(
                submit_button_label="Lock in my answer",
                bordered=True,
                validate=lambda v: None if v and v.get("choice") else "Choose an answer first.",
            )
        )

        def render(locked):
            if locked is None:
                return mo.vstack([
                    form,
                    mo.callout(
                        mo.md("One answer each, so have a think first. You are **not marked "
                              "on getting these right**. They are here so you find out "
                              "what you actually think, and the explanation afterwards is the "
                              "part that matters."),
                        kind="neutral",
                    ),
                ])
            ok = locked == correct
            body = ("**Correct.** " if ok else "**Not quite.** ") + explain[locked]
            if not ok:
                body += BREAK + f"The answer was: *{labels[correct]}*"
            return mo.vstack([
                mo.md(prompt + BREAK + f"You answered: *{labels[locked]}*"),
                mo.callout(mo.md(body), kind="success" if ok else "danger"),
            ])

        return form, render
    return (one_shot,)


@app.cell(hide_code=True)
def _(mo):
    LAB_CSS = mo.Html(
        """
        <style>
          .rl-hero { border: 1px solid #e6e6e6; border-left: 6px solid #f1b82d;
                     background: #fffef8; border-radius: 12px; padding: 20px 24px; }
          .rl-eyebrow { color: #6a5314; font-size: .76rem; font-weight: 800;
                        letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
          .rl-hero h1 { margin: 0 0 8px; font-size: 1.75rem; color: #111; line-height: 1.2; }
          .rl-hero p.sub { margin: 0; color: #3a3a3a; font-size: 1.02rem; line-height: 1.65; }

          .rl-grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 18px 0; }
          @media (max-width: 860px) { .rl-grid2 { grid-template-columns: 1fr; } }

          .rl-card { border: 1px solid #e6e6e6; border-radius: 12px; background: #fff;
                     padding: 16px 18px; }
          .rl-card h4 { margin: 0 0 8px; font-size: 1.02rem; color: #111; }
          .rl-card p { margin: 0; color: #3a3a3a; font-size: .95rem; line-height: 1.6; }
          .rl-card ul { margin: 6px 0 0; padding-left: 18px; color: #3a3a3a;
                        font-size: .95rem; line-height: 1.6; }
          .rl-card-bad  { background: #fef6f6; border-left: 5px solid #c62828; }
          .rl-card-good { background: #f6fbf7; border-left: 5px solid #2e7d32; }

          .rl-steps { counter-reset: rlstep; margin: 16px 0; }
          .rl-step { position: relative; padding: 14px 0 14px 48px;
                     border-bottom: 1px solid #f0f0f0; }
          .rl-step:last-child { border-bottom: 0; }
          .rl-step::before { counter-increment: rlstep; content: counter(rlstep);
                             position: absolute; left: 0; top: 14px;
                             width: 32px; height: 32px; border-radius: 50%;
                             background: #f1b82d; color: #111; font-weight: 800;
                             display: flex; align-items: center; justify-content: center; }
          .rl-step h5 { margin: 0 0 4px; font-size: 1rem; color: #111; }
          .rl-step p { margin: 0; color: #444; font-size: .95rem; line-height: 1.6; }

          .rl-kpi { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 10px 0; }
          @media (max-width: 860px) { .rl-kpi { grid-template-columns: 1fr; } }
          .rl-kpi div { border: 1px solid #e6e6e6; border-radius: 10px;
                        background: #fff; padding: 12px 14px; }
          .rl-kpi .k { color: #4a4a4a; font-size: .76rem; font-weight: 800;
                       letter-spacing: .05em; text-transform: uppercase; }
          .rl-kpi .v { color: #111; font-size: 1.4rem; font-weight: 800; line-height: 1.25; }
          .rl-kpi .n { color: #6f6f6f; font-size: .82rem; line-height: 1.4; }
          .rl-ok   { border-left: 5px solid #2e7d32 !important; }
          .rl-bad  { border-left: 5px solid #c62828 !important; }

          .rl-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                      align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .rl-split { grid-template-columns: 1fr; } }
          .rl-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                font-size: 1rem; line-height: 1.7; }
          .rl-split > .body p:last-child { margin-bottom: 0; }

          .rl-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                      border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .rl-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .rl-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .rl-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                         margin-bottom: 9px; }
          .rl-aside li:last-child { margin-bottom: 0; }
          .rl-aside li::marker { color: #6a5314; font-weight: 800; }
          .rl-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                              padding-top: 11px; padding-left: 24px; }
          .rl-aside .meta div { display: flex; justify-content: space-between;
                                gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .rl-aside .meta div:last-child { margin-bottom: 0; }
          .rl-aside .meta dt { color: #6f6f6f; }
          .rl-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }

          .rl-question { border: 1px solid #f2dfaa; background: #fffdf5;
                         border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .rl-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                              letter-spacing: .06em; text-transform: uppercase; }
          .rl-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                           line-height: 1.55; font-style: italic; }

          .rl-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
          .rl-chip { border: 1px solid #f2dfaa; background: #fff3cc; color: #62490a;
                     border-radius: 999px; padding: 4px 11px; font-size: .72rem;
                     font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
          .rl-chip-plain { border-color: #e0e0e0; background: #f4f4f4; color: #4a4a4a; }

          .rl-conseq { border: 1px solid #e6e6e6; border-left: 5px solid #6a5314;
                       background: #fbfbfb; border-radius: 10px; padding: 13px 17px;
                       margin: 18px 0; }
          .rl-conseq .lbl { color: #6a5314; font-weight: 800; font-size: .74rem;
                            letter-spacing: .06em; text-transform: uppercase; }
          .rl-conseq p { margin: 6px 0 0; color: #2f2f2f; font-size: .97rem; line-height: 1.65; }

          .rl-bar { display: flex; height: 62px; border-radius: 10px; overflow: hidden;
                    border: 1px solid #e6e6e6; margin: 18px 0 0; }
          .rl-bar .model { flex: 5; background: #f1b82d; }
          .rl-bar .rest  { flex: 95; background: #f4f4f4;
                           border-left: 2px solid #e0a91c; }
          .rl-key { display: flex; flex-wrap: wrap; gap: 10px 28px; margin: 12px 0 0;
                    font-size: .93rem; color: #3a3a3a; line-height: 1.5; }
          .rl-key span { display: inline-flex; align-items: baseline; gap: 8px; }
          .rl-key i { flex: 0 0 auto; width: 13px; height: 13px; border-radius: 3px;
                      display: inline-block; transform: translateY(1px); }
          .rl-key i.gold { background: #f1b82d; border: 1px solid #e0a91c; }
          .rl-key i.grey { background: #f4f4f4; border: 1px solid #dcdcdc; }
          .rl-key .n { color: #111; font-weight: 800; }
          .rl-barhead { margin: 0 0 4px; font-size: 1.2rem; color: #111; font-weight: 700; }


        </style>
        """
    )
    LAB_CSS
    return (LAB_CSS,)


@app.cell(hide_code=True)
def _(mo):
    LAB_CSS_B = mo.Html(
        """
        <style>
          .lab-hero { border: 1px solid #e6e6e6; border-left: 5px solid #f1b82d;
                      background: #fffef8; border-radius: 12px;
                      padding: 18px 22px; margin-bottom: 6px; }
          .lab-eyebrow { color: #6a5314; font-size: .78rem; font-weight: 800;
                         letter-spacing: .06em; text-transform: uppercase; margin: 0 0 6px; }
          .lab-hero h1 { margin: 0 0 6px; font-size: 1.6rem; color: #111; line-height: 1.25; }
          .lab-hero p.sub { margin: 0; color: #4a4a4a; font-size: 1rem; }
          .lab-case { border: 1px solid #e6e6e6; border-left: 5px solid #6a5314;
                      background: #fbfbfb; border-radius: 10px; padding: 14px 18px; }
          .lab-case strong.who { color: #6a5314; }
          .lab-kpi { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 6px 0; }
          .lab-kpi div { border: 1px solid #e6e6e6; border-radius: 10px;
                         background: #fff; padding: 12px 14px; }
          .lab-kpi .k { color: #4a4a4a; font-size: .76rem; font-weight: 800;
                        letter-spacing: .05em; text-transform: uppercase; }
          .lab-kpi .v { color: #111; font-size: 1.45rem; font-weight: 800; line-height: 1.2; }
          .lab-kpi .n { color: #6f6f6f; font-size: .8rem; }
          .lab-pass { border-left: 5px solid #2e7d32 !important; }
          .lab-fail { border-left: 5px solid #c62828 !important; }
          .lab-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px;
                       align-items: start; margin: 4px 0; }
          @media (max-width: 900px) { .lab-split { grid-template-columns: 1fr; } }
          .lab-split > .body p { margin: 0 0 12px; color: #2f2f2f;
                                 font-size: 1rem; line-height: 1.7; }
          .lab-split > .body p:last-child { margin-bottom: 0; }
          .lab-aside { border: 1px solid #e6e6e6; border-top: 4px solid #f1b82d;
                       border-radius: 12px; background: #fcfcfc; padding: 15px 17px; }
          .lab-aside h4 { margin: 0 0 10px; padding-left: 24px; font-size: .76rem;
                         color: #6a5314; font-weight: 800; letter-spacing: .06em;
                         text-transform: uppercase; }
          .lab-aside ol { margin: 0; padding-left: 24px; list-style: decimal outside; }
          .lab-aside li { color: #2f2f2f; font-size: .91rem; line-height: 1.5;
                          margin-bottom: 9px; }
          .lab-aside li:last-child { margin-bottom: 0; }
          .lab-aside li::marker { color: #6a5314; font-weight: 800; }
          .lab-aside .meta { border-top: 1px solid #ececec; margin-top: 13px;
                              padding-top: 11px; padding-left: 24px; }
          .lab-aside .meta div { display: flex; justify-content: space-between;
                                 gap: 10px; font-size: .85rem; margin-bottom: 6px; }
          .lab-aside .meta div:last-child { margin-bottom: 0; }
          .lab-aside .meta dt { color: #6f6f6f; }
          .lab-aside .meta dd { margin: 0; color: #111; font-weight: 700; text-align: right; }
          .lab-question { border: 1px solid #f2dfaa; background: #fffdf5;
                          border-radius: 12px; padding: 14px 18px; margin: 18px 0; }
          .lab-question .lbl { color: #6a5314; font-size: .74rem; font-weight: 800;
                               letter-spacing: .06em; text-transform: uppercase; }
          .lab-question p { margin: 6px 0 0; color: #111; font-size: 1.06rem;
                            line-height: 1.55; font-style: italic; }
          .lab-report { border: 1px solid #e6e6e6; border-top: 5px solid #f1b82d;
                        border-radius: 12px; background: #fff; padding: 4px 20px 16px;
                        box-shadow: 0 8px 20px rgba(17, 17, 17, .06); margin: 6px 0 4px; }
          .lab-report .row { display: grid; grid-template-columns: 190px 1fr; gap: 16px;
                             padding: 12px 0; border-bottom: 1px solid #f2f2f2;
                             align-items: baseline; }
          .lab-report .row:last-child { border-bottom: 0; }
          @media (max-width: 720px) {
            .lab-report .row { grid-template-columns: 1fr; gap: 3px; }
          }
          .lab-report .k { color: #6a5314; font-size: .74rem; font-weight: 800;
                           letter-spacing: .06em; text-transform: uppercase; }
          .lab-report .v { color: #1c1c1c; font-size: .99rem; line-height: 1.55; }
          .lab-report .v em { color: #444; }
          .lab-report .tick { color: #2e7d32; font-weight: 800; }
          .lab-report .cross { color: #c62828; font-weight: 800; }
          .lab-report .quote { border-left: 3px solid #f1b82d; padding-left: 12px;
                               color: #333; font-style: italic; }
          .handin-btn { display: inline-block; padding: 12px 22px; border-radius: 999px;
                        background: #f1b82d; border: 1px solid #e0a91c; color: #111;
                        font-size: 1rem; font-weight: 800; text-decoration: none;
                        box-shadow: 0 6px 16px rgba(241, 184, 45, .35); }
          .handin-btn:hover { background: #e8ad19; color: #111; text-decoration: none; }
        </style>
        """
    )
    LAB_CSS_B
    return (LAB_CSS_B,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="rl-hero">
          <p class="rl-eyebrow">CSC/EE 8001 &middot; Week 1</p>
          <h1>Why the Model Is Not the System</h1>
          <p class="sub">Welcome to the first class lab. Nothing to install, nothing to set up.
          The first half shows you why a good model is not the same thing as a working system.
          The second half hands you a real decision and asks you to defend it.</p>
          <div class="rl-chips">
            <span class="rl-chip">Why systems, not models</span>
            <span class="rl-chip">Where the time goes</span>
            <span class="rl-chip">No prerequisites</span>
            <span class="rl-chip-plain rl-chip">Lab v1.0.0</span>
            <span class="rl-chip-plain rl-chip">Report made on your machine</span>
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
        <div class="rl-split">
          <div class="body">
            <p>Most of you have trained a model before. You loaded a dataset, fit something,
            printed an accuracy score, and it worked. That is a real skill and you will use it
            constantly.</p>
            <p>This course is about the part that comes after. It turns out that getting a model
            to be accurate and getting a model to be <em>useful to actual people</em> are two
            different problems, and the second one is where almost all the difficulty lives.</p>
            <p>These labs are how you practise the second one. There is no maths to grind
            through here and nothing to install. Read, poke at one example, and answer two
            questions at the end.</p>
          </div>
          <aside class="rl-aside">
            <h4>By the end you can</h4>
            <ol>
              <li>Explain why a good accuracy score does not mean a system is ready to use.</li>
              <li>Say where the time actually goes when a system answers a request.</li>
              <li>Defend a design decision with numbers instead of a hunch.</li>
            </ol>
            <div class="meta">
              <div><dt>Time</dt><dd>about 30 min</dd></div>
              <div><dt>You need</dt><dd>nothing</dd></div>
              <div><dt>Hand in</dt><dd>one short report</dd></div>
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
        <div class="rl-question">
          <span class="lbl">The question this lab answers</span>
          <p>"What will these labs actually ask me to do, and why are they built that way?"</p>
        </div>
        <p style="color:#3a3a3a; line-height:1.7;"><strong>What is coming up.</strong>
        Parts 1 to 3 are the why: the number that explains this course, the gap between a
        model that works and a system you can use, and why this is harder than ordinary
        software. Parts 4 to 8 are the real thing: a decision your manager is waiting on, the
        evidence to settle it, and a report you hand in.</p>

        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 1: You have trained a model. Have you shipped one?""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Put your hand up if you have ever trained a model.

    Now keep it up if you have ever put one in front of real people, and kept it running.

    In most rooms, nearly every hand goes up for the first question and nearly all of them come
    down for the second. That gap is the entire course.

    This is not a class about machine learning algorithms. You will not be deriving
    backpropagation here. The question we keep asking is the one that starts *after* somebody
    hands you a trained model: **what does it take to actually serve this to people, and what
    is physically possible when you try?**
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The systems you already use have brutal deadlines

    You interact with deployed ML many times a day without noticing. What you do not see is how
    little time each one has to answer.

    | System | Has to respond in |
    | - | - |
    | Voice assistant | 400 to 600 ms today, but humans expect a 200 ms conversational gap |
    | Social media feed ranking | 60 to 200 ms, billions of times a day |
    | Spam filtering | 1 to 5 ms per email, billions a day |
    | Face ID on your phone | 1 to 2 ms, on a battery, without getting warm |

    Nobody in those teams shipped because a notebook said 94%. They shipped because the whole
    system met a hard number, every time, under load.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <p class="rl-barhead">Where the work actually is</p>
        <p style="color:#3a3a3a; line-height:1.7; margin:0;">If you took a real machine
        learning system and measured where the engineering effort went, it would look like
        this.</p>
        <div class="rl-bar" role="img" aria-label="A bar split five per cent to model code and
             ninety-five per cent to everything else">
          <div class="model"></div>
          <div class="rest"></div>
        </div>
        <div class="rl-key">
          <span><i class="gold"></i><span class="n">5%</span> the model</span>
          <span><i class="grey"></i><span class="n">95%</span> data, pipelines, serving,
          monitoring, and keeping the whole thing alive</span>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    That thin gold strip is the part everyone finds interesting. It is what every tutorial is
    about, and it is the part you are already good at.

    The rest of the bar is not the boring admin around the interesting bit. **It is the reason
    most projects never launch.** Depending on whose survey you read, somewhere between 60 and
    85 per cent of machine learning projects never make it in front of a real user at all, and
    it is almost never because the model was not accurate enough.

    The reason is that research and production are not the same game. Research gets a fixed
    dataset, one machine, and one number to push up. Production gets data that keeps changing,
    a pile of different hardware, and has to be accurate *and* fast *and* affordable at the
    same time. A better model does not fix that.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo, one_shot):
    get_q0, set_q0 = mo.state(None)
    q0_form, q0_render = one_shot(
        "**Quick check.** Why do most ML projects never make it to production?",
        {
            'Because the models being used are not accurate enough yet': 'a',
            'Because most of the work is data and infrastructure, and that is where projects fail': 'b',
            'Because companies do not have enough GPUs': 'c',
            'Because the datasets used in research are too small': 'd',
        },
        'b',
        {
            'a': ("This is the assumption those numbers contradict. Plenty of dead projects "
                  "had a perfectly good model sitting in a notebook. It never got out."),
            'b': ("Ninety per cent of the effort is data and infrastructure, and that is exactly "
                  "where things go wrong. The model was rarely the problem."),
            'c': ("Hardware matters, and we spend real time on it. But it is one slice of the "
                  "ninety-five per cent, not the whole story."),
            'd': ("Data quality and drift genuinely matter, and there is a lab on that later. But "
                  "the answer here is bigger than dataset size."),
        },
    )
    return get_q0, set_q0, q0_form, q0_render


@app.cell(hide_code=True)
def _(q0_form, get_q0, set_q0):
    if q0_form.value is not None and get_q0() is None:
        set_q0(q0_form.value["choice"])
    return


@app.cell(hide_code=True)
def _(get_q0, q0_render):
    q0_render(get_q0())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 2: A good model is not the same thing as a working system""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is a situation you will meet again and again.

    You build something in a notebook. It gets 94% accuracy on your test set. You are pleased,
    and you should be. You show it to someone and they ask a completely reasonable question:

    > *"Great. Can we use it?"*

    And you realise you have no idea. Because you have never asked what happens when a thousand
    people use it at once, or how much it costs to run for a month, or how long a person is
    willing to wait for an answer, or what it does when it gets something it has never seen.

    That gap between *the model works* and *we can use this* is what this course is about.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="rl-grid2">
          <div class="rl-card rl-card-bad">
            <h4>The question you already know how to answer</h4>
            <p><em>Is the model accurate?</em></p>
            <p style="margin-top:8px">It is one number, measured on data you chose, on a machine
            you were not paying for, with nobody waiting on the other end. It matters. It is
            just nowhere near enough.</p>
          </div>
          <div class="rl-card rl-card-good">
            <h4>The questions this course adds</h4>
            <ul>
              <li>Where does it run, and does it fit there?</li>
              <li>How long does someone wait for an answer?</li>
              <li>What does a month of this cost?</li>
              <li>What breaks first when it gets busy?</li>
              <li>How would you know it had quietly stopped working?</li>
              <li>Could you convince a sceptical person you are right?</li>
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
    Notice that not one of those questions is answered by a better model. They are answered by
    understanding the *system the model sits inside*: the machine, the memory, the network,
    the people waiting, the budget.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="rl-conseq">
          <span class="lbl">So what follows from that</span>
          <p>Deployment is not a tidying-up job you do at the end, once the interesting part is
          finished. It is usually the thing that decides whether the project happens at all. A
          team can spend months lifting accuracy by two points and then discover the whole idea
          was never going to fit on the hardware they had. That is an expensive way to find out,
          and it is the failure this course is trying to teach you to see coming.</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 3: When it breaks, nothing happens""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    There is a fair objection to everything so far. Computer science has been building large,
    complicated software systems for fifty years and got quite good at it. Why should machine
    learning be any different?

    Because of one thing: **when an ML system breaks, nothing happens.**
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="rl-grid2">
          <div class="rl-card rl-card-good">
            <h4>Ordinary software fails loudly</h4>
            <p>There is a bug, so it crashes. You get a stack trace within milliseconds. You
            read the lines, you find the mistake, you fix it, and it stays fixed.</p>
          </div>
          <div class="rl-card rl-card-bad">
            <h4>ML fails silently</h4>
            <p>There is no crash. It keeps running. It keeps returning predictions. Everything
            looks healthy on every dashboard you have. It is simply, quietly, becoming wrong.</p>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is the shape it usually takes. A spam filter is trained on last year's spam and
    catches 94% of it. Nothing about it changes. Nobody touches the code.

    But the people sending spam do change. They try new wording, new subject lines, new tricks,
    precisely because the old ones stopped working. Month by month, the filter catches a little
    less. By the spring it is somewhere around 80%, and a fifth of the spam is going straight
    to inboxes.

    **Nothing failed.** No error was thrown, no alert fired, every line ran exactly as written,
    and every dashboard was green. If you opened the code looking for the bug, you would not
    find one, because there isn't one.

    **So what do you actually debug?** Not the code. The world it was trained on moved, and the
    model stayed still. The only way anyone finds out before the complaints start is if somebody
    built something whose whole job is to notice.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Why you cannot just read the code and find the problem

    Andrej Karpathy gave this shift a name in 2017.

    **Software 1.0** is instructions a person wrote. If it misbehaves, you open the file and
    read it.

    **Software 2.0** is a neural network, where the behaviour lives in numbers learned from
    data. The code that *trains* a GPT-4 class model is a few thousand lines. The actual
    program is about **1.8 trillion numbers**. You cannot read it. You cannot patch line 4,000.
    You can only retrain it and hope.

    His analogy is the one that sticks: debugging ordinary software is editing text. Debugging
    a model is trying to find the one bad ingredient in a batch of 1.8 trillion cookies,
    without being allowed to open a single cookie.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="rl-conseq">
          <span class="lbl">And you cannot test your way out of it either</span>
          <p>Think about testing a function that adds two numbers. You can write down the cases
          that matter: two positives, a negative, zero, the biggest number it can hold. It is a
          short list and you can tick every item off.</p>
          <p>Now write the list for a photo classifier. Every photo anyone might ever point at
          it. Photos of things that did not exist when you trained it. Photos taken at night, in
          the rain, through a cracked screen, by a camera that has not been invented yet.
          <strong>There is no list.</strong> You cannot finish it, so you cannot tick it off.</p>
          <p style="margin-bottom:0">This is why we give up on proving the thing correct and pay
          for <strong>watching it instead</strong>. Monitoring is not a nice-to-have you add
          when there is time. It is the replacement for the tests you are never able to
          write.</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, one_shot):
    get_q3, set_q3 = mo.state(None)
    q3_form, q3_render = one_shot(
        "**Quick check.** What usually happens when a deployed ML system goes wrong?",
        {
            'It throws an error you can find in the logs': 'a',
            'It keeps running and returning answers, while quietly getting things wrong': 'b',
            'It slows down until somebody notices': 'c',
            'It refuses to make predictions it is unsure about': 'd',
        },
        'b',
        {
            'a': ("That is what ordinary software does, and it is a real comfort. ML takes it away "
                  "from you: the code runs perfectly while the answers rot."),
            'b': ("There is no moment of failure to catch, which is why somebody has to be actively "
                  "watching for the drift. Nothing tells you unless you built the thing that "
                  "tells you."),
            'c': ("Speed problems do happen, and there is a whole lab on them. But the frightening "
                  "failure is the one where speed is fine and the answers are wrong."),
            'd': ("Some systems are built to do this and it is a good design. It does not happen for "
                  "free though. Somebody has to choose the threshold and build the fallback."),
        },
    )
    return get_q3, set_q3, q3_form, q3_render


@app.cell(hide_code=True)
def _(q3_form, get_q3, set_q3):
    if q3_form.value is not None and get_q3() is None:
        set_q3(q3_form.value["choice"])
    return


@app.cell(hide_code=True)
def _(get_q3, q3_render):
    q3_render(get_q3())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 4: A real decision""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <div class="lab-case">
          <p><strong class="who">Your manager:</strong> &ldquo;The classifier gets
          <strong>94% accuracy</strong>. Put it behind the search box. About
          <strong>200 people a second</strong> use that box, and we have promised customers that
          <strong>almost nobody waits longer than 150 milliseconds</strong>.&rdquo;</p>
          <p style="margin-bottom:0">You have <strong>one GPU</strong> to run it on.</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Notice what you have just been asked. Not *is the model good?*, because that is settled.
    You have been asked whether **one machine can answer two hundred people a second without
    keeping any of them waiting**. Accuracy has nothing to say about that.

    Before you can answer it, there are two things you need to know. Neither is complicated,
    and you will use both all semester.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### First thing: what "almost nobody waits longer than 150 ms" actually means

    Your manager did not say *the average wait is 150 ms*, and that difference matters more
    than it sounds.

    Imagine a hundred people use the search box. Ninety-five of them get an answer quickly and
    five of them wait a very long time. The **average** can still look perfectly healthy while
    those five people are having an awful experience and telling their friends about it.

    So promises like this are almost never written about the average. They are written about
    the slowest few. "95% of people get an answer within 150 ms" means: line everybody up from
    fastest to slowest, walk 95% of the way along that line, and *that* person must still have
    waited less than 150 ms.

    You will see this written as **p95**, short for the 95th percentile. When you see p95 in this
    lab, read it as **"the slowest 5% of people"**. That is the number we have to keep under
    150 ms, and it is a much harder promise to keep than an average.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Second thing: what batching is, and why anyone bothers

    A GPU does not like being handed one photo at a time. Every time you ask it to run the
    model, there is a fixed setup cost before any real work starts: moving data across,
    launching the work, waking things up. For our model that fixed cost is about **18 ms**, and
    you pay it whether you hand over one item or a hundred.

    Once it is running, each additional item is cheap: about **0.9 ms** each.

    So you have a choice. You can send items one at a time, or you can collect a few and send
    them together. Sending them together is called **batching**, and the number you collect
    before sending is the **batch size**.

    Here is why it is tempting:

    | You send | Total time | Time per item |
    | - | - | - |
    | 1 item | 18 + 0.9 = **18.9 ms** | **18.9 ms** each |
    | 10 items | 18 + 9 = **27 ms** | **2.7 ms** each |
    | 100 items | 18 + 90 = **108 ms** | **1.08 ms** each |

    Ten items take barely longer than one, because they share that 18 ms. Per item, batching
    looks like an enormous win.

    **But there is a catch, and it is the whole lab.** To send ten items together, you have to
    *wait for ten items to show up*. The first person to arrive sits there while the other nine
    trickle in. At 200 people a second, waiting for 10 means the first one waits about 45 ms
    before the GPU has even started.

    So a bigger batch makes the machine more efficient and makes people wait longer. Those pull
    in opposite directions, and somewhere in between is the answer.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### This pattern has a name

    Almost every "how long will this take?" question in ML systems breaks into the same three
    pieces, and it is worth learning them once because they keep coming back:

    | The three pieces | What it means | In this lab |
    | - | - | - |
    | **Moving data** | how long it takes to get the data where it needs to be | waiting for a batch to fill |
    | **Doing the work** | the actual arithmetic | 0.9 ms for every item |
    | **Setting up** | everything before the real work starts | the fixed 18 ms |

    Add the three together and **the biggest one wins**. That is the whole method, and it is
    almost embarrassingly simple. It earns its keep because people are extremely bad at
    guessing which of the three is the big one. You are about to guess, and you will probably
    guess wrong, and that is the useful part.

    Here is a hint about where to look. **We never change the model in this lab.** Not once.
    The thing doing the predicting stays exactly as it is from start to finish. So if this
    system is in trouble, the trouble is somewhere else entirely, and part of your job is
    working out where.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Now make your guess

    That is everything you need. You know the fixed cost, the per-item cost, how many people
    arrive, and what you promised them.

    Do not work it out on paper. Genuinely guess. Then we will look at the real numbers
    together and see whether your instinct was right.

    Your guess is recorded once and not changed afterwards, which is the only reason it tells
    you anything. **Nobody is marking you on whether it was right.** Plenty of people get this
    one wrong, and the ones who do tend to remember it best.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    get_guess, set_guess = mo.state(None)
    guess_form = (
        mo.md("""
        {choice}

        {why}
        """)
        .batch(
            choice=mo.ui.radio(
                options={
                    "As small as possible (1-4), keep waiting time near zero": "tiny",
                    "Moderate (8-16), balance waiting against efficiency": "moderate",
                    "As large as possible (64+), get the most out of the GPU": "huge",
                },
                label="**Your guess.** Which batch size keeps the slowest 5% of people under 150 ms, when 200 people arrive every second?",
            ),
            why=mo.ui.text_area(
                placeholder="One sentence is fine. What made you pick that one?",
                label="**Why did you pick that?**",
                full_width=True,
                rows=2,
            ),
        )
        .form(
            submit_button_label="Submit my guess",
            bordered=True,
            validate=lambda v: (
                "Pick one of the three options."
                if not v or v.get("choice") is None
                else "Write a sentence saying why, then submit."
                if not (v.get("why") or "").strip()
                else None
            ),
        )
    )
    guess_form
    return get_guess, guess_form, set_guess


@app.cell(hide_code=True)
def _(guess_form, get_guess, mo, set_guess):
    # Latch the first guess. Once it is in, it is in: the whole point of guessing
    # before you look is lost if you can quietly revise it after seeing the answer.
    if guess_form.value is not None and get_guess() is None:
        set_guess((guess_form.value["choice"], guess_form.value["why"].strip()))

    _locked = get_guess()
    mo.stop(
        _locked is None,
        mo.callout(
            mo.md(
                "Choose an answer, say why, then press **Submit my guess**. You get one "
                "attempt, and the rest of the lab opens up once you commit."
            ),
            kind="warn",
        ),
    )
    predict_choice, predict_reason = _locked
    prediction_locked = True
    return predict_choice, predict_reason, prediction_locked


@app.cell(hide_code=True)
def _(mo, prediction_locked):
    _ = prediction_locked
    mo.md(r"""## Part 5: Try it yourself""")
    return


@app.cell(hide_code=True)
def _(mo, prediction_locked):
    _ = prediction_locked
    batch = mo.ui.slider(
        1, 128, value=1, step=1,
        label="Batch size - how many we collect before sending", show_value=True,
    )
    load = mo.ui.slider(
        50, 400, value=200, step=10,
        label="How many people arrive per second", show_value=True,
    )
    mo.vstack([batch, load])
    return batch, load


@app.cell(hide_code=True)
def _(batch, load, np):
    SETUP_MS = 18.0
    PER_ITEM_MS = 0.9
    SLA_MS = 150.0

    _b = int(batch.value)
    _rate = float(load.value)

    # Wall time for one inference call of size _b.
    compute_ms = SETUP_MS + PER_ITEM_MS * _b
    # Sustainable throughput of a single GPU at this batch size.
    throughput = _b / (compute_ms / 1000.0)
    # How long the last item waits for the batch to fill.
    fill_ms = (_b - 1) / _rate * 1000.0 if _b > 1 else 0.0
    # Queue penalty as demand approaches what one GPU can sustain.
    utilisation = _rate / throughput
    if utilisation < 1.0:
        queue_ms = compute_ms * utilisation / (1.0 - utilisation)
    else:
        queue_ms = float("inf")

    p95_ms = fill_ms + queue_ms + compute_ms
    meets_sla = bool(np.isfinite(p95_ms) and p95_ms <= SLA_MS)
    return (
        SLA_MS,
        compute_ms,
        fill_ms,
        meets_sla,
        p95_ms,
        queue_ms,
        throughput,
        utilisation,
    )


@app.cell(hide_code=True)
def _(LAB_CSS_B, SLA_MS, meets_sla, mo, p95_ms, throughput, utilisation):
    _ = LAB_CSS_B
    _p95 = "overloaded" if p95_ms == float("inf") else f"{p95_ms:.0f} ms"
    _cls = "lab-pass" if meets_sla else "lab-fail"
    _verdict = "we keep our promise" if meets_sla else "we break our promise"
    _head = "completely overwhelmed" if utilisation >= 1 else "it has room to spare"
    mo.Html(
        f"""
        <div class="lab-kpi">
          <div class="{_cls}">
            <div class="k">Slowest 5% wait</div>
            <div class="v">{_p95}</div>
            <div class="n">we promised under {SLA_MS:.0f} ms, so {_verdict}</div>
          </div>
          <div>
            <div class="k">Most it can handle</div>
            <div class="v">{throughput:,.0f}/s</div>
            <div class="n">one GPU, at this batch size</div>
          </div>
          <div>
            <div class="k">How busy the GPU is</div>
            <div class="v">{min(utilisation, 9.99):.0%}</div>
            <div class="n">{_head}</div>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, prediction_locked):
    _ = prediction_locked
    mo.md(r"""## Part 6: What is really going on""")
    return


@app.cell(hide_code=True)
def _(compute_ms, fill_ms, mo, queue_ms):
    _q = "unbounded" if queue_ms == float("inf") else f"{queue_ms:.1f} ms"
    mo.md(
        f"""
    When someone waits for an answer, that wait is made of **three separate things**. Most
    people only think about the last one. This is the Iron Law with real numbers in it.

    | What they are waiting for | Right now | Gets worse when |
    | - | - | - |
    | **Waiting for the batch to fill** | {fill_ms:.1f} ms | you use bigger batches |
    | **Stuck in the queue behind others** | {_q} | the GPU cannot keep up |
    | **The model actually running** | {compute_ms:.1f} ms | you use bigger batches |

    Here is the awkward part. Making the batch **bigger** shrinks the middle row, because the
    GPU gets through work faster and the queue drains. But it **grows** the top and bottom rows,
    because more people have to show up before anything starts.

    You cannot make all three small at once. That tension is the entire lab.
    """
    )
    return


@app.cell(hide_code=True)
def _(SLA_MS, mo, np):
    _sizes = np.arange(1, 129)
    _compute = 18.0 + 0.9 * _sizes
    _tput = _sizes / (_compute / 1000.0)
    _fill = (_sizes - 1) / 200.0 * 1000.0
    _util = 200.0 / _tput
    _queue = np.where(
        _util < 1.0, _compute * _util / np.maximum(1.0 - _util, 1e-9), np.inf
    )
    _curve = _fill + _queue + _compute

    _ok = np.isfinite(_curve) & (_curve <= SLA_MS)
    _best = int(_sizes[np.argmin(np.where(_ok, _curve, np.inf))]) if _ok.any() else None

    _plot = np.where(np.isfinite(_curve), np.minimum(_curve, 400.0), 400.0)
    _pts = " ".join(
        f"{40 + (s - 1) / 127 * 600:.1f},{300 - v / 400 * 260:.1f}"
        for s, v in zip(_sizes, _plot)
    )
    _sla_y = 300 - SLA_MS / 400 * 260

    _svg = f"""
    <svg viewBox="0 0 660 330" width="100%" role="img"
         aria-label="How long the slowest 5 percent wait, for each batch size, at 200 people per second">
      <line x1="40" y1="300" x2="640" y2="300" stroke="#111" stroke-width="1.5"/>
      <line x1="40" y1="40" x2="40" y2="300" stroke="#111" stroke-width="1.5"/>
      <line x1="40" y1="{_sla_y:.1f}" x2="640" y2="{_sla_y:.1f}"
            stroke="#c62828" stroke-width="1.5" stroke-dasharray="6 4"/>
      <text x="636" y="{_sla_y - 6:.1f}" font-size="11" fill="#c62828"
            text-anchor="end">what we promised (150 ms)</text>
      <polyline points="{_pts}" fill="none" stroke="#f1b82d" stroke-width="2.5"/>
      <text x="340" y="324" font-size="12" fill="#4a4a4a" text-anchor="middle">batch size</text>
      <text x="14" y="170" font-size="12" fill="#4a4a4a" text-anchor="middle"
            transform="rotate(-90 14 170)">slowest 5% wait (ms)</text>
    </svg>
    """

    if _best is None:
        _msg = ("**No batch size works at 200 people per second.** One GPU is not enough, "
                "and that is a real and reportable answer.")
    else:
        _feasible = _sizes[_ok]
        _msg = (
            f"Batch sizes that keep the promise at 200 people per second: "
            f"**{_feasible.min()} to {_feasible.max()}**. The best is **{_best}**."
        )
    mo.vstack([mo.Html(_svg), mo.md(_msg)])
    return


@app.cell(hide_code=True)
def _(mo, predict_choice, prediction_locked):
    _ = prediction_locked
    _why = {
        "tiny": (
            "**Wrong, and this is the one worth getting wrong.** A batch of 1 takes 18.9 ms, "
            "so the GPU can serve about **53 people a second**. But 200 arrive every second. "
            "About 150 people per second join a queue nobody will ever clear. This does not just "
            "miss the target, it *breaks the service completely*. \"Small batch means fast\" is "
            "true on a quiet system and fatal on a busy one, which is exactly why we asked "
            "you to guess first."
        ),
        "moderate": (
            "**Correct.** Anything from **6 to 19** keeps the promise, and **9 is the sweet "
            "spot, where the slowest 5% wait 102 ms**. Nothing outside that range works."
        ),
        "huge": (
            "**Wrong, but for a much more reasonable reason.** Big batches really are efficient "
            "the cost per person drops from 18.9 ms to 1.18 ms. The problem is that the first person "
            "in a batch of 64 waits **315 ms** for the other 63 to turn up, before the GPU even "
            "starts. That is already double the entire budget. Efficiency you cannot spend is not "
            "worth anything."
        ),
    }
    _ok = predict_choice == "moderate"
    mo.vstack([
        mo.md("### So, was your guess right?"),
        mo.callout(
            mo.md(
                _why[predict_choice]
                + ("" if _ok else "\n\nThe answer is **moderate (8-16)**. Anything from 6 to 19 "
                                  "works, and batch 9 is best and the slowest 5% wait 102 ms.\n\n"
                                  "Getting this wrong is genuinely the useful outcome. Open the "
                                  "full answer below and find the moment your reasoning parted "
                                  "company with what actually happens.")
            ),
            kind="success" if _ok else "danger",
        ),
        mo.accordion({
            "Show me the full answer and why": mo.md(
                """
| Batch | Model runs for | Most it can handle | Waiting for batch | Stuck in queue | **Slowest 5% wait** | |
| - | - | - | - | - | - | - |
| 1 | 18.9 ms | 53/s | 0 ms | forever | **falls over** | cannot keep up with 200/s |
| 4 | 21.6 ms | 185/s | 15 ms | forever | **falls over** | still under 200/s |
| 5 | 22.5 ms | 222/s | 20 ms | 202 ms | 245 ms | only just keeping up |
| 6 | 23.4 ms | 256/s | 25 ms | 83 ms | **131 ms** | first one that works |
| **9** | **26.1 ms** | **345/s** | **40 ms** | **20 ms** | **102 ms** | **the best** |
| 19 | 35.1 ms | 541/s | 90 ms | 20 ms | **145 ms** | last one that works |
| 20 | 36.0 ms | 556/s | 95 ms | 20 ms | 151 ms | waiting time tips it over |
| 64 | 75.6 ms | 847/s | 315 ms | 23 ms | 414 ms | waiting alone blows the budget |

**Read the table from the top and the story tells itself.**

**Step one: can it even keep up?** At batch 1 the GPU finishes a job every 18.9 ms, which is
about **53 people a second**. But 200 people a second are arriving. Every second, roughly 150
people join a queue that nobody is ever going to clear. It does not matter how patient your
customers are. The wait grows forever and the service falls over. Batches of 1 to 4 all have
this problem.

*This is the bit almost everyone gets wrong.* "Small batch means fast" is true when the system
is quiet. When it is busy, small batches are the thing that kills you.

**Step two: stop drowning.** Once the GPU can just about keep up (batch 5), it is running flat
out with no slack. Anything that arrives at a bad moment sits behind a queue, 202 ms of it.
Give the GPU a bit more room and this collapses fast: by batch 9 it is only busy 58% of the
time, and queueing is down to 20 ms.

**Step three: now the waiting bites.** With the queue under control, the only thing left
growing is people waiting for the batch to fill, and at 200 people a second that is 5 ms for
every extra slot you add. It never stops growing. Past batch 19 it eats the whole budget on
its own.

So: **falls over on the left, too much waiting on the right, and a narrow band in the middle
where it works.** That is the U-shape in the chart.

**The thing to take away.** That 18 ms of setup gets shared. At batch 1, one person pays the
whole 18 ms and 95% of their wait is pure overhead. At batch 9, nine people split it and each
effectively pays 2.9 ms. Batching is not a price you pay for speed. When the system is
busy, **it is the only reason the service works at all.**
                """
            ),
            "What if more (or fewer) people showed up?": mo.md(
                """
There is no single right batch size. It depends entirely on how busy you are, which is
why the answer belongs to the *system*, not to the model.

| People per second | Batch sizes that work | Best choice |
| - | - | - |
| 50 | 2 to 7 | batch 2, and nobody waits more than 59 ms |
| 100 | 3 to 12 | batch 4, 77 ms |
| 200 | 6 to 19 | batch 9, 102 ms |
| 400 | **none of them** | the best you can do is 173 ms, so you need another GPU |

Two things worth noticing.

**The busier you get, the bigger your batches have to be** just to keep up. The quiet-day
answer is the wrong answer on a busy day, so design for your busiest hour, not your average
one.

**At 400 people a second, nothing works.** Sometimes the honest answer really is *"we cannot
do this with what we have"*. Saying that clearly, with the numbers to back it up, is a proper
engineering result, not a failure to find the trick.

Try dragging the second slider above and watch the green band move.
"""
            ),
        }),
    ])
    return


@app.cell(hide_code=True)
def _(mo, prediction_locked):
    _ = prediction_locked
    mo.md(r"""## Part 7: Your decision""")
    return


@app.cell(hide_code=True)
def _(batch, mo, prediction_locked):
    _ = prediction_locked
    decision_form = (
        mo.md("""
        {choice}

        {why}
        """)
        .batch(
            choice=mo.ui.radio(
                options={
                    "Yes, ship it. I can name a batch size that keeps our promise": "ship",
                    "Ship it, but buy a second GPU so we are not running at the edge": "ship_scale",
                    "No. We cannot keep this promise on one GPU, and I can show why": "hold",
                },
                label="**Your decision.** What do you tell your manager?",
            ),
            why=mo.ui.text_area(
                placeholder=(
                    "Say which batch size you picked, what the slowest 5% end up waiting, "
                    "and what would make you change your answer."
                ),
                label="**Why?** Write it as if your manager will read it and push back.",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_label="Submit my decision",
            bordered=True,
            validate=lambda v: (
                "Choose one of the three answers."
                if not v or v.get("choice") is None
                else "Write your reasoning, then submit."
                if not (v.get("why") or "").strip()
                else None
            ),
        )
    )
    mo.vstack([
        mo.md(f"Your batch size is currently **{batch.value}**. Change it above if you want to."),
        decision_form,
    ])
    return (decision_form,)


@app.cell(hide_code=True)
def _(decision_form, mo):
    mo.stop(
        decision_form.value is None,
        mo.callout(
            mo.md(
                "Pick a decision, explain it, then press **Submit my decision** to finish "
                "the lab."
            ),
            kind="info",
        ),
    )
    decision_choice = decision_form.value["choice"]
    defence_text = decision_form.value["why"].strip()
    return decision_choice, defence_text


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Part 8: One last question""")
    return


@app.cell(hide_code=True)
def _(mo):
    answers_form = (
        mo.md("{takeaway}")
        .batch(
            takeaway=mo.ui.text_area(
                placeholder="The thing that decided it was... and I would not have found that by looking at accuracy because...",
                label="**In your own words:** what actually decided whether this could ship, and why would you never have found it by looking at the accuracy score?",
                full_width=True,
                rows=4,
            ),
        )
        .form(
            submit_button_label="Finish the lab and make my report",
            bordered=True,
            validate=lambda v: (
                None if v and (v.get("takeaway") or "").strip()
                else "Write a sentence or two, then submit."
            ),
        )
    )
    answers_form
    return (answers_form,)


@app.cell(hide_code=True)
def _(answers_form, mo):
    mo.stop(
        answers_form.value is None,
        mo.callout(
            mo.md("Write both answers, then press **Finish the lab and make my report**."),
            kind="warn",
        ),
    )
    takeaway_text = answers_form.value["takeaway"].strip()
    done = True
    return done, takeaway_text


@app.cell(hide_code=True)
def _(batch, decision_choice, defence_text, meets_sla, mo, p95_ms, predict_choice, predict_reason):
    _p95 = "overloaded" if p95_ms == float("inf") else f"{p95_ms:.0f} ms"
    _label = {
        "tiny": "as small as possible (1-4)",
        "moderate": "moderate (8-16)",
        "huge": "as large as possible (64+)",
    }
    _chosen = int(batch.value)
    _correct = predict_choice == "moderate"
    _optimal = 6 <= _chosen <= 19

    _verdict = ('<span class="tick">right</span>' if _correct
                else '<span class="cross">wrong</span>')
    _promise = ('<span class="tick">keeps</span>' if meets_sla
                else '<span class="cross">breaks</span>')
    _decisions = {
        "ship": "Ship it",
        "ship_scale": "Ship it, and add a second machine",
        "hold": "Do not ship it",
    }
    _warn = ("" if _optimal else
             f'<div class="row"><span class="k">Worth another look</span>'
             f'<span class="v">Batch {_chosen} is outside the 6 to 19 range that actually '
             f'works. Read the full answer again before you hand this in.</span></div>')

    mo.vstack([
        mo.md("## Your Week 1 report"),
        mo.Html(
            f"""
            <div class="lab-report">
              <div class="row">
                <span class="k">You guessed</span>
                <span class="v">{_label[predict_choice]}, which was {_verdict}</span>
              </div>
              <div class="row">
                <span class="k">The answer</span>
                <span class="v">Moderate (8 to 16). Anything from 6 to 19 works, and 9 is
                best at 102 ms.</span>
              </div>
              <div class="row">
                <span class="k">Your reason</span>
                <span class="v quote">{predict_reason}</span>
              </div>
              <div class="row">
                <span class="k">You settled on</span>
                <span class="v">Batch {_chosen}. The slowest 5% wait {_p95}, which
                {_promise} the 150 ms promise.</span>
              </div>
              <div class="row">
                <span class="k">Your decision</span>
                <span class="v">{_decisions.get(decision_choice, decision_choice)}</span>
              </div>
              <div class="row">
                <span class="k">Why</span>
                <span class="v quote">{defence_text}</span>
              </div>
              {_warn}
            </div>
            """
        ),
        mo.md("""
    ### Four things worth remembering

    - **The 94% never came up again.** Not once. Everything that decided this was about the
      machine and the people waiting. You will see this pattern in every lab this semester.
    - **The obvious answer was the worst one.** "Send them one at a time so nobody waits" sounds
      completely sensible, and it breaks the service outright. Sensible-sounding is not the same
      as correct, which is why we make you commit to a guess and then check it.
    - **One dial moved three things at once, in different directions.** Turning up the batch size
      made one part of the wait shorter and two parts longer. Most of the work in this course is
      finding out which part is actually holding you back.
    - **Ask "can it cope?" before "is it fast?"** Batches of 1 to 4 never even got to the
      question of speed, because they simply could not keep up. Survival first, then speed.
    - **A model that misses your deadline is worth nothing, however good it is.** There are
      well known architectures that beat older ones by a point or two of accuracy while costing
      four times the compute and three times the memory traffic. On a leaderboard that is a
      win. Inside a promise like this one it can be a model you are simply not allowed to use.
      Being top of a leaderboard and being right for your system are different things.
    """),
    ])
    return


@app.cell(hide_code=True)
def _(
    HANDIN_URL,
    batch,
    decision_choice,
    defence_text,
    json,
    load,
    meets_sla,
    mo,
    p95_ms,
    predict_choice,
    predict_reason,
    quote,
    takeaway_text,
):
    mo.stop(decision_choice is None or defence_text == "")

    _names = {
        "tiny": "as small as possible (1-4)",
        "moderate": "moderate (8-16)",
        "huge": "as large as possible (64+)",
    }
    _p95 = "overloaded" if p95_ms == float("inf") else f"{p95_ms:.0f} ms"
    _correct = predict_choice == "moderate"

    submission = {
        "lab": "CSC/EE 8001 - Week 1",
        "your_guess": _names[predict_choice],
        "your_reasoning": predict_reason,
        "correct_answer": "moderate (8-16); works from 6 to 19, best at 9",
        "guess_was_correct": _correct,
        "final_batch_size": int(batch.value),
        "arrival_rate_per_second": int(load.value),
        "final_p95_ms": None if p95_ms == float("inf") else round(p95_ms, 1),
        "meets_150ms_target": meets_sla,
        "your_decision": decision_choice,
        "your_defence": defence_text,
        "what_stopped_the_biggest_model": takeaway_text,
    }

    report_text = "\n".join([
        "CSC/EE 8001 - Week 1",
        "=" * 56,
        "",
        "WHAT I GUESSED",
        f"  {_names[predict_choice]}",
        f"  Because: {predict_reason}",
        f"  This was {'CORRECT' if _correct else 'NOT correct'}.",
        "",
        "THE ACTUAL ANSWER",
        "  Moderate batches (8-16). Anything from 6 to 19 meets the target;",
        "  batch 9 is best at 102 ms. Batches of 1-4 cannot keep up at all,",
        "  and batches of 64+ spend longer than the whole budget just waiting",
        "  for the batch to fill.",
        "",
        "WHAT I SETTLED ON",
        f"  Batch size        : {int(batch.value)}",
        f"  Arrival rate      : {int(load.value)} requests/second",
        f"  Slowest 5% wait   : {_p95}",
        f"  Meets the target  : {'yes' if meets_sla else 'no'}",
        "",
        "MY DECISION",
        f"  {decision_choice}",
        "",
        "MY REASONING",
        f"  {defence_text}",
        "",
        "WHAT STOPPED THE BIGGEST MODEL FROM BEING USABLE",
        f"  {takeaway_text}",
    ])

    _names = {
        "tiny": "as small as possible (1 to 4)",
        "moderate": "moderate (8 to 16)",
        "huge": "as large as possible (64+)",
    }
    _decision_words = {
        "ship": "Ship it",
        "ship_scale": "Ship it, and add a second machine",
        "hold": "Do not ship it",
    }
    _p95 = "overloaded" if p95_ms == float("inf") else f"{p95_ms:.0f} ms"

    _downloads = mo.hstack(
        [
            mo.download(data=report_text.encode("utf-8"),
                        filename="week1_report.txt", label="Download my report"),
            mo.download(data=json.dumps(submission, indent=2).encode("utf-8"),
                        filename="week1_report.json", label="Download as JSON"),
        ],
        justify="start",
        gap=1,
    )

    if HANDIN_URL:
        # Everything is already filled in, so handing in is one click and a glance.
        _fill = {
            "GUESSHERE": _names[predict_choice],
            "REASONHERE": predict_reason,
            "BATCHHERE": str(int(batch.value)),
            "WAITHERE": _p95,
            "DECISIONHERE": _decision_words.get(decision_choice, decision_choice),
            "WHYHERE": defence_text,
            "STOPPEDHERE": takeaway_text,
        }
        _link = HANDIN_URL
        for _placeholder, _answer in _fill.items():
            _link = _link.replace(_placeholder, quote(_answer, safe=""))

        _handin = mo.vstack([
            mo.md(
                "## Last step: hand it in\n\nYour answers are already filled in for you. Open "
                "it, check it looks right, and press submit. That is the whole hand-in."
            ),
            mo.Html(
                f'<a class="handin-btn" href="{_link}" target="_blank" '
                f'rel="noopener noreferrer">Hand in my Week 1 answers</a>'
            ),
            mo.accordion({
                "Want your own copy too?": mo.vstack([
                    mo.md("Nothing is saved inside this page, so grab a copy if you would "
                          "like one."),
                    _downloads,
                ]),
            }),
        ])
    else:
        _handin = mo.vstack([
            mo.md(
                "## Last step: hand it in\n\nDownload your report and upload it wherever your "
                "class work goes. That is everything. Nothing here is sent anywhere on its "
                "own, so this file is the only copy."
            ),
            _downloads,
            mo.accordion({
                "The download did not work. What now?": mo.md(
                    "Copy everything below into a document and hand that in instead. It says "
                    "exactly the same thing.\n\n"
                    f"```\n{report_text}\n```"
                ),
            }),
        ])

    _handin
    return


@app.cell(hide_code=True)
def _(decision_choice, mo):
    _ = decision_choice
    mo.vstack([
        mo.md("### Check yourself\n\nAnswer from memory, then open each one."),
        mo.accordion({
            "Why can a GPU that finishes an inference in 18.9 ms not serve 200 requests per second?":
                mo.md(
                    "Because 18.9 ms *per request* is 1000 / 18.9 = **53 requests per second**, and "
                    "the 18 ms setup is paid once per *call*, not per item. At batch 1 you spend 95% "
                    "of the call on overhead to serve a single request. Batching amortises that fixed "
                    "cost: at batch 9 the same overhead is spread across nine items, giving 2.9 ms "
                    "per item and 345 req/s."
                ),
            "Why does p95 latency rise again past batch 19, even though the GPU is more efficient?":
                mo.md(
                    "Because **fill wait** takes over. At 200 req/s a batch of size *b* takes "
                    "`5 x (b - 1)` ms to fill, and that grows linearly forever. Meanwhile queueing "
                    "delay has already bottomed out near 20 ms. Once the GPU has room to spare, extra "
                    "efficiency buys nothing. At batch 64 the fill wait alone is 315 ms. The GPU is "
                    "idle waiting for work that has not arrived yet."
                ),
            "The SLA is p95, not average. Why does that matter?":
                mo.md(
                    "Averages hide the queue. A system at 90% utilisation can have a perfectly "
                    "acceptable mean while the slowest 5% of requests wait several hundred "
                    "milliseconds. Batch 5 in this lab averages far better than its 245 ms p95. "
                    "Contracts are written on tails because that is what users actually notice, and "
                    "tail latency is where queueing shows up first."
                ),
            "Your service is at 400 req/s and no batch size meets the SLA. What do you tell your product lead?":
                mo.md(
                    "That the contract cannot be met on one GPU, with the number that proves it: the "
                    "best achievable p95 is **173 ms against a 150 ms budget**. Then give them the "
                    "options: add a second GPU, renegotiate to 200 ms, or reduce the per-item cost "
                    "(quantisation, a smaller model). **\"No, and here is the evidence\" is a "
                    "legitimate engineering result.** Shipping something you know breaches the "
                    "contract is not."
                ),
            "What single measurement would most change your recommendation?":
                mo.md(
                    "The **arrival rate**, and specifically its peak rather than its mean. Every "
                    "number in this lab is conditional on 200 req/s: at 100 req/s the feasible band "
                    "is 3-12 and batch 4 gives 77 ms; at 400 req/s nothing works. A design defended "
                    "on average load is a design that fails at peak. Second most important: whether "
                    "18 ms of setup is truly fixed. If it can be reduced, the whole curve shifts "
                    "down and the feasible band widens."
                ),
        }),
    ])
    return


if __name__ == "__main__":
    app.run()
