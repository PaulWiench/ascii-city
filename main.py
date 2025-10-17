import requests
import math

import numpy as np

from ascii_renderer import AsciiRenderer
from canvas_handler import CanvasHandler


class NominatimAPI:
    def __init__(
            self
    ) -> None:
        self.url = "https://nominatim.openstreetmap.org/search"

        self.params = {
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }

        self.headers = {
            "User-Agent": "ascii-city/0.1.0 (wienchpaul@gmail.com)"
        }

    def request_data(
            self,
            location: str
    ) -> tuple:
        self.params["q"] = location

        req = requests.get(self.url, params=self.params, headers=self.headers)
        data = req.json()[0]

        lat = data["lat"]
        lon = data["lon"]

        return float(lat), float(lon)


class OverpassAPI:
    def __init__(
            self
    ) -> None:
        self.url = "https://overpass-api.de/api/interpreter"
        
    def request_data(
            self,
            lat: float,
            lon: float,
            radius: int
    ) -> dict:
        query = f"""
            [out:json];
            (
            way["building"](around:{radius},{lat_center},{lon_center});
            );
            out geom;
            """
        
        req = requests.post(self.url, data=query)
        data = req.json()

        buildings = data["elements"]

        return buildings


location = "Frankfurt"
radius = 250

nom = NominatimAPI()
ovp = OverpassAPI()

lat_center, lon_center = nom.request_data(location)
buildings = ovp.request_data(lat_center, lon_center, radius)


radius_earth = 6371000

floor_height = 3
default_height = 10

buildings_polygons = []

for building in buildings:
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

    buildings_polygons.append(building_polygon)

canvas_resolution = (640, 320)
light_position = np.array([1.5, -1.0, 1.0])
camera_position = np.array([1.5, -1.0, 0.8])
focal_length = 1.0

handler = CanvasHandler(canvas_resolution, light_position, camera_position, focal_length)
renderer = AsciiRenderer(canvas_resolution)

handler.process_objects(buildings_polygons)
points = handler.canvas
renderer.render(points)
