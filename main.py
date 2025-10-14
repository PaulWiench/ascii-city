import json
import requests

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


url = "https://overpass-api.de/api/interpreter"

payload = r''
with open('buildings.overpassql', 'r') as query:
    payload += (query.read().replace('\n', ''))

r = requests.post(url, data=payload)
building_data = r.json()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

floor_height = 3
default_height = 10

for element in building_data["elements"]:
    geometry = []
    for lat_long_dict in element["geometry"]:
        geometry.append((lat_long_dict['lat'], lat_long_dict['lon']))

    if "building:levels" in element["tags"]:
        levels = int(element["tags"]["building:levels"])
        height = levels * floor_height
    else:
        height = default_height

    geom = np.array(geometry)
    x, y = geom[:, 0], geom[:, 1]

    bottom = np.column_stack((x, y, np.zeros_like(x)))

    ax.add_collection3d(Poly3DCollection([bottom], color='gray'))

plt.show()
