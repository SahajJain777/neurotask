import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.constants import *
from vassist.assistant import VoiceAssistant
import speech_recognition as sr
import pyttsx3
import math
import time
import random
from neurotask.organizer import extension_based, timeline_based, semantic_based, intent_based
from neurotask.utils.config import load_config

class NeurotaskUI:
    def __init__(self, root, voice_enabled=True):
        self.root = root
        self.root.title("Neurotask")
        self.root.geometry("750x550")  # Increased height for voice assistant box
        self.root.minsize(650, 500)

        self.voice_enabled = voice_enabled
        self.voice_assistant = None
        self.setup_styles()
        self.setup_ui()

        if self.voice_enabled:
            self.setup_voice_assistant()

        self.center_window()

    def setup_voice_assistant(self):
        self.assistant = VoiceAssistant(self.root, self.update_voice_status, self.update_chat_display)

    def update_voice_status(self, state, message):
        if hasattr(self, 'voice_status_label'):
            self.voice_status_label.config(text=message)
            if state == "listening":
                self.voice_btn.config(text="🛑 Stop", style='Danger.TButton')
            else:
                self.voice_btn.config(text="🎙️ Start Voice Assistant", style='Primary.TButton')

    def update_chat_display(self, message, reset=False):
        if reset:
            self.chat_display.delete('1.0', END)
        self.chat_display.insert(END, message + '\n')
        self.chat_display.see(END)

    def toggle_voice(self):
        if self.voice_enabled:
            self.assistant.toggle_listening()
            
    def show_features(self):
        """Display available voice assistant commands in the chat display."""
        features = [
            "🔹 'Organize files by extension' - Organize files based on file type\n   Example: Documents in one folder, images in another, etc.",
            
            "🔹 'Organize files by timeline' - Organize files by creation date\n   Example: Files from 2023, 2022, etc. in separate folders",
            
            "🔹 'Organize files by semantics' - Use AI to organize files by content\n   Example: Groups files with similar content together regardless of file type",
            
            "🔹 'Organize files by intent' - Use AI to organize files by purpose\n   Example: Work files, personal projects, reference materials, etc.",
            
            "🔹 'Select directory [path]' - Choose a directory to organize\n   Example: 'Select directory Documents/Projects'",
            
            "🔹 'Show status' - Display current organization status\n   Example: Shows if organization is in progress or complete",
            
            "🔹 'Stop listening' - Turn off voice assistant\n   Example: Stops the assistant from listening for commands"
        ]
        
        self.update_chat_display("Available Voice Commands:", reset=True)
        for feature in features:
            self.update_chat_display(feature)
            self.update_chat_display("") # Add blank line between features for readability

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Custom colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"
        self.accent_color = "#4fc3f7"
        self.danger_color = "#dc3545"

        # Configure styles
        self.root.configure(bg=self.bg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=self.secondary_color)
        # Add a large title style
        self.style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground=self.secondary_color)
        self.style.configure('Primary.TButton', foreground='white', background=self.primary_color)
        self.style.configure('Danger.TButton', foreground='white', background=self.danger_color)
        self.style.map('Primary.TButton',
                      background=[('active', self.secondary_color), ('disabled', '#cccccc')])
        self.style.configure('TRadiobutton',
                           background=self.bg_color,
                           font=('Segoe UI', 9),
                           padding=(10, 5))

        # Progress bar style
        self.style.configure("Horizontal.TProgressbar",
                           thickness=20,
                           troughcolor='#e0e0e0',
                           background=self.accent_color)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def setup_ui(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # Simple large title label
        title_label = ttk.Label(
            header_frame,
            text="Neurotask",
            style='Title.TLabel'
        )
        title_label.pack(side=LEFT, pady=10)
        
        # Top-right buttons container
        self.top_right_frame = ttk.Frame(header_frame)
        self.top_right_frame.pack(side=RIGHT)

        # --- Voice Assistant Feature Box ---
        if self.voice_enabled:
            voice_frame = ttk.LabelFrame(main_frame, text=" NeuroTask Voice Assistant ", padding=15)
            voice_frame.pack(fill=X, pady=10)
            
            # Voice Assistant Controls
            control_frame = ttk.Frame(voice_frame)
            control_frame.pack(fill=X, pady=(0, 10))
            
            self.voice_btn = ttk.Button(
                control_frame,
                text="🎙️ Start Voice Assistant",
                command=self.toggle_voice,
                style='Primary.TButton'
            )
            self.voice_btn.pack(side=LEFT, padx=(0, 10))
            
            self.voice_status_label = ttk.Label(
                control_frame,
                text="Ready",
                style='TLabel'
            )
            self.voice_status_label.pack(side=LEFT)
            
            # Move Features button to right side
            right_controls = ttk.Frame(control_frame)
            right_controls.pack(side=RIGHT)
            
            self.features_btn = ttk.Button(
                right_controls,
                text="ℹ️ Features",
                command=self.show_features,
                style='Primary.TButton'
            )
            self.features_btn.pack(side=RIGHT)
            
            # Chat Display
            chat_frame = ttk.Frame(voice_frame)
            chat_frame.pack(fill=X, pady=(0, 10))
            
            self.chat_display = tk.Text(
                chat_frame,
                height=5,
                wrap=WORD,
                font=('Segoe UI', 9)
            )
            self.chat_display.pack(fill=X, expand=True)
        
        # --- File Organization Feature Box ---
        feature_frame = ttk.LabelFrame(main_frame, text=" File Organization ", padding=15)
        feature_frame.pack(fill=X, pady=10)
        
        # Directory Selection
        dir_frame = ttk.Frame(feature_frame)
        dir_frame.pack(fill=X, pady=(0, 15))
        
        ttk.Label(dir_frame, text="Directory to organize:").pack(side=LEFT, padx=(0, 10))
        
        self.dir_entry = ttk.Entry(dir_frame, font=('Segoe UI', 10))
        self.dir_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(dir_frame, 
                              text="Browse", 
                              command=self.browse_directory,
                              style='Primary.TButton')
        browse_btn.pack(side=RIGHT)
        
        # Organization Method
        method_frame = ttk.Frame(feature_frame)
        method_frame.pack(fill=X)
        
        ttk.Label(method_frame, text="Organization method:").pack(side=LEFT, padx=(0, 10))
        
        self.org_choice = tk.StringVar(value="extension")
        options = [
            ("Extension", "extension"),
            ("Timeline", "timeline"),
            ("Semantic (LLM)", "semantic"),
            ("Intent (LLM)", "intent")
        ]
        
        # Create radio buttons in a row
        for text, value in options:
            rb = ttk.Radiobutton(method_frame, 
                                text=text, 
                                variable=self.org_choice, 
                                value=value,
                                style='TRadiobutton')
            rb.pack(side=LEFT, padx=10)
        
        # --- Action Button ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=20)
        
        self.org_button = ttk.Button(btn_frame, 
                                   text="Organize Files", 
                                   command=self.run_organization,
                                   style='Primary.TButton')
        self.org_button.pack(fill=X, ipady=8)
        
        # --- Status and Progress ---
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=X, pady=(15, 0))
        
        self.status_label = ttk.Label(status_frame, 
                                    text="Status: Ready", 
                                    anchor="w",
                                    style='TLabel')
        self.status_label.pack(side=LEFT, fill=X, expand=True)
        
        self.progress = ttk.Progressbar(status_frame, 
                                      style="Horizontal.TProgressbar",
                                      mode="indeterminate")
        self.progress.pack(fill=X, pady=5)

    def browse_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.dir_entry.delete(0, END)
            self.dir_entry.insert(0, path)

    def run_organization(self):
        directory = self.dir_entry.get().strip()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        # Update UI
        self.status_label.config(text="Status: Organizing files...")
        self.progress.start(10)
        self.org_button.config(state=DISABLED)

        # Launch in separate thread
        thread = threading.Thread(target=self.organize_files, args=(directory,), daemon=True)
        thread.start()

    def organize_files(self, directory):
        try:
            org_type = self.org_choice.get()
            print(f"[DEBUG] Starting organization with type: {org_type}")
            print(f"[DEBUG] Directory: {directory}")

            if org_type == "extension":
                print("[DEBUG] Running extension-based organizer")
                config = load_config()
                extension_based.organize_by_extension(directory, config["file_categories"])
            elif org_type == "timeline":
                print("[DEBUG] Running timeline-based organizer")
                timeline_based.organize_by_timeline(directory)
            elif org_type == "semantic":
                print("[DEBUG] Running semantic-based organizer")
                semantic_based.organize_by_semantics(directory)
            elif org_type == "intent":
                print("[DEBUG] Running intent-based organizer")
                intent_based.organize_by_intents(directory)

            print("[DEBUG] Organization completed successfully")
            self.root.after(0, self.organization_complete)
        except Exception as e:
            print(f"[DEBUG] Error during organization: {str(e)}")
            import traceback
            traceback.print_exc()
            self.root.after(0, self.organization_failed, str(e))

    def organization_complete(self):
        self.progress.stop()
        self.org_button.config(state=NORMAL)
        self.status_label.config(text="Status: Organization complete!")
        messagebox.showinfo("Success", "File organization completed successfully!")

    def organization_failed(self, error):
        self.progress.stop()
        self.org_button.config(state=NORMAL)
        self.status_label.config(text=f"Status: Error - {error[:30]}...")
        messagebox.showerror("Error", f"An error occurred:\n{error}")

def main():
    root = tk.Tk()

    # Set Windows title bar icon if available
    try:
        root.iconbitmap('assets/icon.ico')  # Provide your icon file
    except:
        pass

    app = NeurotaskUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()