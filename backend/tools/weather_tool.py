import requests
import os
from datetime import datetime, timedelta


def clean(s):
    return str(s).strip().strip('{}').strip('"').strip("'").strip()


def get_weather(query):
    """
    Get weather for a city, optionally for a specific date range.
    Input: 'city' or 'city|YYYY-MM-DD' or 'city|YYYY-MM-DD|YYYY-MM-DD'
    """
    query   = clean(query)
    parts   = query.split("|")
    city    = parts[0].strip()
    date_from = parts[1].strip() if len(parts) > 1 else None
    date_to   = parts[2].strip() if len(parts) > 2 else None

    api_key = os.getenv("OPENWEATHER_API_KEY")

    # Use 5-day forecast endpoint — free tier supports this
    # If dates provided, filter forecast to those days
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": city, "appid": api_key, "units": "metric", "cnt": 40},
            timeout=6,
        )
        if resp.status_code == 200:
            data    = resp.json()
            entries = data.get("list", [])

            # Filter by date range if provided
            if date_from:
                try:
                    start = datetime.strptime(date_from, "%Y-%m-%d")
                    end   = datetime.strptime(date_to, "%Y-%m-%d") if date_to else start + timedelta(days=7)
                    entries = [
                        e for e in entries
                        if start <= datetime.fromtimestamp(e["dt"]) <= end + timedelta(days=1)
                    ]
                except ValueError:
                    pass  # bad date format — show full forecast

            if not entries:
                # Dates beyond 5-day free forecast — use Serper for seasonal info
                return _seasonal_weather(city, date_from)

            # Group by day and summarise
            days = {}
            for e in entries:
                day = datetime.fromtimestamp(e["dt"]).strftime("%Y-%m-%d")
                if day not in days:
                    days[day] = []
                days[day].append(e)

            lines = [f"📅 Weather forecast for {city}:"]
            for day, items in list(days.items())[:7]:
                temps   = [i["main"]["temp"] for i in items]
                desc    = items[len(items)//2]["weather"][0]["description"].capitalize()
                humidity= items[0]["main"]["humidity"]
                rain    = sum(i.get("rain", {}).get("3h", 0) for i in items)
                lines.append(
                    f"\n  {day}: {desc} | "
                    f"{min(temps):.0f}–{max(temps):.0f}°C | "
                    f"Humidity: {humidity}% "
                    + (f"| Rain: {rain:.1f}mm" if rain > 0 else "")
                )

            # Packing tips based on average temp
            avg_temp = sum(e["main"]["temp"] for e in entries) / len(entries)
            lines.append(_packing_tips(avg_temp, entries))
            return "\n".join(lines)

    except Exception as e:
        print(f"[Weather] Forecast error: {e}")

    # Current weather fallback
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=6,
        )
        if resp.status_code == 200:
            data = resp.json()
            return (
                f"Current weather in {city}:\n"
                f"  {data['weather'][0]['description'].capitalize()} | "
                f"{data['main']['temp']}°C | "
                f"Humidity: {data['main']['humidity']}%"
                + (f"\n\n⚠️  Travel dates beyond 5-day forecast — showing current conditions." if date_from else "")
            )
    except Exception as e:
        print(f"[Weather] Current weather error: {e}")

    # Serper fallback
    from backend.tools.search_tool import search_web
    return search_web(f"weather in {city} {date_from or ''} temperature forecast")


def _seasonal_weather(city, date_str):
    """For dates beyond 5-day forecast, return seasonal/historical info via web search."""
    from backend.tools.search_tool import search_web
    try:
        month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B")
        result = search_web(f"weather in {city} in {month} average temperature what to expect")
        return f"📅 Seasonal weather for {city} in {month}:\n\n{result}\n\n⚠️  Live forecast not available for dates beyond 5 days."
    except Exception:
        return search_web(f"weather in {city} {date_str} forecast")


def _packing_tips(avg_temp, entries):
    has_rain = any(e.get("rain", {}).get("3h", 0) > 0 for e in entries)
    tips = ["\n🧳 Packing tips:"]
    if avg_temp < 10:
        tips.append("  • Heavy coat, thermals, gloves, warm hat")
    elif avg_temp < 18:
        tips.append("  • Light jacket, layers, comfortable walking shoes")
    elif avg_temp < 28:
        tips.append("  • Light clothing, sunscreen, sunglasses")
    else:
        tips.append("  • Lightweight breathable clothes, sunscreen, hat")
    if has_rain:
        tips.append("  • Umbrella or rain jacket expected")
    return "\n".join(tips)