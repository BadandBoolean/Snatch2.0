# takes a list of place urls and feeds them through the scraper in parallel
from get_places import get_places_from_googlemaps
from concurrent.futures import ThreadPoolExecutor

'''
# Initialize the dictionary
events = {
    "New York": ["2023-10-02 15:30:00", "2023-10-03 10:00:00"],
    "Los Angeles": ["2023-11-05 12:00:00"],
    "Chicago": ["2023-12-12 09:15:00", "2023-12-13 14:45:00"]
}
# Iterate over the dictionary
for place, date_times in events.items():
    print(f"Place: {place}")
    for dt in date_times:
        print(f" - Date and Time: {dt}")
# Add a new date and time to an existing place
events["New York"].append("2023-10-04 14:00:00")
# Add a new place with its dates and times
events["Boston"] = ["2023-11-20 16:30:00", "2023-11-21 11:00:00"]

'''
import requests

# Parameters:
# place_url_dict: a dictionary of place urls to scrape where the key is name and value is the ulr
def place_multithreader(place_url_dict):
    with ThreadPoolExecutor() as executor:
        futures = []
        for place, url in place_url_dict.items():
            futures.append(executor.submit(sample_function, place, url))
        for future in futures:
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Error: {e}")
         

def sample_function(place, url):
    # just return a concatenated string of the place and url for now, with the word banana on the end
    return f"{place} {url} banana"


if __name__ == "__main__":
    places = get_places_from_googlemaps("94109", "hair salon")
    # need to get only the displayName.text and websiteUri from the places list and convert to a dictionary where the key is the name and the value is the url
    place_url_dict = {}
    for place in places:
        # if the place has a websiteUri, add it to the dictionary
        if 'websiteUri' in place:
            place_url_dict[place["displayName"]["text"]] = place["websiteUri"]
        # if the place doesn't have a websiteUri, skip it
        else:
            continue
        
    
    # call the place_multithreader function with the place_url_dict as the parameter
    place_multithreader(place_url_dict)


    