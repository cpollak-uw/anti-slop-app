"""Shared visual styling, carried over from the HTML site where Streamlit allows it."""

import streamlit as st

CSS = """
<style>
/* Dark banner at the top of each page, like the HTML site's header */
.slop-banner {
  background: #1a1410;
  padding: 36px 32px 30px;
  margin-bottom: 28px;
  border-bottom: 3px solid #c4a882;
}
.slop-kicker {
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.18em;
  text-transform: uppercase; color: #c4a882; margin-bottom: 12px;
}
.slop-banner h1 {
  color: #f5f0e8 !important; font-size: 2.3rem !important;
  line-height: 1.15 !important; padding: 0 !important; margin: 0 0 8px 0 !important;
}
.slop-banner h1 em { color: #c4a882; }
.slop-sub { color: #b8ab98; font-style: italic; font-size: 0.95rem; line-height: 1.6; }

/* Passage boxes (sample texts, exercise passages) */
.slop-passage {
  background: #fff; border-left: 3px solid #c4a882;
  padding: 14px 18px; line-height: 1.8; margin-bottom: 12px;
}

/* Small uppercase section labels */
.slop-label {
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.16em;
  text-transform: uppercase; color: #6b5030; margin: 8px 0 4px;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def banner(kicker: str, title_html: str, sub: str = ""):
    """Render the dark header banner. title_html may contain <em> for the gold italic."""
    sub_html = f'<div class="slop-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="slop-banner"><div class="slop-kicker">{kicker}</div>'
        f"<h1>{title_html}</h1>{sub_html}</div>",
        unsafe_allow_html=True,
    )


def label(text: str):
    st.markdown(f'<div class="slop-label">{text}</div>', unsafe_allow_html=True)
