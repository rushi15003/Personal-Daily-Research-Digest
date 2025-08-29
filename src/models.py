# src/models.py
from typing import List, Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from langgraph.graph import add_messages

class Article(BaseModel):
    """Model for a raw article fetched from the web."""
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp())) 
    title: str
    url: str
    source: str
    published_date: Optional[str] = None
    raw_text: Optional[str] = None  

class ArticleSummary(BaseModel):
    """Model for the summarized output of an Article."""
    article_id: str 
    summary: str
    sentiment: str 
    sentiment_confidence: Optional[str] = None
    sentiment_reason: Optional[str] = None


class ArticleInsight(BaseModel):
    """Actionable insights derived from the full article text (not the summary)."""
    article_id: str
    insights: List[str]
    categories: Optional[List[str]] = None
    confidence: Optional[str] = None  # high | medium | low
    rationale: Optional[str] = None


class DigestState(BaseModel):
    """The shared state for the daily digest workflow."""
    # The input from the user/trigger
    query: str = "top technology news"
    max_articles: int = 5
    
    # The messages represent the sequence of events and results (for debugging/observability)
    messages: Annotated[list, add_messages] = Field(default_factory=list)
    
    # The core data produced by each node/agent
    articles: List[Article] = Field(default_factory=list)
    summaries: List[ArticleSummary] = Field(default_factory=list)
    insights: List[ArticleInsight] = Field(default_factory=list)
    
    # The final output
    report_markdown: str = ""
    report_path: str = ""
    drive_file_id: str = ""
    calendar_event_id: str = ""
