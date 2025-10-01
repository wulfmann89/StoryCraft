from continuity_engine.fantasy_calendar import FantasyCalendar

def extract_explicit_dates(text, calendar=None):
    if calendar:
        # Use fantasy calendar parsing

        return [calendar.parse_date(line) for line in text.splitlines() if "Year" in line]
    else:
        # Use repex for standard dates

        import re
        date_pattern = r"\b(?:\d{1,2}\s)?(?:Jan(?:uary)?|Feb(?:ruary)?|...)\s\d{1,2},?\s\d{4}\b"
        return re.findall(date_pattern, text)
    
def infer_sequence(text):
    sequence_markers = ["then", "after", "before", "later", "earlier"]
    return [line for line in text.splitlines() if any(marker in line.lower() for marker in sequence_markers)]