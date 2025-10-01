from datetime import datetime, timedelta
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

class AlarmManager:
    def __init__(self, alarm_file):
        self.alarm_file = alarm_file
        self.alarms = self._load_alarms()
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self._reschedule_all_alarms()

    def _load_alarms(self):
        if os.path.exists(self.alarm_file):
            with open(self.alarm_file, 'r') as f:
                return json.load(f)
        return []

    def _save_alarms(self):
        with open(self.alarm_file, 'w') as f:
            json.dump(self.alarms, f, indent=4)

    def _reschedule_all_alarms(self):
        self.scheduler.remove_all_jobs()
        for alarm in self.alarms:
            self._schedule_single_alarm(alarm)

    def _schedule_single_alarm(self, alarm):
        # This is a simplified scheduling. Real NLU parsing for recurring alarms is complex.
        # For now, let's assume time is in HH:MM AM/PM format for one-time alarms
        # and for recurring, it includes day of week.

        try:
            # Try to parse as a direct datetime for one-time alarms
            if " " in alarm['time'] and ("AM" in alarm['time'] or "PM" in alarm['time']):
                # Attempt to parse a full date/time string
                try:
                    alarm_datetime = datetime.strptime(alarm['time'], "%Y-%m-%d %I:%M %p")
                except ValueError:
                    # Fallback for simple time, assume for today if time is in future, else tomorrow
                    now = datetime.now()
                    parsed_time = datetime.strptime(alarm['time'].replace(" ", ""), "%I%M%p")
                    alarm_datetime = now.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0)
                    if alarm_datetime < now:
                        alarm_datetime += timedelta(days=1)

                self.scheduler.add_job(self.trigger_alarm, 'date', run_date=alarm_datetime, args=[alarm['id'], alarm['message']], id=alarm['id'])
                print(f"Scheduled one-time alarm {alarm['id']} for {alarm_datetime}")
            elif alarm['recurrence']:
                # Simplified recurring alarm logic (e.g., "every Monday")
                day_map = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                if alarm['recurrence'].lower() in day_map:
                    day_of_week = day_map[alarm['recurrence'].lower()]
                    time_parts = alarm['time'].replace(" ", "").upper().split(':')
                    hour = int(time_parts[0])
                    minute = int(time_parts[1][:2])

                    self.scheduler.add_job(self.trigger_alarm, 'cron', day_of_week=day_of_week, hour=hour, minute=minute, args=[alarm['id'], alarm['message']], id=alarm['id'])
                    print(f"Scheduled recurring alarm {alarm['id']} for every {alarm['recurrence']} at {alarm['time']}")
            else:
                print(f"Could not schedule alarm {alarm['id']} due to unknown time format: {alarm['time']}")
        except Exception as e:
            print(f"Error scheduling alarm {alarm.get('id', 'unknown')}: {e}")

    def add_alarm(self, time_str, message, recurrence=None):
        from uuid import uuid4
        alarm_id = str(uuid4())
        new_alarm = {
            'id': alarm_id,
            'time': time_str,
            'message': message,
            'recurrence': recurrence
        }
        self.alarms.append(new_alarm)
        self._save_alarms()
        self._schedule_single_alarm(new_alarm) # Schedule immediately
        return alarm_id

    def cancel_alarm(self, alarm_id):
        initial_len = len(self.alarms)
        self.alarms = [alarm for alarm in self.alarms if alarm['id'] != alarm_id]
        if len(self.alarms) < initial_len:
            self._save_alarms()
            try:
                self.scheduler.remove_job(alarm_id)
                print(f"Cancelled scheduled job {alarm_id}")
            except Exception as e:
                print(f"Error removing job {alarm_id} from scheduler: {e}")
            return True
        return False

    def update_alarm(self, alarm_id, new_time=None, new_message=None, new_recurrence=None):
        for alarm in self.alarms:
            if alarm['id'] == alarm_id:
                if new_time: alarm['time'] = new_time
                if new_message: alarm['message'] = new_message
                if new_recurrence: alarm['recurrence'] = new_recurrence
                self._save_alarms()
                # Reschedule the updated alarm
                try:
                    self.scheduler.remove_job(alarm_id)
                except Exception as e:
                    print(f"Warning: could not remove old job {alarm_id} for update: {e}")
                self._schedule_single_alarm(alarm)
                return True
        return False

    def get_all_alarms(self):
        return self.alarms

    def trigger_alarm(self, alarm_id, message):
        print(f"!!! ALARM TRIGGERED !!! ID: {alarm_id}, Message: {message}")
        # In a full implementation, this would trigger TTS, UI notification, etc.
        # For one-time alarms, remove them after triggering
        alarm_to_remove = None
        for alarm in self.alarms:
            if alarm['id'] == alarm_id and not alarm['recurrence']:
                alarm_to_remove = alarm_id
                break
        if alarm_to_remove:
            self.cancel_alarm(alarm_to_remove)

    # check_and_trigger_alarms is no longer needed as APScheduler handles triggering.
    # However, for consistency with the original structure, if a method is needed for
    # external calls to check for alarms, it would interact with the scheduler directly.
    def check_and_trigger_alarms(self):
        print("Scheduler is actively managing alarms. This method is a placeholder.")
