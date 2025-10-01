import spacy
import tkinter as tk
from tkinter import font

#Load SpaCy model for entity recognition
nlp = spacy.load("en_core_web_sm")

# Highlights named entities in the given text area
def highlight_entities(self):
    self.text_area.tag_remove("entity", "1.0", tk.END)                          # Clear previous highlights
    text = self.text_area.get("1.0", tk.END)                                    # Get all text from the text area
    doc = self.nlp(text)                                                        # Process text with SpaCy   

    for ent in doc.ents:
        start = f"1.0 + {ent.start_char} chars"                                 # Calculate start and end positions
        end = f"1.0 + {ent.end_char} chars" 
        self.text_area.tag_add("entity", start, end)                            # Add tag to the entity span

    self.text_area.tag_config("entity", foreground="blue", underline=True)      # Configure tag appearance