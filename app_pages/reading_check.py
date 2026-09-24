import streamlit as st

from content.reading_check import CITATIONS, DISCUSSION_PROMPTS, INTRO, QUESTIONS
from utils.downloads import PAGE_NOTE, build_docx, save_section
from utils.exercise import answer_lines
from utils.style import banner, callout, label

LETTERS = ["a", "b", "c", "d"]
N = len(QUESTIONS)

banner(
    "Readings",
    "Reading Check: How LLMs Actually Write",
    "A comprehension check on DeLuca et al. (2025) and Reinhart et al. (2025), plus discussion "
    "prompts for class. Complete this after finishing both readings and before we start the "
    "cover letter unit.",
)

with st.container(border=True):
    st.write(INTRO)
    for c in CITATIONS:
        st.caption(c)
callout("info", PAGE_NOTE)

# ── Part A: quiz ─────────────────────────────────────────────────────────────
st.header("Part A · Comprehension questions")
st.caption(
    "Choose one answer per question. You'll get immediate feedback with a pointer back to "
    "the relevant part of the reading. Your first answer counts; use the retry button at the "
    "bottom to start over."
)


# A student's first answer is stored in st.session_state["rc_answers"] and locked.
if "rc_answers" not in st.session_state:
    st.session_state.rc_answers = {}
if "rc_round" not in st.session_state:
    st.session_state.rc_round = 0  # bumped on retry so the radio buttons start fresh
answers = st.session_state.rc_answers


def lock_answer(i):
    val = st.session_state.get(f"rc_q{i}_{st.session_state.rc_round}")
    if val is not None and i not in answers:
        answers[i] = val


def reset_quiz():
    st.session_state.rc_answers = {}
    st.session_state.rc_round += 1


score = 0
for i, item in enumerate(QUESTIONS):
    with st.container(border=True):
        label(f"Question {i + 1} of {N}")
        if i not in answers:
            st.radio(
                item["q"],
                options=list(range(len(item["opts"]))),
                format_func=lambda j, item=item: f"({LETTERS[j]}) {item['opts'][j]}",
                index=None,
                key=f"rc_q{i}_{st.session_state.rc_round}",
                on_change=lock_answer,
                args=(i,),
            )
        else:
            # Answered: show the options as a static list with the result marked.
            choice = answers[i]
            st.markdown(item["q"])
            labeled = [f"({LETTERS[j]}) {opt}" for j, opt in enumerate(item["opts"])]
            st.markdown(answer_lines(labeled, item["a"], choice), unsafe_allow_html=True)
            if choice == item["a"]:
                score += 1
                callout("correct", "That is the right answer.", title="Correct", announce=True)
            else:
                callout("wrong", f"You chose ({LETTERS[choice]}).", title="Not quite", announce=True)
            callout("info", item["fb"], title="Why")

answered_count = len(answers)
st.progress(answered_count / N, text=f"Answered {answered_count} of {N}")
col1, col2 = st.columns([3, 1])
col1.metric("Your score", f"{score} / {N}")
col2.button("Retry quiz", on_click=reset_quiz, use_container_width=True)

# ── Part B: discussion ──────────────────────────────────────────────────────
st.header("Part B · Discussion prompts")
st.caption("We'll take these up in class. Jot notes for at least two of them.")

for i, prompt in enumerate(DISCUSSION_PROMPTS):
    with st.container(border=True):
        label(f"Prompt {i + 1}")
        st.markdown(prompt)
        st.text_area("Your notes", key=f"rc_note{i}", label_visibility="collapsed",
                     placeholder="Your notes…")

# ── Download ─────────────────────────────────────────────────────────────────
def build(name):
    sections = [("Quiz score", f"{score} / {N} ({answered_count} of {N} answered)")]
    for i, prompt in enumerate(DISCUSSION_PROMPTS):
        plain = prompt.replace("*", "")
        sections.append((f"Prompt {i + 1}: {plain}", st.session_state.get(f"rc_note{i}", "")))
    return build_docx("Reading Check: How LLMs Actually Write", name, sections)


save_section(
    key_prefix="rc",
    name_label="Your name (appears on the downloaded file)",
    field_keys=[f"rc_note{i}" for i in range(len(DISCUSSION_PROMPTS))],
    build=build,
    file_name="ReadingCheck_notes.docx",
    extra_note="Your quiz score goes into the file as well.",
)

st.divider()
st.caption(
    "Part of Writing Against AI Slop · Calvin Pollak · University of Washington. "
    "Quiz content paraphrases findings from the two cited studies for educational purposes."
)
