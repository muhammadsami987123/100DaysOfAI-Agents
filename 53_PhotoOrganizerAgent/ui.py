import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from core.organizer import PhotoOrganizer

class PhotoOrganizerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Organizer Agent")
        self.root.geometry("500x350")
        self.root.configure(bg='#2c3e50')
        self.setup_styles()
        self.create_widgets()
        self.selected_folder = ''

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2c3e50', foreground='#ecf0f1', font=('Arial', 12))
        style.configure('Header.TLabel', background='#2c3e50', foreground='#00b894', font=('Arial', 18, 'bold'))
        style.configure('TButton', font=('Arial', 11))
        style.configure('TFrame', background='#2c3e50')

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill='both', expand=True, padx=30, pady=30)

        ttk.Label(frame, text="📸 Photo Organizer Agent", style='Header.TLabel').pack(pady=(0, 20))

        folder_frame = ttk.Frame(frame)
        folder_frame.pack(fill='x', pady=10)
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=35, state='readonly')
        folder_entry.pack(side='left', padx=(0, 10))
        ttk.Button(folder_frame, text="Select Folder", command=self.select_folder).pack(side='left')

        mode_frame = ttk.Frame(frame)
        mode_frame.pack(fill='x', pady=10)
        ttk.Label(mode_frame, text="Organize by:").pack(side='left', padx=(0, 10))
        self.mode_var = tk.StringVar(value='face')
        ttk.Radiobutton(mode_frame, text='Face', variable=self.mode_var, value='face').pack(side='left')
        ttk.Radiobutton(mode_frame, text='Location', variable=self.mode_var, value='location').pack(side='left')

        ttk.Button(frame, text="Organize Photos", command=self.start_organize).pack(pady=20)

        self.status_label = ttk.Label(frame, text="Status: Waiting", font=('Arial', 11))
        self.status_label.pack(pady=10)

        self.result_text = tk.Text(frame, height=6, bg='#34495e', fg='#ecf0f1', font=('Arial', 10), state='disabled')
        self.result_text.pack(fill='both', expand=True, pady=(10, 0))

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.selected_folder = folder

    def start_organize(self):
        if not self.selected_folder:
            messagebox.showwarning("No Folder", "Please select a folder containing photos.")
            return
        self.status_label.config(text="Status: Organizing...")
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state='disabled')
        threading.Thread(target=self.organize_photos, daemon=True).start()

    def organize_photos(self):
        mode = self.mode_var.get()
        organizer = PhotoOrganizer(mode)
        moved = []
        def log(msg):
            self.result_text.config(state='normal')
            self.result_text.insert(tk.END, msg + '\n')
            self.result_text.config(state='disabled')
            self.result_text.see(tk.END)
        try:
            for filename in os.listdir(self.selected_folder):
                if any(filename.lower().endswith(ext) for ext in organizer.CONFIG.PHOTO_EXTENSIONS):
                    photo_path = os.path.join(self.selected_folder, filename)
                    detected = organizer.mock_detect(photo_path)
                    target_folder = os.path.join(self.selected_folder, detected)
                    os.makedirs(target_folder, exist_ok=True)
                    new_path = os.path.join(target_folder, filename)
                    os.rename(photo_path, new_path)
                    log(f"Moved {filename} to {detected}/")
                    moved.append(filename)
            self.status_label.config(text=f"Status: Done. {len(moved)} photo(s) organized.")
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {e}")
            log(f"Error: {e}")

    def run(self):
        self.root.mainloop()

def start_ui():
    app = PhotoOrganizerUI()
    app.run()

if __name__ == "__main__":
    start_ui()
