# src/agents/summarizer.py
import os
from typing import Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Import our shared models
from src.models import Article, ArticleSummary

load_dotenv()

class SummarizerAgent:
    def __init__(self):  # <-- Fix here
        # Initialize the LLM client
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0.1,
            max_tokens=200
        )
        
        # Initialize text splitter for chunking long articles only
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,  # Leave room for prompt + response
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Define the chains
        # - Summarization chain: Prompt -> LLM -> String Output
        # - Sentiment chain: Prompt -> LLM -> String (JSON) Output
        self.chain = self._create_chain()
        self.sentiment_chain = self._create_sentiment_chain()

    def _create_chain(self):
        """Creates the LangChain LCEL chain for summarization."""
        prompt_template = """
        You are a world-class news summarizer. Create an extremely concise and informative summary of the following article text.

        Requirements:
        - Summary must be exactly one complete sentence
        - Focus on the main event, decision, or outcome
        - Use neutral, factual tone
        - Ensure the sentence is grammatically complete

        Article Text:
        {article_text}

        Summary (one complete sentence):
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        return prompt | self.llm | StrOutputParser()

    def _create_sentiment_chain(self):
        """Creates the chain that returns sentiment and confidence for a summary (JSON only)."""
        prompt_template = """
        You are an expert sentiment analyst specializing in news content. Analyze the sentiment of the following one-sentence news summary and return ONLY a JSON object.

        Sentiment must be one of: positive, negative, neutral, mixed.
        Confidence must be one of: high, medium, low.

        Summary:
        {summary_text}

        Return ONLY JSON:
        {{
          "sentiment": "positive" | "negative" | "neutral" | "mixed",
          "confidence": "high" | "medium" | "low"
        }}
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        return prompt | self.llm | StrOutputParser()

    def _smart_summarize(self, article_text: str) -> str:
        """Smart summarization: only chunk if absolutely necessary."""
        text_length = len(article_text)
        
        # If text is short enough, process directly (fast path)
        if text_length < 3000:
            print(f"🚀 Fast path: Processing {text_length} chars directly")
            return self.chain.invoke({"article_text": article_text})
        
        # If text is moderately long, try direct processing first
        elif text_length < 50000:
            print(f"⚡ Moderate length: Trying direct processing ({text_length} chars)")
            try:
                return self.chain.invoke({"article_text": article_text})
            except Exception as e:
                print(f"⚠️ Direct processing failed, falling back to chunking: {e}")
                return self._chunk_and_summarize(article_text)
        
        # Only chunk if text is very long
        else:
            print(f" Long text detected: Chunking {text_length} chars")
            return self._chunk_and_summarize(article_text)

    def _chunk_and_summarize(self, article_text: str) -> str:
        """Chunks long text and creates a comprehensive summary."""
        chunks = self.text_splitter.split_text(article_text)
        print(f" Article split into {len(chunks)} chunks")
        
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            try:
                chunk_summary = self.chain.invoke({"article_text": chunk})
                chunk_summaries.append(chunk_summary)
                print(f"✅ Chunk {i+1}/{len(chunks)} summarized")
            except Exception as e:
                print(f"⚠️ Failed to summarize chunk {i+1}: {e}")
                continue
        
        if not chunk_summaries:
            return "Failed to generate summary due to processing errors."
        
        # If we have multiple chunks, create a final summary
        if len(chunk_summaries) > 1:
            combined_summaries = " ".join(chunk_summaries)
            final_prompt = f"""
            You are a news summarizer. Combine these chunk summaries into one comprehensive sentence:

            Chunk Summaries:
            {combined_summaries}

            Final One-Sentence Summary:
            """
            try:
                final_summary = self.llm.invoke(final_prompt)
                return final_summary.content if hasattr(final_summary, 'content') else str(final_summary)
            except Exception as e:
                print(f"⚠️ Failed to create final summary: {e}")
                return chunk_summaries[0]
        
        return chunk_summaries[0]

    def summarize(self, article: Article) -> Optional[ArticleSummary]:
        """Summarizes a single article and returns an ArticleSummary object."""
        print(f"📝 Summarizing: {article.title}")
        
        # Check if article has sufficient text
        if not article.raw_text or len(article.raw_text.strip()) < 50:
            print(f"⚠️ Article '{article.title}' has insufficient text for summarization")
            return None
        
        try:
            # Use smart summarization that only chunks when necessary
            summary_text = self._smart_summarize(article.raw_text)
            
            # Analyze sentiment and confidence for the generated summary
            try:
                import json
                raw = self.sentiment_chain.invoke({"summary_text": summary_text})
                data = json.loads(raw)
                sentiment = str(data.get("sentiment", "neutral")).lower()
                confidence = str(data.get("confidence", "medium")).lower()
                if sentiment not in {"positive", "negative", "neutral", "mixed"}:
                    sentiment = "neutral"
                if confidence not in {"high", "medium", "low"}:
                    confidence = "medium"
            except Exception as e:
                print(f"⚠️ Sentiment analysis failed, defaulting: {e}")
                sentiment = "neutral"
                confidence = "low"

            # Create ArticleSummary with sentiment and confidence
            return ArticleSummary(
                article_id=article.id,
                summary=summary_text.strip(),
                sentiment=sentiment,
                sentiment_confidence=confidence,
                sentiment_reason=None
            )
            
        except Exception as e:
            print(f"❌ Failed to summarize article '{article.title}': {e}")
            return None
