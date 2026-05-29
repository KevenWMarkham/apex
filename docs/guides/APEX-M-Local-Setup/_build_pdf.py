"""Render the APEX-M Local Setup README into a polished PDF.

Custom markdown handler tuned for the README's shape: headings,
paragraphs, fenced code blocks, pipe tables, bullets, and inline code.
Not a general-purpose md→pdf — just clean enough for this handoff.

Output: docs/guides/APEX-M-Local-Setup.pdf
"""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    Preformatted,
)

HERE = Path(__file__).parent
SRC = HERE / "README.md"
OUT = HERE.parent / "APEX-M-Local-Setup.pdf"

# --- Deloitte-flavored color palette ---
NAVY = colors.HexColor("#1A2339")
GOLD = colors.HexColor("#C89D3A")
DIM = colors.HexColor("#5A6478")
RULE = colors.HexColor("#E1E5EC")
CODE_BG = colors.HexColor("#F5F7FA")
TABLE_HEADER = colors.HexColor("#EEF1F5")


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Heading1"],
            fontName="Helvetica-Bold", fontSize=22, leading=26,
            textColor=NAVY, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=DIM, spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"],
            fontName="Helvetica-Bold", fontSize=16, leading=20,
            textColor=NAVY, spaceBefore=18, spaceAfter=10,
            borderPadding=(0, 0, 6, 0),
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"],
            fontName="Helvetica-Bold", fontSize=13, leading=17,
            textColor=NAVY, spaceBefore=14, spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading3"],
            fontName="Helvetica-Bold", fontSize=11, leading=15,
            textColor=NAVY, spaceBefore=10, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=NAVY, spaceAfter=6, alignment=TA_LEFT,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"],
            fontName="Helvetica", fontSize=10, leading=14,
            textColor=NAVY, leftIndent=18, bulletIndent=4,
            spaceAfter=2,
        ),
        "code": ParagraphStyle(
            "Code", parent=base["Code"],
            fontName="Courier", fontSize=8.5, leading=11,
            textColor=NAVY, backColor=CODE_BG,
            borderColor=RULE, borderWidth=0.5, borderPadding=8,
            leftIndent=0, rightIndent=0,
            spaceBefore=4, spaceAfter=8,
        ),
        "cell": ParagraphStyle(
            "Cell", parent=base["BodyText"],
            fontName="Helvetica", fontSize=9, leading=12,
            textColor=NAVY, alignment=TA_LEFT,
        ),
        "cell_hdr": ParagraphStyle(
            "CellHdr", parent=base["BodyText"],
            fontName="Helvetica-Bold", fontSize=9, leading=12,
            textColor=NAVY, alignment=TA_LEFT,
        ),
    }


def inline(text: str) -> str:
    """Convert Markdown inline markers to ReportLab inline-XML."""
    text = re.sub(r"`([^`]+)`",
                  r'<font name="Courier" size="9" color="#1A2339" '
                  r'backColor="#F5F7FA">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  r'<link href="\2" color="#1A2339"><u>\1</u></link>', text)
    # Status emoji → text fallback (PDF font doesn't always have color emoji)
    text = (text
            .replace("✅", "<font color='#1E7A1E'>[YES]</font>")
            .replace("❌", "<font color='#B8232F'>[NO]</font>")
            .replace("🟢", "<font color='#1E7A1E'>[OK]</font>")
            .replace("🟡", "<font color='#C89D3A'>[CAUTION]</font>")
            .replace("⚠️", "<font color='#C89D3A'>[!]</font>"))
    return text


def parse_table(lines: list[str], idx: int) -> tuple[list[list[str]], int]:
    """Pipe-table parser. Returns (rows, next_idx)."""
    rows = []
    while idx < len(lines) and lines[idx].lstrip().startswith("|"):
        row = [c.strip() for c in lines[idx].strip().strip("|").split("|")]
        rows.append(row)
        idx += 1
    # Drop the alignment row (|---|---|)
    if len(rows) >= 2 and all(re.fullmatch(r"-+:?|:-+:?|:-+", c.replace(" ", ""))
                              for c in rows[1]):
        rows = [rows[0]] + rows[2:]
    return rows, idx


def build_table(rows: list[list[str]], styles) -> Table:
    data = [[Paragraph(inline(c), styles["cell_hdr"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(inline(c), styles["cell"]) for c in r])
    n_cols = len(rows[0])
    # Even column widths within 6.5" usable
    col_w = (6.5 * inch) / n_cols
    t = Table(data, colWidths=[col_w] * n_cols, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def render(md_path: Path, pdf_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    styles = make_styles()
    story = []

    # --- Header band ---
    story.append(Paragraph("APEX-M · Local Setup Package", styles["title"]))
    story.append(Paragraph(
        "Developer handoff · run APEX-M against in-process mocks · "
        "Independence-clean by construction",
        styles["subtitle"],
    ))

    i = 0
    in_code = False
    code_buf: list[str] = []

    while i < len(lines):
        line = lines[i]

        # --- Fenced code block ---
        if line.lstrip().startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_buf), styles["code"]))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        stripped = line.strip()

        # --- Horizontal rule ---
        if re.fullmatch(r"-{3,}", stripped):
            story.append(Spacer(1, 6))
            story.append(Table([[""]], colWidths=[6.5 * inch], rowHeights=[1],
                               style=TableStyle([
                                   ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
                               ])))
            story.append(Spacer(1, 6))
            i += 1
            continue

        # --- Headings ---
        if stripped.startswith("# "):
            # Skip the top-level title (already rendered)
            if i < 5:
                i += 1
                continue
            story.append(Paragraph(inline(stripped[2:]), styles["h1"]))
            i += 1
            continue
        if stripped.startswith("## "):
            story.append(Paragraph(inline(stripped[3:]), styles["h2"]))
            i += 1
            continue
        if stripped.startswith("### "):
            story.append(Paragraph(inline(stripped[4:]), styles["h3"]))
            i += 1
            continue

        # --- Tables ---
        if stripped.startswith("|") and stripped.endswith("|"):
            rows, i = parse_table(lines, i)
            story.append(build_table(rows, styles))
            story.append(Spacer(1, 6))
            continue

        # --- Bullets ---
        if re.match(r"^\s*[-*]\s+", line):
            content = re.sub(r"^\s*[-*]\s+", "", line)
            story.append(Paragraph(
                f"• {inline(content)}", styles["bullet"]
            ))
            i += 1
            continue

        # --- Blockquote ---
        if stripped.startswith(">"):
            content = stripped.lstrip("> ").strip()
            story.append(Paragraph(
                f'<i><font color="#5A6478">{inline(content)}</font></i>',
                styles["body"],
            ))
            i += 1
            continue

        # --- Empty line ---
        if not stripped:
            i += 1
            continue

        # --- Paragraph (collect continuation lines until break) ---
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_starter(lines[i]):
            para_lines.append(lines[i])
            i += 1
        para = " ".join(l.strip() for l in para_lines)
        story.append(Paragraph(inline(para), styles["body"]))

    # --- Build doc ---
    doc = SimpleDocTemplate(
        str(pdf_path), pagesize=LETTER,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        title="APEX-M Local Setup", author="Deloitte APEX Team",
    )

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(DIM)
        canvas.drawString(0.75 * inch, 0.5 * inch,
                          "APEX-M Local Setup · v1.0 · 2026-05-29")
        canvas.drawRightString(8.0 * inch, 0.5 * inch,
                               f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def _is_block_starter(line: str) -> bool:
    s = line.strip()
    return (
        s.startswith("#")
        or s.startswith("|")
        or s.startswith("- ")
        or s.startswith("* ")
        or s.startswith(">")
        or s.startswith("```")
        or re.fullmatch(r"-{3,}", s) is not None
    )


if __name__ == "__main__":
    render(SRC, OUT)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
