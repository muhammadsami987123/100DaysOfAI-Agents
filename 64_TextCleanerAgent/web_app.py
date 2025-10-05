from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from .config import Config
from .text_cleaner_agent import TextCleanerAgent
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['FLASK_SECRET_KEY']

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Retrieve results from session after a redirect
    original_text = session.pop('original_text', None)
    cleaned_text = session.pop('cleaned_text', None)
    return render_template('index.html', original_text=original_text, cleaned_text=cleaned_text)

@app.route('/clean', methods=['POST'])
def clean_text_web():
    api_key = app.config['GEMINI_API_KEY']
    if not api_key:
        # Store error message in session and redirect
        session['error_message'] = "Error: Gemini API key not configured."
        return redirect(url_for('index'))

    agent = TextCleanerAgent(api_key=api_key)
    input_content = ""
    summarize = 'summarize' in request.form
    provide_diff = 'diff' in request.form

    if 'text_input' in request.form and request.form['text_input']:
        input_content = request.form['text_input']
    elif 'file_input' in request.files:
        file = request.files['file_input']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            if filename.endswith('.docx'):
                input_content = agent._read_docx(filepath)
            else: # .txt
                input_content = agent._read_txt(filepath)
            os.remove(filepath) # Clean up the uploaded file
        else:
            session['error_message'] = "Error: Invalid file type or no file uploaded."
            return redirect(url_for('index'))
    elif 'url_input' in request.form and request.form['url_input']:
        input_content = agent._fetch_url_content(request.form['url_input'])
        if input_content.startswith("Error fetching URL"):
            session['error_message'] = input_content
            return redirect(url_for('index'))
    else:
        session['error_message'] = "Error: No input provided for cleaning."
        return redirect(url_for('index'))

    if not input_content:
        session['error_message'] = "No content to clean or error fetching content."
        return redirect(url_for('index'))

    cleaned_output = agent.clean_text(input_content, summarize=summarize, provide_diff=provide_diff)

    # Store results in session and redirect to GET endpoint
    session['original_text'] = input_content if provide_diff else None
    session['cleaned_text'] = cleaned_output
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
