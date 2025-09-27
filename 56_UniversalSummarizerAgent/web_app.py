import os
import io
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from universal_summarizer_agent import UniversalSummarizerAgent
from config import Config
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

load_dotenv()

app = Flask(__name__)
CORS(app)

agent = UniversalSummarizerAgent()

@app.route('/')
def index():
    content_types = ['text', 'url', 'pdf', 'docx', 'txt']
    return render_template('index.html', languages=Config.LANGUAGE_OPTIONS, formats=Config.SUMMARY_FORMATS, content_types=content_types)

@app.route('/summarize', methods=['POST'])
def summarize():
    content_type = request.form.get('content_type', 'text')
    summary_format = request.form.get('summary_format', 'Bullet Points')
    language = request.form.get('language', 'English')
    content = ""

    if content_type == 'text':
        content = request.form.get('text_content')
    elif content_type == 'url':
        content = request.form.get('url_content')
    elif content_type in ['pdf', 'docx', 'txt']:
        if 'file_content' not in request.files:
            return jsonify({'error': 'No file part.'}), 400
        file = request.files['file_content']
        if file.filename == '':
            return jsonify({'error': 'No selected file.'}), 400
        if file and content_type == 'txt':
            content = file.read().decode('utf-8')
        else: # For PDF and DOCX, save temporarily to a file
            filepath = os.path.join('./temp', file.filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            content = filepath # Pass the file path for extraction by the agent
    else:
        return jsonify({'error': 'Invalid content type.'}), 400

    if not content:
        return jsonify({'error': 'Content is required.'}), 400

    try:
        summary = agent.summarize_content(content, summary_format, language, content_type)
        if content_type in ['pdf', 'docx'] and os.path.exists(content):
            os.remove(content) # Clean up temporary file
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    summary_text = data.get('summary')
    file_format = data.get('format')

    if not summary_text or not file_format:
        return jsonify({'error': 'Summary and format are required.'}), 400

    if file_format == 'pdf':
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        textobject = p.beginText()
        textobject.setTextOrigin(letter[0] * 0.1, letter[1] * 0.9)
        textobject.setFont("Helvetica", 12)
        for line in summary_text.splitlines():
            textobject.textLine(line)
        p.drawText(textobject)
        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='summary.pdf', mimetype='application/pdf')
    elif file_format == 'txt':
        buffer = io.BytesIO(summary_text.encode('utf-8'))
        return send_file(buffer, as_attachment=True, download_name='summary.txt', mimetype='text/plain')
    else:
        return jsonify({'error': 'Invalid file format.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
