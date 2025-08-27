# src/utils/pdf_generator.py
import os
from datetime import datetime
from typing import List, Optional
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

from src.models import Article, ArticleSummary, ArticleInsight


def _safe_filename(base: str) -> str:
    return "".join(c for c in base if c.isalnum() or c in ("_", "-", ".", " ")).rstrip()


def generate_daily_report(
    articles: List[Article],
    summaries: List[ArticleSummary],
    insights: List[ArticleInsight],
    output_dir: str = "data/reports",
    report_title: Optional[str] = None,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    pretty_timestamp = now.strftime("%Y-%m-%d %H:%M")
    title = report_title or f"Daily Research Digest"
    filename = f"{_safe_filename(title)} - {timestamp}.pdf"
    path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(title, styles["Title"]))
    story.append(Paragraph(f"Generated on {pretty_timestamp}", styles["Italic"]))
    story.append(Spacer(1, 0.2 * inch))

    # Index by article id for quick lookup
    summaries_by_article = {s.article_id: s for s in summaries}
    insights_by_article = {}
    for ins in insights:
        insights_by_article.setdefault(ins.article_id, []).append(ins)

    for idx, article in enumerate(articles, start=1):
        # Article Header
        story.append(Paragraph(f"{idx}. {article.title}", styles["Heading2"]))
        meta_text = f"Source: {article.source} | Date: {article.published_date or 'N/A'} | URL: {article.url}"
        story.append(Paragraph(meta_text, styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))

        # Summary + Sentiment
        summary = summaries_by_article.get(article.id)
        if summary:
            story.append(Paragraph("Summary", styles["Heading3"]))
            story.append(Paragraph(summary.summary, styles["BodyText"]))
            sent_meta = f"Sentiment: {summary.sentiment}"
            if getattr(summary, "sentiment_confidence", None):
                sent_meta += f" (confidence={summary.sentiment_confidence})"
            story.append(Paragraph(sent_meta, styles["Italic"]))

        # Insights
        ins_list = insights_by_article.get(article.id, [])
        if ins_list:
            bullets = []
            for record in ins_list:
                for insight in record.insights:
                    bullets.append(Paragraph(insight, styles["BodyText"]))
            if bullets:
                story.append(Spacer(1, 0.05 * inch))
                story.append(Paragraph("Actionable Insights", styles["Heading3"]))
                story.append(
                    ListFlowable(
                        [ListItem(b) for b in bullets],
                        bulletType="bullet",
                        start="circle",
                        bulletColor=colors.black,
                        leftIndent=18,
                    )
                )

        story.append(Spacer(1, 0.25 * inch))

    doc.build(story)
    return path


