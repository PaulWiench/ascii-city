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
    ) -> list:
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


class ModelBuilder:
    def __init__(
            self,
            lat_center: float,
            lon_center: float,
            radius: int
    ) -> None:
        self.radius_earth = 6371000
        self.default_floor_height = 3
        self.default_building_height = 10

        self.lat_center = lat_center
        self.lon_center = lon_center
        self.radius = radius

    def geographic_to_cartesian(
            self,
            lat: float,
            lon: float
    ) -> tuple:
        x = self.radius_earth * math.cos(math.radians(self.lat_center)) * math.radians(lon - self.lon_center)
        y = self.radius_earth * math.radians(lat - self.lat_center)

        x = (x + self.radius) / (self.radius * 2)
        y = (y + self.radius) / (self.radius * 2)

        return x, y
    
    def compute_building_height(
            self,
            tags: dict
    ) -> float:
        if "height" in tags:
            height_tag = tags["height"]
            height_tag = height_tag.replace(";", ".")
            height_tag = height_tag.replace(" m", "")

            height = int(float(height_tag))
        
        elif "building:levels" in tags:
            levels = int(float(tags["building:levels"]))

            height = levels * self.default_floor_height
        
        else:
            height = self.default_building_height

        height /= (self.radius * 2)

        return height

    def compute_buildings_faces(
            self,
            buildings: list
    ) -> list:
        buildings_faces = []

        for building in buildings:
            building_vertices = []
            building_faces = []

            for vertex in building["geometry"]:
                lat = vertex["lat"]
                lon = vertex["lon"]

                x, y = self.geographic_to_cartesian(lat, lon)
                building_vertices.append((x, y))
            
            height = self.compute_building_height(building["tags"])

            building_vertices = np.array(building_vertices)
            x, y = building_vertices[:, 0], building_vertices[:, 1]

            bottom = np.column_stack((x, y, np.zeros_like(x)))
            building_faces.append(bottom)

            top = np.column_stack((x, y, np.full_like(x, height)))
            building_faces.append(top)

            for idx in range(len(x) - 1):
                wall = np.array([bottom[idx], bottom[idx + 1], top[idx + 1], top[idx]])
                building_faces.append(wall)

            buildings_faces.append(building_faces)

        return buildings_faces


location = "Frankfurt"
radius = 250

nom = NominatimAPI()
ovp = OverpassAPI()

lat_center, lon_center = nom.request_data(location)
buildings = ovp.request_data(lat_center, lon_center, radius)

builder = ModelBuilder(lat_center, lon_center, radius)

buildings_faces = builder.compute_buildings_faces(buildings)

canvas_resolution = (640, 320)
light_position = np.array([1.5, -1.0, 1.0])
camera_position = np.array([1.5, -1.0, 0.8])
focal_length = 1.0

handler = CanvasHandler(canvas_resolution, light_position, camera_position, focal_length)
renderer = AsciiRenderer(canvas_resolution)

handler.process_objects(buildings_faces)
points = handler.canvas
renderer.render(points)
