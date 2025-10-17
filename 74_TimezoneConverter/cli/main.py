import sys
from factory import get_agent

def main():
    agent = get_agent()
    print("\nTimezoneConverter CLI Agent — #100DaysOfAI-Agents (Day 74)")
    print("Type your time conversion request. Ctrl+C or Ctrl+D to quit.\n")
    while True:
        try:
            user_input = input("→ ")
            if not user_input.strip():
                continue
            parsed = agent.parse_user_input(user_input)
            result = agent.perform_timezone_conversion(parsed)
            print("\nConverted Time:")
            print(agent.format_output(result))
            agent.log_conversion(user_input, result)
            print()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(agent.handle_error(e))

if __name__ == "__main__":
    main()
