from flask import Flask, render_template, request, jsonify, send_from_directory
from config import Config
from url_shortener_agent import URLShortenerAgent
import pyperclip
import os
import secrets

app = Flask(__name__)
app.config.from_object(Config)

url_shortener_agent = URLShortenerAgent(api_service=app.config['DEFAULT_SHORTENER_API'])

# Ensure QR code directory exists
if not os.path.exists(app.config['QR_CODE_DIR']):
    os.makedirs(app.config['QR_CODE_DIR'])

@app.route('/')
def index():
    return render_template('index.html', languages=Config.LANGUAGES)

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    alias = request.form.get('alias')
    copy_to_clipboard = request.form.get('copy_to_clipboard') == 'on'
    generate_qr = request.form.get('generate_qr') == 'on'

    result = url_shortener_agent.shorten_url(long_url, alias)
    
    if result['error']:
        return jsonify({"error": result['error']})

    short_link = result['short_link']
    qr_code_base64 = None

    if generate_qr:
        qr_code_base64 = url_shortener_agent.generate_qr_code(short_link)

    if copy_to_clipboard:
        try:
            pyperclip.copy(short_link)
            copied_message = "Copied to clipboard!"
        except pyperclip.PyperclipException:
            copied_message = "Failed to copy to clipboard (install xclip or xsel for Linux)."
    else:
        copied_message = ""

    return jsonify({
        "short_link": short_link,
        "qr_code_base64": qr_code_base64,
        "copied_message": copied_message,
        "error": None
    })

@app.route('/static/qrcodes/<path:filename>')
def serve_qrcode(filename):
    return send_from_directory(app.config['QR_CODE_DIR'], filename)

if __name__ == '__main__':
    app.run(debug=True)
