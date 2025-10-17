import json
import requests
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from ascii_renderer import AsciiRenderer
from canvas_handler import CanvasHandler


location_query = "Frankfurt"

nominatim = requests.get("https://nominatim.openstreetmap.org/search", params={"q": location_query, "format": "json", "limit": 1, "addressdetails": 1}, headers={"User-Agent": "MyApp/1.0 (you@example.com)"})

lat_center = float(nominatim.json()[0]["lat"]) # 10 # 48.7877151357412 # 40.764954591693716 # 48.748297
lon_center = float(nominatim.json()[0]["lon"]) # 9.200721837822925 # -73.98034581499466 # 9.104774
radius = 250

radius_earth = 6371000

url = "https://overpass-api.de/api/interpreter"

payload = r''
with open('buildings.overpassql', 'r') as query:
    payload += (query.read().replace('\n', ''))

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
ax = fig.add_subplot(111, projection="3d")

floor_height = 3
default_height = 10

buildings = building_data["elements"]
buildings_polygons = []

for building in buildings:
    
    # for key, val in building.items():
    #     print(f"{key}: {val}")
    
    geometry = []
    for node in building["geometry"]:
        lat = node["lat"]
        lon = node['lon']

        # Transformation from geographic coordinates to cartesian
        y = radius_earth * math.radians(lat - lat_center) # * math.pi / 180
        x = radius_earth * math.cos(math.radians(lat_center)) * math.radians(lon - lon_center) # * math.pi / 180

        # Normalize coordinates
        x = (x + radius) / (radius * 2)
        y = (y + radius) / (radius * 2)

        geometry.append((x, y))

    if "height" in building["tags"]:
        height_tag = building["tags"]["height"]
        height_tag = height_tag.replace(";", ".")
        height_tag = height_tag.replace(" m", "")

        height = int(float(height_tag))
    elif "building:levels" in building["tags"]:
        levels = int(float(building["tags"]["building:levels"]))
        height = levels * floor_height
    else:
        height = default_height

    height /= (radius * 2)

    geom = np.array(geometry)
    x, y = geom[:, 0], geom[:, 1]

    bottom = np.column_stack((x, y, np.zeros_like(x)))
    top = np.column_stack((x, y, np.full_like(x, height)))

    building_polygon = []
    building_polygon.append(bottom)
    building_polygon.append(top)

    for idx in range(len(x) - 1):
        face = np.array([bottom[idx], bottom[idx + 1], top[idx + 1], top[idx]])
        building_polygon.append(face)
        ax.add_collection3d(Poly3DCollection([face], color='gray'))

    ax.add_collection3d(Poly3DCollection([bottom], color='gray'))
    ax.add_collection3d(Poly3DCollection([top], color='gray'))

    buildings_polygons.append(building_polygon)

# ---

canvas_resolution = (640, 320)
light_position = np.array([1.5, -1.0, 1.0])
camera_position = np.array([1.5, -1.0, 0.8])
focal_length = 1.0

handler = CanvasHandler(canvas_resolution, light_position, camera_position, focal_length)
renderer = AsciiRenderer(canvas_resolution)

handler.process_objects(buildings_polygons)
points = handler.canvas
renderer.render(points)

# ---
look_at = np.array([0.5, 0.5, 0.5])

# Compute view direction vector
view_dir = look_at - camera_position
view_dir /= np.linalg.norm(view_dir)

# Convert to spherical coordinates for elevation and azimuth
r = np.linalg.norm(view_dir)
elev = np.degrees(np.arcsin(view_dir[2]))           # z-component controls elevation
azim = np.degrees(np.arctan2(view_dir[1], view_dir[0]))  # y/x gives azimuth

# Apply the camera view
ax.view_init(elev=elev, azim=azim)
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for x, y, z

# Optional: set axis limits (since your buildings are in [0,1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

# plt.show()
