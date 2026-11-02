# -*- coding: utf-8 -*-
"""
generate_deliverables.py
Production-grade deliverable generator for the Josh Talks Growth Assignment.
Preserves all validated numbers, research findings, audit distinctions, and citations.
Produces publication-quality PDFs, high-fidelity mockups, Word documents,
practical execution guides, and synchronizes deliverables to FINAL_SUBMISSION.
"""

from pathlib import Path
from datetime import datetime
import textwrap
import json
import shutil

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas

ROOT = Path(r"D:\AllProjects\Josh Talks assignment")
WORK = ROOT / "Supporting_Work"
TABLES = WORK / "tables"
CHARTS = WORK / "charts"
OUT_DELIV = ROOT / "deliverables"
OUT_FINAL = ROOT / "FINAL_SUBMISSION"

for folder in [
    OUT_DELIV / "Q1",
    OUT_DELIV / "Q2" / "Samarth_Kapdi_Proof",
    OUT_FINAL / "Q1",
    OUT_FINAL / "Q2" / "Samarth_Kapdi_Proof",
    OUT_FINAL / "Supporting_Work" / "tables",
    OUT_FINAL / "Supporting_Work" / "charts",
    OUT_FINAL / "Supporting_Work" / "analysis",
]:
    folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "consolidated_recordings.csv")
df["Nova-3 DER %"] = pd.to_numeric(df["Nova-3 DER %"], errors="coerce")
df = df.sort_values("Nova-3 DER %", ascending=False).reset_index(drop=True)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = self._pagesize
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header on pages 2+
        if self._pageNumber > 1:
            title_text = getattr(self, "doc_title", "Technical Deliverable")
            self.drawString(36, h - 26, title_text)
            self.drawRightString(w - 36, h - 26, "Josh Talks Growth Assignment Audit")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, h - 30, w - 36, h - 30)

        # Running Footer on all pages
        self.drawString(36, 20, "Confidential - Josh Talks Speaker Diarization Benchmark Audit (Nov 2026)")
        self.drawRightString(w - 36, 20, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 30, w - 36, 30)
        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="DocTitle",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=2
    ))
    styles.add(ParagraphStyle(
        name="DocSubtitle",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name="SecHeading",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="SubHeading",
        fontName="Helvetica-Bold",
        fontSize=8.0,
        leading=10.5,
        textColor=colors.HexColor("#334155"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="Callout",
        fontName="Helvetica-Oblique",
        fontSize=7.0,
        leading=9.4,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=2,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=6.5,
        leading=8.0,
        textColor=colors.white,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=6.2,
        leading=7.6,
        textColor=colors.HexColor("#0F172A")
    ))
    styles.add(ParagraphStyle(
        name="TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=6.2,
        leading=7.6,
        textColor=colors.HexColor("#0F172A")
    ))
    styles.add(ParagraphStyle(
        name="TableCellCenter",
        fontName="Helvetica",
        fontSize=6.2,
        leading=7.6,
        textColor=colors.HexColor("#0F172A"),
        alignment=1
    ))
    styles.add(ParagraphStyle(
        name="TableCellCenterBold",
        fontName="Helvetica-Bold",
        fontSize=6.2,
        leading=7.6,
        textColor=colors.HexColor("#0F172A"),
        alignment=1
    ))
    return styles


def build_pdf_document(path, title, story, pagesize=A4):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=pagesize,
        leftMargin=36,
        rightMargin=36,
        topMargin=38,
        bottomMargin=38
    )
    def make_canvas(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c.doc_title = title
        return c
    doc.build(story, canvasmaker=make_canvas)


# ---------------------------------------------------------------------------
# 1. GENERATE HIGH-FIDELITY LEADERBOARD MOCKUP
# ---------------------------------------------------------------------------
def generate_mockup_image():
    out_path = OUT_DELIV / "Q1" / "Q1_Leaderboard_Mockup.png"
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=180)
    ax.axis("off")

    # Header Card
    hdr_box = patches.FancyBboxPatch((0.02, 0.88), 0.96, 0.10, boxstyle="round,pad=0.015",
                                     facecolor="#0F172A", edgecolor="none")
    ax.add_patch(hdr_box)
    ax.text(0.04, 0.94, "Josh Talks | Conversational Diarization Benchmark",
            fontsize=18, weight="bold", color="white")
    ax.text(0.04, 0.90, "Public Evaluation Leaderboard v1.0 • Pinned Zero-Collar Evaluation • Overlap Evaluated • Hungarian Optimal Mapping",
            fontsize=9.5, color="#94A3B8")
    ax.text(0.85, 0.92, "100.0 Hours Held-out\n250 Sessions • Updated Nov 2026",
            fontsize=8.5, color="#38BDF8", ha="center")

    # Filter Bar Card
    filt_box = patches.FancyBboxPatch((0.02, 0.77), 0.96, 0.09, boxstyle="round,pad=0.015",
                                      facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.8)
    ax.add_patch(filt_box)
    ax.text(0.04, 0.825, "FILTER EVALUATION TRACKS:", fontsize=8.5, weight="bold", color="#334155")
    
    filters = [
        ("Language / Accent:", "All (Indian English, Hindi/Hinglish, Regional)"),
        ("Speakers:", "All (1-8 Speakers)"),
        ("Setting:", "All (In-Person / Online)"),
        ("Overlap Track:", "Overlap Included (Strict)"),
        ("Operating Mode:", "Batch Transcription"),
    ]
    cur_x = 0.04
    for k, v in filters:
        ax.text(cur_x, 0.785, f"{k} ", fontsize=8, weight="bold", color="#1E293B")
        kw_len = len(k) * 0.0055
        ax.text(cur_x + kw_len, 0.785, f"[{v}]", fontsize=8, color="#2563EB")
        cur_x += kw_len + len(v) * 0.0055 + 0.022

    # Leaderboard Table
    headers = [
        "Rank", "System / Model Checkpoint", "Provider", "DER ↓ (95% CI)",
        "JER ↓", "Miss %", "FA %", "Conf %", "Overlap DER", "SCE (MAE)",
        "RTF", "Latency (s)", "Cost ($/hr)", "Fail %", "Track"
    ]
    rows = [
        ["1", "speaker-diarization-3.1", "pyannote", "8.4% [7.2 - 9.6]", "10.1%", "3.2%", "1.1%", "4.1%", "14.2%", "0.21", "0.38x", "18.2s", "$0.12*", "0.0%", "Batch (Self)"],
        ["2", "MSDD / ClusteringDiarizer", "NVIDIA NeMo", "9.0% [7.5 - 10.5]", "11.3%", "4.0%", "0.9%", "4.1%", "15.8%", "0.25", "0.22x", "10.5s", "$0.09*", "0.0%", "Batch (Self)"],
        ["3", "Universal-2 (Best + Diarize)", "AssemblyAI", "11.2% [9.6 - 12.8]", "12.8%", "4.8%", "1.2%", "5.2%", "18.5%", "0.32", "0.18x", "8.6s", "$0.90", "0.0%", "Batch (API)"],
        ["4", "Enhanced + Diarization", "Speechmatics", "11.7% [10.1 - 13.3]", "13.2%", "5.4%", "1.4%", "4.9%", "19.1%", "0.30", "0.25x", "12.0s", "$1.05", "0.0%", "Batch (API)"],
        ["5", "Scribe v2 (Speaker Labels)", "ElevenLabs", "12.4% [10.6 - 14.2]", "14.0%", "5.8%", "1.5%", "5.1%", "20.2%", "0.35", "0.30x", "14.4s", "$0.80", "0.0%", "Batch (API)"],
        ["6", "Nova-3 (Benchmark Setting)", "Deepgram", "64.45% [53.1 - 75.8]", "68.2%", "58.1%", "2.4%", "3.9%", "78.4%", "1.48", "0.15x", "7.2s", "$0.43", "13.3%", "Batch (API)"]
    ]

    table = ax.table(cellText=rows, colLabels=headers, loc="center",
                     bbox=[0.02, 0.38, 0.96, 0.36])
    table.auto_set_font_size(False)
    table.set_fontsize(7.5)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        cell.set_height(0.048)
        if r == 0:
            cell.set_facecolor("#1E293B")
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
            cell.get_text().set_fontsize(7.8)
        elif r % 2 == 1:
            cell.set_facecolor("#FFFFFF")
        else:
            cell.set_facecolor("#F8FAFC")
        
        # Highlighting Nova-3 severe underperformance
        if r == 6 and c == 3:
            cell.set_facecolor("#FEE2E2")
            cell.get_text().set_color("#B91C1C")
            cell.get_text().set_weight("bold")
        if r == 6 and c == 5:
            cell.set_facecolor("#FEF2F2")
            cell.get_text().set_color("#DC2626")

    # Bottom Model Drill-Down Card
    dtl_box = patches.FancyBboxPatch((0.02, 0.03), 0.96, 0.31, boxstyle="round,pad=0.015",
                                     facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=0.8)
    ax.add_patch(dtl_box)
    ax.text(0.04, 0.305, "MODEL DETAIL & ERROR DECOMPOSITION VIEW - SELECTED SYSTEM: Deepgram Nova-3 (Batch API)",
            fontsize=9.5, weight="bold", color="#0F172A")
    
    col1 = [
        "Audit Baseline Scope: 15-Recording Workbook Sample",
        "- Sample Mean DER: 64.45% | Median DER: 86.02%",
        "- Historical Public Benchmark (139 recs): 67.1% DER",
        "- Separate Current Leaderboard (1 Nov 2026): 71.89% cpWER",
        "- Primary Error Driver: Missed Speech (avg 58.1% of error)",
        "- 5 Worst Rows: 0.0% to 9.8% Nova-3 speech coverage"
    ]
    col2 = [
        "Acoustic & Environmental Diagnostics",
        "- Indian English In-Person Meetings: Severe Failure (97-100% DER)",
        "- Online Zoom/Meet (Vietnamese/US English): Acceptable (26.8-28.7% DER)",
        "- 2-Speaker In-Person Baseline: 15.13% DER (97.4% speech coverage)",
        "- Silero VAD Reference Coverage: High across all rows (91.5% - 99.0%)",
        "- Empty Nova-3 Output RTTMs: D20260825_S003_012 & S003_015 (0 segments)"
    ]
    col3 = [
        "Fairness & Reproducibility Audit Controls",
        "- Primary Metric: DER with 0.0s collar, overlap evaluated",
        "- Speaker Count Policy: Autonomous estimation (1-8 uniform range)",
        "- Hungarian 1-to-1 Mapping: Optimal bipartite intersection per session",
        "- Diagnostic Parameter Check: diarize_model=latest, metadata.diarize_info",
        "- Manual Run Status: 7 runs required (5 baseline + 2 alt) - NOT PERFORMED"
    ]

    for i, line in enumerate(col1):
        ax.text(0.04, 0.265 - i * 0.038, line, fontsize=7.5, color="#1E293B")
    for i, line in enumerate(col2):
        ax.text(0.36, 0.265 - i * 0.038, line, fontsize=7.5, color="#1E293B")
    for i, line in enumerate(col3):
        ax.text(0.68, 0.265 - i * 0.038, line, fontsize=7.5, color="#1E293B")

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    shutil.copy2(out_path, OUT_FINAL / "Q1" / "Q1_Leaderboard_Mockup.png")
    print("Generated Q1 Leaderboard Mockup PNG successfully")


# ---------------------------------------------------------------------------
# 2. GENERATE Q2 POOR VS GOOD EVIDENCE CHART
# ---------------------------------------------------------------------------
def generate_poor_good_chart():
    chart_path = CHARTS / "q2_poor_good_evidence.png"
    evidence_ids = [
        "D20260825_S003_015_5SPK_IN_EN",
        "D20260825_S003_014_5SPK_IN_EN",
        "D20260826_S001_03_4SPK_IN_EN",
        "D20260826_S001_05_4SPK_IN_EN",
        "D20260825_S004_31_2SPK_IN_EN",
        "O20260826_S010_04_01_4SPK_US_EN",
    ]
    evidence = df[df["Session ID"].isin(evidence_ids)].copy()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.0), dpi=180)
    labels = [x[-14:] for x in evidence["Session ID"]]

    # Subplot 1: DER %
    axes[0].bar(labels, evidence["Nova-3 DER %"], color=["#DC2626"] * 4 + ["#2563EB"] * 2, width=0.55)
    axes[0].set_title("Nova-3 Diarization Error Rate (DER %)\n4 Severe Failures vs 2 Good Controls", fontsize=9.0, weight="bold")
    axes[0].set_ylabel("DER (%) - Lower is Better", fontsize=8.0)
    axes[0].tick_params(axis="x", rotation=40, labelsize=7.0)
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)
    for i, v in enumerate(evidence["Nova-3 DER %"]):
        axes[0].text(i, v + 1.5, f"{v:.1f}%", ha="center", fontsize=7.0, weight="bold")

    # Subplot 2: Speech Coverage %
    axes[1].bar(labels, evidence["Speech covered by Nova-3 (%)"], color=["#DC2626"] * 4 + ["#2563EB"] * 2, width=0.55)
    axes[1].set_title("Nova-3 Speech Coverage (% of Reference Duration)\nReveals Catastrophic Under-Coverage", fontsize=9.0, weight="bold")
    axes[1].set_ylabel("Coverage (%) - Higher is Better", fontsize=8.0)
    axes[1].tick_params(axis="x", rotation=40, labelsize=7.0)
    axes[1].grid(axis="y", linestyle="--", alpha=0.5)
    for i, v in enumerate(evidence["Speech covered by Nova-3 (%)"]):
        axes[1].text(i, v + 1.5, f"{v:.1f}%", ha="center", fontsize=7.0, weight="bold")

    fig.tight_layout()
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)
    shutil.copy2(chart_path, OUT_FINAL / "Supporting_Work" / "charts" / "q2_poor_good_evidence.png")
    print("Generated Q2 Poor vs Good Evidence Chart successfully")


# ---------------------------------------------------------------------------
# 3. BUILD Q1 MAIN RESEARCH DOCUMENT PDF
# ---------------------------------------------------------------------------
def build_q1_main_pdf():
    pdf_path = OUT_DELIV / "Q1" / "Q1_Main_Research_Document.pdf"
    styles = get_styles()
    story = []

    # Title & Subtitle
    story.append(Paragraph("Question 1 - Speaker Diarization Evaluation and Leaderboard Design", styles["DocTitle"]))
    story.append(Paragraph("A Methodological Architecture for Conversational Multi-Speaker Diarization in Indian Audio Contexts", styles["DocSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceAfter=6))

    # Section 1
    story.append(Paragraph("1. Purpose and Evaluation Stakeholders", styles["SecHeading"]))
    story.append(Paragraph(
        "Speaker diarization solves the foundational problem of estimating 'who spoke when' in audio streams, generating time intervals attributed to anonymous speaker IDs. "
        "A single aggregate score cannot satisfy diverse industry requirements: meeting intelligence platforms prioritize conversational turn-taking and overlap attribution; "
        "contact centers need turn-level compliance and agent-customer segmentation; speech analytics vendors depend on temporal stability for downstream LLM prompts; "
        "and enterprise buyers demand empirical trade-offs across accuracy, latency, deployment security, and cost per hour. "
        "This benchmark design establishes a reproducible, multi-dimensional evaluation standard specifically calibrated for challenging Indian conversational acoustic environments.",
        styles["Body"]
    ))

    # Section 2: 10 Systems Table
    story.append(Paragraph("2. Evaluation Shortlist: Ten Representative Systems", styles["SecHeading"]))
    story.append(Paragraph(
        "The evaluation shortlist spans self-hosted neural diarizers and leading commercial speech APIs. All product capabilities, underlying models, and configurations must be pinned on evaluation day from provider metadata.",
        styles["Body"]
    ))

    th = styles["TableHeader"]
    tc = styles["TableCell"]
    tcb = styles["TableCellBold"]
    tcc = styles["TableCellCenter"]

    shortlist_data = [
        [Paragraph("System", th), Paragraph("Provider", th), Paragraph("Model Checkpoint to Freeze", th), Paragraph("Deployment", th), Paragraph("Diarization Mode / Overlap", th), Paragraph("Official Documentation URL", th)],
        [Paragraph("pyannote.audio", tcb), Paragraph("pyannote", tc), Paragraph("speaker-diarization-3.1", tc), Paragraph("Self-hosted", tcc), Paragraph("Offline batch; native multi-speaker overlap", tc), Paragraph("https://github.com/pyannote/pyannote-audio", tc)],
        [Paragraph("NVIDIA NeMo", tcb), Paragraph("NVIDIA", tc), Paragraph("MSDD / Clustering / Sortformer", tc), Paragraph("Self-hosted", tcc), Paragraph("Batch & streaming neural diarizer", tc), Paragraph("https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/models.html", tc)],
        [Paragraph("Deepgram", tcb), Paragraph("Deepgram", tc), Paragraph("Nova-3 (diarize=true, diarize_model=latest)", tc), Paragraph("Commercial API", tcc), Paragraph("Batch & streaming diarization", tc), Paragraph("https://developers.deepgram.com/docs/diarization", tc)],
        [Paragraph("AssemblyAI", tcb), Paragraph("AssemblyAI", tc), Paragraph("Universal-2 (speaker_labels=true)", tc), Paragraph("Commercial API", tcc), Paragraph("Batch transcription + speaker clustering", tc), Paragraph("https://www.assemblyai.com/docs/speech-to-text/speaker-diarization", tc)],
        [Paragraph("Google Cloud", tcb), Paragraph("Google", tc), Paragraph("Chirp 2 (diarization_config)", tc), Paragraph("Commercial API", tcc), Paragraph("Batch & streaming Speech-to-Text", tc), Paragraph("https://cloud.google.com/speech-to-text/docs/multiple-voices", tc)],
        [Paragraph("Azure AI Speech", tcb), Paragraph("Microsoft", tc), Paragraph("ConversationTranscriber / Batch STT", tc), Paragraph("Commercial API", tcc), Paragraph("Real-time & batch conversation diarization", tc), Paragraph("https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-stt-diarization", tc)],
        [Paragraph("AWS Transcribe", tcb), Paragraph("Amazon", tc), Paragraph("Amazon Transcribe (ShowSpeakerLabels)", tc), Paragraph("Commercial API", tcc), Paragraph("Batch & streaming speaker labels", tc), Paragraph("https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html", tc)],
        [Paragraph("Speechmatics", tcb), Paragraph("Speechmatics", tc), Paragraph("Enhanced model with diarization", tc), Paragraph("Commercial API", tcc), Paragraph("Batch & real-time diarization", tc), Paragraph("https://docs.speechmatics.com/features/speaker-diarization", tc)],
        [Paragraph("Gladia", tcb), Paragraph("Gladia", tc), Paragraph("Gladia STT with speaker diarization", tc), Paragraph("Commercial API", tcc), Paragraph("Batch API diarization architecture", tc), Paragraph("https://docs.gladia.io/docs/speaker-diarization", tc)],
        [Paragraph("ElevenLabs", tcb), Paragraph("ElevenLabs", tc), Paragraph("Scribe v2 with speaker labels", tc), Paragraph("Commercial API", tcc), Paragraph("Batch STT with speaker diarization", tc), Paragraph("https://elevenlabs.io/docs/api-reference/speech-to-text", tc)],
    ]
    t_shortlist = Table(shortlist_data, colWidths=[68, 62, 105, 50, 105, 133])
    t_shortlist.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_shortlist)
    story.append(Paragraph(
        "<b>Terminology Disclosure:</b> AWS Transcribe documentation uses the terms 'speaker labels' or 'speaker identification'. "
        "In this benchmark, AWS output is evaluated strictly as anonymous speaker clustering (diarization), NOT as biometric speaker recognition or personal identity verification.",
        styles["Callout"]
    ))

    # Section 3
    story.append(Paragraph("3. Version Freezing, Capability Disclosure, and Vendor Limitations", styles["SecHeading"]))
    story.append(Paragraph(
        "Commercial cloud APIs present rolling update risks: vendors frequently release undocumented backend updates without version-tag increments. "
        "To enforce rigorous scientific reproducibility: (a) exact API request dates, query parameters, SDK versions, and returned response headers must be logged; "
        "(b) request JSON payloads and raw provider responses must be permanently archived; and (c) if an official endpoint fails or mutates during evaluation, "
        "the capability is flagged as 'Unknown / Disclosed Limitation' rather than inferred.",
        styles["Body"]
    ))

    # Section 4
    story.append(Paragraph("4. Committed Primary Scoring Policy & Algorithmic Rules", styles["SecHeading"]))
    story.append(Paragraph(
        "To prevent ambiguity, the benchmark explicitly commits to a single primary scoring standard: "
        "<br/>- <b>Primary Metric:</b> Diarization Error Rate (DER) evaluated at <b>0.0 s collar (zero-collar)</b> with <b>overlap included</b>. "
        "Conversational Indian speech features frequent interruptions and short turn durations (median 1.2 s). Forgiving 250 ms at every boundary artificially obscures turn-boundary errors. "
        "<br/>- <b>Secondary / Legacy Track:</b> DER evaluated with 0.25 s collar (reported in auxiliary columns for historical benchmark comparison). "
        "<br/>- <b>Speaker Mapping Algorithm:</b> Global Hungarian (Munkres) optimal bipartite matching per session, maximizing total overlapping speech duration between reference and hypothesis speakers. No cross-session speaker tracking is assumed. "
        "<br/>- <b>Speaker-Count Policy:</b> Unconstrained / autonomous speaker counting. Systems must determine speaker cardinality autonomously. Ground-truth speaker count hints are strictly forbidden on the primary leaderboard; if an API mandates an upper bound, a uniform range of 1-8 is passed to all eligible systems.",
        styles["Body"]
    ))

    # Section 5
    story.append(PageBreak())
    story.append(Paragraph("5. Mathematical Definitions of Core Diarization Metrics", styles["SecHeading"]))
    story.append(Paragraph(
        "<b>Diarization Error Rate (DER):</b> Let T_ref be total reference speech time across all speakers (including overlapping speech). DER is the fraction of reference speech incorrectly attributed:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>DER = (T_miss + T_fa + T_conf) / T_ref</b><br/>"
        "where <i>T_miss</i> (Missed Speech) is reference speech detected as silence; <i>T_fa</i> (False Alarm) is hypothesis speech where no reference speech exists; "
        "and <i>T_conf</i> (Speaker Confusion) is hypothesis speech attributed to the wrong mapped speaker under the optimal Hungarian bijection.<br/>"
        "<b>Jaccard Error Rate (JER):</b> Evaluates per-speaker segmentation accuracy with equal weight per speaker regardless of total talking time:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>JER = (1 / |S_eval|) * sum_{s in S_eval} [ 1 - |R_s intersect H_m(s)| / |R_s union H_m(s)| ]</b><br/>"
        "where R_s is reference speech for speaker s, H_m(s) is hypothesis speech for mapped speaker m(s), and S_eval contains all reference speakers plus unmapped hypothesis speakers (penalized at 1.0). "
        "JER prevents a single dominant talker from masking complete failure on minor conversational participants.",
        styles["Body"]
    ))

    # Section 6: 100-Hour Corpus
    story.append(Paragraph("6. Stratified 100-Hour Evaluation Corpus", styles["SecHeading"]))
    story.append(Paragraph(
        "The evaluation corpus totals exactly <b>100.0 hours</b> across ~250 held-out conversational sessions, reflecting realistic Indian linguistic and acoustic diversity: "
        "<br/>- <b>Stratum 1 (40.0 hrs, 100 sessions):</b> Indian English conversations across professional and casual domains (1-8 speakers; 50% in-person, 50% online). "
        "<br/>- <b>Stratum 2 (25.0 hrs, 65 sessions):</b> Hindi and Hinglish conversational code-switching (1-6 speakers; mixed in-person and online). "
        "<br/>- <b>Stratum 3 (20.0 hrs, 50 sessions):</b> Regional Indian languages with English code-switching: Tamil, Telugu, Marathi, and Bengali (2-6 speakers). "
        "<br/>- <b>Stratum 4 (15.0 hrs, 35 sessions):</b> Acoustic & noise stress cases: 8 kHz PSTN telephony, reverberant halls, cafeteria ambient noise, and low-SNR field recordings (2-8 speakers). "
        "<br/>Total allocation: <b>40.0 + 25.0 + 20.0 + 15.0 = 100.0 hours</b>. Speaker distribution across all strata: 25% (1-2 spk), 45% (3-4 spk), 25% (5-6 spk), 5% (7-8 spk). Minimum 20% overlapping speech.",
        styles["Body"]
    ))

    # Section 7: Device Cross-Tabulation
    story.append(Paragraph("7. Hardware Capture Device Allocation & Cross-Tabulation Matrix", styles["SecHeading"]))
    story.append(Paragraph(
        "Hardware capture device significantly impacts acoustic SNR, reverberation, and far-field microphone array beamforming. The 100 hours are cross-tabulated across physical hardware and acoustic settings:",
        styles["Body"]
    ))

    device_data = [
        [Paragraph("Acoustic Setting / Strata", th), Paragraph("Smartphone Tabletop / Handset", th), Paragraph("Laptop Built-in Array Mic", th), Paragraph("Meeting Room Boundary Mic", th), Paragraph("Headset / Lapel Wearable", th), Paragraph("Total Hours", th)],
        [Paragraph("In-Person Meetings & Huddles", tcb), Paragraph("20.0 hrs", tcc), Paragraph("0.0 hrs", tcc), Paragraph("20.0 hrs", tcc), Paragraph("10.0 hrs", tcc), Paragraph("50.0 hrs", tcc)],
        [Paragraph("Online Conferencing (Meet/Zoom)", tcb), Paragraph("0.0 hrs", tcc), Paragraph("30.0 hrs", tcc), Paragraph("0.0 hrs", tcc), Paragraph("10.0 hrs", tcc), Paragraph("40.0 hrs", tcc)],
        [Paragraph("Telephony & Ambient Noise Stress", tcb), Paragraph("10.0 hrs", tcc), Paragraph("0.0 hrs", tcc), Paragraph("0.0 hrs", tcc), Paragraph("0.0 hrs", tcc), Paragraph("10.0 hrs", tcc)],
        [Paragraph("Total Allocation Across Corpus", styles["TableCellBold"]), Paragraph("30.0 hrs (30%)", styles["TableCellCenterBold"]), Paragraph("30.0 hrs (30%)", styles["TableCellCenterBold"]), Paragraph("20.0 hrs (20%)", styles["TableCellCenterBold"]), Paragraph("20.0 hrs (20%)", styles["TableCellCenterBold"]), Paragraph("100.0 hrs (100%)", styles["TableCellCenterBold"])],
    ]
    t_device = Table(device_data, colWidths=[123, 95, 95, 95, 65, 50])
    t_device.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_device)

    # Section 8: Supporting Metrics Suite
    story.append(Paragraph("8. Comprehensive Supporting Metrics Suite", styles["SecHeading"]))
    story.append(Paragraph(
        "To provide holistic evaluation beyond aggregate DER, the platform computes 10 supporting metrics: "
        "<br/>1. <b>Missed Speech Rate (MISS %):</b> T_miss / T_ref - measures detector under-coverage and voice activity omission. "
        "<br/>2. <b>False Alarm Rate (FA %):</b> T_fa / T_ref - measures hallucinated speech over background silence or noise. "
        "<br/>3. <b>Speaker Confusion Rate (CONF %):</b> T_conf / T_ref - measures speaker classification error during detected speech. "
        "<br/>4. <b>Overlap DER (%):</b> DER computed exclusively on time intervals where >=2 reference speakers speak simultaneously. "
        "<br/>5. <b>Speaker Count Error (SCE):</b> Mean Absolute Error |N_hyp - N_ref| and signed bias (N_hyp - N_ref) measuring cardinality drift. "
        "<br/>6. <b>Speech Coverage (%):</b> Hypothesis speech duration overlapping reference speech divided by total reference duration. "
        "<br/>7. <b>Real-Time Factor (RTF):</b> Total processing wall-clock time divided by audio duration (latency / duration). "
        "<br/>8. <b>Latency / Turnaround (s):</b> P50 and P90 turnaround time from session ingestion to completed RTTM emission. "
        "<br/>9. <b>Cost per Audio Hour ($/hr):</b> Commercial API list pricing or dedicated GPU cloud infrastructure amortization cost. "
        "<br/>10. <b>Evaluation Failure Rate (%):</b> Percentage of sessions triggering 4xx/5xx HTTP errors, API timeouts, or zero-length/empty RTTMs.",
        styles["Body"]
    ))

    # Section 9 & 10
    story.append(Paragraph("9. Annotation Quality Assurance & Statistical Uncertainty", styles["SecHeading"]))
    story.append(Paragraph(
        "<b>Two-Stage Adjudication QA:</b> Dual independent annotators mark turn boundaries, overlaps, fillers, and laughter. Disagreements exceeding 200 ms at boundaries or any speaker identity dispute trigger formal third-party adjudication. Synthetic validation scripts verify positive durations and absence of overlapping segments per speaker.<br/>"
        "<b>Paired Stratified Bootstrap (95% CI):</b> To determine whether ranking differences are statistically significant, whole conversations are resampled with replacement (B=2,000 iterations). Paired delta DER confidence intervals are computed. If the 95% confidence interval for (DER_A - DER_B) spans zero, the systems are declared statistically tied.",
        styles["Body"]
    ))

    # Section 11 & 12
    story.append(Paragraph("10. Public Leaderboard Architecture & Reflection", styles["SecHeading"]))
    story.append(Paragraph(
        "The public leaderboard features interactive multi-dimensional filtering (Accent, Setting, Speaker Count, Overlap, Track) and model drill-down cards displaying breakdown curves across SNR, conversation duration, and failure rates. "
        "<b>Strategic Reflection:</b> The most impactful methodological choice is the zero-collar overlap-inclusive policy: while strict, it directly exposes systems that collapse under multi-party conversational Indian audio, providing buyers with an uncompromised measure of operational readiness.",
        styles["Body"]
    ))

    build_pdf_document(pdf_path, "Question 1 - Speaker Diarization Evaluation and Leaderboard", story)
    shutil.copy2(pdf_path, OUT_FINAL / "Q1" / "Q1_Main_Research_Document.pdf")
    print("Generated Q1 Main Research Document PDF successfully")


# ---------------------------------------------------------------------------
# 4. BUILD Q1 ONE-PAGE EXECUTIVE REPORT PDF
# ---------------------------------------------------------------------------
def build_q1_one_page_pdf():
    pdf_path = OUT_DELIV / "Q1" / "Q1_One_Page_Report.pdf"
    styles = get_styles()
    story = []

    story.append(Paragraph("Question 1 - Executive Diarization Benchmark Report", styles["DocTitle"]))
    story.append(Paragraph("Public Evaluation Standard for Conversational Indian Speech - Executive Briefing", styles["DocSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceAfter=5))

    story.append(Paragraph("Core Strategic Objective", styles["SecHeading"]))
    story.append(Paragraph(
        "Enterprise conversational AI, customer QA, and meeting platforms require robust speaker diarization ('who spoke when'). "
        "Single aggregate scores fail because production systems face diverse trade-offs across overlap handling, reverberant hardware, latency, and cost. "
        "This benchmark establishes a transparent, reproducible 100-hour evaluation standard specifically targeted at Indian conversational speech.",
        styles["Body"]
    ))

    story.append(Paragraph("Committed Primary Scoring Standard", styles["SecHeading"]))
    story.append(Paragraph(
        "- <b>Primary Metric:</b> Diarization Error Rate (DER) evaluated at <b>0.0 s collar (zero-collar)</b> with <b>overlap speech included</b>.<br/>"
        "- <b>Speaker Mapping:</b> Optimal Hungarian bijection per session; no cross-session identity leakage.<br/>"
        "- <b>Speaker Cardinality:</b> Autonomous estimation; oracle speaker counts strictly forbidden on primary leaderboard.<br/>"
        "- <b>Statistical Rigor:</b> Paired conversation-level bootstrap 95% confidence intervals; overlapping CIs declared ties.",
        styles["Body"]
    ))

    story.append(Paragraph("Corpus Allocation: Exactly 100.0 Hours", styles["SecHeading"]))
    story.append(Paragraph(
        "Held-out dataset of 250 conversations across 4 stratified cohorts: (1) 40.0 hrs Indian English (1-8 spk, 50% in-person/50% online); "
        "(2) 25.0 hrs Hindi & Hinglish code-switching; (3) 20.0 hrs Regional code-switching (Tamil, Telugu, Marathi, Bengali); "
        "and (4) 15.0 hrs Telephony & noise stress cases (8 kHz PSTN, reverberant halls, cafeteria ambient).",
        styles["Body"]
    ))

    story.append(Paragraph("Evaluation Shortlist: 10 Systems Across Deployment Paradigms", styles["SecHeading"]))
    th = styles["TableHeader"]
    tc = styles["TableCell"]
    tcb = styles["TableCellBold"]
    tcc = styles["TableCellCenter"]

    exec_table_data = [
        [Paragraph("System", th), Paragraph("Provider", th), Paragraph("Model Checkpoint", th), Paragraph("Deployment", th), Paragraph("Key Evaluation Focus", th)],
        [Paragraph("pyannote.audio", tcb), Paragraph("pyannote", tc), Paragraph("speaker-diarization-3.1", tc), Paragraph("Self-hosted", tcc), Paragraph("Open-source neural baseline; native overlap", tc)],
        [Paragraph("NVIDIA NeMo", tcb), Paragraph("NVIDIA", tc), Paragraph("MSDD / Sortformer", tc), Paragraph("Self-hosted", tcc), Paragraph("Production GPU streaming & batch diarization", tc)],
        [Paragraph("Deepgram", tcb), Paragraph("Deepgram", tc), Paragraph("Nova-3 (diarize=true)", tc), Paragraph("API", tcc), Paragraph("Fast turnaround speech API diarization", tc)],
        [Paragraph("AssemblyAI", tcb), Paragraph("AssemblyAI", tc), Paragraph("Universal-2 + Diarize", tc), Paragraph("API", tcc), Paragraph("Commercial batch transcription & speaker labels", tc)],
        [Paragraph("Google Cloud", tcb), Paragraph("Google", tc), Paragraph("Chirp 2 (diarize)", tc), Paragraph("API", tcc), Paragraph("Multilingual foundation model diarization", tc)],
        [Paragraph("Azure AI Speech", tcb), Paragraph("Microsoft", tc), Paragraph("ConversationTranscriber", tc), Paragraph("API", tcc), Paragraph("Enterprise meeting transcription & turn attribution", tc)],
        [Paragraph("AWS Transcribe", tcb), Paragraph("Amazon", tc), Paragraph("ShowSpeakerLabels", tc), Paragraph("API", tcc), Paragraph("Asynchronous speaker clustering in batch STT", tc)],
        [Paragraph("Speechmatics", tcb), Paragraph("Speechmatics", tc), Paragraph("Enhanced Diarization", tc), Paragraph("API", tcc), Paragraph("High-accuracy multilingual turn alignment", tc)],
        [Paragraph("Gladia", tcb), Paragraph("Gladia", tc), Paragraph("Whisper-based Diarize", tc), Paragraph("API", tcc), Paragraph("Real-world audio transcription with speaker ID", tc)],
        [Paragraph("ElevenLabs", tcb), Paragraph("ElevenLabs", tc), Paragraph("Scribe v2", tc), Paragraph("API", tcc), Paragraph("Speech-to-text with turn boundary attribution", tc)],
    ]
    t_exec = Table(exec_table_data, colWidths=[80, 75, 115, 60, 193])
    t_exec.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_exec)

    story.append(Paragraph("Enterprise Buyer Decision Framework", styles["SecHeading"]))
    story.append(Paragraph(
        "The public leaderboard provides 10 supporting metrics: Missed Speech %, False Alarm %, Speaker Confusion %, Overlap DER %, "
        "Speaker Count Error (SCE), Speech Coverage %, Real-Time Factor (RTF), Latency (s), Cost/hour, and Failure Rate %. "
        "This multi-metric architecture empowers buyers to select systems optimized for their precise acoustic environment and SLA constraints.",
        styles["Body"]
    ))

    build_pdf_document(pdf_path, "Question 1 - Executive Diarization Benchmark Report", story, pagesize=letter)
    shutil.copy2(pdf_path, OUT_FINAL / "Q1" / "Q1_One_Page_Report.pdf")
    print("Generated Q1 One-Page Report PDF successfully")


# ---------------------------------------------------------------------------
# 5. BUILD Q2 SAMARTH KAPDI REPORT PDF (STRICT 4-PAGE BALANCED LAYOUT)
# ---------------------------------------------------------------------------
def build_q2_pdf():
    pdf_path = OUT_DELIV / "Q2" / "Samarth_Kapdi_Report.pdf"
    styles = get_styles()
    story = []

    # ---------------- PAGE 1 ----------------
    story.append(Paragraph("Deepgram Nova-3 Diarization Performance on Voice Arena Benchmark", styles["DocTitle"]))
    story.append(Paragraph("A Technical Root-Cause Investigation of Severe Output Under-Coverage in Conversational Indian Audio", styles["DocSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceAfter=5))

    story.append(Paragraph("1. Executive Summary", styles["SecHeading"]))
    story.append(Paragraph(
        "<b>Rigorous Scope Distinction:</b> The original assessment references a historical public Voice Arena benchmark snapshot of 139 recordings with Nova-3 scoring <b>67.1% DER</b>, noting that missed speech accounts for the majority of error. "
        "That historical 139-recording benchmark is separate from the supplied workbook sample of <b>15 recordings</b> analyzed herein, which yields a mean Nova-3 DER of <b>64.45%</b> and a median DER of <b>86.02%</b>. These scopes must never be conflated.<br/>"
        "<b>Separate Diarization+ASR Leaderboard:</b> Voice Arena separately publishes a combined diarization-plus-ASR leaderboard where Nova-3 achieves <b>71.89% cpWER</b> (Composite Word Error Rate, accessed 1 Nov 2026). "
        "cpWER combines lexical transcription errors with speaker assignment; it is a completely distinct metric from pure diarization DER and must never be substituted for or averaged with DER.<br/>"
        "<b>The Severe Failure Pattern:</b> In the 15-recording sample, the five worst recordings suffer near-total collapse (DER 97.0% to 100.0%) with catastrophic Nova-3 speech coverage ranging from <b>0.0% to 9.8%</b>. "
        "Two Nova-3 RTTM files contain exactly zero speech segments: <code>D20260825_S003_015_5SPK_IN_EN</code> (present in workbook) and <code>D20260825_S003_012_5SPK_IN_EN</code> (in the 20-file RTTM zip package).<br/>"
        "<b>Root Cause Finding:</b> The primary failure mechanism in this sample is established as <b>severe output under-coverage / speech omission</b> rather than speaker label swapping. "
        "However, whether this omission occurs inside Deepgram's acoustic/VAD front-end, the English ASR language decoder, or downstream word-to-RTTM segment conversion cannot be isolated without raw API JSON responses.",
        styles["Body"]
    ))

    story.append(Paragraph("2. Dated Leaderboard & Metric Hygiene Standard", styles["SecHeading"]))
    story.append(Paragraph(
        "<b>Official Benchmark Citation (Access Date: 1 November 2026):</b> Voice Arena Diarization-Bench, <code>https://voicearena.com/diarization-bench</code>. "
        "The historical benchmark snapshot reports Nova-3 at 67.1% DER (139 recordings), dominated by missed speech. "
        "A separately published track reports Nova-3 at 71.89% cpWER (<code>https://voicearena.com/research/diarization-bench/diarization-asr-track-cpwer-results</code>, accessed 1 Nov 2026). "
        "cpWER evaluates joint word transcription and speaker attribution: cpWER = (Substitutions + Deletions + Insertions + Speaker_Confusion_Words) / Total_Reference_Words. "
        "Because cpWER penalizes word spelling, vocabulary, and grammar errors alongside speaker attribution, it measures a different capability than acoustic boundary diarization (DER). "
        "No live leaderboard rank or component values were machine-readable during this audit; hence, no synthetic leaderboard values are invented.",
        styles["Body"]
    ))

    story.append(Paragraph("3. Metric Interpretation and Component Identity", styles["SecHeading"]))
    story.append(Paragraph(
        "- <b>Lower DER is Better:</b> DER = Missed Speech % + False Alarm % + Speaker Confusion %. Component sums match workbook DER within 0.01 percentage points due to displayed rounding.<br/>"
        "- <b>Speech Coverage (%):</b> Percentage of reference speech duration represented in hypothesis output. While high coverage does not guarantee low DER, low coverage mathematically forces high DER via Missed Speech.",
        styles["Body"]
    ))

    story.append(Paragraph("4. 15-Recording Comprehensive Overview Table", styles["SecHeading"]))
    th = styles["TableHeader"]
    tc = styles["TableCell"]
    tcb = styles["TableCellBold"]
    tcc = styles["TableCellCenter"]

    overview_rows = [
        [Paragraph("Session ID", th), Paragraph("Setting", th), Paragraph("Accent", th), Paragraph("Spk", th), Paragraph("Words", th), Paragraph("DER %", th), Paragraph("Miss %", th), Paragraph("FA %", th), Paragraph("Conf %", th), Paragraph("Nova Cov", th), Paragraph("VAD Cov", th)]
    ]
    for _, r in df.iterrows():
        sid = str(r["Session ID"])
        setting = "In person" if "In person" in str(r.get("Setting", "")) else "Online"
        accent = "Indian" if "Indian" in str(r.get("Accent", "")) else ("US" if "US" in str(r.get("Accent", "")) else "Vietnamese")
        spk = str(int(r.get("Speakers", 0))) if pd.notna(r.get("Speakers")) else "-"
        words = str(int(r.get("Nova-3 words returned", 0))) if pd.notna(r.get("Nova-3 words returned")) else "-"
        der = f"{float(r['Nova-3 DER %']):.2f}" if pd.notna(r["Nova-3 DER %"]) else "-"
        miss = f"{float(r.get('Nova-3 missed speech %', 0)):.2f}" if pd.notna(r.get("Nova-3 missed speech %")) else "-"
        fa = f"{float(r.get('Nova-3 false alarm %', 0)):.2f}" if pd.notna(r.get("Nova-3 false alarm %")) else "-"
        conf = f"{float(r.get('Nova-3 speaker confusion %', 0)):.2f}" if pd.notna(r.get("Nova-3 speaker confusion %")) else "-"
        cov = f"{float(r.get('Speech covered by Nova-3 (%)', 0)):.1f}%" if pd.notna(r.get("Speech covered by Nova-3 (%)")) else "-"
        vad = f"{float(r.get('Speech covered by VAD (%)', 0)):.1f}%" if pd.notna(r.get("Speech covered by VAD (%)")) else "-"
        
        overview_rows.append([
            Paragraph(sid, tcb if float(r['Nova-3 DER %']) > 90 else tc),
            Paragraph(setting, tc),
            Paragraph(accent, tc),
            Paragraph(spk, tcc),
            Paragraph(words, tcc),
            Paragraph(der, tcc),
            Paragraph(miss, tcc),
            Paragraph(fa, tcc),
            Paragraph(conf, tcc),
            Paragraph(cov, tcc),
            Paragraph(vad, tcc)
        ])

    t_overview = Table(overview_rows, colWidths=[133, 42, 58, 22, 32, 40, 40, 36, 40, 40, 40])
    t_overview.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_overview)

    # ---------------- PAGE 2 ----------------
    story.append(PageBreak())
    story.append(Paragraph("5. Recording-Level Contrast: Four Poor vs Two Good Controls", styles["SecHeading"]))
    story.append(Paragraph(
        "To isolate the root cause, we compare the four most severe failure sessions against two well-performing control sessions. "
        "The comparison illustrates a stark bimodal divergence between near-zero word emission and normal operation:",
        styles["Body"]
    ))

    # Evidence Chart
    chart_img = CHARTS / "q2_poor_good_evidence.png"
    if chart_img.exists():
        story.append(Image(str(chart_img), width=6.8 * inch, height=2.4 * inch))
        story.append(Spacer(1, 4))

    contrast_ids = [
        "D20260825_S003_015_5SPK_IN_EN",
        "D20260825_S003_014_5SPK_IN_EN",
        "D20260826_S001_03_4SPK_IN_EN",
        "D20260826_S001_05_4SPK_IN_EN",
        "D20260825_S004_31_2SPK_IN_EN",
        "O20260826_S010_04_01_4SPK_US_EN",
    ]
    contrast_df = df[df["Session ID"].isin(contrast_ids)].copy()
    comp_cols = [c for c in contrast_df.columns if "DER %" in c and "Nova" not in c]
    contrast_df["Best Comp DER %"] = contrast_df[comp_cols].min(axis=1)

    contrast_rows = [
        [Paragraph("Session ID", th), Paragraph("Words", th), Paragraph("Nova Cov", th), Paragraph("DER %", th), Paragraph("Miss %", th), Paragraph("Best Comp DER", th), Paragraph("VAD Cov", th), Paragraph("dBFS", th), Paragraph("Clip %", th), Paragraph("SNR dB", th)]
    ]
    for _, r in contrast_df.iterrows():
        sid = str(r["Session ID"])
        words = str(int(r.get("Nova-3 words returned", 0)))
        cov = f"{float(r.get('Speech covered by Nova-3 (%)', 0)):.1f}%"
        der = f"{float(r['Nova-3 DER %']):.2f}%"
        miss = f"{float(r.get('Nova-3 missed speech %', 0)):.2f}%"
        best_der = f"{float(r.get('Best Comp DER %', 0)):.2f}%"
        vad = f"{float(r.get('Speech covered by VAD (%)', 0)):.1f}%"
        dbfs = f"{float(r.get('Overall loudness (dBFS)', 0)):.1f}" if pd.notna(r.get("Overall loudness (dBFS)")) else "-"
        clip = f"{float(r.get('Clipped samples (%)', 0)):.3f}%" if pd.notna(r.get("Clipped samples (%)")) else "-"
        snr = f"{float(r.get('Speech above background (dB)', 0)):.1f}" if pd.notna(r.get("Speech above background (dB)")) else "-"

        contrast_rows.append([
            Paragraph(sid, tcb if float(r['Nova-3 DER %']) > 90 else tc),
            Paragraph(words, tcc),
            Paragraph(cov, tcc),
            Paragraph(der, tcc),
            Paragraph(miss, tcc),
            Paragraph(best_der, tcc),
            Paragraph(vad, tcc),
            Paragraph(dbfs, tcc),
            Paragraph(clip, tcc),
            Paragraph(snr, tcc),
        ])

    t_contrast = Table(contrast_rows, colWidths=[135, 34, 44, 42, 42, 60, 42, 40, 40, 44])
    t_contrast.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_contrast)

    story.append(Paragraph(
        "<b>Analytical Takeaways:</b><br/>"
        "1. <b>Under-Coverage, Not Swapped Labels:</b> In the four poor rows, Nova-3 returned only 0, 34, 114, and 211 words, yielding 0.0% to 9.8% speech coverage. Missed speech accounts for 93.75% to 100.0% of total error.<br/>"
        "2. <b>VAD Does Not Explain Failure:</b> Silero VAD achieves 91.5% to 99.0% speech coverage across these identical files. The speech energy was acoustically detectable; Nova-3 specifically dropped it.<br/>"
        "3. <b>Audio Quality Contrast:</b> While clipping reaches 3.39% and 6.98% on the S001 files, the worst files (S003_014 and S003_015) show 0.000% clipping with acceptable loudness (-31 to -34 dBFS) and 16.7-17.9 dB SNR.<br/>"
        "4. <b>Alternative Systems Succeed:</b> Competitor models (pyannote, Meta Muse, Soniox) achieved 18.91% to 31.56% DER on these exact files, confirming the audio was fully parseable.",
        styles["Body"]
    ))

    # ---------------- PAGE 3 ----------------
    story.append(PageBreak())
    story.append(Paragraph("6. Deepgram Settings Sheet Diagnostic Re-Runs", styles["SecHeading"]))
    story.append(Paragraph(
        "The workbook's <code>Deepgram settings</code> sheet provides empirical re-runs across eight recordings and nine configurations. "
        "These re-runs are transcribed below for complete independent auditability:",
        styles["Body"]
    ))

    # Settings Table 1: DER %
    story.append(Paragraph("<b>Table 1: Diarization Error Rate (DER %) Across Configurations</b>", styles["SubHeading"]))
    s1_rows = [
        [Paragraph("Session ID", th), Paragraph("Bench", th), Paragraph("en-IN", th), Paragraph("en-US", th), Paragraph("auto", th), Paragraph("multi", th), Paragraph("multi+v1", th), Paragraph("nova-2", th), Paragraph("enhanced", th), Paragraph("whisper", th)],
        [Paragraph("D20260825_S003_014", tc), Paragraph("99.07", tcc), Paragraph("99.07", tcc), Paragraph("99.07", tcc), Paragraph("99.07", tcc), Paragraph("88.15", tcc), Paragraph("82.45", tcc), Paragraph("98.25", tcc), Paragraph("90.51", tcc), Paragraph("67.66", tcc)],
        [Paragraph("D20260825_S003_015", tc), Paragraph("100.00", tcc), Paragraph("100.00", tcc), Paragraph("100.00", tcc), Paragraph("100.00", tcc), Paragraph("93.06", tcc), Paragraph("89.76", tcc), Paragraph("98.97", tcc), Paragraph("93.82", tcc), Paragraph("64.95", tcc)],
        [Paragraph("D20260825_S004_26", tc), Paragraph("85.11", tcc), Paragraph("85.11", tcc), Paragraph("85.11", tcc), Paragraph("85.11", tcc), Paragraph("53.93", tcc), Paragraph("45.86", tcc), Paragraph("76.30", tcc), Paragraph("63.91", tcc), Paragraph("48.24", tcc)],
        [Paragraph("D20260826_S001_03", tc), Paragraph("98.47", tcc), Paragraph("98.47", tcc), Paragraph("98.53", tcc), Paragraph("98.53", tcc), Paragraph("77.66", tcc), Paragraph("66.87", tcc), Paragraph("97.50", tcc), Paragraph("78.57", tcc), Paragraph("58.52", tcc)],
        [Paragraph("D20260826_S001_05", tc), Paragraph("98.35", tcc), Paragraph("97.84", tcc), Paragraph("98.35", tcc), Paragraph("97.83", tcc), Paragraph("85.33", tcc), Paragraph("78.15", tcc), Paragraph("97.01", tcc), Paragraph("88.04", tcc), Paragraph("71.72", tcc)],
        [Paragraph("D20260905_S003_04", tc), Paragraph("98.03", tcc), Paragraph("98.03", tcc), Paragraph("98.03", tcc), Paragraph("97.91", tcc), Paragraph("59.78", tcc), Paragraph("43.99", tcc), Paragraph("93.74", tcc), Paragraph("69.68", tcc), Paragraph("42.20", tcc)],
        [Paragraph("D20260906_S003_04", tc), Paragraph("96.55", tcc), Paragraph("96.55", tcc), Paragraph("96.55", tcc), Paragraph("96.55", tcc), Paragraph("65.48", tcc), Paragraph("46.58", tcc), Paragraph("91.23", tcc), Paragraph("59.25", tcc), Paragraph("33.15", tcc)],
        [Paragraph("D20260906_S003_09", tc), Paragraph("97.07", tcc), Paragraph("97.07", tcc), Paragraph("97.07", tcc), Paragraph("96.98", tcc), Paragraph("64.72", tcc), Paragraph("52.57", tcc), Paragraph("91.55", tcc), Paragraph("68.31", tcc), Paragraph("49.14", tcc)],
    ]
    t_s1 = Table(s1_rows, colWidths=[119, 45, 45, 45, 45, 45, 50, 43, 43, 43])
    t_s1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_s1)

    # Settings Table 2: Words Returned
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 2: Words Returned Across Configurations</b>", styles["SubHeading"]))
    s2_rows = [
        [Paragraph("Session ID", th), Paragraph("Bench", th), Paragraph("en-IN", th), Paragraph("en-US", th), Paragraph("auto", th), Paragraph("multi", th), Paragraph("multi+v1", th), Paragraph("nova-2", th), Paragraph("enhanced", th), Paragraph("whisper", th)],
        [Paragraph("D20260825_S003_014", tc), Paragraph("34", tcc), Paragraph("34", tcc), Paragraph("34", tcc), Paragraph("34", tcc), Paragraph("983", tcc), Paragraph("981", tcc), Paragraph("131", tcc), Paragraph("753", tcc), Paragraph("1934", tcc)],
        [Paragraph("D20260825_S003_015", tc), Paragraph("0", tcc), Paragraph("0", tcc), Paragraph("0", tcc), Paragraph("0", tcc), Paragraph("465", tcc), Paragraph("389", tcc), Paragraph("28", tcc), Paragraph("419", tcc), Paragraph("1661", tcc)],
        [Paragraph("D20260825_S004_26", tc), Paragraph("299", tcc), Paragraph("299", tcc), Paragraph("299", tcc), Paragraph("298", tcc), Paragraph("908", tcc), Paragraph("905", tcc), Paragraph("533", tcc), Paragraph("772", tcc), Paragraph("864", tcc)],
        [Paragraph("D20260826_S001_03", tc), Paragraph("114", tcc), Paragraph("114", tcc), Paragraph("111", tcc), Paragraph("112", tcc), Paragraph("1549", tcc), Paragraph("1543", tcc), Paragraph("225", tcc), Paragraph("1512", tcc), Paragraph("2120", tcc)],
        [Paragraph("D20260826_S001_05", tc), Paragraph("166", tcc), Paragraph("200", tcc), Paragraph("166", tcc), Paragraph("201", tcc), Paragraph("1052", tcc), Paragraph("1126", tcc), Paragraph("319", tcc), Paragraph("890", tcc), Paragraph("1842", tcc)],
        [Paragraph("D20260905_S003_04", tc), Paragraph("56", tcc), Paragraph("56", tcc), Paragraph("56", tcc), Paragraph("56", tcc), Paragraph("1624", tcc), Paragraph("1622", tcc), Paragraph("246", tcc), Paragraph("1212", tcc), Paragraph("1607", tcc)],
        [Paragraph("D20260906_S003_04", tc), Paragraph("74", tcc), Paragraph("74", tcc), Paragraph("74", tcc), Paragraph("74", tcc), Paragraph("1159", tcc), Paragraph("1159", tcc), Paragraph("234", tcc), Paragraph("1288", tcc), Paragraph("1435", tcc)],
        [Paragraph("D20260906_S003_09", tc), Paragraph("83", tcc), Paragraph("83", tcc), Paragraph("83", tcc), Paragraph("84", tcc), Paragraph("1644", tcc), Paragraph("1644", tcc), Paragraph("368", tcc), Paragraph("1298", tcc), Paragraph("1730", tcc)],
    ]
    t_s2 = Table(s2_rows, colWidths=[119, 45, 45, 45, 45, 45, 50, 43, 43, 43])
    t_s2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_s2)

    story.append(Paragraph(
        "<b>Key Technical Findings:</b><br/>"
        "- <b>English Acoustic/Language Pipeline Collapse:</b> Across all 8 rows, benchmark Nova-3 (<code>language=en</code>) behaves identically to <code>en-IN</code>, <code>en-US</code>, and <code>auto-detect</code> (e.g. S003_015 returns exactly 0 words across all four).<br/>"
        "- <b>Multilingual Recovery:</b> Switching to <code>language=multi</code> immediately recovers 465 words on S003_015 and drops DER to 93.06%; Whisper-large recovers 1,661 words and drops DER to 64.95%.<br/>"
        "- <b>Non-Acoustic Setting Neutrality:</b> The sheet explicitly notes that <code>smart_format</code>, <code>punctuate</code>, <code>filler_words</code>, <code>paragraphs</code>, <code>numerals</code>, <code>diarize_model latest vs v2</code>, <code>utt_split</code> (0.1 to 2.0 s), and word-vs-utterance timelines changed DER by <=2 percentage points on 7 of 8 files.<br/>"
        "- <b>Workbook Re-Runs != Manual Playground Runs:</b> These 8 workbook re-runs document alternate API settings but do NOT replace the seven manual playground experiments, which require genuine screenshots, request IDs, and live output captures.",
        styles["Body"]
    ))

    # ---------------- PAGE 4 ----------------
    story.append(PageBreak())
    story.append(Paragraph("7. Tripartite Root-Cause Classification", styles["SecHeading"]))
    story.append(Paragraph(
        "To uphold scientific integrity, we separate established findings, inferred hypotheses, and unresolved questions: "
        "<br/>1. <b>Established Facts:</b> The 15-recording sample statistics (mean 64.45% DER, median 86.02%); the five worst rows (DER 97-100%, coverage 0-9.8%); "
        "the two empty Nova-3 RTTMs (<code>D20260825_S003_012</code> and <code>D20260825_S003_015</code>); component identity matching DER within 0.01%; and the workbook settings re-runs.<br/>"
        "2. <b>Inferred with High Confidence:</b> The severe DER is overwhelmingly driven by missing speech output rather than speaker attribution swapping, "
        "because missed speech accounts for >93% of error and Silero VAD detects >91% speech duration on identical audio.<br/>"
        "3. <b>Unresolved Mechanisms:</b> Whether the speech omission occurred at the Deepgram VAD front-end, within the English language model decoder, "
        "or during benchmark word-to-RTTM conversion. Distinguishing these requires inspecting raw API JSON responses.",
        styles["Body"]
    ))

    story.append(Paragraph("8. Root Cause Synthesis & Confirmation Testing Framework", styles["SecHeading"]))
    story.append(Paragraph(
        "<b>Output Omission vs Converter Loss:</b> Zero-word returns in the workbook settings sheet strongly support service-side omission. "
        "However, word-to-RTTM conversion loss remains plausible because Nova-3 RTTM files are derived from returned words using a 0.5 s gap joining heuristic. "
        "Raw word JSON is required to confirm whether words were emitted by Deepgram but dropped by the converter.<br/>"
        "<b>Conditional Diagnostic: <code>diarize_model</code> and <code>metadata.diarize_info</code>:</b> Current Deepgram documentation introduces <code>diarize_model=latest</code> "
        "and returns diarizer build information in <code>metadata.diarize_info</code>. While populated workbook rows report <code>Diarizer reported = v2</code>, "
        "the workbook lacks raw response metadata. Thus, <code>metadata.diarize_info</code> must be audited during live replays, but is NOT asserted as an established cause.<br/>"
        "<b>Benchmark Reproducibility Caveat:</b> Exact benchmark DER cannot be recomputed from supplied RTTMs because the benchmark author utilized an earlier reference build. "
        "File syntax, timing validity, and RTTM triplet pairings are confirmed, but exact score equality is impossible from the current files alone.<br/>"
        "<b>Status of Seven Manual Playground Experiments:</b> As documented in the execution log, all seven runs remain <b>NOT PERFORMED - manual run required</b>. No manual findings are fabricated.",
        styles["Body"]
    ))

    story.append(Paragraph("9. Recommendations for Deepgram Engineering & Voice Arena", styles["SecHeading"]))
    story.append(Paragraph(
        "- <b>Deepgram Engineering:</b> (1) Introduce an explicit 'zero-output' warning when VAD detects audio energy but ASR returns empty transcript; "
        "(2) Retain full request and response JSON payloads with request IDs in client SDKs; (3) Optimize Nova-3 acoustic front-end for far-field Indian English table-top audio; "
        "(4) Document the exact interaction between <code>diarize_model</code>, <code>language</code>, and utterance timelines.<br/>"
        "- <b>Voice Arena Benchmark Team:</b> (1) Publish cryptographic SHA-256 hashes for all input audio and reference RTTMs; "
        "(2) Disclose exact word-to-RTTM conversion source code; (3) Report per-session speech coverage alongside DER to detect silence-collapse; "
        "(4) Retain raw API responses to distinguish service drops from evaluation pipeline errors.",
        styles["Body"]
    ))

    story.append(Paragraph("10. Limitations & Retrospective", styles["SecHeading"]))
    story.append(Paragraph(
        "<b>Limitations:</b> Assessment PDF absent from workspace; workbook contains 15 rows; RTTM package contains 20 IDs; current live leaderboard values not machine-readable in local environment; manual playground runs require physical execution. "
        "<b>Retrospective:</b> The most striking finding is the bimodal performance gap: Deepgram Nova-3 functions normally on clean online audio (26.8% DER) but collapses completely on multi-party in-person Indian English audio. "
        "Given additional time, research should prioritize raw API JSON payload logging and station-level acoustic replication.",
        styles["Body"]
    ))

    build_pdf_document(pdf_path, "Deepgram Nova-3 Diarization Performance on Voice Arena Benchmark", story)
    shutil.copy2(pdf_path, OUT_FINAL / "Q2" / "Samarth_Kapdi_Report.pdf")
    print("Generated Q2 Samarth Kapdi Report PDF successfully")


# ---------------------------------------------------------------------------
# 6. BUILD WORKSPACE AUDIT PDF
# ---------------------------------------------------------------------------
def build_workspace_audit_pdf():
    pdf_path = OUT_DELIV / "Workspace_Audit.pdf"
    styles = get_styles()
    story = []

    story.append(Paragraph("Josh Talks Growth Assignment - Workspace Audit", styles["DocTitle"]))
    story.append(Paragraph("Technical Integrity, Evidence Triangulation, and Scope Boundaries", styles["DocSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceAfter=6))

    story.append(Paragraph("1. Primary Data Sources & Scope Disclosures", styles["SecHeading"]))
    story.append(Paragraph(
        "- <b>Supplied Workbook:</b> <code>Deepgram_Failure_Analysis_Data.xlsx</code> contains 7 sheets (Read me, Sessions, Results, Transcripts, Deepgram API check, Audio quality, Deepgram settings) joining to 15 recording IDs.<br/>"
        "- <b>RTTM Zip Package:</b> Contains 60 files across 3 folders (reference, deepgram_nova3, silero_vad) covering 20 recording IDs. Five IDs are outside the workbook scope and excluded from workbook statistical aggregates.<br/>"
        "- <b>Missing Source Assessment PDF:</b> The original assessment PDF referenced in instructions is not present in the workspace, representing an audited workspace limitation.",
        styles["Body"]
    ))

    story.append(Paragraph("2. Quality Control & File Integrity Checks", styles["SecHeading"]))
    story.append(Paragraph(
        "- <b>RTTM Timing Validity:</b> 100% of the 60 RTTM files contain valid non-negative timestamps and positive segment durations. No timing corruption detected.<br/>"
        "- <b>Empty Output Files:</b> Exactly two Nova-3 RTTM files are empty (0 bytes, 0 segments): <code>D20260825_S003_015</code> (workbook ID) and <code>D20260825_S003_012</code> (package-only ID).<br/>"
        "- <b>Component Identity Verification:</b> Workbook DER matches (Miss % + FA % + Conf %) within 0.01 percentage points across all 15 rows due to displayed rounding.<br/>"
        "- <b>API Check Findings:</b> API check sheet reports zero warnings for inspected rows. However, this only logs provider error strings; it does not prove upstream acoustic integrity.",
        styles["Body"]
    ))

    story.append(Paragraph("3. Reproducibility & Pipeline Automation", styles["SecHeading"]))
    story.append(Paragraph(
        "- Re-running <code>Supporting_Work/analysis/analyze_dataset.py</code> deterministically regenerates consolidated tables, correlation matrices, and RTTM validation files.<br/>"
        "- Re-running <code>Supporting_Work/analysis/independent_quality_audit.py</code> verifies mean DER (64.4506...%), median DER (86.02%), and worst recording subsets.<br/>"
        "- Re-running <code>generate_deliverables.py</code> compiles all submission-ready PDFs, Word documents, mockups, and execution guides.",
        styles["Body"]
    ))

    build_pdf_document(pdf_path, "Workspace Audit - Josh Talks Growth Assignment", story)
    shutil.copy2(pdf_path, OUT_FINAL / "Workspace_Audit.pdf")
    print("Generated Workspace Audit PDF successfully")


# ---------------------------------------------------------------------------
# 7. BUILD DOCX DELIVERABLES (NO [LINK] PLACEHOLDERS)
# ---------------------------------------------------------------------------
def build_docx_deliverables():
    # 1. Samarth_Kapdi_Posts.docx
    doc_posts = Document()
    doc_posts.add_heading("Deepgram Nova-3 Investigation - Social Media Drafts", 0)

    doc_posts.add_heading("X (Twitter) Thread (5 Posts)", level=1)
    x_posts = [
        "1/ The assessment's historical Voice Arena benchmark snapshot reports 67.1% DER on 139 recordings. I analyzed a separate supplied 15-recording sample: Nova-3 DER mean 64.45%, median 86.02%. These represent different scopes and must not be conflated. Detailed report: deliverables/Q2/Samarth_Kapdi_Report.pdf",
        "2/ Five severe failures in the sample reached 97.0-100.0% DER with only 0.0-9.8% Nova-3 speech coverage. Missed speech dominated the error. Two Nova-3 RTTM files were completely empty: D20260825_S003_012_5SPK_IN_EN and D20260825_S003_015_5SPK_IN_EN.",
        "3/ Crucial contrast: the failure is not universal. On an in-person 2-speaker Indian English recording, Nova-3 achieved 15.13% DER with 97.4% coverage. On an online 4-speaker recording, it achieved 26.81% DER with 94.6% coverage. The collapse concentrates on multi-party in-person tables.",
        "4/ The evidence establishes severe output under-coverage. It does not yet distinguish ASR/diarization omission from word-to-RTTM conversion loss. Note: DER is not cpWER. The workbook re-runs report DER and word counts, not cpWER (Voice Arena separately reports 71.89% cpWER).",
        "5/ Next decisive action: execute raw-output replication with exact audio URLs, capture request IDs and API JSON payloads. Full root-cause evidence matrix and diagnostic recommendations: deliverables/Q2/Samarth_Kapdi_Report.pdf"
    ]
    for p in x_posts:
        doc_posts.add_paragraph(p)

    doc_posts.add_heading("LinkedIn Executive Post", level=1)
    li_post = (
        "The assessment's historical Voice Arena benchmark snapshot reports 67.1% DER on 139 recordings for Deepgram Nova-3. "
        "I conducted an independent technical audit on a separate supplied 15-recording sample: Nova-3 averaged 64.45% DER (median 86.02%). "
        "Five severe failure rows reached 97.0-100.0% DER, covering only 0.0-9.8% of reference speech; missed speech accounted for over 93% of error, "
        "and two RTTM output files were completely empty. Yet the same sample includes solid results: 15.13% DER with 97.4% coverage on an in-person 2-speaker recording, "
        "and 26.81% DER with 94.6% coverage on an online 4-speaker meeting. "
        "The evidence conclusively establishes severe output under-coverage rather than swapped speaker labels, but raw API JSON responses are required to isolate "
        "service-side speech omission from word-to-RTTM converter loss. Pure diarization DER must not be confused with combined diarization+ASR cpWER (71.89%). "
        "Full technical report, evidence matrix, and reproducible benchmark recommendations: deliverables/Q2/Samarth_Kapdi_Report.pdf"
    )
    doc_posts.add_paragraph(li_post)
    doc_posts.save(OUT_DELIV / "Q2" / "Samarth_Kapdi_Posts.docx")
    shutil.copy2(OUT_DELIV / "Q2" / "Samarth_Kapdi_Posts.docx", OUT_FINAL / "Q2" / "Samarth_Kapdi_Posts.docx")

    # 2. Q1 Walkthrough Script & Checklist DOCX & MD
    q1_script_content = [
        ("Recording Objective & Technical Setup", [
            "Video Duration: 2 to 3 minutes (120 to 180 seconds target).",
            "Screen Recording: 1080p full-screen capture showing deliverables/Q1/Q1_Main_Research_Document.pdf and Q1_Leaderboard_Mockup.png.",
            "Audio Setup: Quiet environment, external microphone, clear delivery.",
            "Pre-recording Checklist: Open Q1 Main Research PDF to Section 2 (System Table) and Section 4 (Primary Policy); open Q1_Leaderboard_Mockup.png in high-res viewer."
        ]),
        ("0:00 - 0:30: Introduction & Strategic Purpose", [
            "Show on Screen: Q1_One_Page_Report.pdf (Executive Briefing).",
            "Talking Points: Introduce the core objective: designing a rigorous, fair, multi-dimensional speaker diarization benchmark for conversational Indian audio. Emphasize that single aggregate scores fail enterprise buyers because meeting intelligence, contact center QA, and speech tech vendors face different trade-offs across overlap, hardware, latency, and cost."
        ]),
        ("0:30 - 1:10: Evaluation Shortlist & Committed Primary Scoring Policy", [
            "Show on Screen: Q1_Main_Research_Document.pdf (Section 2: 10 Systems Table & Section 4: Primary Policy).",
            "Talking Points: Walk through the 10 representative systems across self-hosted neural diarizers (pyannote 3.1, NVIDIA NeMo) and leading commercial APIs (Deepgram, AssemblyAI, Google Cloud, Azure Speech, AWS Transcribe, Speechmatics, Gladia, ElevenLabs). Clarify that AWS 'speaker labels' is evaluated strictly as diarization clustering, not biometric recognition. Commit unambiguously to the primary scoring policy: zero-collar (0.0s), overlap included, Hungarian optimal mapping per session, and unconstrained/autonomous speaker counting."
        ]),
        ("1:10 - 1:50: Stratified 100-Hour Indian Corpus & Hardware Cross-Tabulation", [
            "Show on Screen: Q1_Main_Research_Document.pdf (Section 6: Corpus Matrix & Section 7: Device Matrix).",
            "Talking Points: Explain the exact 100.0-hour allocation across 4 strata: 40 hrs Indian English, 25 hrs Hindi/Hinglish, 20 hrs Regional code-switching (Tamil, Telugu, Marathi, Bengali), and 15 hrs stress cases. Highlight the hardware cross-tabulation table cross-referencing smartphone tabletop mics, laptop array mics, conference room boundary mics, and wearables."
        ]),
        ("1:50 - 2:30: Public Leaderboard Walkthrough & Detail Inspection", [
            "Show on Screen: Q1_Leaderboard_Mockup.png.",
            "Talking Points: Walk through the interactive mockup: filter controls (accent, speakers, setting, overlap), the 14-column leaderboard table showing DER with 95% bootstrap confidence intervals, JER, Miss %, FA %, Conf %, Overlap DER, Speaker Count Error, RTF, Latency, Cost/hr, and Failure Rate. Point to the model drill-down card showing granular SNR and condition curves."
        ]),
        ("2:30 - 3:00: Statistical Uncertainty, QA & Strategic Reflection", [
            "Show on Screen: Q1_Main_Research_Document.pdf (Section 9: Annotation QA & Section 10: Bootstrap).",
            "Talking Points: Summarize the two-stage annotation adjudication QA and paired stratified bootstrap confidence intervals (B=2,000). Conclude with the core takeaway: zero-collar overlap-inclusive evaluation is tough but essential for conversational Indian speech, turning reproducibility into a product feature."
        ])
    ]
    doc_q1 = Document()
    doc_q1.add_heading("Question 1 - 2-3 Minute Walkthrough Video Script & Checklist", 0)
    md_q1 = ["# Question 1 - 2-3 Minute Walkthrough Video Script & Checklist\n"]
    for title, paras in q1_script_content:
        doc_q1.add_heading(title, level=1)
        md_q1.append(f"## {title}\n")
        for p in paras:
            doc_q1.add_paragraph(p)
            md_q1.append(f"{p}\n")
        md_q1.append("\n")
    doc_q1.save(OUT_DELIV / "Q1" / "Q1_Walkthrough_Script_and_Checklist.docx")
    shutil.copy2(OUT_DELIV / "Q1" / "Q1_Walkthrough_Script_and_Checklist.docx", OUT_FINAL / "Q1" / "Q1_Walkthrough_Script_and_Checklist.docx")
    (OUT_DELIV / "Q1" / "Q1_Walkthrough_Script_and_Checklist.md").write_text("".join(md_q1), encoding="utf-8")
    shutil.copy2(OUT_DELIV / "Q1" / "Q1_Walkthrough_Script_and_Checklist.md", OUT_FINAL / "Q1" / "Q1_Walkthrough_Script_and_Checklist.md")
    (OUT_DELIV / "Q1" / "Q1_Video_Script.md").write_text("".join(md_q1), encoding="utf-8")
    shutil.copy2(OUT_DELIV / "Q1" / "Q1_Video_Script.md", OUT_FINAL / "Q1" / "Q1_Video_Script.md")

    # 3. Q2 Walkthrough Script & Checklist DOCX & MD
    q2_script_content = [
        ("Recording Objective & Technical Setup", [
            "Video Duration: 2 to 3 minutes (120 to 180 seconds target).",
            "Screen Recording: 1080p full-screen capture showing deliverables/Q2/Samarth_Kapdi_Report.pdf and Supporting_Work/charts/q2_poor_good_evidence.png.",
            "Audio Setup: Quiet room, external microphone, professional presentation tone.",
            "Pre-recording Checklist: Open Samarth_Kapdi_Report.pdf to Section 1 (Executive Summary), Section 4 (Overview Table), Section 5 (Poor vs Good Chart), and Section 6 (Settings Re-Runs)."
        ]),
        ("0:00 - 0:35: Scope Clarification & Metric Hygiene", [
            "Show on Screen: Samarth_Kapdi_Report.pdf (Section 1: Executive Summary & Section 2: Dated Leaderboard Note).",
            "Talking Points: Begin with strict scope hygiene: the assessment's historical 139-recording benchmark reports 67.1% DER. We audited a separate 15-recording workbook sample that yields mean DER 64.45% and median DER 86.02%. Never confuse these scopes. Clarify that Voice Arena separately reports 71.89% cpWER for Nova-3 on a combined diarization+ASR track; DER and cpWER are distinct metrics and must never be combined."
        ]),
        ("0:35 - 1:15: Severe Output Under-Coverage & Poor vs Good Contrast", [
            "Show on Screen: q2_poor_good_evidence.png and Table 5 in Samarth_Kapdi_Report.pdf.",
            "Talking Points: Present the empirical core: five severe failures suffered 97-100% DER with catastrophic speech coverage of 0.0% to 9.8%, dominated by missed speech. Name the two empty Nova-3 RTTMs: D20260825_S003_015 (workbook) and S003_012 (package-only). Contrast this against good rows: an in-person 2-speaker session scored 15.13% DER with 97.4% coverage, and an online meeting scored 26.81% DER. Point out that Silero VAD achieved >91% coverage across all rows, proving acoustic speech energy was present."
        ]),
        ("1:15 - 1:55: Deepgram Settings Sheet Diagnostic Re-Runs", [
            "Show on Screen: Samarth_Kapdi_Report.pdf (Section 6: Tables 1 & 2).",
            "Talking Points: Walk through the workbook's 8 recording re-runs across 9 settings. Show that Nova-3 with language=en, en-IN, en-US, and auto-detect fails identically (0 words on S003_015). But switching to language=multi recovers 465 words, and Whisper-large recovers 1,661 words. Mention that non-acoustic parameters changed DER by <=2 points. Explain that these workbook re-runs differ from the 7 manual playground runs, which require live execution."
        ]),
        ("1:55 - 2:30: Root-Cause Synthesis & Proof Gate", [
            "Show on Screen: ROOT_CAUSE_EVIDENCE_MATRIX.md and Section 7 of Samarth_Kapdi_Report.pdf.",
            "Talking Points: Present the tripartite root-cause synthesis: established facts vs inferred speech omission vs unresolved converter loss. Discuss the conditional diagnostic check for diarize_model=latest and metadata.diarize_info. Note that exact benchmark reproduction is impossible because the benchmark author used an earlier reference build. Confirm that all 7 manual runs are preserved as NOT PERFORMED without fabrication."
        ]),
        ("2:30 - 3:00: Engineering Recommendations & Conclusion", [
            "Show on Screen: Samarth_Kapdi_Report.pdf (Section 9: Recommendations).",
            "Talking Points: Summarize actionable recommendations for Deepgram (zero-output diagnostic alert, raw JSON retention, multi-talker table acoustic tuning) and Voice Arena (audio hashes, reference builds, coverage reporting). Close on the importance of evidence-backed, reproducible benchmarking."
        ])
    ]
    doc_q2 = Document()
    doc_q2.add_heading("Question 2 - 2-3 Minute Walkthrough Video Script & Checklist", 0)
    md_q2 = ["# Question 2 - 2-3 Minute Walkthrough Video Script & Checklist\n"]
    for title, paras in q2_script_content:
        doc_q2.add_heading(title, level=1)
        md_q2.append(f"## {title}\n")
        for p in paras:
            doc_q2.add_paragraph(p)
            md_q2.append(f"{p}\n")
        md_q2.append("\n")
    doc_q2.save(OUT_DELIV / "Q2" / "Q2_Walkthrough_Script_and_Checklist.docx")
    shutil.copy2(OUT_DELIV / "Q2" / "Q2_Walkthrough_Script_and_Checklist.docx", OUT_FINAL / "Q2" / "Q2_Walkthrough_Script_and_Checklist.docx")
    (OUT_DELIV / "Q2" / "Q2_Walkthrough_Script_and_Checklist.md").write_text("".join(md_q2), encoding="utf-8")
    shutil.copy2(OUT_DELIV / "Q2" / "Q2_Walkthrough_Script_and_Checklist.md", OUT_FINAL / "Q2" / "Q2_Walkthrough_Script_and_Checklist.md")
    (OUT_DELIV / "Q2" / "Q2_Video_Script.md").write_text("".join(md_q2), encoding="utf-8")
    shutil.copy2(OUT_DELIV / "Q2" / "Q2_Video_Script.md", OUT_FINAL / "Q2" / "Q2_Video_Script.md")
    print("Generated Word documents and walkthrough scripts successfully")


# ---------------------------------------------------------------------------
# 8. BUILD MANUAL EXPERIMENT EXECUTION GUIDE
# ---------------------------------------------------------------------------
def generate_manual_experiment_guide():
    guide_path = OUT_DELIV / "Q2" / "Samarth_Kapdi_Proof" / "MANUAL_EXPERIMENT_EXECUTION_GUIDE.md"
    content = """# Manual Deepgram Playground Experiment Execution Guide

This guide provides exact step-by-step instructions for executing the seven manual Deepgram playground experiments required by the assignment.
**Current Status:** All seven experiments remain `NOT PERFORMED - manual run required`. No experimental evidence is fabricated.

---

## 1. Required Experiments Overview

The assignment requires exactly seven manual playground runs:
- **Five Baseline Runs (Runs 1 to 5):** Model `nova-3`, `diarize=true`, `utterances=true`, default English / auto language.
- **Two Alternative Configuration Runs (Runs 6 & 7):** On the worst-performing recording, test alternate models/languages to isolate the speech omission mechanism.

---

## 2. Detailed Run Specifications

### Run 1: Baseline — Worst Failure Case (0 words in workbook)
- **Recording ID:** `D20260825_S003_015_5SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_015_5SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3` (`general-nova-3`), Language: `English` (`en` or default)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**, Smart Format: Default, Punctuate: Default
- **Workbook Comparison:** Workbook reports 0 words, 0.0% coverage, 100.0% DER. Nova-3 RTTM is completely empty.

### Run 2: Baseline — Severe Failure Case 2
- **Recording ID:** `D20260825_S003_014_5SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260825_S003_014_5SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 34 words, 1.7% coverage, 99.14% DER.

### Run 3: Baseline — Severe Failure Case 3
- **Recording ID:** `D20260826_S001_03_4SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_energy_edges_sept5/D20260826_S001_03_4SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 114 words, 5.5% coverage, 98.59% DER.

### Run 4: Baseline — Good In-Person Control
- **Recording ID:** `D20260825_S004_31_2SPK_IN_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_day3_2person_full_pad30_split_none/D20260825_S004_31_2SPK_IN_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 788 words, 97.4% coverage, 15.13% DER.

### Run 5: Baseline — Good Online Control
- **Recording ID:** `O20260826_S010_04_01_4SPK_US_EN`
- **Audio URL:** `https://storage.googleapis.com/delivery_team_data/diarization/platform_test/platform_transcripts_online_pad30_split_none/O20260826_S010_04_01_4SPK_US_EN/merged.wav`
- **Configuration to Select:** Model: `Nova-3`, Language: `English` (`en`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Workbook reports 2,453 words, 94.6% coverage, 26.81% DER.

### Run 6: Alternative 1 — Multilingual Nova-3 on Worst Failure
- **Recording ID:** `D20260825_S003_015_5SPK_IN_EN`
- **Audio URL:** Same as Run 1
- **Configuration to Select:** Model: `Nova-3`, Language: `Multilingual` (`multi`)
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Settings sheet reports 465 words returned, 93.06% DER (proves English acoustic pipeline collapse).

### Run 7: Alternative 2 — Alternate Architecture / Nova-2 on Worst Failure
- **Recording ID:** `D20260825_S003_015_5SPK_IN_EN`
- **Audio URL:** Same as Run 1
- **Configuration to Select:** Model: `Nova-2` (`general-nova-2`) or hosted `Whisper-Large`
- **Settings to Enable:** Diarization: **ON**, Utterances: **ON**
- **Workbook Comparison:** Settings sheet reports Nova-2 returns 28 words (98.97% DER), while Whisper-Large returns 1,661 words (64.95% DER).

---

## 3. What to Capture During Execution

For every single run, capture:
1. **Full-Window Screenshot:** Showing audio URL/upload, model dropdown, language setting, diarization toggle, utterances toggle, and the returned response window.
2. **Raw API Response JSON:** Save the complete response JSON including `results.channels[0].alternatives[0].words`, `utterances`, and `metadata`.
3. **Deepgram Request ID:** Copy the `request_id` from the JSON response or UI header (e.g. `metadata.request_id`).
4. **Execution Timestamp:** Record exact UTC date and time of request submission.
5. **Returned Metrics:** Count of words returned, number of unique speaker labels assigned, and total speech timeline duration.

---

## 4. Evidence Storage Structure

Save all captured artifacts into:
```
deliverables/Q2/Samarth_Kapdi_Proof/evidence/
  ├── run1_D20260825_S003_015_baseline.png
  ├── run1_D20260825_S003_015_baseline_response.json
  ├── run2_D20260825_S003_014_baseline.png
  ├── run2_D20260825_S003_014_baseline_response.json
  ├── run3_D20260826_S001_03_baseline.png
  ├── run3_D20260826_S001_03_baseline_response.json
  ├── run4_D20260825_S004_31_baseline.png
  ├── run4_D20260825_S004_31_baseline_response.json
  ├── run5_O20260826_S010_04_baseline.png
  ├── run5_O20260826_S010_04_baseline_response.json
  ├── run6_D20260825_S003_015_alt1_multi.png
  ├── run6_D20260825_S003_015_alt1_multi_response.json
  ├── run7_D20260825_S003_015_alt2_nova2.png
  └── run7_D20260825_S003_015_alt2_nova2_response.json
```

---

## 5. Updating the Run Log

Once genuine runs are executed, open `Supporting_Work/playground_run_log.xlsx` and update:
- `request_id`: Captured Deepgram request ID string.
- `run_datetime`: ISO-8601 timestamp (e.g. `2026-11-02T14:30:00Z`).
- `screenshot_path`: Path to saved PNG.
- `status`: Change from `NOT PERFORMED - manual run required` to `COMPLETE`.
"""
    guide_path.write_text(content, encoding="utf-8")
    shutil.copy2(guide_path, OUT_FINAL / "Q2" / "Samarth_Kapdi_Proof" / "MANUAL_EXPERIMENT_EXECUTION_GUIDE.md")
    print("Generated Manual Experiment Execution Guide successfully")


# ---------------------------------------------------------------------------
# 9. GENERATE PRE-POPULATED PLAYGROUND RUN LOG
# ---------------------------------------------------------------------------
def generate_playground_run_log():
    runlog_data = [
        {"recording_id": "D20260825_S003_015_5SPK_IN_EN", "run_type": "baseline", "model": "nova-3", "language": "en", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
        {"recording_id": "D20260825_S003_014_5SPK_IN_EN", "run_type": "baseline", "model": "nova-3", "language": "en", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
        {"recording_id": "D20260826_S001_03_4SPK_IN_EN", "run_type": "baseline", "model": "nova-3", "language": "en", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
        {"recording_id": "D20260825_S004_31_2SPK_IN_EN", "run_type": "baseline", "model": "nova-3", "language": "en", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
        {"recording_id": "O20260826_S010_04_01_4SPK_US_EN", "run_type": "baseline", "model": "nova-3", "language": "en", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
        {"recording_id": "D20260825_S003_015_5SPK_IN_EN", "run_type": "alternative 1", "model": "nova-3", "language": "multi", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
        {"recording_id": "D20260825_S003_015_5SPK_IN_EN", "run_type": "alternative 2", "model": "nova-2", "language": "en", "diarization": "ON", "utterances": "ON", "request_id": None, "run_datetime": None, "screenshot_path": None, "status": "NOT PERFORMED - manual run required"},
    ]
    runlog_df = pd.DataFrame(runlog_data)
    runlog_path = WORK / "playground_run_log.xlsx"
    runlog_df.to_excel(runlog_path, index=False)
    shutil.copy2(runlog_path, OUT_FINAL / "Supporting_Work" / "playground_run_log.xlsx")
    print("Generated pre-populated playground_run_log.xlsx successfully")


# ---------------------------------------------------------------------------
# 10. SYNCHRONIZE ALL DELIVERABLES TO FINAL_SUBMISSION
# ---------------------------------------------------------------------------
def sync_final_submission():
    # Sync Supporting_Work tables and charts
    for p in TABLES.glob("*.csv"):
        shutil.copy2(p, OUT_FINAL / "Supporting_Work" / "tables" / p.name)
    for p in CHARTS.glob("*.png"):
        shutil.copy2(p, OUT_FINAL / "Supporting_Work" / "charts" / p.name)
    for p in (WORK / "analysis").glob("*.py"):
        shutil.copy2(p, OUT_FINAL / "Supporting_Work" / "analysis" / p.name)

    # Sync Root-level markdown files
    for doc in ["ROOT_CAUSE_EVIDENCE_MATRIX.md", "SEVEN_RUN_CHECKLIST.md", "MANUAL_RUN_CHECKLIST.md"]:
        src = OUT_DELIV / "Q2" / "Samarth_Kapdi_Proof" / doc
        if src.exists():
            shutil.copy2(src, OUT_FINAL / "Q2" / "Samarth_Kapdi_Proof" / doc)
    
    src_matrix = OUT_DELIV / "Q2" / "ROOT_CAUSE_EVIDENCE_MATRIX.md"
    if src_matrix.exists():
        shutil.copy2(src_matrix, OUT_FINAL / "Q2" / "ROOT_CAUSE_EVIDENCE_MATRIX.md")

    # Sync README
    readme_src = WORK / "reproducibility_README.md"
    if readme_src.exists():
        shutil.copy2(readme_src, OUT_FINAL / "Supporting_Work" / "reproducibility_README.md")

    print("Synchronized all files to FINAL_SUBMISSION successfully")


def main():
    print("Starting production deliverable generation...")
    generate_mockup_image()
    generate_poor_good_chart()
    build_q1_main_pdf()
    build_q1_one_page_pdf()
    build_q2_pdf()
    build_workspace_audit_pdf()
    build_docx_deliverables()
    generate_manual_experiment_guide()
    generate_playground_run_log()
    sync_final_submission()
    print("All deliverables generated and synchronized.")


if __name__ == "__main__":
    main()
