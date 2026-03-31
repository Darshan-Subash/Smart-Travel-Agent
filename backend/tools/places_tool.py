import requests
import os
import re


def clean(s):
    return str(s).strip().strip('{}').strip('"').strip("'").strip()


# ── Serper Places (PRIMARY) ───────────────────────────────────────────────────

def _serper_places(city, category):
    api_key = os.getenv("SERPER_API_KEY", "")
    if not api_key:
        print("[Serper Places] SERPER_API_KEY not set in .env")
        return None

    try:
        resp = requests.post(
            "https://google.serper.dev/places",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": f"{category} in {city}", "location": city},
            timeout=8,
        )
        print(f"[Serper Places] '{category}' in '{city}' → status {resp.status_code}")

        if resp.status_code != 200:
            print(f"[Serper Places] Error: {resp.text[:200]}")
            return None

        places = resp.json().get("places", [])
        print(f"[Serper Places] Found {len(places)} places")

        if not places:
            return None

        lines = []
        for i, p in enumerate(places, 1):
            name        = p.get("title", "Unknown")
            address     = p.get("address", "")
            rating      = p.get("rating", "")
            reviews     = p.get("ratingCount", "")
            category_lbl= p.get("type", "")
            hours       = p.get("openingHours", "")
            phone       = p.get("phoneNumber", "")
            website     = p.get("website", "")
            price       = p.get("priceLevel", "")

            line = f"{i}. {name}"
            if rating:
                line += f" ⭐ {rating}"
                if reviews: line += f" ({reviews} reviews)"
            if price:       line += f" · {price}"
            if category_lbl: line += f"\n   🏷️  {category_lbl}"
            if address:     line += f"\n   📍 {address}"
            if hours:       line += f"\n   🕐 {hours}"
            if phone:       line += f"\n   📞 {phone}"
            if website:     line += f"\n   🌐 {website}"
            lines.append(line)

        return lines

    except Exception as e:
        print(f"[Serper Places] Error: {e}")
    return None


# ── Foursquare (SECONDARY) ────────────────────────────────────────────────────

FSQ_CATEGORIES = {
    "restaurants":   "13065",
    "food":          "13065",
    "cafes":         "13035",
    "coffee":        "13035",
    "hotels":        "19014",
    "accommodation": "19014",
    "attractions":   "16000",
    "sights":        "16000",
    "museums":       "10027",
    "parks":         "16032",
    "nature":        "16032",
    "shopping":      "17000",
    "malls":         "17114",
    "nightlife":     "10032",
    "bars":          "13003",
    "beaches":       "16010",
    "sports":        "18000",
}

CATEGORY_FILTERS = {
    "restaurants":  ["restaurant", "dining", "bbq", "pizza", "burger", "kebab", "food", "grill", "diner"],
    "cafes":        ["cafe", "coffee", "tea", "bakery"],
    "hotels":       ["hotel", "inn", "lodge", "resort", "hostel", "guesthouse"],
    "attractions":  ["museum", "monument", "park", "beach", "landmark", "gallery", "heritage", "zoo"],
    "museums":      ["museum", "gallery", "heritage", "history", "art"],
    "parks":        ["park", "garden", "nature", "green", "reserve"],
    "shopping":     ["mall", "market", "shop", "store", "retail", "bazaar", "plaza"],
    "nightlife":    ["bar", "club", "lounge", "nightlife", "hookah", "pub", "rooftop"],
    "bars":         ["bar", "pub", "lounge", "hookah"],
    "beaches":      ["beach", "seafront", "waterfront"],
}


def _matches_category(cats_str, category):
    filters = CATEGORY_FILTERS.get(category.lower())
    if not filters:
        return True
    return any(kw in cats_str.lower() for kw in filters)


def _foursquare_places(city, category):
    api_key = os.getenv("FOURSQUARE_API_KEY", "")
    if not api_key:
        return None

    city_title  = city.strip().title()
    category_id = FSQ_CATEGORIES.get(category.lower())

    params = {"near": city_title, "limit": 50, "sort": "RATING"}
    if category_id:
        params["categories"] = category_id
    else:
        params["query"] = category

    try:
        resp = requests.get(
            "https://places-api.foursquare.com/places/search",
            headers={
                "X-Places-Api-Version": "2025-06-17",
                "accept":               "application/json",
                "authorization":        f"Bearer {api_key}",
            },
            params=params,
            timeout=8,
        )
        print(f"[Foursquare] '{category}' in '{city_title}' → status {resp.status_code}")
        if resp.status_code != 200:
            return None

        results  = resp.json().get("results", [])
        filtered = [
            (p, ", ".join(c.get("name", "") for c in p.get("categories", [])))
            for p in results
            if _matches_category(", ".join(c.get("name", "") for c in p.get("categories", [])), category)
        ]
        print(f"[Foursquare] {len(results)} raw → {len(filtered)} filtered")
        if not filtered:
            return None

        lines = []
        for i, (p, cats_str) in enumerate(filtered[:15], 1):
            name    = p.get("name", "Unknown")
            address = p.get("location", {}).get("formatted_address", "")
            rating  = p.get("rating", "")
            line    = f"{i}. {name}"
            if rating:   line += f" ⭐ {rating}"
            if cats_str: line += f" ({cats_str})"
            if address:  line += f"\n   📍 {address}"
            lines.append(line)
        return lines

    except Exception as e:
        print(f"[Foursquare] Error: {e}")
    return None


# ── Wikivoyage (TERTIARY) ─────────────────────────────────────────────────────

_wv_token = None


def _wikivoyage_login():
    global _wv_token
    if _wv_token:
        return _wv_token
    username = os.getenv("WIKIMEDIA_USERNAME", "")
    password = os.getenv("WIKIMEDIA_PASSWORD", "")
    if not username or not password:
        print("[Wikivoyage] Credentials not set in .env")
        return None
    try:
        resp = requests.post(
            "https://auth.enterprise.wikimedia.com/v1/login",
            headers={"Content-Type": "application/json"},
            json={"username": username, "password": password},
            timeout=8,
        )
        print(f"[Wikivoyage] Login status: {resp.status_code}")
        if resp.status_code == 200:
            _wv_token = resp.json().get("access_token")
            return _wv_token
        print(f"[Wikivoyage] Login failed: {resp.text[:200]}")
    except Exception as e:
        print(f"[Wikivoyage] Login error: {e}")
    return None


def _wikivoyage_places(city, category):
    token = _wikivoyage_login()
    if not token:
        return None

    section_keywords = {
        "restaurants": ["eat", "food", "dining"],
        "hotels":      ["sleep", "stay", "accommodation"],
        "attractions": ["see", "sights", "do"],
        "shopping":    ["buy", "shop"],
        "nightlife":   ["drink", "nightlife"],
        "parks":       ["do", "outdoors"],
    }
    keywords   = section_keywords.get(category.lower(), [category.lower()])
    city_title = city.strip().title().replace(" ", "_")

    try:
        resp = requests.post(
            f"https://api.enterprise.wikimedia.com/v2/structured-contents/{city_title}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"filters": [{"field": "is_part_of.identifier", "value": "enwikivoyage"}]},
            timeout=10,
        )
        print(f"[Wikivoyage] Status for '{city_title}': {resp.status_code}")
        if resp.status_code != 200:
            return None

        items = resp.json()
        if not isinstance(items, list):
            items = [items]

        places = []
        for item in items:
            for section in item.get("sections", []):
                if not any(kw in section.get("title", "").lower() for kw in keywords):
                    continue
                for entry in section.get("has_parts", []):
                    name    = entry.get("name") or entry.get("title", "")
                    desc    = (entry.get("abstract") or "")[:150]
                    address = entry.get("address", "")
                    if not name:
                        continue
                    line = name
                    if address: line += f"\n   📍 {address}"
                    if desc:    line += f"\n   {desc}"
                    places.append(line)

        print(f"[Wikivoyage] Found {len(places)} places")
        return places[:8] if places else None
    except Exception as e:
        print(f"[Wikivoyage] Error: {e}")
    return None


# ── Main entry ────────────────────────────────────────────────────────────────

def get_places(city, category="attractions"):
    city     = clean(city)
    category = clean(category).split(",")[0].strip()
    print(f"\n[Places] Looking for '{category}' in '{city}'")

    # 1. Serper Places — Google Places data, most accurate
    srp = _serper_places(city, category)
    if srp:
        return f"📍 {category.title()} in {city}:\n\n" + "\n\n".join(srp)

    # 2. Foursquare — fallback
    fsq = _foursquare_places(city, category)
    if fsq:
        return f"📍 {category.title()} in {city} (Foursquare):\n\n" + "\n\n".join(fsq)

    # 3. Wikivoyage — structured travel content
    wv = _wikivoyage_places(city, category)
    if wv:
        return f"📍 {category.title()} in {city} (Wikivoyage):\n\n" + \
               "\n\n".join(f"{i}. {p}" for i, p in enumerate(wv, 1))

    return f"No {category} found in {city}."