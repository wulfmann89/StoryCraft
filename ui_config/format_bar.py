
        # format_bar.py
import tkinter as tk
from tkinter import font, messagebox

# Define a list of royalty-free fonts (safe for commercial use)

SAFE_FONTS = [
    "Arial", "Courier New", "Georgia", "Verdana", "Tahoma", "Trebuchet MS", "Helvetica"
]

def build_format_bar(root, text_area):
        
        format_bar = tk.Frame(root)
        format_bar.pack(fill='x')

        # Font dropdown

        font_var = tk.StringVar(value=SAFE_FONTS[0])
        font_menu = tk.OptionMenu(format_bar, font_var, *SAFE_FONTS, command=lambda f: apply_font(text_area, f))
        font_menu.pack(side='left', padx=2, pady=2)

        # Bold Button

        bold_btn = tk.Button(format_bar, text="Bold", command=toggle_tag(text_area, "bold", ("Helvetica", 12, "bold")))
        bold_btn.pack(side='left', padx=2, pady=2)

        # Italic Button

        italic_btn = tk.Button(format_bar, text="Italic", command=toggle_tag(text_area, "italic", ("Helvetica", 12, "italic")))
        italic_btn.pack(side='left', padx=2, pady=2)

        # Underline Button

        underline_btn = tk.Button(format_bar, text="Underline", command=toggle_tag(text_area, "underline", ("Helvetica", 12, "underline")))
        underline_btn.pack(side='left', padx=2, pady=2)

def toggle_tag(text_area, tag_name, font_style):
    try:
        current_tags = text_area.tag_names("sel.first")
        if tag_name in current_tags:
            text_area.tag_remove(tag_name, "sel.first", "sel.last")
        else:
            text_area.tag_add(tag_name, "sel.first", "sel.last")
            text_area.tag_config(tag_name, font=font_style)
    except tk.TclError:
        pass # No selection

def apply_font(text_area, font_name):
    try: 
        text_area.tag_add("custom_font", "sel.first", "sel.last")
        text_area.tag_config("custom_font", font=(font_name, 12))
    except tk.TclError:
        pass