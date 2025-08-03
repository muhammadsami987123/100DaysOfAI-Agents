import tkinter as tk
from voice import listen_and_respond

def start_ui():
    root = tk.Tk()
    root.title("Jarvis File Manager")
    root.geometry("400x200")

    status = tk.Label(root, text="Ready", font=("Arial", 16))
    status.pack(padx=20, pady=10)

    last_command_label = tk.Label(root, text="Last command: ", font=("Arial", 12), fg="gray")
    last_command_label.pack(padx=20, pady=5)

    def handle_command():
        status.config(text="Listening...", fg="blue")
        root.update()
        # Listen for voice input only
        command_text = listen_and_respond(listen_only=True)
        if command_text:
            last_command_label.config(text=f"Last command: {command_text}", fg="gray")
            status.config(text="Processing...", fg="orange")
            root.update()
            # Now process the command
            result = listen_and_respond(command_text=command_text)
            status.config(text=result, fg="green")
        else:
            status.config(text="Didn't catch that. Try again.", fg="red")
        # Automatically listen again after a short delay
        root.after(2000, handle_command)

    root.after(1000, handle_command)
    root.mainloop()