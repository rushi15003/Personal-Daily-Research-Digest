# src/agents/curator.py
import os
from typing import List, Dict, Any 
from serpapi import GoogleSearch
from newspaper import Article as NewspaperArticle
from dotenv import load_dotenv
import json  

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

        news_items = results.get("news_results", [])
        print(f"SerpAPI returned {len(news_items)} raw items.")
        
        articles = []
        processed_count = 0
        
        # 2. For each item, try to extract a URL and parse it
        for item in news_items:
            if processed_count >= max_articles:
                break
                
            # Get the URL using .get() to avoid KeyError. Try common keys.
            url = item.get('link') or item.get('url') or item.get('source', {}).get('link')
            if not url:
                print(f"⚠️ Skipping item with no available URL: {item.get('title', 'No Title')}")
                continue
            
            # Get a title for logging
            title = item.get('title', 'No Title')
            print(f"⏳ ({processed_count+1}/{max_articles}) Parsing: {title}")
            
            try:
                npp_article = NewspaperArticle(url)
                npp_article.download()
                npp_article.parse()

                # DEBUG: Check if we actually got text
                if not npp_article.text or len(npp_article.text.strip()) < 50:
                    print(f"⚠️ Article '{title}' has insufficient text ({len(npp_article.text or '')} chars). Skipping.")
                    continue

                # 3. Create our own Article object
                article = Article(
                    title=title,
                    url=url,
                    source=item.get('source', {}).get('name', 'Unknown'),
                    published_date=item.get('date', None),
                    raw_text=npp_article.text
                )
                articles.append(article)
                processed_count += 1
                print(f"✅ Successfully parsed article: {title} ({len(npp_article.text)} chars)")
                
            except Exception as e:
                # Don't crash the whole pipeline if one article fails!
                print(f"❌ Failed to parse article '{title}' ({url}): {e}")
                continue

        print(f"✅ Curator successfully parsed {len(articles)} out of {max_articles} requested articles.")
        return articles

