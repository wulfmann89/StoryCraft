import tkinter as tk
import threading
from tkinter import filedialog, messagebox, scrolledtext
from rewrite.suggest import suggest_rewrite
from entity_highlighter.highlight import highlight_entities
import spacy
from ui_config.format_bar import build_format_bar
from ui_config.layout import apply_theme, add_padding, set_default_font
from appearance.dictionary.dictionary import show_definition, lookup_word
from entity_rec_profiler.entity_recognition import extract_entities
from entity_rec_profiler.profile_generator import generate_profile
from entity_rec_profiler.timeline_inference import extract_explicit_dates, infer_sequence
from continuity_engine.timeline_inference import extract_explicit_dates, infer_sequence
from continuity_engine.fantasy_calendar import FantasyCalendar
from continuity_engine.consistency_checker import check_consistency
from continuity_engine.universe_tagger import tag_entity
import json
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, END
LOG_PATH = "logs/focus_sessions.json"

class WordProcessor:                                                                                                   # A simple word processor application
    def __init__(self, root):
        self.root = root

        apply_theme(self.root, mode = "dark")  # Apply dark theme
        
        self.root.title("Simple Word Processor")
        self.root.geometry("600x400")
        self.real_time_profiling_enabled = False

        # Create a text area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True)                                 # Text area with scroll                     
        self.text_area.pack(expand=True, fill='both')                                                                  # Expand to fill window
        self.text_area.bind("<<Modified>>", self.on_text_modified)                                                     # Bind modification event
        self.timer_canvas = tk.Canvas(self.root, width=100, height=100, bg="#1e1e1e", highlightthickness=0)          # Timer canvas
        self.timer_canvas.place(x=10, y=10)                                                                            # Position timer canvas, adjust as needed

        add_padding(self.text_area, padx=15, pady=15)                                                                  # Add padding

        set_default_font(self.text_area, font_name="Georgia", font_size=14)                                            # Set default font
        
        # Focus Mode
        self.focus_mode_active = False
        self.focus_timer_duration = 20 * 60                                                                            # 20 minutes in seconds

        self.focus_timer_remaining = self.focus_timer_duration
        self.focus_timer_id = None

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)                                                                             # Menu bar
        self.root.config(menu=self.menu_bar)
        
        # Add File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)                                                             # File operations
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)                                                   # New file, Open, Save
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Highlight Entities", command=lambda: highlight_entities(self.text_area))     # Highlight entities
        self.file_menu.add_command(label="Suggest Rewrite", command=lambda: suggest_rewrite(self.text_area))           # Suggest rewrite
        self.file_menu.add_command(label="Lookup Word", command=self.lookup_selected_word)                             # Lookup selected word
        self.file_menu.add_separator()
        self.analyze_menu = tk.Menu(self.file_menu, tearoff=0)                                                         # Entity analysis options
        self.analyze_menu.add_command(label="Run Once", command=self.analyze_entities)                                 # Analyze entities once
        self.analyze_menu.add_command(label="Toggle Real-Time Profiling", command=self.toggle_real_time_profiling)     # Toggle real-time profiling
        self.file_menu.add_cascade(label="Analyze Entities", menu=self.analyze_menu)
        self.file_menu.add_command(label="Exit", command=self.exit_application)                                        # Exit application
        
        # Add Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)                                                             # Edit operations including Undo/Redo
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)

        # Add View Menu

        # Focus Mode Menu
        self.focus_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.focus_menu.add_command(label="Start Focus Session", command=self.start_focus_session)                       # Start/Stop Focus Timer
        self.focus_menu.add_command(label="Stop Focus Session", command=self.stop_focus_session)                         # Stop Focus Timer
        self.focus_menu.add_command(label="Customize Duration", command=self.customize_focus_duration)                 # Customize Focus Duration
        self.focus_menu.add_command(label="ViewSessionLog", command=self.view_focus_log)                               # View Focus Session Log
        self.menu_bar.add_cascade(label="Focus Mode", menu = self.focus_menu)

        build_format_bar(self.root, self.text_area)                                                                    # Formatting options

        # Sidebar for definitions
        self.sidebar = tk.Text(self.root, width=30, bg="#f9f9f9", wrap=tk.WORD)                                      # Sidebar for dictionary
        self.sidebar.pack(side="right", fill="y")                                                                      # Sidebar on the right
        self.sidebar.insert(tk.END, "Dictionary results will appear here.")                                            # Initial message
        self.sidebar.bind("<Button-1>", lambda event: self.lookup_selected_word())                                     # Lookup on click
        self.sidebar.config(state="disabled")                                                                          # Make sidebar read-only

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Real-Time Profiling: OFF", anchor='w', bg="#eaeaea", relief="sunken")    # Status bar at the bottom
        self.status_bar.pack(side="bottom", fill="x")

    def on_text_modified(self, event=None):
        if self.real_time_profiling_enabled:
            self.text_area.edit_modified(False)                                                                        # Reset modified flag

            if hasattr(self, "_profiling_timer"):
                 self.root.after_cancel(self._profiling_timer)                                                         # Cancel previous timer
            self._profiling_timer = self.root.after(2000, self.run_entity_profiling)                                   # Delay profiling by 2 seconds

    def run_entity_profiling(self):
         self.status_bar.config(text="Profiling entities...")                                                          # Update status
         threading.Thread(target=self.analyze_entities).start()                                                        # Run entity profiling in a separate thread

    def _threaded_entity_analysis(self):
        self.analyze_entities()
        self.status_bar.config(text=f"Real-Time Profiling: {'ON' if self.real_time_profiling_enabled else 'OFF'}")     # Reset status

    def new_file(self):                                                                                                # Clear text area for new file
        self.text_area.delete(1.0, tk.END)                                                                             # Clear text area

    def open_file(self):                                                                                               # Open a text file
        file_path= filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"),
                                                         ("All files", "*.*")])
        if file_path:
            self.text_area.delete(1.0, tk.END)                                                                         # Clear current text
            with open(file_path, "r") as file: 
                                self.text_area.insert(tk.END, file.read())

    def save_file(self):                                                                                               # Save current text to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                 file.write(self.text_area.get(1.0, tk.END))

    def exit_application(self):                                                                                        # Confirm before exiting
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
             self.root.destroy()

    def lookup_selected_word(self):
        try:
                selected_text = self.text_area.get("sel.first", "sel.last").strip()                                    # Get selected text
                if selected_text:
                    definition, synonyms = lookup_word(selected_text)                                                  # Lookup definition and synonyms
                    self.sidebar.config(state="normal")                                                                # Enable editing
                    self.sidebar.delete(1.0, tk.END)                                                                   # Clear previous content
                    self.sidebar.insert(tk.END, f"{selected_text}\n\nDefinition:\n{definition}\n\nSynonyms:\n{', '.join(synonyms) if synonyms else 'None'}") # Display definition and synonyms
                    self.sidebar.config(state="disabled")                                                              # Disable editing
                else:
                    self.sidebar.config(state="normal")                                                                # Enable editing
                    self.sidebar.delete(1.0, tk.END)                                                                   # Clear previous content
                    self.sidebar.insert(tk.END, "Please select a word to look up.")                                    # Prompt to select a word
                    self.sidebar.config(state="disabled")                                                              # Disable editing
        except tk.TclError:
            pass  # No text selected, ignore

    def _format_profile_block(self, profile):
         lines = [
             f"Name: {profile['name']}",
             f"Type: {profile['type']}",
             f"Roles: {', '.join(profile['roles'])}",
             f"Traits: {', '.join(profile['traits'])}",
             f"Tone: {profile['emotional_tone']}",
             "-" * 40
         ]
         return "\n".join(lines)

    def analyze_entities(self):
         text = self.text_area.get(1.0, tk.END)
         entities = extract_entities(text)
         profiles = [generate_profile(ent) for ent in entities]
         self.entity_profiles = profiles                                                                            # Store profiles for potential future use

         self.sidebar.config(state="normal")
         self.sidebar.delete(1.0, tk.END)

         if not profiles:
             self.sidebar.insert(tk.END, "No entities found.\n")
         else:
             for profile in profiles:
                 block = self._format_profile_block(profile)
                 self.sidebar.insert(tk.END, block + "\n\n")

         self.sidebar.config(state="disabled")

    def toggle_real_time_profiling(self):                                                                             # Toggle real-time entity profiling
        self.real_time_profiling_enabled = not self.real_time_profiling_enabled
        state = "enabled" if self.real_time_profiling_enabled else "disabled"
        self.status_bar.config(text=f"Real-Time Profiling: {'ON' if self.real_time_profiling_enabled else 'OFF'}")
        messagebox.showinfo("Real-Time Profiling", f"Real-time entity profiling {state}.")

    def start_focus_session(self):
        from datetime import datetime
        self.focus_mode_active = True
        self.focus_timer_remaining = self.focus_timer_duration
        self.real_time_profiling_enabled = False
        self.update_focus_timer()
        self.focus_session_start = datetime.now()

    def update_focus_timer(self):
        from focus_mode.session_logger import log_session
        from datetime import datetime
        from reminders.break_reminder import show_break_reminder
        self.timer_canvas.delete("all")
        angle = (self.focus_timer_remaining / self.focus_timer_duration) * 360
        color = "#00cc99" if self.focus_timer_remaining > 60 else "#ff6600"  # Calm to urgent
        self.timer_canvas.create_arc(10, 10, 90, 90, start=90, extent=-angle, fill=color, outline="")
        mins, secs = divmod(self.focus_timer_remaining, 60)
        self.timer_canvas.create_text(50, 50, text=f"{mins:02d}:{secs:02d}", fill="white", font=("Helvetica", 12))
        if self.focus_timer_remaining > 0:
            self.focus_timer_remaining -= 1
            self.focus_timer_id = self.root.after(1000, self.update_focus_timer)
        else:
            self.focus_mode_active = False
            self.timer_canvas.create_text(50, 50, text="Done!", fill="white", font=("Helvetica", 12))
            log_session(self.focus_session_start, datetime.now(), interrupted=False)
            show_break_reminder()

    def stop_focus_session(self):                                                                                      # Stop focus session and log
        from focus_mode.session_logger import log_session
        from datetime import datetime
        from focus_mode.tone_snapshot import analyze_tone
        session_text = self.text_area.get("1.0", "end-1c")                                                             # Get all text
        tone_result = analyze_tone(session_text)                                                                       # Analyze tone
        print("Tone Snapshot:", tone_result)                                                                           # Log tone result (for demo, print to console)
        if self.focus_timer_id:
            self.root.after_cancel(self.focus_timer_id)                                                                # Cancel timer
            self.focus_timer_id = None                                                                                 # Reset timer ID
        self.focus_mode_active = False                                                                                 # Reset focus mode
        self.timer_canvas.delete("all")                                                                                # Clear timer display
        if hasattr(self, "focus_session_start"):                                                                       # Log session if it was started
            log_session(self.focus_session_start, datetime.now(), interrupted=True)
        self.text_area.delete("1.0", "end")                                                                            # Clear text area

    def customize_focus_duration(self):
        # Optional: use a dialog to set duration
        pass

    def view_focus_log(self):
        log_window = Toplevel(self.root)
        log_window.title("Focus Session Log")
        log_window.geometry("400x300")
        text = Text(log_window, wrap="word")
        scrollbar = Scrollbar(log_window, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        try:
             with open(LOG_PATH, "r") as f:
                  sessions = json.load(f)
                  for s in sessions:
                       text.insert(END, F"Start: {s['start']}\nEND: {s['end']}\nDuration: {s['duration_minutes']} min\nInterrupted: {s['interrupted']}\n\n")
        except Exception as e:
            text.insert(END, f"Error loading log: {e}")
        
    def update_entity_timeline(self):
         timeline = extract_explicit_dates(self.entity_profiles)
         self.entity_timeline = timeline

    def update_scene_timeline(self):
         text = self.text_area.get("1.0", "end-1c")
         calendar = FantasyCalendar(self.user_calendar_config)
         explicit = extract_explicit_dates(text, calendar)
         inferred = infer_sequence(text)
         self.timeline_events = explicit + inferred

    def run_consistency_checks(self):
         issues = check_consistency(self.entity_profiles, self.timeline_events)
         self.display_continuity_alerts(issues)

    def tag_entity_scope(self, entity_id, scope):
         tag = tag_entity(entity_id, scope)
         self.entity_profiles[entity_id]["scope"] = tag["scope"]

if __name__ == "__main__":                                                                                             # Run the application
    root = tk.Tk()
    app = WordProcessor(root)
    root.mainloop()