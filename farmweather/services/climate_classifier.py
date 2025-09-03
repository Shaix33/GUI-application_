def classify_climate(climate_data):
    """
    Classifies climate conditions based on temperature, rainfall, and humidity.

    Args:
        climate_data (dict): Dictionary with keys 'temperature', 'rainfall', 'humidity'

    Returns:
        str: Climate classification label
    """
    try:
        temp = climate_data['temperature']
        rain = climate_data['rainfall']
        humidity = climate_data['humidity']

        if rain < 20 and temp > 32:
            return "High drought risk"
        elif humidity > 80 and temp > 25:
            return "Disease-prone conditions"
        elif 18 <= temp <= 28 and rain > 40:
            return "Optimal for maize"
        else:
            return "Unfavorable"
    except KeyError as e:
        return f"Missing climate field: {e}"