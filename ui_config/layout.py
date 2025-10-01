import tkinter as tk

def apply_theme(root, mode="light"):
    if mode == "dark":
        root.configure(bg="#2e2e2e")
    else:
        root.configure(bg="#f0f0f0")

def add_padding(widget, padx=10, pady=10):
    widget.pack_configure(padx=padx, pady=pady)

def set_default_font(widget, font_name="Georgia", font_size=12):
    widget.configure(font=(font_name, font_size))