from crewai import Task
from datetime import datetime, timedelta


class TravelTasks:

    def research_flights(self, agent, origin, destination):
        return Task(
            description=(
                f"Find flight options from {origin} to {destination} using the Flight Tool. "
                f"Input format: '{origin}|{destination}|YYYY-MM-DD'. "
                f"Report: airline name, flight number, departure time, arrival time, duration, stops, price range USD."
            ),
            agent=agent,
            expected_output=(
                f"2-3 flights from {origin} to {destination} with airline, flight number, "
                f"times, duration, stops, and price in USD."
            )
        )

    def find_attractions(self, agent, destination, interests=""):
        interest_note = f" Focus on: {interests}." if interests else ""
        return Task(
            description=(
                f"Find top places in {destination} using Places Tool.{interest_note}\n"
                f"Call Places Tool with '{destination}|attractions' then '{destination}|restaurants'.\n"
                f"If interests mention specific categories (water parks, museums, etc), search those too.\n"
                f"For each place include: name, address, opening hours, entry cost, travel time from center."
            ),
            agent=agent,
            expected_output=(
                f"List of 6+ attractions and 5+ restaurants in {destination} with "
                f"name, address, hours, cost, and travel time."
            )
        )

    def check_weather(self, agent, destination, depart_date=None, duration=7):
        if depart_date:
            try:
                start = datetime.strptime(str(depart_date), "%Y-%m-%d")
                end   = start + timedelta(days=int(duration))
                period = f"{start.strftime('%B %d')} to {end.strftime('%B %d, %Y')}"
            except Exception:
                period = "the travel period"
        else:
            period = "the coming week"

        return Task(
            description=(
                f"Get the weather forecast for {destination} during {period}.\n"
                f"Use Weather Tool with input: '{destination}'\n"
                f"Then use Web Search to find typical weather for {destination} in {period}.\n"
                f"Provide: day-by-day conditions, temperature range, humidity, and packing list."
            ),
            agent=agent,
            expected_output=(
                f"Day-by-day weather for {destination} during travel showing temperatures, "
                f"conditions, and a packing list."
            )
        )

    def find_hotels(self, agent, destination):
        return Task(
            description=(
                f"Find hotels in {destination} using Places Tool with '{destination}|hotels'.\n"
                f"For each hotel include: exact name, address, neighborhood, star rating, "
                f"price per night USD, key amenities.\n"
                f"List 3-5 options across budget/mid-range/luxury."
            ),
            agent=agent,
            expected_output=(
                f"3-5 real hotels in {destination} with name, address, stars, price/night, amenities."
            )
        )

    def plan_itinerary(self, agent, destination, duration,
                       budget="mid-range", travel_style="balanced",
                       travelers=1, interests=""):
        return Task(
            description=(
                f"Create a {duration}-day travel itinerary for {destination}.\n"
                f"Travelers: {travelers} | Budget: {budget} | Style: {travel_style}"
                + (f" | Interests: {interests}" if interests else "") + "\n\n"
                f"Use ONLY the places, flights, hotels, and weather from previous tasks.\n\n"
                f"Format the output EXACTLY like this:\n\n"
                f"# {destination} {duration}-Day Travel Guide\n\n"
                f"## ✈️ RECOMMENDED FLIGHT\n"
                f"[Flight details from flights task]\n\n"
                f"## 🏨 RECOMMENDED HOTEL\n"
                f"[Hotel name, address, price/night, why it suits the budget]\n\n"
                f"## 🌤️ WEATHER SUMMARY\n"
                f"[Day-by-day weather from weather task]\n\n"
                f"## 🧳 PACKING LIST\n"
                f"[Based on weather]\n\n"
                f"## 📅 DAY-BY-DAY ITINERARY\n\n"
                f"### Day 1: [Date]\n"
                f"**Morning:** [Venue name] - [Address] - [What to do]\n"
                f"**Getting there:** [Transport + time]\n"
                f"**Afternoon:** [Venue name] - [Address] - [What to do]\n"
                f"**Getting there:** [Transport + time]\n"
                f"**Dinner:** [Restaurant name] - [Address] - [What to try]\n"
                f"**Daily Budget:** $X-Y\n\n"
                f"[Repeat for each day]\n\n"
                f"## 💰 TOTAL TRIP BUDGET\n"
                f"- Flights: $X\n"
                f"- Hotel ({duration} nights): $X\n"
                f"- Food & Activities: $X\n"
                f"- **Total: $X - $Y**\n"
            ),
            agent=agent,
            expected_output=(
                f"A complete {duration}-day itinerary with flight, hotel, weather summary, "
                f"packing list, day-by-day plan with venue names and addresses, and budget breakdown."
            )
        )