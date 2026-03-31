import requests

def get_wiki_info(city):
    """
    Search for a city on Wikivoyage and return a summary.
    Fixes 404 errors by searching for the correct page title first.
    """
    url = "https://en.wikivoyage.org/w/api.php"
    
    # Step 1: Search for the correct Page Title
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": city,
        "format": "json"
    }
    
    try:
        search_res = requests.get(url, params=search_params).json()
        search_items = search_res.get('query', {}).get('search', [])
        
        if not search_items:
            return f"No Wikivoyage data found for {city}."
            
        # Get the 'Best Match' title (e.g., converts 'karachi' -> 'Karachi')
        correct_title = search_items[0]['title']
        
        # Step 2: Get the summary (extract) of that page
        content_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": correct_title,
            "format": "json"
        }
        
        content_res = requests.get(url, params=content_params).json()
        pages = content_res.get('query', {}).get('pages', {})
        
        for page_id, page_data in pages.items():
            return page_data.get('extract', 'No content available.')[:800] + "..."

    except Exception as e:
        return f"Wiki Error: {str(e)}"