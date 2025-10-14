import requests


url = "https://overpass-api.de/api/interpreter"

payload = """
[out:json];
(
  way["building"](around:100,48.748297,9.104774);
);
out geom;
"""

r = requests.post(url, data=payload)

print(r.json())
