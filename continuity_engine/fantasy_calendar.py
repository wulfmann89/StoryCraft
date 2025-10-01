class FantasyCalendar:
    def __init__(self, config):
        self.eras = config.get("eras", [])
        self.months = config.get("months", [])
        self.days_per_month = config.get("days_per_month", 30)
        self.weekdays = config.get("weekdays", [])

    def parse_date(self, date_str):
        # Example: "12 Ashfall, Year 5 of the Ember Cycle"

        # Parse into structured metadata

        return {
            "day": 12,
            "month": "Ashfall",
            "year": 5,
            "era": "Ember Cycle"
        }
    
    def format_date(self, date_obj):
        return f"{date_obj['day']} {date_obj['month']}, Year {date_obj['year']} of the {date_obj['era']}"