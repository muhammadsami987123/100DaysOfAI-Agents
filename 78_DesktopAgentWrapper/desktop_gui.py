"""
Main Desktop GUI Framework for wrapping AI agents
"""

import os
import sys
import json
import logging
import threading
import time
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog

from config import Config

# Ensure log directory exists BEFORE configuring logging (important for packaged EXE)
try:
    Path(Config.LOGS_DIR).mkdir(parents=True, exist_ok=True)
except Exception:
    # As a last resort, fallback to current directory
    try:
        Path("logs").mkdir(parents=True, exist_ok=True)
        Config.LOGS_DIR = "logs"  # use fallback
    except Exception:
        pass

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(Config.LOGS_DIR, 'desktop_gui.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DesktopAgentWrapper:
    """Main wrapper class for creating desktop GUI applications for AI agents"""
    
    def __init__(self, 
                 agent_class: type,
                 agent_name: str,
                 description: str = "",
                 icon_path: Optional[str] = None,
                 ui_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the desktop agent wrapper
        
        Args:
            agent_class: The agent class to wrap
            agent_name: Display name for the agent
            description: Description of the agent
            icon_path: Path to agent icon
            ui_config: Custom UI configuration
        """
        self.agent_class = agent_class
        self.agent_name = agent_name
        self.description = description
        self.icon_path = icon_path
        self.ui_config = ui_config or {}
        
        # Initialize agent instance
        self.agent = None
        self.agent_config = {}
        
        # GUI components
        self.root = None
        self.main_frame = None
        self.sidebar = None
        self.content_frame = None
        self.status_bar = None
        
        # UI state
        self.current_theme = Config.DEFAULT_THEME
        self.session_data = {}
        self.history = []
        
        # Initialize configuration
        Config.validate()
        
    def _init_agent(self):
        """Initialize the agent instance"""
        try:
            self.agent = self.agent_class()
            self.agent_config = getattr(self.agent, 'get_ui_config', lambda: {})()
            logger.info(f"Initialized agent: {self.agent_name}")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            messagebox.showerror("Agent Error", f"Failed to initialize {self.agent_name}: {str(e)}")
            return False
        return True
    
    def _create_main_window(self):
        """Create the main application window"""
        # Set appearance mode and color theme
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title(f"{Config.APP_NAME} - {self.agent_name}")
        self.root.geometry(f"{Config.WINDOW_SIZE[0]}x{Config.WINDOW_SIZE[1]}")
        self.root.minsize(*Config.MIN_WINDOW_SIZE)
        
        # Set window icon if available
        if self.icon_path and os.path.exists(self.icon_path):
            try:
                self.root.iconbitmap(self.icon_path)
            except Exception as e:
                logger.warning(f"Could not set window icon: {e}")
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main layout
        self._create_sidebar()
        self._create_content_area()
        self._create_status_bar()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _create_sidebar(self):
        """Create the sidebar with agent information and controls"""
        self.sidebar = ctk.CTkFrame(self.root, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar.grid_propagate(False)
        
        # Agent info section
        info_frame = ctk.CTkFrame(self.sidebar)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Agent icon and name
        if self.icon_path and os.path.exists(self.icon_path):
            try:
                icon_image = Image.open(self.icon_path)
                icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_image)
                
                icon_label = ctk.CTkLabel(info_frame, image=icon_photo, text="")
                icon_label.image = icon_photo  # Keep a reference
                icon_label.pack(pady=10)
            except Exception as e:
                logger.warning(f"Could not load agent icon: {e}")
        
        # Agent name
        name_label = ctk.CTkLabel(
            info_frame, 
            text=self.agent_name,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        name_label.pack(pady=5)
        
        # Agent description
        if self.description:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=self.description,
                font=ctk.CTkFont(size=12),
                wraplength=200
            )
            desc_label.pack(pady=5)
        
        # Controls section
        controls_frame = ctk.CTkFrame(self.sidebar)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Theme toggle
        theme_label = ctk.CTkLabel(controls_frame, text="Theme:")
        theme_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.theme_var = ctk.StringVar(value=self.current_theme)
        theme_menu = ctk.CTkOptionMenu(
            controls_frame,
            values=["dark", "light"],
            variable=self.theme_var,
            command=self._change_theme
        )
        theme_menu.pack(fill="x", padx=10, pady=5)
        
        # Session controls
        session_label = ctk.CTkLabel(controls_frame, text="Session:")
        session_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        session_frame = ctk.CTkFrame(controls_frame)
        session_frame.pack(fill="x", padx=10, pady=5)
        
        save_btn = ctk.CTkButton(
            session_frame,
            text="Save Session",
            command=self._save_session,
            width=100
        )
        save_btn.pack(side="left", padx=5, pady=5)
        
        load_btn = ctk.CTkButton(
            session_frame,
            text="Load Session", 
            command=self._load_session,
            width=100
        )
        load_btn.pack(side="right", padx=5, pady=5)
        
        # History section
        history_frame = ctk.CTkFrame(self.sidebar)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        history_label = ctk.CTkLabel(history_frame, text="History:")
        history_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # History listbox
        self.history_listbox = tk.Listbox(
            history_frame,
            height=8,
            font=ctk.CTkFont(size=10)
        )
        self.history_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.history_listbox.bind("<Double-Button-1>", self._load_history_item)
        
        # Clear history button
        clear_history_btn = ctk.CTkButton(
            history_frame,
            text="Clear History",
            command=self._clear_history,
            width=100
        )
        clear_history_btn.pack(pady=5)
        
    def _create_content_area(self):
        """Create the main content area with input and output sections"""
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Input section
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="Input Parameters",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_label.pack(anchor="w", padx=10, pady=10)
        
        # Create input fields based on agent configuration
        self.input_widgets = {}
        self._create_input_fields(input_frame)
        
        # Action buttons
        button_frame = ctk.CTkFrame(input_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.process_btn = ctk.CTkButton(
            button_frame,
            text="Process",
            command=self._process_input,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.process_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self._clear_inputs,
            width=120,
            height=40
        )
        self.clear_btn.pack(side="left", padx=5)
        
        # Output section
        output_frame = ctk.CTkFrame(self.content_frame)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="Output",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        output_label.pack(anchor="w", padx=10, pady=10)
        
        # Output text area
        self.output_text = ctk.CTkTextbox(
            output_frame,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Output controls
        output_controls = ctk.CTkFrame(output_frame)
        output_controls.pack(fill="x", padx=10, pady=10)
        
        copy_btn = ctk.CTkButton(
            output_controls,
            text="Copy",
            command=self._copy_output,
            width=80
        )
        copy_btn.pack(side="left", padx=5)
        
        export_btn = ctk.CTkButton(
            output_controls,
            text="Export",
            command=self._export_output,
            width=80
        )
        export_btn.pack(side="left", padx=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(output_controls)
        self.progress_bar.pack(side="right", padx=5, fill="x", expand=True)
        self.progress_bar.set(0)
        
    def _create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_bar = ctk.CTkFrame(self.root, height=30)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Version info
        version_label = ctk.CTkLabel(
            self.status_bar,
            text=f"v{Config.APP_VERSION}",
            font=ctk.CTkFont(size=10)
        )
        version_label.pack(side="right", padx=10, pady=5)
        
    def _create_input_fields(self, parent):
        """Create input fields based on agent configuration"""
        if not self.agent_config.get("inputs"):
            # Default input field
            content_label = ctk.CTkLabel(parent, text="Content:")
            content_label.pack(anchor="w", padx=10, pady=5)
            
            self.input_widgets["content"] = ctk.CTkTextbox(
                parent,
                height=150,
                font=ctk.CTkFont(size=12)
            )
            self.input_widgets["content"].pack(fill="x", padx=10, pady=5)
            return
        
        # Create fields based on configuration
        for input_config in self.agent_config["inputs"]:
            field_name = input_config["name"]
            field_type = input_config["type"]
            field_label = input_config.get("label", field_name.title())
            
            # Field label
            label = ctk.CTkLabel(parent, text=f"{field_label}:")
            label.pack(anchor="w", padx=10, pady=5)
            
            # Create appropriate widget
            if field_type == "textarea":
                widget = ctk.CTkTextbox(
                    parent,
                    height=100,
                    font=ctk.CTkFont(size=12)
                )
            elif field_type == "dropdown":
                options = input_config.get("options", [])
                widget = ctk.CTkOptionMenu(
                    parent,
                    values=options,
                    width=200
                )
            elif field_type == "checkbox":
                widget = ctk.CTkCheckBox(
                    parent,
                    text=field_label
                )
            else:  # text input
                widget = ctk.CTkEntry(
                    parent,
                    width=300,
                    font=ctk.CTkFont(size=12)
                )
            
            widget.pack(fill="x" if field_type == "textarea" else None, padx=10, pady=5)
            self.input_widgets[field_name] = widget
    
    def _change_theme(self, theme):
        """Change the application theme"""
        self.current_theme = theme
        ctk.set_appearance_mode(theme)
        logger.info(f"Changed theme to: {theme}")
    
    def _process_input(self):
        """Process the input using the agent"""
        if not self.agent:
            messagebox.showerror("Error", "Agent not initialized")
            return
        
        # Get input values
        inputs = {}
        for field_name, widget in self.input_widgets.items():
            if isinstance(widget, ctk.CTkTextbox):
                inputs[field_name] = widget.get("1.0", "end-1c")
            elif isinstance(widget, ctk.CTkEntry):
                inputs[field_name] = widget.get()
            elif isinstance(widget, ctk.CTkOptionMenu):
                inputs[field_name] = widget.get()
            elif isinstance(widget, ctk.CTkCheckBox):
                inputs[field_name] = widget.get()
            else:
                inputs[field_name] = widget.get()
        
        # Update status
        self._update_status("Processing...")
        self.progress_bar.set(0.1)
        
        # Disable process button
        self.process_btn.configure(state="disabled")
        
        # Process in separate thread
        def process_thread():
            try:
                # Simulate progress
                for i in range(10):
                    time.sleep(0.1)
                    self.progress_bar.set(0.1 + (i * 0.08))
                
                # Call agent process method
                if hasattr(self.agent, 'process'):
                    result = self.agent.process(**inputs)
                elif hasattr(self.agent, 'rewrite_article'):
                    result = self.agent.rewrite_article(**inputs)
                elif hasattr(self.agent, 'generate_story'):
                    result = self.agent.generate_story(**inputs)
                else:
                    # Try to call the agent with inputs
                    result = self.agent(**inputs)
                
                # Update UI in main thread
                self.root.after(0, lambda: self._display_result(result))
                
            except Exception as e:
                logger.error(f"Processing error: {e}")
                self.root.after(0, lambda: self._display_error(str(e)))
        
        # Start processing thread
        thread = threading.Thread(target=process_thread)
        thread.daemon = True
        thread.start()
    
    def _display_result(self, result):
        """Display the processing result"""
        self.progress_bar.set(1.0)
        
        # Display result in output text area
        if isinstance(result, dict):
            if result.get("success", True):
                output_text = result.get("result", result.get("rewritten_content", str(result)))
            else:
                output_text = f"Error: {result.get('error', 'Unknown error')}"
        else:
            output_text = str(result)
        
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", output_text)
        
        # Add to history
        self._add_to_history(inputs, output_text)
        
        # Update status
        self._update_status("Completed")
        
        # Re-enable process button
        self.process_btn.configure(state="normal")
        
        # Reset progress bar
        self.root.after(2000, lambda: self.progress_bar.set(0))
    
    def _display_error(self, error_message):
        """Display error message"""
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", f"Error: {error_message}")
        
        self._update_status("Error")
        self.process_btn.configure(state="normal")
        self.progress_bar.set(0)
        
        messagebox.showerror("Processing Error", error_message)
    
    def _update_status(self, message):
        """Update status bar message"""
        self.status_label.configure(text=message)
        logger.info(f"Status: {message}")
    
    def _copy_output(self):
        """Copy output to clipboard"""
        output_text = self.output_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        self._update_status("Copied to clipboard")
    
    def _export_output(self):
        """Export output to file"""
        output_text = self.output_text.get("1.0", "end-1c")
        
        if not output_text.strip():
            messagebox.showwarning("Export", "No output to export")
            return
        
        # Ask user for file format
        file_types = [
            ("Text files", "*.txt"),
            ("JSON files", "*.json"),
            ("HTML files", "*.html"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Export Output",
            defaultextension=".txt",
            filetypes=file_types
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                self._update_status(f"Exported to {filename}")
                messagebox.showinfo("Export", f"Successfully exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def _clear_inputs(self):
        """Clear all input fields"""
        for widget in self.input_widgets.values():
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
            elif isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkCheckBox):
                widget.deselect()
    
    def _save_session(self):
        """Save current session"""
        session_data = {
            "agent_name": self.agent_name,
            "inputs": {},
            "output": self.output_text.get("1.0", "end-1c"),
            "timestamp": time.time()
        }
        
        # Save input values
        for field_name, widget in self.input_widgets.items():
            if isinstance(widget, ctk.CTkTextbox):
                session_data["inputs"][field_name] = widget.get("1.0", "end-1c")
            elif isinstance(widget, ctk.CTkEntry):
                session_data["inputs"][field_name] = widget.get()
            elif isinstance(widget, ctk.CTkOptionMenu):
                session_data["inputs"][field_name] = widget.get()
            elif isinstance(widget, ctk.CTkCheckBox):
                session_data["inputs"][field_name] = widget.get()
        
        # Save to file
        session_file = os.path.join(Config.SESSIONS_DIR, f"{self.agent_name}_{int(time.time())}.json")
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)
            self._update_status(f"Session saved: {session_file}")
            messagebox.showinfo("Session", "Session saved successfully")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save session: {str(e)}")
    
    def _load_session(self):
        """Load a saved session"""
        session_files = []
        for file in os.listdir(Config.SESSIONS_DIR):
            if file.endswith('.json') and self.agent_name in file:
                session_files.append(file)
        
        if not session_files:
            messagebox.showinfo("Load Session", "No saved sessions found")
            return
        
        # Show file selection dialog
        filename = filedialog.askopenfilename(
            title="Load Session",
            initialdir=Config.SESSIONS_DIR,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Load inputs
                for field_name, value in session_data.get("inputs", {}).items():
                    if field_name in self.input_widgets:
                        widget = self.input_widgets[field_name]
                        if isinstance(widget, ctk.CTkTextbox):
                            widget.delete("1.0", "end")
                            widget.insert("1.0", value)
                        elif isinstance(widget, ctk.CTkEntry):
                            widget.delete(0, "end")
                            widget.insert(0, value)
                        elif isinstance(widget, ctk.CTkOptionMenu):
                            widget.set(value)
                        elif isinstance(widget, ctk.CTkCheckBox):
                            if value:
                                widget.select()
                            else:
                                widget.deselect()
                
                # Load output
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", session_data.get("output", ""))
                
                self._update_status(f"Session loaded: {filename}")
                messagebox.showinfo("Load Session", "Session loaded successfully")
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load session: {str(e)}")
    
    def _add_to_history(self, inputs, output):
        """Add current session to history"""
        history_item = {
            "timestamp": time.time(),
            "inputs": inputs,
            "output": output[:100] + "..." if len(output) > 100 else output
        }
        self.history.append(history_item)
        
        # Update history listbox
        self.history_listbox.insert(0, f"{time.strftime('%H:%M:%S')} - {self.agent_name}")
        
        # Limit history size
        if len(self.history) > Config.UI_DEFAULTS["max_history_items"]:
            self.history.pop()
            self.history_listbox.delete(tk.END)
    
    def _load_history_item(self, event):
        """Load a history item"""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.history):
                history_item = self.history[index]
                
                # Load inputs
                for field_name, value in history_item["inputs"].items():
                    if field_name in self.input_widgets:
                        widget = self.input_widgets[field_name]
                        if isinstance(widget, ctk.CTkTextbox):
                            widget.delete("1.0", "end")
                            widget.insert("1.0", value)
                        elif isinstance(widget, ctk.CTkEntry):
                            widget.delete(0, "end")
                            widget.insert(0, value)
                
                # Load output
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", history_item["output"])
    
    def _clear_history(self):
        """Clear history"""
        self.history.clear()
        self.history_listbox.delete(0, tk.END)
        self._update_status("History cleared")
    
    def _on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    
    def run(self):
        """Run the desktop application"""
        try:
            # Initialize agent
            if not self._init_agent():
                return
            
            # Create main window
            self._create_main_window()
            
            # Start the application
            logger.info(f"Starting {Config.APP_NAME} for {self.agent_name}")
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Application error: {e}")
            messagebox.showerror("Application Error", f"Failed to start application: {str(e)}")
