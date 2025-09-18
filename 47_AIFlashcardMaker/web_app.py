import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import fitz  # PyMuPDF

from config import Config
from flashcard_agent import FlashcardAgent

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

agent = FlashcardAgent(openai_api_key=app.config['OPENAI_API_KEY'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_txt(txt_path):
    text = ""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error extracting text from TXT: {e}")
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_flashcards():
    text_input = request.form.get('text_input')
    file = request.files.get('file')
    num_flashcards = request.form.get('num_flashcards', type=int)
    difficulty = request.form.get('difficulty')
    subject = request.form.get('subject')
    language = request.form.get('language')

    print(f"Received request - Text: {text_input[:50]}..., File: {file.filename if file else 'None'}, Num: {num_flashcards}, Diff: {difficulty}, Subj: {subject}, Lang: {language}")

    content = ""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        if filename.endswith('.pdf'):
            content = extract_text_from_pdf(filepath)
        elif filename.endswith('.txt'):
            content = extract_text_from_txt(filepath)
        
        os.remove(filepath) # Clean up the uploaded file after processing

    elif text_input:
        content = text_input
    else:
        return jsonify({'error': 'No text or file provided'}), 400

    if not content:
        print("Error: No content extracted from input.")
        return jsonify({'error': 'Could not extract content from provided input.'}), 400

    # Generate flashcards using the agent
    flashcards = agent.generate_flashcards(
        text=content,
        num_flashcards=num_flashcards,
        difficulty=difficulty,
        subject=subject,
        language=language
    )
    print(f"Generated flashcards: {flashcards}")

    return jsonify({'flashcards': flashcards})
