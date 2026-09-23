"""Writing Against AI Slop: classroom version (Streamlit).

This is the file Streamlit runs. It sets up the page list and the sidebar
navigation. Each page's content lives in the app_pages/ folder.
"""

import streamlit as st

from utils.style import inject_css

st.set_page_config(
    page_title="Writing Against AI Slop",
    page_icon="✎",
    layout="centered",
)
inject_css()

# Setup check: if the hidden .streamlit/config.toml file didn't make it to GitHub,
# the app still works but loses its colors and fonts. Say so, so it's easy to notice.
if st.get_option("theme.primaryColor") is None:
    st.warning(
        "Setup note for the instructor: the color and font settings file "
        "(.streamlit/config.toml) is missing, so the app is using Streamlit's default look. "
        "See step 3 in the README to add it. This note disappears once the file is in place.",
        icon=":material/palette:",
    )


pages = {
    "": [
        st.Page("app_pages/home.py", title="Home", icon=":material/home:", default=True),
    ],
    "Start here": [
        st.Page("app_pages/reading_check.py", title="Reading Check", icon=":material/menu_book:"),
    ],
    "Course units": [
        st.Page("app_pages/unit1_cover_letters.py", title="Unit 1: Cover Letters", icon=":material/mail:"),
        st.Page("app_pages/unit2_instructions.py", title="Unit 2: Instructions", icon=":material/list:"),
        st.Page("app_pages/unit3_proposals.py", title="Unit 3: Proposals", icon=":material/description:"),
    ],
    "Practice anytime": [
        st.Page("app_pages/exercise_set1_style.py", title="Exercise Set 1: Style Comparison", icon=":material/compare:"),
        st.Page("app_pages/exercise_set2_genre.py", title="Exercise Set 2: Genre Exercises", icon=":material/edit_note:"),
    ],
}

nav = st.navigation(pages)
nav.run()
