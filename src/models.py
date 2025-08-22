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


