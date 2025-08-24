# src/pipelines/daily_digest.py
"""
Main entry point for the News Digest pipeline.
Uses the LangGraph orchestrator.
"""
from src.pipelines.orchestrator import run_digest_pipeline

def main():
    print("🌅 Generating Your Daily Research Digest")
    print("="*55)
    
    query = "Indian Independence Day" 
    final_state = run_digest_pipeline(query)
    
    print("\n" + "📄 DIGEST REPORT" + "\n" + "-"*40)
    print(f"Query: '{query}'")  
    print(f"Number of Articles: {len(final_state.get('articles', []))}")
    print(f"Number of Summaries: {len(final_state.get('summaries', []))}")

    summaries = final_state.get('summaries', [])
    articles = final_state.get('articles', [])
    
    for summary in summaries:
        article = next((a for a in articles if a.id == summary.article_id), None)
        title = article.title if article else "Unknown Title"
        print(f"\n📌 {title}")
        print(f"   💡 {summary.summary}")
        print(f"   🎭 Sentiment: {summary.sentiment}")

if __name__ == "__main__":
    main()