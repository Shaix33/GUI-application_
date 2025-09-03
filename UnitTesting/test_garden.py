# test_garden.py
import pytest
from datetime import datetime, date
from garden_logic import is_frost_alert, calculate_harvest_date, search_pests, sample_pest_db

# Test Case 1: Frost Alert
def test_frost_alert_positive():
    assert is_frost_alert(-1) == True

def test_frost_alert_zero():
    assert is_frost_alert(0) == True

def test_frost_alert_negative():
    assert is_frost_alert(5) == False

def test_frost_alert_none():
    assert is_frost_alert(None) == False

# Test Case 2: Harvest Date Calculation
def test_harvest_date_calculation():
    planted_date = date(2024, 1, 1)
    expected_date = date(2024, 3, 16) # 75 days after Jan 1
    assert calculate_harvest_date(planted_date, 75) == expected_date

# Test Case 3: Pest Search
def test_pest_search_by_name():
    results = search_pests(sample_pest_db, "Aphid")
    assert len(results) == 1
    assert results[0]['name'] == "Aphid"

def test_pest_search_by_description():
    results = search_pests(sample_pest_db, "fungal")
    assert len(results) == 1
    assert results[0]['name'] == "Powdery Mildew"

def test_pest_search_not_found():
    results = search_pests(sample_pest_db, "rabbit")
    assert len(results) == 0

def test_pest_search_empty_term():
    results = search_pests(sample_pest_db, "")
    assert len(results) == 0