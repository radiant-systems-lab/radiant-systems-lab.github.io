# Starter for a lab that signs students in and saves their progress.
#
# Copy this file to labs/_src/week_NN/notebook.py and write the lab around it.
# The build notices the "radiant-lab-" channel name below and puts the sign-in
# gate in front of the lab. Labs without it (weeks 1 to 3) stay open.
#
# The pattern, for every answer you want kept:
#   1. create the widget with   value=saved.get("key", default), disabled=locked
#      (radios take a label, so use value=pick(options, saved.get("key")))
#   2. pass its value to        lab_sync.record(key=widget.value)
#      in a cell that exists from the start; answers that only appear after a
#      form is submitted get their own record cell
#   3. for a form, fall back to saved.get("key") where you read form.value, so
#      a returning student is not asked to submit it again
# Keys only need to be unique within the lab. Values must be JSON: strings,
# numbers, booleans, None, lists and dicts.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Week NN - Lab title")


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
            return await self._request("submit", timeout=45, state=self.state)

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

        Returns (radio, render, summarise). The answer is restored from `key`.
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
    mo.md(
        r"""
    # Week NN: Lab title

    Replace this with the lab. Everything below is a working example of the
    saving pattern: answer, close the tab, come back, and your answers are still here.
    """
    )
    return


@app.cell(hide_code=True)
def _(ask):
    q1, q1_render, q1_sum = ask(
        "**Quick check.** Where does a student's progress get saved?",
        {
            "In this browser only": "a",
            "In the course database, under their own account": "b",
            "Nowhere until they download the report": "c",
        },
        "b",
        {
            "a": "It used to be. Now it follows the student to any computer they sign in on.",
            "b": "Every answer is saved against the signed-in account as they go.",
            "c": "The download is still there as a copy, but saving happens on its own.",
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
def _(locked, mo, saved):
    batch = mo.ui.slider(
        1, 64, value=saved.get("batch", 8), step=1, disabled=locked,
        label="An example slider", show_value=True,
    )
    cache = mo.ui.checkbox(
        value=saved.get("cache", False), disabled=locked,
        label="An example checkbox",
    )
    mo.vstack([batch, cache])
    return batch, cache


@app.cell(hide_code=True)
def _(batch, cache, mo):
    mo.md(f"The slider is at **{batch.value}** and the box is "
          f"**{'ticked' if cache.value else 'not ticked'}**.")
    return


@app.cell(hide_code=True)
def _(locked, mo, pick, saved):
    _saved = saved.get("decision") or {}
    _choices = {
        "Option one": "one",
        "Option two": "two",
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
                label="**An example decision.**",
            ),
            why=mo.ui.text_area(
                value=_saved.get("why", ""),
                disabled=locked,
                placeholder="Why?",
                label="**Why?**",
                full_width=True,
                rows=3,
            ),
        )
        .form(
            submit_button_label="Submit my decision",
            submit_button_disabled=locked,
            bordered=True,
            validate=lambda v: (
                "Choose one."
                if not v or v.get("choice") is None
                else "Say why, then submit."
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
def _(decision_choice, locked, mo, saved):
    _ = decision_choice
    _saved = saved.get("reflection") or {}
    reflect_form = (
        mo.md("{takeaway}")
        .batch(
            takeaway=mo.ui.text_area(
                value=_saved.get("takeaway", ""),
                disabled=locked,
                placeholder="One or two sentences.",
                label="**Last one.** An example closing question.",
                full_width=True,
                rows=3,
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
def _(batch, cache, decision_form, lab_sync, q1):
    # Everything on the page from the start. A form's value is None until it is
    # submitted in this visit, so only record it once it has one.
    if lab_sync is not None:
        lab_sync.record(q1=q1.value, batch=batch.value, cache=cache.value)
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
async def _(done, lab_status, lab_sync, mo, reflect_form):
    _ = done
    if lab_sync is None:
        _msg, _kind = (
            "You opened this lab outside the course site, so nothing was sent to your "
            "instructor. Use the download below to keep a copy.", "neutral")
    elif reflect_form.value is None:
        # Came back to a lab they had already finished.
        _when = (lab_status.get("submittedAt") or "")[:10]
        if lab_status.get("submitted"):
            _msg, _kind = (
                f"**Submitted on {_when}.** You can change answers and press "
                "**Finish the lab** again to resubmit.", "success")
        else:
            _msg, _kind = (
                "Your answers are saved but the lab is **not submitted** yet. "
                "Press **Finish the lab** to submit it.", "warn")
    else:
        _reply = await lab_sync.submit(reflection=reflect_form.value, finished=True)
        if _reply.get("ok"):
            _msg, _kind = ("**Submitted.** Your instructor can see your answers. You can "
                           "still change them and submit again.", "success")
        elif _reply.get("locked"):
            _msg, _kind = ("**Not submitted.** An instructor has locked this lab.", "danger")
        else:
            _msg, _kind = (
                f"**Not submitted:** {_reply.get('error', 'unknown error')}. Your answers "
                "are still saved as you go. Press **Finish the lab** to try again.", "danger")
    mo.callout(mo.md(_msg), kind=_kind)
    return


@app.cell(hide_code=True)
def _(decision_choice, decision_why, done, mo, q1, q1_sum, takeaway_text):
    _ = done
    _text, _ok = q1_sum(q1.value)
    mo.md(f"""
    ## Your report

    - **Quick check:** {_text} ({'right' if _ok else 'not answered' if _ok is None else 'wrong'})
    - **Decision:** {decision_choice}, because {decision_why}
    - **Last answer:** {takeaway_text}
    """)
    return


if __name__ == "__main__":
    app.run()
