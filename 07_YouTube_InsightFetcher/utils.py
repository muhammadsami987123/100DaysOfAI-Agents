import os
from colorama import init, Fore, Style
import pyperclip
import sys
import time
init(autoreset=True)

def print_colored(text, color, bright=False):
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }
    style = Style.BRIGHT if bright else Style.NORMAL
    print(f"{color_map.get(color, Fore.WHITE)}{style}{text}{Style.RESET_ALL}")

def save_to_file(output):
    folder = "summaries"
    if not os.path.exists(folder):
        os.makedirs(folder)
    fname = input("Enter filename to save (with .txt or .md extension): ").strip()
    if not fname:
        print_colored("Filename cannot be empty.", "red")
        return
    path = os.path.join(folder, fname)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(output)
        print_colored(f"Saved to {path}", "green")
    except Exception as e:
        print_colored(f"Failed to save file: {e}", "red")

def copy_to_clipboard(output):
    try:
        pyperclip.copy(output)
        # Verify by reading back
        if pyperclip.paste() == output:
            print_colored("Output copied to clipboard.", "green")
        else:
            print_colored("Tried to copy, but clipboard contents do not match.", "yellow")
    except Exception as e:
        print_colored(f"Could not copy to clipboard: {e}", "red")

def parse_time(t):
    if not t:
        return None
    parts = [int(p) for p in t.split(":")]
    if len(parts) == 2:
        return parts[0]*60 + parts[1]
    elif len(parts) == 3:
        return parts[0]*3600 + parts[1]*60 + parts[2]
    return None

def format_output(insights):
    buf = []
    buf.append("===== Key Actionable Takeaways =====\n")
    for t in insights.get("takeaways", []):
        sentiment = t.get('sentiment', 'Unknown')
        buf.append(f"- {t.get('text', str(t))} [{sentiment}]\n")
    buf.append("\n===== Memorable Quotes =====\n")
    for q in insights.get("quotes", []):
        buf.append(f"- {q}\n")
    buf.append("\n===== Important Statistics/Data Points =====\n")
    for s in insights.get("statistics", []):
        buf.append(f"- {s}\n")
    return "".join(buf)

def show_loading(message="Processing", duration=0):
    # duration=0 means indefinite until stopped by user logic
    spinner = ['|', '/', '-', '\\']
    idx = 0
    start = time.time()
    try:
        while duration == 0 or (time.time() - start < duration):
            sys.stdout.write(f"\r{message}... {spinner[idx % len(spinner)]}")
            sys.stdout.flush()
            time.sleep(0.2)
            idx += 1
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()
