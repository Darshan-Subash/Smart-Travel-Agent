from crewai import Agent
from crewai.tools import tool
from backend.tools.weather_tool import get_weather
from backend.tools.flight_tool import get_flights
from backend.tools.places_tool import get_places
from backend.tools.search_tool import search_web

def clean_input(s):
    return str(s).strip().strip('{}').strip('"').strip("'").strip()

@tool("Weather Tool")
def weather_tool(city: str) -> str:
    """Get weather forecast for a city. Input: city name only. Example: Karachi"""
    return get_weather(clean_input(city))

@tool("Flight Tool")
def flight_tool(origin: str, destination: str, date: str) -> str:
    """Search for real-time flights. Input: origin city, destination city, date (YYYY-MM-DD)."""
    return get_flights(clean_input(origin), clean_input(destination), clean_input(date))

@tool("Places Tool")
def places_tool(query: str) -> str:
    """Find physical places like hotels/restaurants. Input: city|category."""
    query = clean_input(query)
    if "|" in query:
        city, category = query.split("|", 1)
    else:
        city, category = query, "attractions"
    return get_places(city.strip(), category.strip())

@tool("Web Search Tool")
def web_search_tool(query: str) -> str:
    """Search the web for travel tips, safety, or events."""
    return search_web(clean_input(query))

class TravelAgents:
    def __init__(self, llm, *fallback_llms):
        self.llm = llm
        self.fallbacks = list(fallback_llms)

    def logistics_agent(self):
        return Agent(
            role='Flight & Logistics Specialist',
            goal='Find the best flights and transport options',
            backstory='Expert using AirLabs to find routes. Can find 1-stop connections via global hubs.',
            tools=[flight_tool, web_search_tool],
            llm=self.llm,
            verbose=True
        )

    def scout_agent(self):
        return Agent(
            role='Destination Scout',
            goal='Find top attractions and restaurants using Places Tool',
            backstory='Experienced traveler who always uses Places Tool for physical venues.',
            tools=[places_tool, web_search_tool],
            llm=self.llm,
            verbose=True
        )

    def concierge_agent(self):
        return Agent(
            role='Travel Concierge',
            goal='Find hotels, check weather, and build the final itinerary',
            backstory='Concierge who uses Places Tool for hotels and Weather Tool for forecasts.',
            tools=[weather_tool, places_tool, web_search_tool],
            llm=self.llm,
            verbose=True
        )