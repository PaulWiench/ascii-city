import fastapi
import numpy as np

from apis.nominatim import NominatimAPI
from apis.overpass import OverpassAPI
from model.builder import ModelBuilder
from render.ascii_renderer import AsciiRenderer
from render.canvas_handler import CanvasHandler


def display_attribution(
        location: str,
        lat_center: float,
        lon_center: float
) -> str:
    info = f"Ascii visualization of '{location}' ({lat_center:.4f}, {lon_center:.4f})\n"
    hint = "Press 10x 'CTRL -' (or 'CTRL SHIFT -') to reduce font size for proper scaling\n"
    attribution = "Data © OpenStreetMaps (https://www.openstreetmap.org/copyright)"

    out = info + hint + attribution
    return out


def main(
    location: str = "15 E 57th St, New York",
    radius: int = 250
) -> str:
    radius = max(0, min(500, radius))

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
    render = renderer.render(points)

    attribution = display_attribution(location, lat_center, lon_center)

    return render + attribution


app = fastapi.FastAPI()

@app.get("/", response_class=fastapi.responses.PlainTextResponse)
def default_render() -> str:
    render = main()

    return render

@app.get("/{location}", response_class=fastapi.responses.PlainTextResponse)
def location_render(
    location: str
) -> str:
    render = main(location)

    return render

@app.get("/{location}/{radius}", response_class=fastapi.responses.PlainTextResponse)
def radius_render(
    location: str,
    radius: int
) -> str:
    render = main(location, radius)

    return render
