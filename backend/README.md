# Backend - Smart Travel Agent 🤖

The backend is powered by **CrewAI**, a framework for orchestrating role-playing autonomous AI agents.

## 🏗️ Core Architecture

The backend logic is centralized in `backend/crew.py`, which defines the `SmartTravelCrew`.

### Agents (`backend/agents/`)

- **Flight & Logistics Specialist**: Expert in finding the best flight routes and transportation.
- **Destination Scout**: Discovers attractions, restaurants, and hidden gems.
- **Travel Concierge**: Focuses on accommodation, weather, and final coordination.

### Tasks (`backend/tasks/`)

- **research_flights**: Searches for flight options using real-time data.
- **find_attractions**: Gathers recommendations for points of interest.
- **check_weather**: Retrieves weather forecasts for the travel period.
- **find_hotels**: Locates suitable hotels based on the user's budget.
- **plan_itinerary**: Integrates all previous research into a detailed day-by-day plan.

### Custom Tools (`backend/tools/`)

Custom tools are built to fetch real-time data from various sources:
- `flight_tool.py`: Interfaces with aviation APIs.
- `places_tool.py`: Searches for physical venues.
- `weather_tool.py`: Fetches meteorological forecasts.
- `search_tool.py`: Performs web searches for broad travel information.
- `wiki_tool.py`: Extracts structured data from Wikipedia.

## ⚙️ Resilience & Fallbacks

To ensure high availability, the `SmartTravelCrew` implements a robust retry and fallback mechanism:
- **Multiple LLMs**: Configurable list of LLM providers (Groq, Gemini, etc.).
- **Automatic Retries**: Handles transient tool errors and rate limits by switching models or pausing before retrying.
- **Sequential Context**: Tasks are executed in sequence, with each subsequent task receiving context from previous ones to minimize hallucinations and ensure data consistency.
