import json
import requests
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from ascii_renderer import AsciiRenderer
from canvas_handler import CanvasHandler


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
ax = fig.add_subplot(111, projection="3d")

floor_height = 3
default_height = 10

buildings = building_data["elements"]
building = buildings[0]

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

if "building:levels" in building["tags"]:
    levels = int(building["tags"]["building:levels"])
    height = levels * floor_height
else:
    height = default_height

height /= radius

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

# ---

canvas_resolution = (160, 80)
light_position = np.array([1.0, 0.4, 0.8])
camera_position = np.array([0.5, -1.0, 0.5])
focal_length = 1.0

handler = CanvasHandler(canvas_resolution, light_position, camera_position, focal_length)
renderer = AsciiRenderer(canvas_resolution)

# Define vertices of a cube floating in the middle of a unit room
cube_verts = np.array([
    # x     y     z
    [0.25, 0.25, 0.25], # 0: bottom front left corner
    [0.75, 0.25, 0.25], # 1: bottom front right corner
    [0.75, 0.75, 0.25], # 2: bottom back right corner
    [0.25, 0.75, 0.25], # 3: bottom back left corner
    [0.25, 0.25, 0.75], # 4: top front left corner
    [0.75, 0.25, 0.75], # 5: top front right corner
    [0.75, 0.75, 0.75], # 6: top back right corner
    [0.25, 0.75, 0.75]  # 7: top back left corner
])

# # # Define faces of the cube
cube_faces = np.array([
    [0, 1, 2, 3], # 0: bottom
    [4, 5, 6, 7], # 1: top
    [0, 1, 5, 4], # 2: front
    [1, 2, 6, 5], # 3: right
    [2, 3, 7, 6], # 4: back
    [3, 0, 4, 7]  # 5: left
])

cube = []
for face in cube_faces:
    face_verts = cube_verts[face]
    cube.append(face_verts)

cubes = [cube]

buildings_polygons = [building_polygon]

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

plt.show()
