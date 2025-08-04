import tkinter as tk
from tkinter import ttk
import threading
import time
from voice import listen_and_respond

class JarvisUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis File Manager - Voice Assistant")
        self.root.geometry("600x400")
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window()
        
        # Configure style
        self.setup_styles()
        
        # Create UI elements
        self.create_widgets()
        
        # State variables
        self.is_listening = True
        self.command_history = []
        
        # Start automatic listening
        self.start_automatic_listening()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure modern styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 24, 'bold'))
        
        style.configure('Status.TLabel', 
                       background='#2c3e50', 
                       foreground='#3498db', 
                       font=('Arial', 14))
        
        style.configure('History.TLabel', 
                       background='#34495e', 
                       foreground='#bdc3c7', 
                       font=('Arial', 10))
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🎤 Jarvis File Manager", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill='x', pady=10)
        
        # Status indicator with animation
        self.status_label = ttk.Label(status_frame, 
                                     text="🎧 Listening...", 
                                     style='Status.TLabel')
        self.status_label.pack()
        
        # Listening indicator
        self.listening_indicator = tk.Label(status_frame,
                                           text="🔴",
                                           bg='#2c3e50',
                                           fg='#e74c3c',
                                           font=('Arial', 20))
        self.listening_indicator.pack(pady=5)
        
        # Current command display
        command_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        command_frame.pack(fill='x', pady=10)
        
        tk.Label(command_frame, 
                text="Last Command:", 
                bg='#34495e', 
                fg='#ecf0f1', 
                font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.command_label = tk.Label(command_frame,
                                     text="Waiting for voice command...",
                                     bg='#34495e',
                                     fg='#bdc3c7',
                                     font=('Arial', 11),
                                     wraplength=550)
        self.command_label.pack(anchor='w', padx=10, pady=(0, 10))
        
        # Command history
        history_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        history_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(history_frame,
                text="Command History:",
                bg='#34495e',
                fg='#ecf0f1',
                font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        
        # Scrollable history
        history_container = tk.Frame(history_frame, bg='#34495e')
        history_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.history_text = tk.Text(history_container,
                                   bg='#2c3e50',
                                   fg='#ecf0f1',
                                   font=('Arial', 10),
                                   height=6,
                                   wrap='word',
                                   state='disabled')
        
        scrollbar = tk.Scrollbar(history_container, orient='vertical', command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Instructions
        instructions = tk.Label(main_frame,
                               text="💡 Just speak naturally: 'Open Notepad', 'Create folder', 'Go to Downloads'",
                               bg='#2c3e50',
                               fg='#95a5a6',
                               font=('Arial', 10, 'italic'))
        instructions.pack(pady=10)
    
    def start_automatic_listening(self):
        """Start automatic continuous listening"""
        threading.Thread(target=self.continuous_listen_loop, daemon=True).start()
        self.animate_listening_indicator()
    
    def animate_listening_indicator(self):
        """Animate the listening indicator"""
        if self.is_listening:
            current_color = self.listening_indicator.cget('fg')
            new_color = '#e74c3c' if current_color == '#95a5a6' else '#95a5a6'
            self.listening_indicator.config(fg=new_color)
            self.root.after(500, self.animate_listening_indicator)
    
    def continuous_listen_loop(self):
        """Continuous listening loop"""
        while self.is_listening:
            try:
                # Update status to listening
                self.root.after(0, lambda: self.status_label.config(text="🎧 Listening..."))
                
                # Listen for command
                command_text = listen_and_respond(listen_only=True)
                
                if command_text:
                    # Update UI in main thread
                    self.root.after(0, self.process_command, command_text)
                    
                    # Brief pause after processing
                    time.sleep(1)
                else:
                    # Brief pause before trying again
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error in listening: {e}")
                time.sleep(1)
    
    def process_command(self, command_text):
        """Process the voice command"""
        # Update command display
        self.command_label.config(text=command_text)
        
        # Update status
        self.status_label.config(text="⚙️ Processing command...")
        self.root.update()
        
        try:
            # Process the command
            response = listen_and_respond(command_text=command_text)
            
            # Update status with result
            self.status_label.config(text="✅ Command completed")
            
            # Add to history
            self.add_to_history(command_text, response)
            
            # Reset status after 2 seconds
            self.root.after(2000, lambda: self.status_label.config(text="🎧 Listening..."))
            
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}")
            self.add_to_history(command_text, f"Error: {str(e)}")
            
            # Reset status after 3 seconds
            self.root.after(3000, lambda: self.status_label.config(text="🎧 Listening..."))
    
    def add_to_history(self, command, response):
        """Add command and response to history"""
        timestamp = time.strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {command}\n   → {response}\n\n"
        
        self.command_history.append(history_entry)
        
        # Keep only last 10 entries
        if len(self.command_history) > 10:
            self.command_history.pop(0)
        
        # Update history display
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(1.0, ''.join(self.command_history))
        self.history_text.config(state='disabled')
        self.history_text.see(tk.END)
    
    def run(self):
        """Start the UI"""
        self.root.mainloop()

def start_ui():
    """Start the Jarvis UI"""
    app = JarvisUI()
    app.run()

if __name__ == "__main__":
    start_ui()