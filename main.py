import json
import requests


url = "https://overpass-api.de/api/interpreter"

payload = r''
with open('buildings.overpassql', 'r') as query:
    payload += (query.read().replace('\n', ''))

r = requests.post(url, data=payload)

building_data = r.json()

building_geometries = []
for element in building_data["elements"]:
    geometry = []
    for lat_long_dict in element["geometry"]:
        geometry.append((lat_long_dict['lat'], lat_long_dict['lon']))
    building_geometries.append(geometry)
