import json
import os

import requests

API_KEY = os.getenv('API_KEY')

def get_public_IP():
    response = requests.get('https://api.ipify.org')
    return response.text

def get_geolocation():
    response = requests.get(f"https://api.maptiler.com/geolocation/ip.json?key={API_KEY}").json()
    lat, long = response['latitude'], response['longitude']
    return lat, long

def get_map(lat, long, mapId):
    response = requests.get(f"https://api.maptiler.com/maps/{mapId}/static/{long},{lat},1/512x512.webp")
    return response.text


def get_parking_overlays(dataID):
    response = requests.get(f"https://api.maptiler.com/data/{dataID}/features.json?key={API_KEY}")
    parking_info_map = response.json()
    with open("parking_pune.json", "w") as f:
        json.dump(parking_info_map, f, indent=4)

    return parking_info_map

dataid = "01975d8a-630c-7dc7-b6ff-7175c84fa2ec"
print(get_parking_overlays(dataid))