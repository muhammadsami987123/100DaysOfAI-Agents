from flask import Flask, render_template, request, jsonify, url_for
from meditation_agent import MeditationBot
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
meditation_bot = MeditationBot()

@app.route('/')
def index():
    background_sound_options = []
    for sound in meditation_bot.background_sounds:
        if sound == "none":
            background_sound_options.append({"name": "None", "value": "none"})
        else:
            background_sound_options.append({"name": sound.replace("_", " ").title(), "value": url_for('static', filename=f'{sound}.mp3')})
    return render_template('index.html', background_sound_options=background_sound_options)

@app.route('/start_session', methods=['POST'])
def start_session():
    meditation_type = request.json.get('meditation_type')
    duration = request.json.get('duration')
    background_sound = request.json.get('background_sound')
    
    script = meditation_bot.start_meditation(meditation_type, duration)
    audio_scripts = []
    for line in script:
        audio = meditation_bot.generate_tts_script(line)
        audio_scripts.append({"text": line, "audio": audio})

    return jsonify({"script": audio_scripts})

@app.route('/get_background_sounds')
def get_background_sounds():
    return jsonify({"background_sounds": meditation_bot.background_sounds})

if __name__ == '__main__':
    app.run(debug=True)
