def suggest_crops(avg_temp: float | None, total_rain_mm: float | None):
    """
    Very simple, explainable rules:
    - Warm (>=22°C): warm-season crops
    - Mild (15–22°C): cool-season leafy/root crops
    - Cold (<15°C): hardy cool-season crops
    Then tweak a bit for very dry or very wet forecasts.
    """
    if avg_temp is None:
        return ["(No forecast available to suggest crops)"]

    crops = []
    if avg_temp >= 22:
        crops = ["Tomatoes", "Maize (corn)", "Green beans", "Peppers", "Sweet potato"]
    elif 15 <= avg_temp < 22:
        crops = ["Cabbage", "Spinach", "Beetroot", "Carrots", "Lettuce", "Peas"]
    else:
        crops = ["Kale", "Broccoli", "Onions", "Garlic", "Potatoes"]

    # Rainfall adjustments for next ~5 days
    if total_rain_mm is not None:
        if total_rain_mm < 5:
            # very dry
            crops = ["Sorghum", "Millet", "Cowpeas", "Sweet potato"] + [c for c in crops if c not in ["Lettuce"]]
        elif total_rain_mm > 40:
            # very wet
            crops = ["Rice (paddy if fields allow)", "Taro", "Celery"] + crops

    # Keep a compact list for the UI
    seen, unique = set(), []
    for c in crops:
        if c not in seen:
            unique.append(c)
            seen.add(c)
    return unique[:8]
