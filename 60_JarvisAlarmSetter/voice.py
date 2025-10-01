from agent import JarvisAlarmSetter
from stt_service import STTService
from tts_service import TTSService
from alarm_manager import AlarmManager
from config import Config

def main():
    stt = STTService()
    tts = TTSService()
    alarm_manager = AlarmManager(Config.ALARM_FILE)
    agent = JarvisAlarmSetter(tts, alarm_manager)

    while True:
        command = stt.listen()
        if command:
            agent.process_command(command)

if __name__ == '__main__':
    main()
