"""Building blocks shared by the exercise pages."""

import html

import streamlit as st

HL_CSS = """
<style>
mark.hl-a { background: #fde68a; border-radius: 2px; padding: 0 2px; }
mark.hl-b { background: #bfdbfe; border-radius: 2px; padding: 0 2px; }
</style>
"""


def highlight(text: str, terms: list[str], cls: str = "hl-a") -> str:
    """Wrap each term (in order of appearance) in <mark>. Same logic as the HTML site."""
    ordered = sorted(terms, key=lambda t: text.find(t))
    out, cur = "", 0
    for t in ordered:
        i = text.find(t, cur)
        if i < 0:
            continue
        out += html.escape(text[cur:i]) + f'<mark class="{cls}">{html.escape(t)}</mark>'
        cur = i + len(t)
    return out + html.escape(text[cur:])


def passage(text: str, terms: list[str] | None = None, cls: str = "hl-a", italic: bool = True):
    body = highlight(text, terms, cls) if terms else html.escape(text)
    style = "font-style:italic;" if italic else ""
    st.markdown(HL_CSS + f'<div class="slop-passage" style="{style}">{body}</div>',
                unsafe_allow_html=True)


def locked_choice(key: str, prompt: str, options: list[str], correct: int,
                  explanation: str, horizontal: bool = False) -> None:
    """A multiple-choice item whose first answer locks, with feedback afterwards."""
    store = st.session_state.setdefault("locked_answers", {})
    widget_key = f"{key}_widget"

    def lock():
        val = st.session_state.get(widget_key)
        if val is not None and key not in store:
            store[key] = val

    if key not in store:
        st.radio(prompt, options=list(range(len(options))), format_func=lambda j: options[j],
                 index=None, key=widget_key, on_change=lock, horizontal=horizontal)
        return

    choice = store[key]
    if prompt:
        st.markdown(prompt)
    lines = []
    for j, opt in enumerate(options):
        if j == correct:
            lines.append(f":green-background[✓ {opt}]")
        elif j == choice:
            lines.append(f":red-background[✗ {opt}]")
        else:
            lines.append(f":gray[{opt}]")
    st.markdown("\n\n".join(lines))
    if choice == correct:
        st.success("Correct.", icon=":material/check:")
    else:
        st.error(f"Not quite. The better answer is: {options[correct]}", icon=":material/close:")
    st.info(explanation)


def model_answer(text: str):
    with st.expander("Show model answer"):
        st.markdown(
            f'<div class="slop-passage" style="font-style:italic;background:#eaf4ee;'
            f'border-left-color:#4a8c5c;">{html.escape(text)}</div>',
            unsafe_allow_html=True,
        )


def response_box(key: str, placeholder: str = "Write your more human version here…"):
    st.text_area("Your version", key=key, placeholder=placeholder, label_visibility="collapsed")
