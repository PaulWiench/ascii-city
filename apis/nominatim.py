import requests


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
