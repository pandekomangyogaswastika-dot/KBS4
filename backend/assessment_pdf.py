"""Bilingual PDF report for an assessment session (ReportLab)."""
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

from assessment_engine import OTHER_SENTINEL, evaluate_show_if

INDIGO = colors.HexColor("#5B49C9")
TEAL = colors.HexColor("#1D7874")
INK = colors.HexColor("#1A1C25")
MUTED = colors.HexColor("#5B6070")
SOFT = colors.HexColor("#EEF1F7")


def _loc(val, locale):
    if isinstance(val, dict):
        return val.get(locale) or val.get("id") or val.get("en") or ""
    return str(val) if val is not None else ""


def _esc(text):
    return (str(text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _render_answer(q, ans, locale):
    skipped_txt = "(dilewati)" if locale == "id" else "(skipped)"
    none_txt = "(belum diisi)" if locale == "id" else "(not answered)"
    other_lbl = "Lainnya" if locale == "id" else "Other"
    if not ans:
        return none_txt
    if ans.get("skipped"):
        return skipped_txt
    val = ans.get("value")
    other = (ans.get("other_text") or "").strip()
    qtype = q.get("type")
    options = {o["value"]: o for o in q.get("options", [])}
    if qtype == "single_choice":
        if val == OTHER_SENTINEL:
            return f"{other_lbl}: {other}" if other else none_txt
        opt = options.get(val)
        return _loc(opt["label"], locale) if opt else (str(val) if val not in (None, "") else none_txt)
    if qtype == "multi_choice":
        if not val:
            return none_txt
        parts = []
        for v in val:
            if v == OTHER_SENTINEL:
                if other:
                    parts.append(f"{other_lbl}: {other}")
            else:
                opt = options.get(v)
                parts.append(_loc(opt["label"], locale) if opt else str(v))
        return ", ".join(parts) if parts else none_txt
    if qtype == "yes_no":
        if val in (True, "yes", "true"):
            return "Ya" if locale == "id" else "Yes"
        if val in (False, "no", "false"):
            return "Tidak" if locale == "id" else "No"
        return none_txt
    if qtype == "scale_1_5":
        return f"{val} / 5" if val not in (None, "") else none_txt
    if val in (None, ""):
        return none_txt
    return str(val)


def build_pdf(session, template, answers_map, progress, attachments_by_question, locale="id"):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                            leftMargin=16 * mm, rightMargin=16 * mm, title="Assessment Report")
    ss = getSampleStyleSheet()
    h_title = ParagraphStyle("t", parent=ss["Title"], textColor=INDIGO, fontSize=22, spaceAfter=2)
    h_sub = ParagraphStyle("s", parent=ss["Normal"], textColor=MUTED, fontSize=10, spaceAfter=2)
    h_dom = ParagraphStyle("d", parent=ss["Heading2"], textColor=colors.white, fontSize=12, leftIndent=4, spaceBefore=2, spaceAfter=2)
    q_style = ParagraphStyle("q", parent=ss["Normal"], textColor=INK, fontSize=10, leading=13, spaceBefore=6, alignment=TA_LEFT)
    a_style = ParagraphStyle("a", parent=ss["Normal"], textColor=TEAL, fontSize=10, leading=13, leftIndent=8)
    n_style = ParagraphStyle("n", parent=ss["Normal"], textColor=MUTED, fontSize=9, leading=12, leftIndent=8)

    story = []
    story.append(Paragraph("KUBUS TEKNOLOGI INDONESIA", h_sub))
    story.append(Paragraph(_esc(_loc(template.get("name"), locale)), h_title))
    meta = [
        ["Klien" if locale == "id" else "Client", _esc(session.get("client_name", "-"))],
        ["Proyek" if locale == "id" else "Project", _esc(session.get("project_name") or "-")],
        ["Kontak" if locale == "id" else "Contact", _esc(session.get("contact_person") or "-")],
        ["Status", _esc(session.get("status", "-"))],
        ["Progress", f"{progress.get('answered', 0)}/{progress.get('total', 0)} ({progress.get('percent', 0)}%)"],
    ]
    mt = Table(meta, colWidths=[35 * mm, 130 * mm])
    mt.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (0, -1), MUTED),
        ("TEXTCOLOR", (1, 0), (1, -1), INK),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, SOFT),
    ]))
    story.append(Spacer(1, 6))
    story.append(mt)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", color=INDIGO, thickness=1.2))

    answers_map = answers_map or {}
    for d in template.get("domains", []):
        visible = [q for q in d.get("questions", []) if evaluate_show_if(q.get("show_if"), answers_map)]
        if not visible:
            continue
        story.append(Spacer(1, 10))
        hdr = Table([[Paragraph(f"{d.get('number', '')}. {_esc(_loc(d.get('title'), locale))}", h_dom)]], colWidths=[166 * mm])
        hdr.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), INDIGO), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story.append(hdr)
        for q in visible:
            ans = answers_map.get(q["id"])
            story.append(Paragraph(f"<b>{_esc(_loc(q.get('prompt'), locale))}</b>", q_style))
            story.append(Paragraph(_esc(_render_answer(q, ans, locale)), a_style))
            note = (ans or {}).get("note")
            if note:
                story.append(Paragraph(f"{'Catatan' if locale == 'id' else 'Note'}: {_esc(note)}", n_style))
            atts = (attachments_by_question or {}).get(q["id"], [])
            if atts:
                names = ", ".join(_esc(a.get("original_name", "file")) for a in atts)
                story.append(Paragraph(f"\U0001F4CE {'Lampiran' if locale == 'id' else 'Attachments'} ({len(atts)}): {names}", n_style))

    doc.build(story)
    return buf.getvalue()
