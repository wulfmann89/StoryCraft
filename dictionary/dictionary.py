import requests
from tkinter import messagebox

# Uses Free Dictionary API (or similar) to fetch definitions

def lookup_word(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code ==200:
            data = response.json()[0]
            definition = data['meanings'][0]['definitions'][0]['definition']
            synonyms = data["meanings"][0]["definitions"][0].get("synonyms", [])   
            return definition, synonyms
        else:
            return "Definition not found", []
    except Exception as e:
        return f"Error: {str(e)}", []

# Popup integration
def show_definition(word):
    definition, synonyms = lookup_word(word)
    message = f"Definition: \n{definition}\n\nSynonyms: \n{', '.join(synonyms) if synonyms else 'None'}"
    messagebox.showinfo(f"Lookup: {word}", message)