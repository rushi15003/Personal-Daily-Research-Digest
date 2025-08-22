# 📰 Personal Newsroom Editor  

The **Personal Newsroom Editor** is an AI-powered system that curates, analyzes, and generates personalized daily news digests.  
It combines **LangGraph-driven orchestration** with specialized AI agents to fetch, summarize, fact-check, and present actionable insights from the latest news.  

---

## 🚀 Features  

- **Curator Agent** – Fetches and ranks the most relevant articles.  
- **Sentiment Agent** – Analyzes sentiment of news content.  
- **Summarizer Agent** – Produces concise and clear summaries.   
- **Fact Checker Agent** – Validates claims and filters misinformation.  
- **Insights Agent** – Generates key takeaways and actionable insights.  
- **PDF Generator** – Produces a polished daily digest report.  
- **Web Dashboard** – Simple frontend to view or download daily reports.  

---

## 🏗️ Project Structure  
```bash
personal-newsroom-editor/
│── README.md # Project overview
│── requirements.txt # Python dependencies
│── .env # Environment variables template (API keys etc.)
│
│── data/
│ └── reports/ # Final daily digest reports (PDFs)
│
│── src/
│ ├── init.py
│ ├── main.py # Orchestration entry point
│ ├── config.py # Config loader
│ ├── orchestrator.py # LangGraph workflow definition
│ │
│ ├── agents/ # Specialized AI agents
│ │ ├── curator_agent.py
│ │ ├── sentiment_agent.py
│ │ ├── summarizer_agent.py
│ │ ├── fact_checker_agent.py
│ │ └── insights_agent.py
│ │
│ ├── utils/ # Helper utilities
│ │ ├── pdf_generator.py
│ │
│ └── pipelines/
│ └── daily_digest.py # Main daily workflow script
│
│── frontend/ # Lightweight web dashboard
│ ├── index.html
│ ├── styles.css
│ └── script.js
```
---

## 📊 Workflow  

1. **Curator Agent** fetches and filters news articles.  
2. **Sentiment Agent** analyzes tone and public mood.  
3. **Summarizer Agent** condenses information.    
4. **Fact Checker Agent** validates claims.  
5. **Insights Agent** produces key takeaways.  
6. **PDF Generator** formats everything into a professional report.  
7. **Frontend Dashboard** allows users to view/download the digest.  

---

## 📅 Usage  

- The daily workflow is run via:  
python src/pipelines/daily_digest.py
- Generated reports are saved under `data/reports/` and available in the frontend. 
