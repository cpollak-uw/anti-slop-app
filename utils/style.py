"""Shared visual styling, carried over from the HTML site where Streamlit allows it."""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&display=swap');

/* Palette and fonts, applied here as well as in .streamlit/config.toml. The config
   file sets Streamlit's own theme, but a viewer's saved theme choice can override it,
   so these rules keep the page looking the same for everyone. */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background: #f5f0e8 !important;
  color: #1a1410 !important;
}
[data-testid="stSidebar"] { background: #ede8de !important; }
[data-testid="stSidebar"] * { color: #3a3028 !important; }
/* No !important here on purpose: these rules are inherited by ordinary text but
   leave Streamlit's icon fonts alone, which would otherwise print as words. */
.stApp { font-family: 'Source Serif 4', Georgia, serif; }
.stApp textarea, .stApp input, .stApp button, .stApp select {
  font-family: 'Source Serif 4', Georgia, serif;
}
/* Streamlit's icons are glyphs in an icon font. Without this they inherit the serif
   above and print as words such as "home" or "mail". */
[data-testid="stIconMaterial"] { font-family: 'Material Symbols Rounded' !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: 'Playfair Display', Georgia, serif !important;
  color: #1a1410 !important;
}
.stApp a { color: #6b5030 !important; }
[data-testid="stBaseButton-primary"] {
  background: #6b5030 !important; border-color: #6b5030 !important; color: #f5f0e8 !important;
}
[data-testid="stBaseButton-primary"] * { color: #f5f0e8 !important; }

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
