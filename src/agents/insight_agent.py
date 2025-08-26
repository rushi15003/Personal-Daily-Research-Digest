# src/agents/insight_agent.py
import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.models import Article, ArticleInsight

load_dotenv()


class InsightAgent:
    """Generates actionable insights directly from full article text."""

    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0.2,
            max_tokens=300,
        )
        self.chain = self._create_chain()

    def _create_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an analyst generating concise, actionable insights from news articles. "
                        "Read the full article text and produce 3-5 bullet insights focused on decisions, risks, opportunities, and next steps. "
                        "Return JSON with keys: insights (list of strings), categories (list of strings), confidence (high|medium|low), rationale (short string). "
                        "Be concrete and avoid generic statements."
                    ),
                ),
                (
                    "human",
                    (
                        "Title: {title}\n\n"
                        "Source: {source}\n\n"
                        "Full Article:\n" 
                        "{article_text}\n\n"
                        "Respond with ONLY the JSON."
                    ),
                ),
            ]
        )
        return prompt | self.llm | StrOutputParser()

    def analyze(self, article: Article) -> Optional[ArticleInsight]:
        if not article.raw_text or len(article.raw_text.strip()) < 50:
            return None
        try:
            import json
            raw = self.chain.invoke({
                "title": article.title,
                "source": article.source,
                "article_text": article.raw_text,
            })
            data = json.loads(raw)
            insights_list: List[str] = [i for i in data.get("insights", []) if isinstance(i, str)]
            categories = data.get("categories") or None
            confidence = data.get("confidence") or None
            rationale = data.get("rationale") or None
            if not insights_list:
                return None
            return ArticleInsight(
                article_id=article.id,
                insights=[i.strip() for i in insights_list if i.strip()],
                categories=[c.strip() for c in categories] if isinstance(categories, list) else None,
                confidence=str(confidence).lower() if isinstance(confidence, str) else None,
                rationale=rationale.strip() if isinstance(rationale, str) else None,
            )
        except Exception as e:
            print(f"⚠️ Insight extraction failed for '{article.title}': {e}")
            return None