import streamlit as st

from content.reading_check import CITATIONS
from content.style_comparison import EXERCISES, EXERCISES_INTRO, PARAGRAPHS, PARAGRAPHS_INTRO
from utils.downloads import build_docx
from utils.exercise import HL_CSS, highlight, locked_choice, model_answer, passage, response_box
from utils.style import banner, label

banner(
    "Exercise Set 1",
    "AI Slop Style vs. a More Human Style",
    "A comparative guide to nominal and clausal prose styles",
)
with st.expander("Sources for this exercise set"):
    for c in CITATIONS:
        st.caption(c)

tab_paras, tab_ex = st.tabs(["Paragraph examples", "Exercises"])

# ── Paragraph examples ───────────────────────────────────────────────────────
with tab_paras:
    st.caption(PARAGRAPHS_INTRO)
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    topic = c1.segmented_control(
        "Topic", [p["topic"] for p in PARAGRAPHS], default=PARAGRAPHS[0]["topic"], key="s1_topic"
    ) or PARAGRAPHS[0]["topic"]
    hl_on = c2.toggle("Show highlights", key="s1_hl")
    para = next(p for p in PARAGRAPHS if p["topic"] == topic)

    left, right = st.columns(2)
    for col, style_name, sub, text, terms, cls in [
        (left, "AI slop style", "Nominal, dense, direct", para["a"], para["hlA"], "hl-a"),
        (right, "A more human style", "Verbal, clausal, hedged", para["b"], para["hlB"], "hl-b"),
    ]:
        with col.container(border=True):
            label(style_name)
            st.caption(sub)
            body = highlight(text, terms, cls) if hl_on else text
            st.markdown(HL_CSS + f'<div style="line-height:1.8">{body}</div>', unsafe_allow_html=True)
    if hl_on:
        st.markdown(
            HL_CSS + '<div class="slop-passage" style="font-size:0.9rem"><strong>Highlights:</strong> '
            'In AI slop style, <mark class="hl-a">yellow</mark> marks nominalizations, participial '
            'clauses, and dense noun phrases. In a more human style, <mark class="hl-b">blue</mark> '
            'marks hedges, agentless passives, and co-ordinating conjunctions.</div>',
            unsafe_allow_html=True,
        )

# ── Exercises ────────────────────────────────────────────────────────────────
STYLE_LABELS = ["AI slop style", "A more human style"]

with tab_ex:
    st.caption(EXERCISES_INTRO)
    for i, ex in enumerate(EXERCISES):
        with st.container(border=True):
            kind = "Identification" if ex["type"] == "identify" else "Transformation"
            label(f"Exercise {i + 1} · {kind}")
            st.markdown(f"**{ex['question']}**")
            passage(ex["passage"])
            if ex["type"] == "identify":
                locked_choice(
                    key=f"s1_ex{i}", prompt="", options=STYLE_LABELS,
                    correct=0 if ex["answer"] == "A" else 1,
                    explanation=ex["explanation"], horizontal=True,
                )
            else:
                st.caption(f"💡 Hint: {ex['tip']}")
                response_box(f"s1_resp{i}", "Type your rewritten sentence here…")
                model_answer(ex["model"])

    st.subheader("Save your work")
    st.caption("This app doesn't store anything you type. Download your rewrites before you leave.")
    name = st.text_input("Your name (appears on the downloaded file)", key="student_name")
    sections = []
    for i, ex in enumerate(EXERCISES):
        if ex["type"] == "transform":
            sections.append((f"Exercise {i + 1}: {ex['question']}", f"Original: {ex['passage']}\n\n"
                             f"My version: {st.session_state.get(f's1_resp{i}', '') or '(no response)'}"))
    st.download_button(
        "Download as Word document",
        data=build_docx("Exercise Set 1: AI Slop Style vs. a More Human Style", name, sections),
        file_name="ExerciseSet1_responses.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        icon=":material/download:", type="primary",
    )
