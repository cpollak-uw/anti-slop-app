"""Build a Word document from a student's responses so they can download it.

Nothing is stored on the server: the file is generated in memory and handed
straight to the student's browser.
"""

import io
from datetime import date

from docx import Document
from docx.shared import Pt


def build_docx(title: str, student_name: str, sections: list[tuple[str, str]]) -> bytes:
    """sections is a list of (heading, body) pairs. Empty bodies are marked as such."""
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Georgia"
    style.font.size = Pt(11)

    doc.add_heading(title, level=1)
    meta = doc.add_paragraph()
    meta.add_run(f"Name: {student_name or '(not entered)'}\n").bold = True
    meta.add_run(f"Date: {date.today().strftime('%B %d, %Y')}")

    for heading, body in sections:
        doc.add_heading(heading, level=2)
        doc.add_paragraph(body.strip() if body and body.strip() else "(no response)")

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()
