import shodan
import os

def shodan_search(target):
    api_key = os.getenv("SHODAN_API_KEY")
    api = shodan.Shodan(api_key)

    try:
        results = api.search(target)
        return results['matches'][:3]
    except Exception as e:
        return[{"error": str(e)}]
    


    