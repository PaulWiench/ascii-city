import requests

from db.caching import get_cache, set_cache


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
        cache_key = f"nominatim:{location.lower().replace(' ', '-')}"

        cached = get_cache(cache_key)
        if cached:
            return float(cached["lat"]), float(cached["lon"])

        self.params["q"] = location

        req = requests.get(self.url, params=self.params, headers=self.headers)
        data = req.json()[0]

        lat = data["lat"]
        lon = data["lon"]

        set_cache(cache_key, {"lat": lat, "lon": lon})

        return float(lat), float(lon)
