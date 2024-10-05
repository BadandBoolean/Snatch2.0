# copyright badandboolean 2024 all rights reserved
# getplaces.py
# takes a zipcode and a service type (currently hair salon, eyebrow threading, and massage)
# returns the google maps results (for ingestion)

import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
from rich import print_json

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_places_from_googlemaps(zipcode, service_type):
    if not GOOGLE_MAPS_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY is not set")
    
    # base API endpoint url
    base_url = "https://places.googleapis.com/v1/places:searchText"

    # headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,nextPageToken"
    }

    data = {
        "textQuery": f"{service_type} near {zipcode}",
        "pageSize": 20 # then you need the nextpagetoken to get more
    }

    # Make the POST request
    response = requests.post(base_url, headers=headers, json=data)
    # print_json(data=response.json())

    # get another page of results for a total of 40 results, note that some of them may not have websites! 

    data2 = {
        "textQuery": f"{service_type} near {zipcode}",
        "pageSize": 20,
        "pageToken": response.json()["nextPageToken"]
    }

    response2 = requests.post(base_url, headers=headers, json=data2)
    

    # concatenate the two responses, which are dictionaries, by extending the first one with the second one
    # holy fuck this works AND it removes the nextpagetoken from the response. nice. 
    alist = []
    alist.extend(response.json()["places"])
    alist.extend(response2.json()["places"])
    
    return alist

# Main tester class 

if __name__ == "__main__":
    # test the function
    response = get_places_from_googlemaps("94109", "hair salon")
    
    print_json(data=response)
    ''' format is this, for reference: 
    [
  {
    "formattedAddress": "2435 Polk St #10, San Francisco, CA 94109, USA",
    "websiteUri": "https://www.headandsoulsalonsf.com/",
    "displayName": {
      "text": "Head & Soul Salon",
      "languageCode": "en"
    }
  },
  {
    "formattedAddress": "1538 Pacific Ave #101, San Francisco, CA 94109, USA",
    "websiteUri": "http://www.salonvillagestudios.com/",
    "displayName": {
      "text": "Salon Village",
      "languageCode": "en"
    }
  },
  ...
  ]
    '''

# next stop: go to each website and scrape the next available appointments! 
