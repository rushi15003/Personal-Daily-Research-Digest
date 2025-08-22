# src/agents/curator.py
import os
from typing import List
from serpapi import GoogleSearch
from newspaper import Article as NewspaperArticle
from dotenv import load_dotenv

# Import our shared model
from src.models import Article

load_dotenv()

class CuratorAgent:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")

    def fetch_articles(self, query: str, max_articles: int = 10) -> List[Article]:
        """Fetches articles from SerpAPI and parses them with newspaper3k."""
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY not found in environment variables.")

        # 1. Get URLs from SerpAPI
        print("📡 Fetching articles from SerpAPI...")
        search_params = {
            "engine": "google_news",
            "q": query,
            "api_key": self.api_key,
        }
        search = GoogleSearch(search_params)
        results = search.get_dict()
        news_items = results.get("news_results", [])[:max_articles] # Limit results

        articles = []
        # 2. For each URL, use newspaper3k to get the full text
        for item in news_items:
            try:
                print(f"⏳ Parsing: {item.get('title', 'No title')}")
                npp_article = NewspaperArticle(item['link'])
                npp_article.download()
                npp_article.parse()

                # 3. Create our own Article object
                article = Article(
                    title=item.get('title', npp_article.title),
                    url=item['link'],
                    source=item.get('source', {}).get('name', 'Unknown'),
                    published_date=item.get('date', None),
                    raw_text=npp_article.text # This is the key step!
                )
                articles.append(article)
            except Exception as e:
                # Don't crash the whole pipeline if one article fails!
                print(f"❌ Failed to parse article {item.get('link')}: {e}")
                continue

        print(f"✅ Curator found {len(articles)} valid articles.")
        return articles

# Simple test function
if __name__ == "__main__":
    curator = CuratorAgent()
    articles = curator.fetch_articles("AI news", max_articles=3)
    for article in articles:
        print(f"\n--- {article.title} ---")
        print(f"Source: {article.source}")
        print(f"Text Preview: {article.raw_text[:200]}...")