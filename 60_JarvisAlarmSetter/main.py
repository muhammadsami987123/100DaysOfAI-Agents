from flask import Flask
from ui import app as ui_app
from config import Config
from voice import main as voice_main
import threading

# app = Flask(__name__) # No need for a separate Flask app instance here
# app.config.from_object(Config)

# # Register UI blueprints (if using blueprints, otherwise just run the app)
# app.register_blueprint(ui_app)

def start_voice_assistant():
    voice_main()

if __name__ == '__main__':
    # Start the voice assistant in a separate thread
    voice_thread = threading.Thread(target=start_voice_assistant)
    voice_thread.daemon = True  # Allow the main program to exit even if thread is still running
    voice_thread.start()

    # Start the Flask UI
    ui_app.run(debug=Config.DEBUG, port=Config.PORT)
