"""Writing Against AI Slop: classroom version (Streamlit).

This is the file Streamlit runs. It sets up the page list and the sidebar
navigation. Each page's content lives in the app_pages/ folder.
"""

from pathlib import Path

import streamlit as st

from utils.a11y import patch_streamlit_a11y
from utils.style import callout, inject_css

st.set_page_config(
    page_title="Writing Against AI Slop",
    page_icon="✎",
    layout="centered",
)
inject_css()
patch_streamlit_a11y()

# Setup check: look for the settings file itself, next to this script. Checking the
# theme values instead gave a false alarm on Streamlit Community Cloud, which supplies
# its own theme defaults.
if not (Path(__file__).parent / ".streamlit" / "config.toml").is_file():
    callout(
        "note",
        "Setup note for the instructor: the color and font settings file "
        "(.streamlit/config.toml) is missing. The app still looks right, because its colors "
        "are also set in utils/style.py, but see step 4 in the README to add the file back.",
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
