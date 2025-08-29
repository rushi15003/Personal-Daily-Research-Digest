# 🌅 Daily Research Digest

> **AI-Powered Research Digest Generator with Beautiful Web Interface**

A sophisticated AI-driven system that automatically curates, analyzes, and generates personalized daily research digests. Built with LangGraph orchestration, specialized AI agents, and a beautiful beach-themed web interface.

![Daily Research Digest](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange)
![Flask](https://img.shields.io/badge/Flask-Web%20Server-lightgrey)

## 🚀 Features

### 🤖 AI Agents
- **Curator Agent** – Fetches and ranks relevant articles using SerpAPI
- **Summarizer Agent** – Produces concise, clear summaries with sentiment analysis
- **Insight Agent** – Extracts actionable insights and categorizes content
- **Calendar Agent** – Creates Google Calendar events for scheduled digests
- **Drive Upload Agent** – Automatically uploads reports to Google Drive

### 🎨 Web Interface
- **Beautiful Beach-Themed UI** – Relaxing ocean gradient design
- **Real-time Processing** – Live progress updates and status indicators
- **Responsive Design** – Works seamlessly on desktop, tablet, and mobile
- **PDF Download** – One-click report downloads
- **Interactive Reports** – Rich display of articles, summaries, and insights

### 📊 Advanced Capabilities
- **Multi-Source News Aggregation** – Google News integration via SerpAPI
- **Intelligent Content Processing** – Newspaper3k for article parsing
- **Sentiment Analysis** – Automated tone and mood detection
- **Category Classification** – Automatic content categorization
- **Professional PDF Reports** – Polished, formatted output
- **Google Services Integration** – Drive storage and Calendar scheduling

## 🏗️ Architecture

```
Daily Research Digest/
├── 📁 src/                          # Core application logic
│   ├── 🤖 agents/                   # Specialized AI agents
│   │   ├── curator.py              # Article fetching & curation
│   │   ├── summarizer.py           # Content summarization
│   │   ├── insight_agent.py        # Insight extraction
│   │   ├── calendar_agent.py       # Google Calendar integration
│   │   └── drive_upload.py         # Google Drive upload
│   ├── 🔄 pipelines/               # Workflow orchestration
│   │   └── orchestrator.py         # LangGraph workflow definition
│   ├── 🛠️ utils/                   # Utility functions
│   │   └── pdf_generator.py        # PDF report generation
│   └── 📋 models.py                # Pydantic data models
├── 🌊 frontend/                     # Web interface
│   ├── DailyDigest.html           # Main HTML page
│   ├── styles.css                 # Beach-themed CSS
│   └── script.js                  # Interactive JavaScript
├── 📊 data/                        # Generated content
│   └── reports/                   # PDF reports storage
├── 🖥️ app.py                       # Flask web server
├── 📋 requirements.txt             # Python dependencies
└── 📖 README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Cloud Platform account (for Drive & Calendar)
- SerpAPI account (for news fetching)

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Personal-Daily-Research-Digest

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
# SerpAPI for news fetching
SERPAPI_API_KEY=your_serpapi_key_here

# Google Cloud credentials (optional)
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### 3. Start the Application

```bash
# Start the Flask server
python app.py
```

### 4. Access the Application

Open your browser and navigate to: **http://localhost:5000**

## 🎯 Usage

### Web Interface
1. **Enter Research Query** – Specify your topic (e.g., "AI Trends", "Machine Learning")
2. **Select Article Count** – Choose 1-20 articles to analyze
3. **Generate Digest** – Click the button to start processing
4. **View Results** – Browse articles, summaries, and insights
5. **Download Report** – Get the complete PDF digest

### API Endpoints

#### Generate Digest
```http
POST /api/generate-digest
Content-Type: application/json

{
    "query": "AI Trends articles",
    "articles": 5
}
```

#### Health Check
```http
GET /api/health
```

#### Download Report
```http
GET /download-report?path=data/reports/filename.pdf
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SERPAPI_API_KEY` | API key for SerpAPI news fetching | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to Google Cloud credentials | No |

### Customization

#### Adding New Agents
1. Create a new agent class in `src/agents/`
2. Implement the required interface
3. Add the agent to the orchestrator workflow

#### Modifying the UI
- Edit `frontend/styles.css` for styling changes
- Modify `frontend/script.js` for functionality updates
- Update `frontend/DailyDigest.html` for structure changes

## 🛠️ Development

### Project Structure

The application follows a modular architecture:

- **Agents** (`src/agents/`) – Specialized AI components for specific tasks
- **Pipelines** (`src/pipelines/`) – LangGraph workflow orchestration
- **Models** (`src/models.py`) – Pydantic data models for type safety
- **Utils** (`src/utils/`) – Helper functions and utilities
- **Frontend** (`frontend/`) – Web interface with beach theme

### Adding New Features

1. **New Agent**: Create a new agent class and add it to the orchestrator
2. **New API Endpoint**: Add routes to `app.py`
3. **UI Enhancement**: Modify frontend files as needed

### Testing

The application includes comprehensive error handling and logging. Check:
- Browser console for frontend errors
- Server logs for backend issues
- Network tab for API call debugging

## 🎨 Design System

### Color Palette
- **Sky Blue** (#87CEEB) – Primary color
- **Light Blue** (#98D8E8) – Secondary color
- **Light Green** (#B8E6B8) – Accent color
- **Khaki** (#F0E68C) – Sand color
- **Light Pink** (#FFB6C1) – Sunset color

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔍 Troubleshooting

### Common Issues

#### "Failed to connect to backend"
- Ensure `app.py` is running on port 5000
- Check if all dependencies are installed
- Verify firewall settings

#### "SerpAPI connection error"
- Verify your SerpAPI key is correct
- Check internet connectivity
- Ensure you have sufficient API credits

#### "Google Drive upload failed"
- Verify Google Cloud credentials
- Check Drive API permissions
- Ensure proper authentication

### Debug Mode

Enable debug logging by setting `debug=True` in `app.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
```

## 📈 Performance

### Optimization Features
- **Asynchronous Processing** – Non-blocking article fetching
- **Caching** – Intelligent result caching
- **Error Recovery** – Graceful failure handling
- **Resource Management** – Efficient memory usage

### Scalability
- **Modular Architecture** – Easy to add new agents
- **Stateless Design** – Horizontal scaling ready
- **API-First Approach** – RESTful endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph** – For workflow orchestration
- **SerpAPI** – For news article fetching
- **Newspaper3k** – For article parsing
- **Flask** – For web server framework
- **ReportLab** – For PDF generation

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

---

**🌅 Enjoy your AI-powered research digest experience!** 🏖️

