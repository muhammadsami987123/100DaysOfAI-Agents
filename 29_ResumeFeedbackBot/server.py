import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import traceback

from config import Config
from resume_analyzer import ResumeAnalyzer
from portfolio_analyzer import PortfolioAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(Config.LOGS_FOLDER, 'resume_feedback_bot.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize analyzers
resume_analyzer = ResumeAnalyzer()
portfolio_analyzer = PortfolioAnalyzer()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """API endpoint for resume analysis"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or DOCX files.'}), 400
        
        # Get form data
        target_role = request.form.get('target_role', '')
        industry = request.form.get('industry', '')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
        
        file.save(file_path)
        logger.info(f"File saved: {file_path}")
        
        # Extract text from file
        try:
            resume_text = resume_analyzer.extract_text_from_file(file_path)
            logger.info(f"Text extracted from {filename}, length: {len(resume_text)}")
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return jsonify({'error': f'Failed to extract text from file: {str(e)}'}), 500
        
        # Analyze resume
        try:
            analysis = resume_analyzer.analyze_resume(resume_text, target_role, industry)
            logger.info(f"Resume analysis completed for {filename}")
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500
        
        # Save analysis
        try:
            analysis_file = resume_analyzer.save_analysis(analysis, safe_filename)
            logger.info(f"Analysis saved to: {analysis_file}")
        except Exception as e:
            logger.warning(f"Failed to save analysis: {e}")
        
        # Generate improved version
        try:
            improvements = resume_analyzer.generate_improved_version(resume_text, analysis)
            analysis['improvements'] = improvements
        except Exception as e:
            logger.warning(f"Failed to generate improvements: {e}")
            analysis['improvements'] = {
                'improved_resume': resume_text,
                'key_improvements': ['Could not generate improvements'],
                'error': True
            }
        
        # Add metadata
        analysis['metadata'] = {
            'filename': filename,
            'target_role': target_role,
            'industry': industry,
            'analysis_date': datetime.now().isoformat(),
            'file_size': os.path.getsize(file_path),
            'word_count': len(resume_text.split())
        }
        
        return jsonify(analysis)
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413
    except Exception as e:
        logger.error(f"Unexpected error in analyze_resume: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/analyze-portfolio', methods=['POST'])
def analyze_portfolio():
    """API endpoint for portfolio analysis"""
    try:
        data = request.get_json()
        if not data or 'portfolio_url' not in data:
            return jsonify({'error': 'Portfolio URL is required'}), 400
        
        portfolio_url = data['portfolio_url'].strip()
        if not portfolio_url:
            return jsonify({'error': 'Portfolio URL cannot be empty'}), 400
        
        logger.info(f"Analyzing portfolio: {portfolio_url}")
        
        # Analyze portfolio
        try:
            analysis = portfolio_analyzer.analyze_portfolio(portfolio_url)
            logger.info(f"Portfolio analysis completed for {portfolio_url}")
        except Exception as e:
            logger.error(f"Error analyzing portfolio: {e}")
            return jsonify({'error': f'Failed to analyze portfolio: {str(e)}'}), 500
        
        # Save analysis
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_filename = f"{timestamp}_portfolio"
            analysis_file = portfolio_analyzer.save_analysis(analysis, safe_filename)
            logger.info(f"Portfolio analysis saved to: {analysis_file}")
        except Exception as e:
            logger.warning(f"Failed to save portfolio analysis: {e}")
        
        # Add metadata
        analysis['metadata'] = {
            'portfolio_url': portfolio_url,
            'analysis_date': datetime.now().isoformat()
        }
        
        return jsonify(analysis)
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze_portfolio: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for AI chat assistance"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message'].strip()
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        logger.info(f"Chat message: {message[:100]}...")
        
        # Generate response using OpenAI
        try:
            import openai
            client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            
            # Build context-aware prompt
            system_prompt = """You are an expert career consultant and resume reviewer. 
            Help users with specific questions about their resume, portfolio, or career development.
            Provide actionable, specific advice."""
            
            user_prompt = f"""
            User Question: {message}
            
            Context: {json.dumps(context, indent=2) if context else 'No specific context provided'}
            
            Please provide a helpful, specific response to the user's question.
            """
            
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            return jsonify({
                'response': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return jsonify({'error': f'Failed to generate response: {str(e)}'}), 500
        
    except Exception as e:
        logger.error(f"Unexpected error in chat: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/api/download-analysis/<filename>')
def download_analysis(filename):
    """Download analysis results"""
    try:
        file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Analysis file not found'}), 404
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Error downloading analysis: {e}")
        return jsonify({'error': 'Failed to download analysis'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to run the Flask app"""
    # Validate configuration
    errors = Config.validate_config()
    if errors:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        return
    
    logger.info("Starting ResumeFeedbackBot server...")
    logger.info(f"Server will run on http://{Config.HOST}:{Config.PORT}")
    
    # Run the Flask app
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

if __name__ == '__main__':
    main()
