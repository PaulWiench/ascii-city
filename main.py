import json
import requests
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


lat_center = 48.748297
lon_center = 9.104774
radius = 100

radius_earth = 6371000

url = "https://overpass-api.de/api/interpreter"

# payload = r''
# with open('buildings.overpassql', 'r') as query:
#     payload += (query.read().replace('\n', ''))

payload = f"""
[out:json];
(
  way["building"](around:{radius},{lat_center},{lon_center});
);
out geom;
"""

r = requests.post(url, data=payload)
building_data = r.json()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

floor_height = 3
default_height = 10

for element in building_data["elements"]:
    geometry = []
    for node in element["geometry"]:
        lat = node["lat"]
        lon = node['lon']

        # Transformation from geographic coordinates to cartesian
        x = radius_earth * math.cos(lat_center) * (lon - lon_center) * math.pi / 180
        y = radius_earth * (lat - lat_center) * math.pi / 180

        # Normalize coordinates
        x = x / radius
        y = y / radius

    if "building:levels" in element["tags"]:
        levels = int(element["tags"]["building:levels"])
        height = levels * floor_height
    else:
        height = default_height

    geom = np.array(geometry)
    y, x = geom[:, 0], geom[:, 1]

    bottom = np.column_stack((x, y, np.zeros_like(x)))
    top = np.column_stack((x, y, np.full_like(x, height)))

    for idx in range(len(x) - 1):
        verts = [[bottom[idx], bottom[idx + 1], top[idx + 1], top[idx]]]
        ax.add_collection3d(Poly3DCollection(verts, color='gray'))

    ax.add_collection3d(Poly3DCollection([bottom], color='gray'))
    ax.add_collection3d(Poly3DCollection([top], color='gray'))

plt.show()
