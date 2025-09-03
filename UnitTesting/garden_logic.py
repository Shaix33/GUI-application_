# garden_logic.py

def is_frost_alert(temperature):
    """Returns True if temperature is at or below freezing."""
    if temperature is None:
        return False
    return temperature <= 0

def calculate_harvest_date(planted_date, days_to_maturity):
    """Calculates the harvest date based on planted date and days to maturity."""
    from datetime import timedelta
    return planted_date + timedelta(days=days_to_maturity)

def search_pests(pest_database, search_term):
    """Searches the pest database (list of dicts) for a term in name or description."""
    if not search_term:
        return []
    search_term = search_term.lower()
    results = [pest for pest in pest_database if 
               search_term in pest['name'].lower() or 
               search_term in pest['description'].lower()]
    return results

# Example pest database structure
sample_pest_db = [
    {"name": "Aphid", "description": "Small sap-sucking insects", "solution": "Use ladybugs."},
    {"name": "Tomato Hornworm", "description": "Large green caterpillars", "solution": "Handpick them."},
    {"name": "Powdery Mildew", "description": "Fungal disease on leaves", "solution": "Apply fungicide."}
]