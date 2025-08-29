// Global variables
let currentReportData = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Form submission
    document.getElementById('digestForm').addEventListener('submit', handleFormSubmission);
    
    // Input focus effects
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });

    // Submit button hover effects
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.addEventListener('mouseenter', function() {
        this.style.background = 'linear-gradient(135deg, #98D8E8, #B8E6B8)';
    });
    
    submitBtn.addEventListener('mouseleave', function() {
        this.style.background = 'linear-gradient(135deg, #87CEEB, #98D8E8)';
    });
}

async function handleFormSubmission(e) {
    e.preventDefault();
    
    const query = document.getElementById('query').value;
    const articles = document.getElementById('articles').value;
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const reportSection = document.getElementById('reportSection');
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Processing...';
    loading.style.display = 'block';
    result.style.display = 'none';
    reportSection.style.display = 'none';
    
    try {
        // Call the backend API
        const response = await callBackendAPI(query, articles);
        
        // Store the report data
        currentReportData = response;
        
        // Show success result
        result.className = 'result success';
        result.innerHTML = `
            <h3>✅ Digest Generated Successfully!</h3>
            <p><strong>Query:</strong> ${query}</p>
            <p><strong>Articles Processed:</strong> ${response.articles_count || articles}</p>
            <p><strong>Status:</strong> Research digest report has been generated and uploaded to your Google Drive.</p>
        `;
        result.style.display = 'block';
        
        // Display the report
        displayReport(response);
        
    } catch (error) {
        // Show error result
        result.className = 'result error';
        result.innerHTML = `
            <h3>❌ Error Occurred</h3>
            <p>${error.message}</p>
            <p>Please check your input and try again.</p>
        `;
        result.style.display = 'block';
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.textContent = '🚀 Generate Digest';
        loading.style.display = 'none';
    }
}

async function callBackendAPI(query, articles) {
    try {
        const response = await fetch('/api/generate-digest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                articles: parseInt(articles)
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API call failed:', error);
        
        // For development/testing, fall back to simulation
        if (error.message.includes('fetch')) {
            console.log('Falling back to simulation mode...');
            return await simulateBackendCall(query, articles);
        }
        
        throw new Error('Failed to connect to backend. Please try again.');
    }
}

// Simulate backend API call for development
function simulateBackendCall(query, articles) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (Math.random() > 0.1) {
                // Simulate successful response with mock data
                const mockData = generateMockReportData(query, articles);
                resolve(mockData);
            } else {
                reject(new Error('Failed to generate digest. Please try again.'));
            }
        }, 3000);
    });
}

function generateMockReportData(query, articles) {
    const mockArticles = [];
    const mockSummaries = [];
    const mockInsights = [];
    
    for (let i = 1; i <= Math.min(articles, 5); i++) {
        const articleId = `article_${i}`;
        
        mockArticles.push({
            id: articleId,
            title: `Sample Article ${i} about ${query}`,
            url: `https://example.com/article-${i}`,
            source: `Sample Source ${i}`,
            published_date: new Date().toISOString().split('T')[0],
            raw_text: `This is a sample article about ${query}. It contains relevant information and insights that would be processed by our AI agents.`
        });
        
        mockSummaries.push({
            article_id: articleId,
            summary: `This article discusses important developments in ${query}. Key findings include technological advancements and market trends that could impact the industry.`,
            sentiment: ['positive', 'neutral', 'negative'][Math.floor(Math.random() * 3)],
            sentiment_confidence: 'high'
        });
        
        mockInsights.push({
            article_id: articleId,
            insights: [
                `Market opportunity identified in ${query} sector`,
                `Technology adoption rate increasing by 25%`,
                `Regulatory changes expected in Q3 2024`
            ],
            categories: ['Technology', 'Market Analysis'],
            confidence: 'high'
        });
    }
    
    return {
        query: query,
        articles_count: mockArticles.length,
        articles: mockArticles,
        summaries: mockSummaries,
        insights: mockInsights,
        report_path: `data/reports/Daily Research Digest - ${query} - ${Date.now()}.pdf`,
        calendar_event_id: 'mock_calendar_event_123',
        drive_file_id: 'mock_drive_file_456'
    };
}

function displayReport(data) {
    const reportSection = document.getElementById('reportSection');
    const reportContent = document.getElementById('reportContent');
    
    // Generate HTML for the report
    let reportHTML = `
        <h2>📊 Daily Research Digest: ${data.query}</h2>
        <p><strong>Generated on:</strong> ${new Date().toLocaleDateString()}</p>
        <p><strong>Articles analyzed:</strong> ${data.articles_count}</p>
    `;
    
    // Display articles with summaries and insights
    if (data.articles && data.articles.length > 0) {
        reportHTML += '<h3>📰 Article Summaries & Insights</h3>';
        
        data.articles.forEach((article, index) => {
            const summary = data.summaries.find(s => s.article_id === article.id);
            const insight = data.insights.find(i => i.article_id === article.id);
            
            reportHTML += `
                <div class="article-item">
                    <div class="article-title">
                        ${article.title}
                        ${summary ? `<span class="sentiment-badge sentiment-${summary.sentiment}">${summary.sentiment}</span>` : ''}
                    </div>
                    <div class="article-meta">
                        <strong>Source:</strong> ${article.source} | 
                        <strong>Date:</strong> ${article.published_date || 'N/A'}
                    </div>
                    ${summary ? `<div class="article-summary">${summary.summary}</div>` : ''}
                    ${insight && insight.insights ? `
                        <div>
                            <strong>💡 Key Insights:</strong>
                            <ul class="insights-list">
                                ${insight.insights.map(insight => `<li>${insight}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
        });
    }
    
    // Add download button if report path exists
    if (data.report_path) {
        reportHTML += `
            <div style="text-align: center; margin-top: 30px;">
                <a href="/download-report?path=${encodeURIComponent(data.report_path)}" 
                   class="download-btn" download>
                    📥 Download PDF Report
                </a>
            </div>
        `;
    }
    
    reportContent.innerHTML = reportHTML;
    reportSection.style.display = 'block';
    
    // Scroll to report section
    reportSection.scrollIntoView({ behavior: 'smooth' });
}

// Utility function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Export functions for potential use in other scripts
window.DailyDigestApp = {
    handleFormSubmission,
    callBackendAPI,
    displayReport,
    generateMockReportData
};
