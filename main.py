import requests


url = "https://overpass-api.de/api/interpreter"

payload = r''
with open('buildings.overpassql', 'r') as query:
    payload += (query.read().replace('\n', ''))

r = requests.post(url, data=payload)

print(r.json())
