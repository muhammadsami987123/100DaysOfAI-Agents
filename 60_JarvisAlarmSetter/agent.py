import re
from datetime import datetime, timedelta
from alarm_manager import AlarmManager
from tts_service import TTSService

class JarvisAlarmSetter:
    def __init__(self, tts_service: TTSService, alarm_manager: AlarmManager):
        self.tts = tts_service
        self.alarm_manager = alarm_manager

    def process_command(self, command: str):
        command = command.lower()
        response = ""

        if "set an alarm" in command or "remind me" in command:
            response = self._handle_set_alarm(command)
        elif "cancel the alarm" in command or "delete the alarm" in command:
            response = self._handle_cancel_alarm(command)
        elif "what are my alarms" in command or "list alarms" in command:
            response = self._handle_list_alarms()
        else:
            response = "I'm sorry, I didn't understand that command. Please try again."

        self.tts.speak(response)

    def _handle_set_alarm(self, command: str) -> str:
        # Example NLU: "set an alarm for 6 AM tomorrow"
        # "remind me in 25 minutes"
        # "set an alarm for every Monday at 7 PM"

        time_match = re.search(r'for (\d{1,2}(?:\s?[ap]m)?(?:\s?tomorrow)?)', command)
        minute_match = re.search(r'in (\d+)\s?minute', command)
        hour_match = re.search(r'in (\d+)\s?hour', command)
        recurrence_match = re.search(r'every (monday|tuesday|wednesday|thursday|friday|saturday|sunday)', command)

        time_str = None
        message = "Your alarm"
        recurrence = None
        alarm_time = None

        if time_match:
            time_str = time_match.group(1).strip()
            # Further parsing for time_str (e.g., "6 AM tomorrow" -> actual datetime object)
            # For now, let's assume time_str is in a simple format like "6 AM"
            message = f"Alarm for {time_str}"

        elif minute_match:
            minutes = int(minute_match.group(1))
            alarm_time = datetime.now() + timedelta(minutes=minutes)
            time_str = alarm_time.strftime("%I:%M %p")
            message = f"Reminder in {minutes} minutes"

        elif hour_match:
            hours = int(hour_match.group(1))
            alarm_time = datetime.now() + timedelta(hours=hours)
            time_str = alarm_time.strftime("%I:%M %p")
            message = f"Reminder in {hours} hours"

        if recurrence_match:
            recurrence = recurrence_match.group(1)
            message += f" every {recurrence}"

        if time_str:
            # Need to implement proper datetime parsing and conversion
            # For now, just add a placeholder
            alarm_id = self.alarm_manager.add_alarm(time_str, message, recurrence)
            if alarm_id:
                return f"{message} has been set."
            else:
                return "Failed to set alarm."
        else:
            return "I couldn't understand the time for the alarm."

    def _handle_cancel_alarm(self, command: str) -> str:
        # Example: "cancel the 3 PM alarm"
        alarm_id_match = re.search(r'(\d{1,2}(?:\s?[ap]m)?)', command)
        if alarm_id_match:
            alarm_time_str = alarm_id_match.group(1)
            # In a real scenario, you'd need to match this to an actual alarm ID
            # For simplicity, let's assume we can find an alarm by its time string
            # This needs to be improved to actually get the alarm_id.
            # For now, a placeholder:
            return "Cancelling alarms by time is not yet fully implemented. Please use the UI."
        else:
            return "I need an alarm identifier to cancel. For example, 'cancel the 3 PM alarm'."

    def _handle_list_alarms(self) -> str:
        alarms = self.alarm_manager.get_all_alarms()
        if not alarms:
            return "You have no active alarms."
        else:
            alarm_list_str = ", ".join([f"{alarm['message']} at {alarm['time']}" for alarm in alarms])
            return f"You have the following alarms: {alarm_list_str}."
