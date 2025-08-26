# src/pipelines/daily_digest.py
"""
Main entry point for the News Digest pipeline.
Uses the LangGraph orchestrator.
"""
from src.pipelines.orchestrator import run_digest_pipeline

def main():
    print("🌅 Generating Your Daily Research Digest")
    print("="*55)
    
    query = "Murder" 
    final_state = run_digest_pipeline(query)
    
    print("\n" + "📄 DIGEST REPORT" + "\n" + "-"*40)
    print(f"Query: '{query}'")  
    print(f"Number of Articles: {len(final_state.get('articles', []))}")
    print(f"Number of Summaries: {len(final_state.get('summaries', []))}")
    print(f"Number of Insight Records: {len(final_state.get('insights', []))}")

    summaries = final_state.get('summaries', [])
    articles = final_state.get('articles', [])
    insights = final_state.get('insights', [])
    
    for summary in summaries:
        article = next((a for a in articles if a.id == summary.article_id), None)
        title = article.title if article else "Unknown Title"
        print(f"\n📌 {title}")
        print(f"   💡 {summary.summary}")
        extras = []
        if getattr(summary, 'sentiment_confidence', None):
            extras.append(f"confidence={summary.sentiment_confidence}")
        extras_str = f" ({', '.join(extras)})" if extras else ""
        print(f"   🎭 Sentiment: {summary.sentiment}{extras_str}")

    if insights:
        print("\n🔎 ACTIONABLE INSIGHTS")
        for insight in insights:
            article = next((a for a in articles if a.id == insight.article_id), None)
            title = article.title if article else "Unknown Title"
            print(f"\n📌 {title}")
            for idx, bullet in enumerate(insight.insights, start=1):
                print(f"   {idx}. {bullet}")
            meta = []
            if getattr(insight, 'categories', None):
                meta.append(f"categories={', '.join(insight.categories)}")
            if getattr(insight, 'confidence', None):
                meta.append(f"confidence={insight.confidence}")
            meta_str = f" ({'; '.join(meta)})" if meta else ""
            print(f"   ↳{meta_str}")


if __name__ == "__main__":
    main()