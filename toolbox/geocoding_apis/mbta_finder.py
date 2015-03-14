"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    import urllib2, json
    # from pprint import pprint
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    response_data = get_json(GMAPS_BASE_URL+"?address="+(place_name.replace(' ','%')))
    lat_lng_data = response_data["results"][0]["geometry"]["location"]
    return (lat_lng_data['lat'],lat_lng_data['lng'])

def get_nearest_station(latitude,longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    import pprint
    from pprint import pprint
    mbta_data = get_json(str(MBTA_BASE_URL+'?api_key='+MBTA_DEMO_API_KEY+'&lat='+str(latitude)+'&lon='+str(longitude)+'&format=json'))
    # print pprint(mbta_data)
    closest_station = mbta_data["stop"][0]["stop_name"]
    distance = mbta_data["stop"][0]["distance"]
    return str('The closest station is '+closest_station+', '+distance+' miles away from your destination.')

def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    """
    return get_nearest_station(get_lat_long(place_name)[0],get_lat_long(place_name)[1])

print find_stop_near('harvard')