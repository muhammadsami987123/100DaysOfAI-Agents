from flask import Flask, render_template, request, jsonify
from config import Config
from alarm_manager import AlarmManager

app = Flask(__name__)
app.config.from_object(Config)
alarm_manager = AlarmManager(app.config['ALARM_FILE'])

@app.route('/')
def index():
    alarms = alarm_manager.get_all_alarms()
    return render_template('index.html', alarms=alarms)

@app.route('/add_alarm', methods=['POST'])
def add_alarm_ui():
    time_str = request.form.get('time')
    message = request.form.get('message')
    recurrence = request.form.get('recurrence')
    alarm_manager.add_alarm(time_str, message, recurrence)
    return jsonify({'status': 'success', 'message': 'Alarm added successfully'})

@app.route('/update_alarm/<string:alarm_id>', methods=['POST'])
def update_alarm_ui(alarm_id):
    new_time = request.form.get('time')
    new_message = request.form.get('message')
    new_recurrence = request.form.get('recurrence')
    alarm_manager.update_alarm(alarm_id, new_time, new_message, new_recurrence)
    return jsonify({'status': 'success', 'message': 'Alarm updated successfully'})

@app.route('/cancel_alarm/<string:alarm_id>', methods=['POST'])
def cancel_alarm_ui(alarm_id):
    alarm_manager.cancel_alarm(alarm_id)
    return jsonify({'status': 'success', 'message': 'Alarm cancelled successfully'})
