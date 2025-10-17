import requests


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
            way["building"](around:{radius},{lat},{lon});
            );
            out geom;
            """
        
        req = requests.post(self.url, data=query)
        data = req.json()

        buildings = data["elements"]

        return buildings
