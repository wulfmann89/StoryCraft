import re
from datetime import datetime

def extract_explicit_dates(text):
    # Matches formats like "January 5, 2020" or "5 Jan 2020"

    date_pattern = r"\b(?:\d{1,2}\s)?(?:Jan(?uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2},?\s\d{4}\b"
    return re.findall(date_pattern, text)

def infer_sequence(text):
    # Simple heuristic: look for phrases like "then", "after", "before"

    sequence_markers = ["then", "after", "before", "later", "earlier"]
    return [line for line in text.splitlines() if any(marker in line.lower() for marker in sequence_markers)]