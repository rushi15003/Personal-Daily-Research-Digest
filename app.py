#!/usr/bin/env python3
"""
Flask backend for the Daily Research Digest application.
Serves the frontend and provides API endpoints for the digest pipeline.
"""

from flask import Flask, request, jsonify, send_file, send_from_directory, render_template_string
from flask_cors import CORS
import os
import json
from datetime import datetime
from src.pipelines.orchestrator import run_digest_pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Serve static files from frontend directory
@app.route('/')
def index():
    try:
        return send_from_directory('frontend', 'DailyDigest.html')
    except Exception:
        return "DailyDigest.html not found", 404

@app.route('/styles.css')
def styles():
    try:
        return send_from_directory('frontend', 'styles.css', mimetype='text/css')
    except Exception:
        return "styles.css not found", 404

@app.route('/script.js')
def script():
    try:
        return send_from_directory('frontend', 'script.js', mimetype='application/javascript')
    except Exception:
        return "script.js not found", 404

@app.route('/api/generate-digest', methods=['POST'])
def generate_digest():
    """API endpoint to generate a research digest."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        query = data.get('query', 'AI Trends articles')
        articles = data.get('articles', 5)
        
        # Validate inputs
        if not query or not query.strip():
            return jsonify({'error': 'Query is required'}), 400
        
        if not isinstance(articles, int) or articles < 1 or articles > 20:
            return jsonify({'error': 'Articles must be between 1 and 20'}), 400
        
        print(f"🌊 Generating digest for query: '{query}' with {articles} articles")
        
        # Run the digest pipeline
        final_state = run_digest_pipeline(query, articles)
        
        # Handle both DigestState object and dictionary responses
        if hasattr(final_state, 'query'):
            # It's a DigestState object
            response_data = {
                'query': final_state.query,
                'articles_count': len(final_state.articles),
                'articles': [
                    {
                        'id': article.id,
                        'title': article.title,
                        'url': article.url,
                        'source': article.source,
                        'published_date': article.published_date,
                        'raw_text': article.raw_text[:500] + '...' if article.raw_text and len(article.raw_text) > 500 else article.raw_text
                    }
                    for article in final_state.articles
                ],
                'summaries': [
                    {
                        'article_id': summary.article_id,
                        'summary': summary.summary,
                        'sentiment': summary.sentiment,
                        'sentiment_confidence': summary.sentiment_confidence
                    }
                    for summary in final_state.summaries
                ],
                'insights': [
                    {
                        'article_id': insight.article_id,
                        'insights': insight.insights,
                        'categories': insight.categories,
                        'confidence': insight.confidence
                    }
                    for insight in final_state.insights
                ],
                'report_path': (final_state.report_path or '').replace('\\','/'),
                'calendar_event_id': final_state.calendar_event_id,
                'drive_file_id': final_state.drive_file_id,
                'generated_at': datetime.now().isoformat()
            }
        else:
            # It's a dictionary (LangGraph response)
            response_data = {
                'query': final_state.get('query', query),
                'articles_count': len(final_state.get('articles', [])),
                'articles': [
                    {
                        'id': article.id,
                        'title': article.title,
                        'url': article.url,
                        'source': article.source,
                        'published_date': article.published_date,
                        'raw_text': article.raw_text[:500] + '...' if article.raw_text and len(article.raw_text) > 500 else article.raw_text
                    }
                    for article in final_state.get('articles', [])
                ],
                'summaries': [
                    {
                        'article_id': summary.article_id,
                        'summary': summary.summary,
                        'sentiment': summary.sentiment,
                        'sentiment_confidence': summary.sentiment_confidence
                    }
                    for summary in final_state.get('summaries', [])
                ],
                'insights': [
                    {
                        'article_id': insight.article_id,
                        'insights': insight.insights,
                        'categories': insight.categories,
                        'confidence': insight.confidence
                    }
                    for insight in final_state.get('insights', [])
                ],
                'report_path': (final_state.get('report_path', '') or '').replace('\\','/'),
                'calendar_event_id': final_state.get('calendar_event_id', ''),
                'drive_file_id': final_state.get('drive_file_id', ''),
                'generated_at': datetime.now().isoformat()
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error generating digest: {str(e)}")
        return jsonify({'error': f'Failed to generate digest: {str(e)}'}), 500

@app.route('/download-report')
def download_report():
    """Download the generated PDF report."""
    try:
        from urllib.parse import unquote
        report_path_param = request.args.get('path')
        
        if not report_path_param:
            return jsonify({'error': 'No report path provided'}), 400
        
        # Decode URL-encoded path and normalize separators
        report_path_param = unquote(report_path_param)
        report_path_param = report_path_param.replace('\\', '/')
        
        # Resolve absolute paths and enforce directory constraint
        reports_dir = os.path.abspath(os.path.join(os.getcwd(), 'data', 'reports'))
        # If a relative path like "data/reports/.." is provided, join to CWD and resolve
        abs_requested_path = os.path.abspath(os.path.join(os.getcwd(), report_path_param))
        
        # If the provided path was just a filename, look for it inside reports_dir
        if not abs_requested_path.startswith(reports_dir):
            abs_requested_path = os.path.abspath(os.path.join(reports_dir, os.path.basename(report_path_param)))
        
        # Security: ensure the final path is inside reports_dir
        if os.path.commonpath([abs_requested_path, reports_dir]) != reports_dir:
            return jsonify({'error': 'Invalid report path'}), 400
        
        if not os.path.exists(abs_requested_path):
            return jsonify({'error': 'Report file not found'}), 404
        
        return send_file(
            abs_requested_path,
            as_attachment=True,
            download_name=os.path.basename(abs_requested_path),
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"❌ Error downloading report: {str(e)}")
        return jsonify({'error': f'Failed to download report: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Daily Research Digest API'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🌅 Starting Daily Research Digest Server...")
    print("📱 Frontend available at: http://localhost:5000")
    print("🔌 API available at: http://localhost:5000/api")
    print("=" * 50)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
