from flask import Flask, render_template, request, jsonify, flash
import os
from datetime import datetime
from pathlib import Path

from config import Config
from search_service import fetch_latest_insights
from ai_service import generate_social_post
from poster import save_post_to_file

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    """Main page with form for post generation"""
    platforms = list(Config.PLATFORM_LIMITS.keys())
    tones = ["professional", "casual", "witty", "inspirational", "friendly", "authoritative", "playful"]
    
    return render_template('index.html', platforms=platforms, tones=tones)


@app.route('/generate', methods=['POST'])
def generate_post():
    """Generate a social media post based on form input"""
    try:
        platform = request.form.get('platform')
        topic = request.form.get('topic')
        tone = request.form.get('tone')
        save_to_file = request.form.get('save_to_file') == 'on'
        
        if not all([platform, topic, tone]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate platform
        if platform not in Config.PLATFORM_LIMITS:
            return jsonify({'error': 'Invalid platform selected'}), 400
        
        # Get character limit for the platform
        char_limit = Config.PLATFORM_LIMITS.get(platform, 280)
        
        # Fetch insights and generate post
        insights = fetch_latest_insights(topic)
        post_text = generate_social_post(platform, topic, tone, insights)
        
        # Prepare response data
        response_data = {
            'success': True,
            'post_text': post_text,
            'platform': platform,
            'topic': topic,
            'tone': tone,
            'char_count': len(post_text),
            'char_limit': char_limit,
            'insights': insights
        }
        
        # Save to file if requested
        if save_to_file:
            try:
                filepath = save_post_to_file(post_text, platform, topic, tone)
                response_data['saved_to'] = filepath
            except Exception as e:
                response_data['save_error'] = str(e)
        
        return jsonify(response_data)
        
    except Exception as e:
        import traceback
        print(f"Error generating post: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Error generating post: {str(e)}'}), 500


@app.route('/save', methods=['POST'])
def save_post():
    """Save a generated post to file"""
    try:
        data = request.get_json()
        post_text = data.get('post_text')
        platform = data.get('platform')
        topic = data.get('topic')
        tone = data.get('tone')
        
        if not all([post_text, platform, topic, tone]):
            return jsonify({'error': 'Missing required data'}), 400
        
        filepath = save_post_to_file(post_text, platform, topic, tone)
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'message': f'Post saved to {filepath}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error saving post: {str(e)}'}), 500


@app.route('/copy', methods=['POST'])
def copy_to_clipboard():
    """Copy post text to clipboard (returns success status)"""
    try:
        data = request.get_json()
        post_text = data.get('post_text')
        
        if not post_text:
            return jsonify({'error': 'No post text provided'}), 400
        
        # In a real implementation, you might use pyperclip or similar
        # For now, we'll just return success as the frontend handles copying
        return jsonify({
            'success': True,
            'message': 'Post text ready for copying'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error preparing copy: {str(e)}'}), 500


if __name__ == '__main__':
    # Ensure posts directory exists
    posts_dir = Path(Config.POSTS_DIR)
    posts_dir.mkdir(exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
