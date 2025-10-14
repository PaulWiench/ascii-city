import json
import requests


url = "https://overpass-api.de/api/interpreter"

payload = r''
with open('buildings.overpassql', 'r') as query:
    payload += (query.read().replace('\n', ''))

r = requests.post(url, data=payload)

building_data = r.json()

for element in building_data["elements"]:
    print(element["tags"]["building"])
