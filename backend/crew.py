import os
import re
import time

os.environ["OPENAI_API_KEY"]           = "not-used"
os.environ["CREWAI_DISABLE_BRAVE_SEARCH"] = "true"
os.environ["BRAVE_API_KEY"]               = ""
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from crewai import Crew, Process, LLM
from backend.agents.travel_agents import TravelAgents
from backend.tasks.travel_tasks import TravelTasks


def _parse_retry_delay(error_str):
    match = re.search(r'retry[^\d]*(\d+)s', error_str, re.IGNORECASE)
    return int(match.group(1)) + 2 if match else 5


def _error_type(error_str):
    """Classify the error so we know how to handle it."""
    e = error_str.lower()
    if any(w in e for w in ["429", "rate_limit", "quota", "resource_exhausted", "too many requests"]):
        return "rate_limit"
    if any(w in e for w in ["tool_use_failed", "failed to call a function", "invalid_request_error"]):
        return "tool_error"
    if any(w in e for w in ["connection", "timeout", "network", "unreachable"]):
        return "network"
    return "other"


def get_available_llms():
    llms = []

    if os.getenv("GROQ_API_KEY"):
        llms.append(LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
        ))

    # Gemini removed — quota exhausted on free tier
    # Re-add if you upgrade: uncomment below and add GEMINI_API_KEY to .env
    # gemini_key = os.getenv("GEMINI_API_KEY")
    # if gemini_key:
    #     llms.append(LLM(model="gemini/gemini-2.0-flash", api_key=gemini_key))

    # Uncomment to add more providers:
    # if os.getenv("ANTHROPIC_API_KEY"):
    #     llms.append(LLM(model="anthropic/claude-3-haiku-20240307", api_key=os.getenv("ANTHROPIC_API_KEY")))
    # if os.getenv("MISTRAL_API_KEY"):
    #     llms.append(LLM(model="mistral/mistral-small", api_key=os.getenv("MISTRAL_API_KEY")))

    if not llms:
        raise ValueError("No LLM key found. Set GROQ_API_KEY or GEMINI_API_KEY in .env")

    return llms


class SmartTravelCrew:
    def __init__(self):
        self.llms  = get_available_llms()
        self.tasks = TravelTasks()
        print(f"[LLM] {len(self.llms)} LLM(s) loaded: {[l.model for l in self.llms]}")

    def _build_crew(self, llm):
        agents          = TravelAgents(llm, *[l for l in self.llms if l is not llm])
        logistics_agent = agents.logistics_agent()
        scout_agent     = agents.scout_agent()
        concierge_agent = agents.concierge_agent()

        flight_task      = self.tasks.research_flights(logistics_agent, self._origin, self._destination)
        attractions_task = self.tasks.find_attractions(scout_agent, self._destination, self._interests)
        weather_task     = self.tasks.check_weather(concierge_agent, self._destination, self._depart_date, self._duration)
        hotel_task       = self.tasks.find_hotels(concierge_agent, self._destination)
        itinerary_task   = self.tasks.plan_itinerary(concierge_agent, self._destination, self._duration, self._budget, self._travel_style, self._travelers, self._interests)

        # Pass all previous task outputs as context to itinerary planner
        # This ensures it uses the EXACT hotel and flight chosen — no hallucination
        itinerary_task.context = [flight_task, attractions_task, weather_task, hotel_task]

        return Crew(
            agents=[logistics_agent, scout_agent, concierge_agent],
            tasks=[flight_task, attractions_task, weather_task, hotel_task, itinerary_task],
            process=Process.sequential,
            verbose=True,
            planning=False,
        )

    def run(self, origin, destination, duration, depart_date=None, budget="mid-range", travel_style="balanced", travelers=1, interests=""):
        self._origin       = origin
        self._destination  = destination
        self._duration     = duration
        self._depart_date  = depart_date
        self._budget       = budget
        self._travel_style = travel_style
        self._travelers    = travelers
        self._interests    = interests

        last_error = None

        for i, llm in enumerate(self.llms):
            # Each LLM gets up to 2 attempts (handles transient tool errors)
            for attempt in range(2):
                try:
                    print(f"\n[LLM] Trying {llm.model} (attempt {attempt + 1})")
                    result = self._build_crew(llm).kickoff()
                    print(f"\n[LLM] ✅ Success with: {llm.model}")
                    return result

                except Exception as e:
                    last_error  = e
                    etype       = _error_type(str(e))
                    delay       = _parse_retry_delay(str(e)) if etype == "rate_limit" else 3

                    print(f"\n[LLM] ❌ {etype.upper()} on {llm.model} (attempt {attempt + 1}): {str(e)[:200]}")

                    if etype == "rate_limit":
                        # Rate limited — no point retrying same model, move to next
                        print(f"[LLM] Rate limited. Moving to next LLM after {delay}s.")
                        time.sleep(delay)
                        break  # break inner attempt loop, go to next LLM

                    elif etype == "tool_error" and attempt == 0:
                        # Tool format error — retry once on same LLM (sometimes transient)
                        print(f"[LLM] Tool error — retrying same LLM in 2s...")
                        time.sleep(2)
                        continue

                    else:
                        # Other error or second attempt failed — move to next LLM
                        time.sleep(2)
                        break

        raise RuntimeError(
            f"All {len(self.llms)} LLM(s) failed. Last error: {last_error}\n"
            "Tip: Add ANTHROPIC_API_KEY or MISTRAL_API_KEY in .env and uncomment in crew.py."
        )