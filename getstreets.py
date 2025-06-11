import json
import os
from geopy.distance import distance
import requests
from dotenv import load_dotenv

load_dotenv()

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

def generate_circle_around_me(lat, long, radius, num_points=36):
    points = []
    for angle in range(0, 360, int(360 / num_points)):
        # Compute a point at a given bearing and distance
        d = distance(kilometers=radius)
        point = d.destination((lat, long), bearing=angle)
        points.append((point.latitude, point.longitude))
    return points

lat, long = get_geolocation()
circle = generate_circle_around_me(lat, long, 1.0)
for point in circle:
    print(point)

# TODO: import geopandas and figure out how to find the parking zones that are within the 1km circle.


dataid = "01975d8a-630c-7dc7-b6ff-7175c84fa2ec"
# print(get_parking_overlays(dataid))