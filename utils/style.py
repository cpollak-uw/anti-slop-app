"""Shared visual styling, carried over from the HTML site where Streamlit allows it.

The app pins its own colors rather than relying on Streamlit's theme. A viewer can
switch Streamlit to dark mode from the app's Settings menu, and when that happened the
page kept this light background while Streamlit recolored its own text and widgets for
a dark one, which left text that was hard to read. Everything below sets both the
background and the text color of each surface, so the result is the same in either mode.
"""

import re

import streamlit as st

INK = "#1a1410"       # body text
CREAM = "#f5f0e8"     # page background
WARM = "#ede8de"      # sidebar, secondary surfaces
CARD = "#ffffff"      # cards, inputs
RULE = "#d5ccc0"      # borders
GOLD = "#c4a882"
BROWN = "#6b5030"     # primary accent
MUTED = "#5a4f44"     # captions

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,300..700;1,8..60,300..700&display=swap');

/* ── Surfaces ──────────────────────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"],
[data-testid="stBottomBlockContainer"] {{
  background: {CREAM} !important;
}}
[data-testid="stSidebar"], [data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {{ background: {WARM} !important; }}

/* Every piece of text, then the exceptions further down. Colour only: the icon
   font is set separately, because changing it prints icons as words. */
.stApp, .stApp *, [data-testid="stSidebar"] * {{ color: {INK} !important; }}
/* Streamlit dims captions with opacity, which axe-core reads as a much lighter
   colour than the one we set. Opacity is reset here so the contrast is real. */
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] * {{ color: {MUTED} !important; opacity: 1 !important; }}
.stApp [data-testid="stCaptionContainer"] {{ opacity: 1 !important; }}

/* Segmented control (the topic picker) keeps the theme's own button colours. */
.stApp [data-testid="stButtonGroup"] button,
.stApp [data-baseweb="button-group"] button {{
  background-color: {CARD} !important; border-color: {RULE} !important; color: {INK} !important;
}}
.stApp [data-testid="stButtonGroup"] button[aria-checked="true"],
.stApp [data-testid="stButtonGroup"] button[aria-pressed="true"],
.stApp [data-baseweb="button-group"] button[aria-checked="true"] {{
  background-color: {WARM} !important; border-color: {BROWN} !important;
}}
.stApp a, .stApp a * {{ color: {BROWN} !important; }}

/* ── Fonts (no !important, so Streamlit's icon font keeps working) ─────── */
.stApp {{ font-family: 'Source Serif 4', Georgia, serif; }}
.stApp textarea, .stApp input, .stApp button, .stApp select {{
  font-family: 'Source Serif 4', Georgia, serif;
}}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
  font-family: 'Playfair Display', Georgia, serif !important;
  color: {INK} !important;
}}
[data-testid="stIconMaterial"] {{ font-family: 'Material Symbols Rounded' !important; }}

/* ── Cards and expanders ──────────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {{
  border-color: {RULE} !important;
}}
.stApp [data-testid="stExpander"] details,
.stApp [data-testid="stExpander"] summary {{
  background: {CARD} !important; border-color: {RULE} !important;
}}

/* ── Form controls ────────────────────────────────────────────────────── */
.stApp textarea, .stApp input, .stApp [data-baseweb="input"],
.stApp [data-baseweb="base-input"], .stApp [data-baseweb="textarea"],
.stApp [data-baseweb="select"] > div {{
  background: {CARD} !important; color: {INK} !important; border-color: {RULE} !important;
}}
/* Placeholder and disabled text are checked against WCAG AA too: #6b6258 on white
   is about 6:1, where the lighter grey Streamlit uses is about 3.8:1. */
.stApp textarea::placeholder, .stApp input::placeholder {{ color: #6b6258 !important; opacity: 1 !important; }}
.stApp [disabled], .stApp [aria-disabled="true"], .stApp [disabled] *, .stApp [aria-disabled="true"] * {{
  opacity: 1 !important; color: {MUTED} !important; -webkit-text-fill-color: {MUTED} !important;
}}
/* Dropdown menus are drawn outside .stApp, so they need their own rules. */
[data-baseweb="popover"] [role="listbox"], [data-baseweb="popover"] li,
[data-baseweb="menu"], [data-baseweb="menu"] li {{
  background: {CARD} !important; color: {INK} !important;
}}
[data-baseweb="menu"] li:hover, [data-baseweb="popover"] li:hover {{ background: {WARM} !important; }}

[data-testid="stBaseButton-secondary"] {{
  background: {CARD} !important; color: {INK} !important; border-color: {GOLD} !important;
}}
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primary"] * {{
  background: {BROWN} !important; color: {CREAM} !important; border-color: {BROWN} !important;
}}
/* Radio circles: an outer ring with an inner dot. Both take their colour from the
   active Streamlit theme, so in dark mode the dot was drawn in near-black. */
[data-testid="stRadioOption"] > div > div:first-child {{
  background-color: {CARD} !important; border: 1.5px solid {BROWN} !important;
}}
[data-testid="stRadioOption"] > div > div:first-child > div {{ background-color: transparent !important; }}
[data-testid="stRadioOption"]:has(input:checked) > div > div:first-child > div {{
  background-color: {BROWN} !important;
}}
/* Checkbox: one box, filled when checked. */
[data-testid="stCheckbox"] label > div:not([data-testid]) {{
  background-color: {CARD} !important; border: 1.5px solid {BROWN} !important;
}}
[data-testid="stCheckbox"] label:has(input:checked) > div:not([data-testid]) {{
  background-color: {BROWN} !important;
}}
[data-testid="stProgressBarTrack"] {{ background-color: {RULE} !important; }}
[data-testid="stProgressBarTrack"] > div {{ background-color: {BROWN} !important; }}

/* Focus rings and other accents borrow Streamlit's primary color, which is red in
   the default dark theme. */
.stApp [data-baseweb="textarea"]:focus-within, .stApp [data-baseweb="input"]:focus-within,
.stApp [data-baseweb="base-input"]:focus-within, .stApp textarea:focus, .stApp input:focus {{
  border-color: {BROWN} !important; box-shadow: none !important; outline-color: {BROWN} !important;
}}
.stApp [data-baseweb="radio"] div[aria-checked="true"],
.stApp [data-baseweb="checkbox"] span[aria-checked="true"] {{ background-color: {BROWN} !important; }}

/* ── Tabs ─────────────────────────────────────────────────────────────── */
[data-baseweb="tab-list"], [data-baseweb="tab"] {{ background: transparent !important; }}
[data-baseweb="tab"] {{ color: {MUTED} !important; }}
[data-baseweb="tab"][aria-selected="true"], [data-baseweb="tab"][aria-selected="true"] * {{
  color: {INK} !important;
}}
[data-baseweb="tab-highlight"] {{ background-color: {BROWN} !important; }}
[data-baseweb="tab-border"] {{ background-color: {RULE} !important; }}

/* ── Banner ───────────────────────────────────────────────────────────── */
.slop-banner {{
  background: {INK} !important;
  padding: 36px 32px 30px;
  margin-bottom: 28px;
  border-bottom: 3px solid {GOLD};
}}
.slop-kicker {{
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.18em;
  text-transform: uppercase; color: {GOLD} !important; margin-bottom: 12px;
}}
.slop-banner h1 {{
  color: {CREAM} !important; font-size: 2.3rem !important;
  line-height: 1.15 !important; padding: 0 !important; margin: 0 0 8px 0 !important;
}}
.slop-banner h1 em {{ color: {GOLD} !important; }}
.slop-sub {{ color: #b8ab98 !important; font-style: italic; font-size: 0.95rem; line-height: 1.6; }}

/* ── Passages and labels ──────────────────────────────────────────────── */
.slop-passage {{
  background: {CARD}; border-left: 3px solid {GOLD};
  padding: 14px 18px; line-height: 1.8; margin-bottom: 12px; color: #2a201a;
}}
.slop-label {{
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.16em;
  text-transform: uppercase; color: {BROWN} !important; margin: 8px 0 4px;
}}

/* ── Callout boxes (used instead of Streamlit's own, which invert in dark mode) ── */
.slop-callout {{
  border-left: 3px solid; padding: 13px 17px; margin: 6px 0 14px;
  line-height: 1.7; font-size: 0.95rem;
}}
.slop-callout, .slop-callout * {{ color: #2a2118 !important; }}
.slop-callout strong {{ font-weight: 700; }}
.slop-callout.info    {{ background: {WARM};   border-color: {BROWN}; }}
.slop-callout.correct {{ background: #e8f4ee; border-color: #4a8c5c; }}
.slop-callout.wrong   {{ background: #fce8e8; border-color: #9c3a3a; }}
.slop-callout.note    {{ background: #fffbf2; border-color: #d4a840; }}
.slop-callout.refusal {{ background: #f0eef8; border-color: #5a4d8c; }}
.slop-callout.deliver {{ background: #eaf4ee; border-color: #4a8c5c; }}
.slop-callout .slop-callout-label {{
  display: block; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; margin-bottom: 5px;
}}

/* ── Keyboard focus ───────────────────────────────────────────────────── */
/* A visible focus indicator matters for anyone navigating by keyboard, and the
   rules above would otherwise leave only Streamlit's own faint ring. */
.stApp :focus-visible {{
  outline: 3px solid {BROWN} !important; outline-offset: 2px !important; border-radius: 2px;
}}

/* Text for screen readers only: gives the check and cross marks below a spoken
   equivalent, since a glyph alone tells a screen reader user nothing. */
.slop-sr-only {{
  position: absolute !important; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;
}}

/* ── Answer lines in locked quiz questions ───────────────────────────── */
.slop-opt {{ display: block; padding: 3px 6px; margin: 2px 0; line-height: 1.6; }}
.slop-opt.ok  {{ background: #e8f4ee; color: #1a3a28 !important; }}
.slop-opt.no  {{ background: #fce8e8; color: #5a1a1a !important; }}
.slop-opt.dim {{ color: #6b6258 !important; }}

/* ── Highlight marks ──────────────────────────────────────────────────── */
mark.hl-a {{ background: #fde68a !important; color: #2a2118 !important; border-radius: 2px; padding: 0 2px; }}
mark.hl-b {{ background: #bfdbfe !important; color: #2a2118 !important; border-radius: 2px; padding: 0 2px; }}
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


def light_markdown(text: str) -> str:
    """Convert the small amount of markdown used in our content into HTML.

    Needed because the callout boxes below are HTML, and Streamlit renders markdown
    only in its own elements.
    """
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    out = re.sub(r"(?<![\*\w])\*([^*]+?)\*(?!\*)", r"<em>\1</em>", out)
    lines = out.split("\n")
    rendered = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            rendered.append(f"&bull;&nbsp;{stripped[2:]}")
        else:
            rendered.append(stripped)
    return "<br>".join(x for x in rendered if x)


def callout(kind: str, body: str, title: str | None = None, icon: str | None = None,
             announce: bool = False):
    """A colored box with fixed colors, in place of st.info / st.success / st.warning.

    kind: info, correct, wrong, note, refusal, deliver
    """
    head = f'<span class="slop-callout-label">{title}</span>' if title else ""
    lead = f"{icon} " if icon else ""
    # announce=True marks the box as a live region, so a screen reader reads the
    # feedback out when it appears instead of leaving it to be discovered.
    role = ' role="status" aria-live="polite"' if announce else ""
    st.markdown(
        f'<div class="slop-callout {kind}"{role}>{head}{lead}{light_markdown(body)}</div>',
        unsafe_allow_html=True,
    )
