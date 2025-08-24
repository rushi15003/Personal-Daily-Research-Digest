# src/agents/sentiment_analyzer.py
import os
from typing import List, Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from src.models import ArticleSummary

load_dotenv()

class SentimentAnalyzerAgent:
    def init(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=100
        )
        
        self.chain = self._create_chain()

    def _create_chain(self):
        """Creates the LangChain LCEL chain for sentiment analysis."""
        prompt_template = """
        You are an expert sentiment analyst specializing in news content. Analyze the sentiment of the following news summary and provide a precise sentiment classification.

        Sentiment Categories:
        - positive: Optimistic, favorable, beneficial, successful outcomes
        - negative: Pessimistic, unfavorable, harmful, concerning developments
        - neutral: Balanced, factual, neither particularly positive nor negative
        - mixed: Contains both positive and negative elements that balance each other

        Analysis Guidelines:
        - Consider the overall tone and implications of the news
        - Look for emotional language, outcomes, and potential impact
        - Focus on the main event or decision being reported
        - Consider the broader context and implications

        News Summary:
        {summary_text}

        Sentiment Analysis:
        Based on the above summary, the sentiment is: [positive/negative/neutral/mixed]

        Confidence Level:
        [high/medium/low] - based on how clear the sentiment indicators are

        Brief Reasoning:
        [1-2 sentences explaining why this sentiment was chosen]
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        return prompt | self.llm | StrOutputParser()

    def analyze_sentiment(self, summary: ArticleSummary) -> ArticleSummary:
        """Analyzes the sentiment of a single summary and returns updated ArticleSummary."""
        print(f"🎭 Analyzing sentiment for: {summary.summary[:50]}...")
        
        try:
            # Get the sentiment analysis
            analysis_result = self.chain.invoke({"summary_text": summary.summary})
            
            # Parse the result to extract sentiment
            sentiment = self._extract_sentiment(analysis_result)
            
            # Update the summary with the analyzed sentiment
            summary.sentiment = sentiment
            print(f"✅ Sentiment analyzed: {sentiment}")
            
            return summary
            
        except Exception as e:
            print(f"❌ Failed to analyze sentiment: {e}")
            # Fallback to neutral sentiment
            summary.sentiment = "neutral"
            return summary

    def _extract_sentiment(self, analysis_result: str) -> str:
        """Extracts the sentiment from the analysis result."""
        analysis_lower = analysis_result.lower()
        
        # Look for sentiment indicators in the response
        if "positive" in analysis_lower:
            return "positive"
        elif "negative" in analysis_lower:
            return "negative"
        elif "mixed" in analysis_lower:
            return "mixed"
        else:
            return "neutral"

    def analyze_batch(self, summaries: List[ArticleSummary]) -> List[ArticleSummary]:
        """Analyzes sentiment for a batch of summaries."""
        print(f"\n🎭 Starting batch sentiment analysis for {len(summaries)} summaries...")
        
        analyzed_summaries = []
        for i, summary in enumerate(summaries):
            print(f"  Processing summary {i+1}/{len(summaries)}")
            analyzed_summary = self.analyze_sentiment(summary)
            analyzed_summaries.append(analyzed_summary)
        
        print(f"✅ Batch sentiment analysis complete!")
        return analyzed_summaries