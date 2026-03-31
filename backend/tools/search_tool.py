import requests
import os


def clean(s):
    return s.strip().strip('{}').strip('"').strip("'").strip()


def search_web(query):
    query   = clean(query)
    api_key = os.getenv("SERPER_API_KEY")

    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": query, "num": 5}
    )

    if response.status_code != 200:
        return f"Search failed for: {query}"

    data    = response.json()
    results = data.get("organic", [])

    if not results:
        return "No results found."

    # Return "Title: snippet" per line so callers can parse cleanly
    lines = []
    for r in results:
        title   = r.get("title", "").strip()
        snippet = r.get("snippet", "").strip()
        if title and snippet:
            lines.append(f"{title}: {snippet}")
        elif title:
            lines.append(title)

    return "\n".join(lines)