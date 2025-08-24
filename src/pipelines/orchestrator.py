# src/orchestrator.py
from typing import Literal
from langgraph.graph import StateGraph, END
from src.models import DigestState
from src.agents.curator import CuratorAgent
from src.agents.summarizer import SummarizerAgent
from src.agents.sentiment_analyzer import SentimentAnalyzerAgent

# Initialize the agents that will be our graph nodes
curator_agent = CuratorAgent()
summarizer_agent = SummarizerAgent()
sentiment_analyzer_agent = SentimentAnalyzerAgent()

def curator_node(state: DigestState) -> dict:
    """Node function to fetch and parse articles."""
    print("\n" + "="*30)
    print("🤖 Curator Agent Working...")
    print("="*30)
    
    articles = curator_agent.fetch_articles(state.query, max_articles=10)
    return {"articles": articles}

def summarizer_node(state: DigestState) -> dict:
    """Node function to summarize all articles in the state."""
    print("\n" + "="*30)
    print("🤖 Summarizer Agent Working...")
    print("="*30)
    
    print(f"📊 Processing {len(state.articles)} articles:")
    for i, article in enumerate(state.articles):
        print(f"  {i+1}. {article.title} (ID: {article.id})")
    
    new_summaries = []
    processed_article_ids = set()
    
    for article in state.articles:
        if article.id in processed_article_ids:
            print(f"⚠️ Skipping duplicate article: {article.title} (ID: {article.id})")
            continue
            
        print(f"\n Processing article {len(new_summaries)+1}/{len(state.articles)}: {article.title}")
        summary = summarizer_agent.summarize(article)
        
        if summary:
            new_summaries.append(summary)
            processed_article_ids.add(article.id)
            print(f"✅ Summary created for: {article.title}")
        else:
            print(f"❌ Summary failed for article {article.id}: {article.title}")
    
    print(f"\n Summary: Created {len(new_summaries)} summaries from {len(state.articles)} articles")
    return {"summaries": new_summaries}

def sentiment_analyzer_node(state: DigestState) -> dict:
    """Node function to analyze sentiment of all summaries."""
    print("\n" + "="*30)
    print(" Sentiment Analyzer Agent Working...")
    print("="*30)
    
    if not state.summaries:
        print("⚠️ No summaries to analyze")
        return {}
    
    # Analyze sentiment for all summaries
    analyzed_summaries = sentiment_analyzer_agent.analyze_batch(state.summaries)
    
    return {"summaries": analyzed_summaries}

# --- Define the Graph ---
workflow = StateGraph(DigestState)

# Add the nodes
workflow.add_node("curator", curator_node)
workflow.add_node("summarizer", summarizer_node)
workflow.add_node("sentiment_analyzer", sentiment_analyzer_node)

# Define the flow: Start -> Curator -> Summarizer -> Sentiment Analyzer -> End
workflow.set_entry_point("curator")
workflow.add_edge("curator", "summarizer")
workflow.add_edge("summarizer", "sentiment_analyzer")
workflow.add_edge("sentiment_analyzer", END)

# Compile the graph
app = workflow.compile()

def run_digest_pipeline(query: str = "AI news") -> DigestState:
    """Runs the compiled graph with an initial state."""
    print("🎯 Initializing LangGraph Workflow...")
    initial_state = DigestState(query=query)
    final_state = app.invoke(initial_state)
    print("\n✅ Pipeline execution complete!")
    return final_state