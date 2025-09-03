#!/usr/bin/env python3
"""
Flask Web Server for AI Quiz Maker

This module provides a web interface for the AI Quiz Maker application.
Users can generate quizzes through a beautiful web UI with file upload,
text input, and various export options.
"""

import os
import json
import secrets
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, jsonify, render_template, request, send_from_directory, session
from werkzeug.utils import secure_filename
from config import FLASK_PORT, FLASK_DEBUG, UPLOADS_DIR, OUTPUTS_DIR, QUIZES_DIR, get_api_key
from quiz_generator import QuizGenerator

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'md', 'doc', 'docx'}

# Initialize quiz generator
try:
    quiz_generator = QuizGenerator()
    print("✅ Quiz Generator initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize Quiz Generator: {e}")
    quiz_generator = None

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_session_data() -> Dict[str, Any]:
    """Get or create session data."""
    if 'quiz_data' not in session:
        session['quiz_data'] = {}
    if 'history' not in session:
        session['history'] = []
    return session['quiz_data']

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'quiz_generator': 'ready' if quiz_generator else 'not_ready'
    })

@app.route('/api/generate', methods=['POST'])
def generate_quiz():
    """Generate quiz from various input sources."""
    try:
        if not quiz_generator:
            return jsonify({'success': False, 'error': 'Quiz generator not available'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Extract parameters
        content = data.get('content', '').strip()
        num_questions = int(data.get('questions', 5))
        difficulty = data.get('difficulty', 'medium')
        include_answers = data.get('include_answers', True)
        
        # Validate input
        if not content:
            return jsonify({'success': False, 'error': 'Content is required'}), 400
        
        if not (1 <= num_questions <= 50):
            return jsonify({'success': False, 'error': 'Questions must be between 1 and 50'}), 400
        
        if difficulty not in ['easy', 'medium', 'hard']:
            return jsonify({'success': False, 'error': 'Invalid difficulty level'}), 400
        
        # Generate quiz
        quiz_data = quiz_generator.generate_quiz(
            content=content,
            num_questions=num_questions,
            difficulty=difficulty,
            include_answers=include_answers
        )
        
        # Store in session
        session_data = get_session_data()
        session_data['current_quiz'] = quiz_data
        session_data['last_generated'] = datetime.now().isoformat()
        
        # Add to history
        history_entry = {
            'id': secrets.token_hex(8),
            'topic': quiz_data['topic'],
            'questions': quiz_data['questions'],
            'difficulty': quiz_data['difficulty'],
            'timestamp': quiz_data['generated_at'],
            'quiz_data': quiz_data
        }
        session['history'].insert(0, history_entry)
        
        # Keep only last 10 entries
        if len(session['history']) > 10:
            session['history'] = session['history'][:10]
        
        return jsonify({
            'success': True,
            'quiz': quiz_data,
            'message': 'Quiz generated successfully!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for quiz generation."""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOADS_DIR, safe_filename)
        file.save(filepath)
        
        # Read file content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Clean up file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'content': content,
            'filename': filename,
            'message': 'File uploaded and processed successfully!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fetch-url', methods=['POST'])
def fetch_url():
    """Fetch content from a URL for quiz generation."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        url = data.get('url', '').strip()
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({'success': False, 'error': 'Invalid URL format. Must start with http:// or https://'}), 400
        
        # Fetch content from URL
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML and extract text content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Extract text content
        text_content = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit content length to prevent abuse
        if len(text_content) > 50000:
            text_content = text_content[:50000] + "... [Content truncated due to length]"
        
        if len(text_content) < 100:
            return jsonify({'success': False, 'error': 'Could not extract meaningful content from URL'}), 400
        
        return jsonify({
            'success': True,
            'content': text_content,
            'url': url,
            'content_length': len(text_content),
            'message': 'Content fetched successfully from URL'
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Failed to fetch URL: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error processing URL: {str(e)}'}), 500

@app.route('/api/export', methods=['POST'])
def export_quiz():
    """Export quiz in various formats."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        quiz_data = data.get('quiz')
        format_type = data.get('format', 'md')
        filename = data.get('filename', 'quiz')
        
        if not quiz_data:
            return jsonify({'success': False, 'error': 'Quiz data is required'}), 400
        
        if format_type not in ['md', 'json', 'csv']:
            return jsonify({'success': False, 'error': 'Invalid format'}), 400
        
        # Export quiz
        exported_content = quiz_generator.export_quiz(quiz_data, format_type)
        
        # Save to file
        safe_filename = f"{filename}_{format_type}.{format_type}"
        filepath = quiz_generator.save_quiz(quiz_data, safe_filename, format_type)
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'filename': safe_filename,
            'content': exported_content,
            'message': f'Quiz exported as {format_type.upper()} successfully!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get quiz generation history."""
    try:
        history = session.get('history', [])
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history/<quiz_id>')
def get_quiz_from_history(quiz_id: str):
    """Get a specific quiz from history."""
    try:
        history = session.get('history', [])
        quiz_entry = next((entry for entry in history if entry['id'] == quiz_id), None)
        
        if not quiz_entry:
            return jsonify({'success': False, 'error': 'Quiz not found'}), 404
        
        return jsonify({
            'success': True,
            'quiz': quiz_entry['quiz_data']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear quiz generation history."""
    try:
        session['history'] = []
        return jsonify({
            'success': True,
            'message': 'History cleared successfully!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get quiz generation statistics."""
    try:
        session_data = get_session_data()
        history = session.get('history', [])
        
        if not history:
            return jsonify({
                'success': True,
                'statistics': {
                    'total_quizzes': 0,
                    'average_questions': 0,
                    'difficulty_distribution': {'easy': 0, 'medium': 0, 'hard': 0},
                    'last_generated': None
                }
            })
        
        # Calculate statistics
        total_quizzes = len(history)
        total_questions = sum(entry['questions'] for entry in history)
        average_questions = total_questions / total_quizzes if total_quizzes > 0 else 0
        
        difficulty_distribution = {'easy': 0, 'medium': 0, 'hard': 0}
        for entry in history:
            difficulty = entry['difficulty']
            if difficulty in difficulty_distribution:
                difficulty_distribution[difficulty] += 1
        
        last_generated = session_data.get('last_generated')
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_quizzes': total_quizzes,
                'average_questions': round(average_questions, 1),
                'difficulty_distribution': difficulty_distribution,
                'last_generated': last_generated
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename: str):
    """Download generated quiz files."""
    try:
        return send_from_directory(OUTPUTS_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/validate-input', methods=['POST'])
def validate_input():
    """Validate user input before quiz generation."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        content = data.get('content', '').strip()
        num_questions = data.get('questions', 5)
        difficulty = data.get('difficulty', 'medium')
        
        errors = []
        warnings = []
        
        # Validate content
        if not content:
            errors.append('Content is required')
        elif len(content) < 10:
            errors.append('Content is too short (minimum 10 characters)')
        elif len(content) > 10000:
            warnings.append('Content is very long, this may take longer to process')
        
        # Validate questions
        try:
            num_questions = int(num_questions)
            if not (1 <= num_questions <= 50):
                errors.append('Number of questions must be between 1 and 50')
            elif num_questions > 20:
                warnings.append('Generating many questions may take longer')
        except (ValueError, TypeError):
            errors.append('Number of questions must be a valid integer')
        
        # Validate difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            errors.append('Difficulty must be easy, medium, or hard')
        
        return jsonify({
            'success': True,
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.before_request
def before_request():
    """Set up before each request."""
    # Ensure session is initialized
    if 'quiz_data' not in session:
        session['quiz_data'] = {}
    if 'history' not in session:
        session['history'] = []

if __name__ == '__main__':
    print("🚀 Starting AI Quiz Maker Web Server...")
    print(f"   Port: {FLASK_PORT}")
    print(f"   Debug: {FLASK_DEBUG}")
    print(f"   Uploads: {UPLOADS_DIR}")
    print(f"   Outputs: {OUTPUTS_DIR}")
    print(f"   Quizzes: {QUIZES_DIR}")
    print()
    print("🌐 Open your browser and navigate to:")
    print(f"   http://localhost:{FLASK_PORT}")
    print()
    
    try:
        app.run(
            host='0.0.0.0',
            port=FLASK_PORT,
            debug=FLASK_DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)
