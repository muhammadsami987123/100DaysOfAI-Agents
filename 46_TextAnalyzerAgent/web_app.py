import os
from flask import Flask, render_template, request, jsonify
from text_analyzer_agent import TextAnalyzerAgent
from config import Config
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

if not Config.GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is not set. The Text Analyzer Agent may not function correctly.")

analyzer = TextAnalyzerAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_text = request.json.get('text')
    if not user_text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        analysis_result = analyzer.analyze_text(user_text)
        return jsonify({'result': analysis_result})
    except Exception as e:
        app.logger.error(f"Error during text analysis: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'An internal server error occurred during analysis.'}), 500
