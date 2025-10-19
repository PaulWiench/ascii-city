import requests

from db.caching import get_cache, set_cache


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
        cache_key = f"nominatim:{lat}-{lon}-{radius}"

        cached = get_cache(cache_key)
        if cached:
            return cached["buildings"]

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

        set_cache(cache_key, {"buildings": buildings}, ttl_days=3)

        return buildings
