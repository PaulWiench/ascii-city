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
    x = radius_earth * (lat - lat_center) * math.pi / 180
    y = radius_earth * math.cos(lat_center) * (lon - lon_center) * math.pi / 180

    # Normalize coordinates
    x /= radius
    y /= radius

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

sides = []
for idx in range(len(x) - 1):
    verts = [[bottom[idx], bottom[idx + 1], top[idx + 1], top[idx]]]
    sides.append(verts)
    ax.add_collection3d(Poly3DCollection(verts, color='gray'))

print(sides)

ax.add_collection3d(Poly3DCollection([bottom], color='gray'))
ax.add_collection3d(Poly3DCollection([top], color='gray'))

plt.show()

# ---

# canvas_resolution = (80, 40)
# light_position = np.array([1.0, 0.4, 0.8])
# camera_position = np.array([1.5, -2.0, 1.0])
# focal_length = 2.0

# handler = CanvasHandler(canvas_resolution, light_position, camera_position, focal_length)
# renderer = AsciiRenderer(canvas_resolution)

# # Define vertices of a cube floating in the middle of a unit room
# cube_verts = np.array([
#     # x     y     z
#     [0.25, 0.25, 0.25], # 0: bottom front left corner
#     [0.75, 0.25, 0.25], # 1: bottom front right corner
#     [0.75, 0.75, 0.25], # 2: bottom back right corner
#     [0.25, 0.75, 0.25], # 3: bottom back left corner
#     [0.25, 0.25, 0.75], # 4: top front left corner
#     [0.75, 0.25, 0.75], # 5: top front right corner
#     [0.75, 0.75, 0.75], # 6: top back right corner
#     [0.25, 0.75, 0.75]  # 7: top back left corner
# ])

# # # Define faces of the cube
# cube_faces = np.array([
#     [0, 1, 2, 3], # 0: bottom
#     [4, 5, 6, 7], # 1: top
#     [0, 1, 5, 4], # 2: front
#     [1, 2, 6, 5], # 3: right
#     [2, 3, 7, 6], # 4: back
#     [3, 0, 4, 7]  # 5: left
# ])

# cube_front_verts = cube_verts[cube_faces[2]]

# sideways_rectangle_verts = np.array([
#     [0.5, 0.5, 0.25],
#     [0.75, 0.5, 0.5],
#     [0.5, 0.5, 0.75],
#     [0.25, 0.5, 0.5]
# ])

# weird_shape_verts = np.array([
#     [0.1, 0.5, 0.1],
#     [0.5, 0.5, 0.4],
#     [0.9, 0.5, 0.1],
#     [0.9, 0.5, 0.9],
#     [0.3, 0.5, 0.8],
#     [0.5, 0.5, 0.9],
#     [0.1, 0.5, 0.9],
#     [0.1, 0.5, 0.7],
#     [0.4, 0.5, 0.4]
# ])

# cube = []
# for face in cube_faces:
#     face_verts = cube_verts[face]
#     cube.append(face_verts)

# cubes = [cube]

# handler.process_objects(cubes)
# points = handler.canvas
# renderer.render(points)

