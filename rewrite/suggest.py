import requests
import tkinter as tk
from tkinter import messagebox


# Sends current text to backend API and replaces it with suggested rewrite
def suggest_rewrite(text_area):
    original_text = text_area.get(1.0, tk.END).strip()
    if not original_text:
        messagebox.showinfo("Empty", "No text to analyze.")
        return
    
    try:
        response = requests.post("http://localhost:8000/suggest_rewrite", json={"text": original_text})
        if response.status_code == 200:
            revised_text = response.json().get("rewrite", "")
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, revised_text)
        else:
            messagebox.showerror("Error", f"Server returned {response.status_code}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))