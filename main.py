import argparse

import numpy as np

from apis.nominatim import NominatimAPI
from apis.overpass import OverpassAPI
from model.builder import ModelBuilder
from render.ascii_renderer import AsciiRenderer
from render.canvas_handler import CanvasHandler


def main(args):
    location = args.location
    radius = args.radius

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ascii-city",
        description="Render 3D ascii image of any location."
    )

    parser.add_argument("-l", "--location", type=str, default="15 E 57th St, New York")
    parser.add_argument("-r", "--radius", type=int, default=250)

    args = parser.parse_args()

    main(args)
