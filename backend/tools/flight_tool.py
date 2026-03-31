"""
flight_tool.py  –  city→IATA loaded live from IATA-Code-List.pdf
"""
import os, re, requests, pdfplumber

# ── Country list for line parsing ─────────────────────────────────────────────
_COUNTRIES = sorted({
    "Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla",
    "Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan",
    "Bahamas","The Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize",
    "Benin","Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil",
    "Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada",
    "Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China",
    "Colombia","Comoros","Comoros (Comores)","Congo (DRC)","Congo (ROC)","Cook Island",
    "Costa Rica","Cote d'Ivoire","Croatia (Hrvatska)","Cuba","Cyprus","Czech Republic",
    "Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador",
    "Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France",
    "French Guiana","French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana",
    "Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guinea",
    "Guinea-Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India",
    "Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan",
    "Kazakhstan","Kenya","Kiribati","Korea South","South Korea","Kuwait","Kyrgyzstan",
    "Lao PDR","Latvia","Lebanon","Lesotho","Liberia","Libya","Lithuania","Luxembourg",
    "Macau, China SAR","Macedonia","Madagascar","Malawi","Malaysia","Maledives","Maldives",
    "Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte",
    "Mexico","Micronesia","Moldova","Mongolia","Montenegro","Morocco","Mozambique",
    "Myanmar","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia",
    "New Zealand","Nicaragua","Niger","Nigeria","North Korea","Northern Mariana Islands",
    "Norway","Oman","Pakistan","Palestinian Territory","Panama","Papua New Guinea",
    "Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion",
    "Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia",
    "Saint Vincent and the Grenadines","Saint Vincent & the Grenadines","Samoa",
    "Sao Tome & Principe","Saudi Arabia","Saudi Arabien","Senegal","Serbia","Seychelles",
    "Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia",
    "South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Svalbard/Norway",
    "Swaziland","Sweden","Switzerland","Switzerland/France","Syria","Taiwan","Tajikistan",
    "Tanzania","Thailand","Timor Leste (East Timor)","Togo","Tonga",
    "Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Uganda","Ukraine",
    "United Arab Emirates","United Kingdom","USA","US Minor Outlying Islands","Uruguay",
    "Uzbekistan","Vanuatu","Venezuela","Viet Nam","Wallis and Futuna Islands","Yemen",
    "Zambia","Zimbabwe","Scotland, UK","Virgin Islands (U.S.)","Virgin Islands (British)",
    "British Virgin Islands","Ibiza/Spain","Teneriffa/Spain","Loyaute, Pazifik",
    "Gabon/Loyautte","Hokkaido, Japan","King Island (Australia)",
    "Guangdong, PR China","Sichuan, PR China","Jilin, PR China","Heilongjiang, PR China",
    "Shandong, PR China","Xinjiang, PR China","Yunnan, PR China","Liaoning, PR China",
    "Shaanxi, PR China","Hubei, PR China","Jiangxi, China","Fujian, PR China",
    "Guangxi, PR China","PR China","Channel Islands","Cote d'Ivoire","Cote d Ivoire",
    "India, Maharashtra","St. Kitts and Nevis","St. Martin (Guadeloupe)",
}, key=len, reverse=True)   # longest first for greedy suffix match

# ── Preferred airport for multi-airport cities ────────────────────────────────
_PREFERRED = {
    "london":"LHR","london metropolitan area":"LHR","paris":"CDG","tokyo":"NRT",
    "osaka":"KIX","sapporo":"CTS","chicago":"ORD","new york":"JFK","new york city":"JFK",
    "houston":"IAH","washington dc":"IAD","washington":"DCA","miami":"MIA",
    "san francisco":"SFO","los angeles":"LAX","boston":"BOS","dallas":"DFW",
    "fort worth":"DFW","atlanta":"ATL","seattle":"SEA","detroit":"DTW",
    "minneapolis":"MSP","denver":"DEN","phoenix":"PHX","toronto":"YYZ",
    "montreal":"YUL","edmonton":"YEG","stockholm":"ARN","oslo":"OSL","helsinki":"HEL",
    "milan":"MXP","rome":"FCO","beijing":"PEK","shanghai":"PVG","guangzhou":"CAN",
    "canton":"CAN","kuala lumpur":"KUL","taipei":"TPE","bangkok":"BKK","seoul":"ICN",
    "mexico city":"MEX","buenos aires":"EZE","rio de janeiro":"GIG","sao paulo":"GRU",
    "johannesburg":"JNB","cairo":"CAI","moscow":"SVO","istanbul":"IST","amsterdam":"AMS",
    "frankfurt":"FRA","berlin":"BER","madrid":"MAD","zurich":"ZRH","vienna":"VIE",
    "copenhagen":"CPH","brussels":"BRU","lisbon":"LIS","dublin":"DUB","edinburgh":"EDI",
    "manchester":"MAN","birmingham":"BHX","glasgow":"GLA","singapore":"SIN",
    "hong kong":"HKG","jakarta":"CGK","manila":"MNL","karachi":"KHI","islamabad":"ISB",
    "lahore":"LHE","mumbai":"BOM","bombay":"BOM","delhi":"DEL","madras":"MAA",
    "calcutta":"CCU","kolkata":"CCU","sydney":"SYD","melbourne":"MEL","brisbane":"BNE",
    "auckland":"AKL","dubai":"DXB","abu dhabi":"AUH","doha":"DOH","riyadh":"RUH",
    "jeddah":"JED","beirut":"BEY","tehran":"THR","ankara":"ESB","kiev":"KBP",
    "kyiv":"KBP","bucharest":"OTP","belgrade":"BEG","warsaw":"WAW","prague":"PRG",
    "budapest":"BUD","nairobi":"NBO","addis ababa":"ADD","lagos":"LOS",
    "casablanca":"CMN","bogota":"BOG","lima":"LIM","santiago":"SCL","reykjavik":"KEF",
    "ho chi minh city":"SGN","saigon":"SGN","yangon":"RGN","rangoon":"RGN",
    "tashkent":"TAS","almaty":"ALA","kathmandu":"KTM","colombo":"CMB","dhaka":"DAC",
    "bali":"DPS","denpasar":"DPS","peking":"PEK",
}

# ── Hub list for 1-stop routing ────────────────────────────────────────────────
_ALL_HUBS = [
    "DXB","DOH","AUH","IST","JED",           # Middle East
    "LHR","AMS","FRA","CDG","MAD","ZRH",     # Europe
    "SIN","HKG","ICN","NRT","BKK","KUL",     # Asia-Pacific
    "JFK","ATL","ORD","DFW","LAX","YYZ",     # Americas
    "ADD","JNB","CAI","CMN","NBO",            # Africa
    "DEL","BOM","CMB","DAC",                  # South Asia
    "SYD",                                    # Oceania
]

AIRLINE_NAMES = {
    "PK":"Pakistan International Airlines","EK":"Emirates","TK":"Turkish Airlines",
    "EY":"Etihad Airways","QR":"Qatar Airways","SV":"Saudia","ET":"Ethiopian Airlines",
    "FZ":"flydubai","G9":"Air Arabia","PA":"Airblue","BA":"British Airways",
    "LH":"Lufthansa","AF":"Air France","KL":"KLM","AI":"Air India",
    "SQ":"Singapore Airlines","CX":"Cathay Pacific","MH":"Malaysia Airlines",
    "TG":"Thai Airways","MS":"EgyptAir","RJ":"Royal Jordanian","GF":"Gulf Air",
    "WY":"Oman Air","XY":"flynas","J9":"Jazeera Airways","UA":"United Airlines",
    "AA":"American Airlines","DL":"Delta Airlines","AC":"Air Canada",
    "QF":"Qantas","NZ":"Air New Zealand","SA":"South African Airways",
    "KQ":"Kenya Airways","IB":"Iberia","TP":"TAP Portugal","SK":"SAS",
    "AY":"Finnair","LX":"Swiss International","OS":"Austrian Airlines",
    "SN":"Brussels Airlines",
}

_CACHE: dict | None = None


def _parse_line(line: str):
    line = line.strip()
    if not line:
        return None
    parts = line.rsplit(None, 1)
    if len(parts) != 2:
        return None
    rest, iata = parts
    if not re.match(r'^[A-Z]{3}$', iata):
        return None
    city_part = None
    for country in _COUNTRIES:
        if rest.rstrip().endswith(country):
            city_part = rest.rstrip()[:-len(country)].strip()
            break
    if not city_part:
        tokens = rest.split()
        city_part = tokens[0] if tokens else None
    if not city_part or len(city_part) < 2:
        return None
    short = re.split(r'\s+-\s+|\s+\(', city_part)[0].strip().rstrip('-').strip()
    if len(short) < 2:
        short = city_part.split()[0]
    return short, iata


def _load(pdf_path: str = "IATA-Code-List.pdf") -> dict:
    result: dict = {}
    if os.path.exists(pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    for line in text.split("\n"):
                        parsed = _parse_line(line)
                        if parsed:
                            k = parsed[0].lower()
                            if k not in result:
                                result[k] = parsed[1]
        except Exception as e:
            print(f"[IATA] PDF error: {e}")
    else:
        print(f"[IATA] PDF not found at '{pdf_path}'")
    result.update(_PREFERRED)          # preferred always wins
    print(f"[IATA] {len(result)} cities loaded.")
    return result


def _db() -> dict:
    global _CACHE
    if _CACHE is None:
        _CACHE = _load()
    return _CACHE


def get_all_cities() -> list:
    return sorted({k.title() for k in _db().keys()})


def clean(s: str) -> str:
    return str(s).strip().strip("{}").strip('"').strip("'").strip()


def city_to_iata(city: str) -> str:
    city = clean(city)
    if re.match(r'^[A-Z]{3}$', city):
        return city
    db = _db()
    key = city.lower()
    if key in db:
        return db[key]
    # Partial prefix match
    for k, v in db.items():
        if k.startswith(key):
            return v
    print(f"[IATA] Unknown city '{city}'")
    return city[:3].upper()


def _fetch(dep: str, arr: str, api_key: str) -> list:
    try:
        r = requests.get(
            "https://airlabs.co/api/v9/routes",
            params={"dep_iata": dep, "arr_iata": arr, "api_key": api_key},
            timeout=10,
        )
        if r.status_code != 200:
            return []
        data = r.json()
        if data.get("error"):
            return []
        return data.get("response") or []
    except Exception as e:
        print(f"[Airlabs] {dep}→{arr}: {e}")
        return []


def _fmt(routes: list, n: int = 6) -> list:
    lines, seen = [], set()
    for r in routes:
        flt = r.get("flight_iata","")
        if flt in seen:
            continue
        seen.add(flt)
        al  = AIRLINE_NAMES.get(r.get("airline_iata",""), r.get("airline_iata","?"))
        dt  = r.get("dep_time",""); at = r.get("arr_time","")
        dur = r.get("duration",""); dy = r.get("days",[])
        ds  = f"{int(dur)//60}h {int(dur)%60}m" if dur else ""
        ln  = f"  ✈  {al} ({flt}) | {r.get('dep_iata','')}→{r.get('arr_iata','')}"
        if dt: ln += f" dep {dt}"
        if at: ln += f" arr {at}"
        if ds: ln += f" | {ds}"
        if dy: ln += f" | {', '.join(dy)}"
        lines.append(ln)
        if len(lines) >= n:
            break
    return lines


def _serper(origin: str, dest: str, date: str) -> str:
    key = os.getenv("SERPER_API_KEY","")
    if not key:
        return ""
    out = []
    for q in [f"flights {origin} to {dest} {date}", f"{origin} {dest} direct flight"]:
        try:
            r = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": key, "Content-Type": "application/json"},
                json={"q": q, "num": 4}, timeout=8,
            )
            if r.status_code == 200:
                for x in r.json().get("organic",[]):
                    t,s = x.get("title","").strip(), x.get("snippet","").strip()
                    if t and s:
                        out.append(f"• {t}: {s}")
        except Exception as e:
            print(f"[Serper] {e}")
    return "\n".join(out[:8])


def get_flights(origin: str, destination: str, date: str) -> str:
    origin, destination, date = clean(origin), clean(destination), clean(date)
    oi, di = city_to_iata(origin), city_to_iata(destination)
    print(f"\n[Flights] {origin}({oi}) → {destination}({di}) on {date}")

    key = os.getenv("AIRLABS_API_KEY","")

    if key:
        # ── Direct ────────────────────────────────────────────────────────────
        direct = _fetch(oi, di, key)
        if direct:
            lines = _fmt(direct)
            if lines:
                return (
                    f"Direct flights  {origin} ({oi}) → {destination} ({di}):\n\n"
                    + "\n".join(lines)
                    + f"\n\n💡 Book on airline websites or Google Flights for {date}."
                )

        # ── 1-stop via hub ────────────────────────────────────────────────────
        print("[Flights] No direct — trying 1-stop hubs…")
        for hub in _ALL_HUBS:
            if hub in (oi, di):
                continue
            l1 = _fetch(oi, hub, key)
            if not l1:
                continue
            l2 = _fetch(hub, di, key)
            if not l2:
                continue
            f1, f2 = _fmt(l1, 3), _fmt(l2, 3)
            return (
                f"No direct flight found.\n"
                f"1-stop via {hub}  ({origin} → {hub} → {destination}):\n\n"
                f"Leg 1  ({oi} → {hub}):\n" + "\n".join(f1) + "\n\n"
                f"Leg 2  ({hub} → {di}):\n" + "\n".join(f2)
                + f"\n\n💡 Book on airline websites or Google Flights for {date}."
            )

    # ── Serper fallback ───────────────────────────────────────────────────────
    s = _serper(origin, destination, date)
    if s:
        return f"Flight options  {origin} → {destination} on {date}:\n\n{s}"

    return (
        f"No flight data found for {origin} ({oi}) → {destination} ({di}) on {date}. "
        "Try Google Flights or Skyscanner."
    )
    