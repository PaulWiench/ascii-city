# ascii-city
**ascii-city** is a terminal-based 3D renderer that turns any address into a 3D ascii scene.

Currently only buildings are rendered. So locations with a lot of tall buildings will result in the most interesting renders.

## Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/PaulWiench/ascii-city.git
cd ascii-city
```

The code is built with Python 3.12.5. It is recommended to setup a virtual environment to install the required packages:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required packages inside the virtual environment:
```bash
pip install -r requirements.txt
```

## How to Use
First you need to start a server to run the api application using uvicorn:
```bash
uvicorn main:app --reload
```

The you can fetch an ascii render by specifying a location and a radius (optional) in the url route:
```bash
curl http://127.0.0.1:8000/Johannesburg
curl http://127.0.0.1:8000/Hongkong+20+Pedder+Street
curl http://127.0.0.1:8000/New+York/500
```

Route schema: `url/location/radius`

`location`: Specifies the location to render. Whitespaces have to be replaced with '+' signs.

`radius`: Specifies the radius around the location to render (default: 250, recommended: 100 - 500)

To achieve actually good looking renders the render canvas size is currently hardcoded to a very large value. To be able to see good results, you have to decrease the font size of your terminal emulator. For most emulators this can easily be done by pressing `ctrl -` or `ctrl shift -` a few times. For most setups, decreasing the font size 10 times and maximizing the terminal emulator window yields the best results.

## Examples

**20 Pedder Street, Central, Hongkong**
![Hongkong](data/hongkong.png)

**41 Kruis St, Johannesburg**
![Johannisburg](data/johannisburg.png)

**401 S Hope St, Los Angeles**
![Los Angeles](data/losangeles.png)

## Attribution
This project relies on OSMs Overpass API and Nominatim API. So, huge thanks to the OSM contributors and the whole community!
- [Overpass API](https://overpass-api.de)
- [Nominatim API](https://nominatim.org)

Data © [OpenStreetMap](https://www.openstreetmap.org/copyright)
