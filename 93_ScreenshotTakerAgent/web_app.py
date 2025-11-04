from flask import Flask, render_template, request, jsonify
import threading
import time
from agent import ScreenshotTakerAgent

app = Flask(__name__)
agent = ScreenshotTakerAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    command_text = data.get('command')
    
    if command_text:
        # Process command in a separate thread to avoid blocking the web app
        threading.Thread(target=agent.process_command, args=(command_text,)).start()
        return jsonify({"status": "success", "message": f"Command '{command_text}' received."})
    return jsonify({"status": "error", "message": "No command provided."}), 400

def start_agent_listening():
    """
    Starts the agent's listening loop in a separate thread.
    """
    agent.run()

if __name__ == '__main__':
    # Start the agent's listening in a separate thread
    # This is a basic example, for a real web app, you might use a message queue or more robust inter-process communication
    # threading.Thread(target=start_agent_listening).start()
    app.run(debug=True)
