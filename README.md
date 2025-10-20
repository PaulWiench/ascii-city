# ascii-city
**ascii-city** is a terminal-based 3D renderer that turns any address into a 3D ASCII scene.

**api.ascii-city.com**

Currently only buildings are rendered. So locations with a lot of tall buildings will result in the most interesting renders.

## Usage
You can render your location from the shell or a web browser by using curl and specifying a location and a radius (optional) in the url route:
```bash
curl https://api.ascii-city.com/Johannesburg
curl https://api.ascii-city.com/Hongkong+20+Pedder+Street
curl https://api.ascii-city.com/New+York/500
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

## Local Installation and Usage
### From Source
Clone the repository to your local machine:
```bash
git clone https://github.com/PaulWiench/ascii-city.git
cd ascii-city
```

The code is built with Python 3.12.5. It is recommended to setup a virtual environment to install the required packages:
```bash
pyenv local 3.12.5
python -m venv .venv
source .venv/bin/activate
```

Install the required packages inside the virtual environment:
```bash
pip install -r requirements.txt
```

Install uvicorn to host a local server:
```bash
pip install uvicorn
```

Start a server to run the api application using uvicorn:
```bash
uvicorn src.main:app --reload
```

Then you can fetch an ascii render as explained above:
```bash
curl http://127.0.0.1:8000/Amsterdam
```

### With Docker
Pull latest image from [Docker Hub](https://hub.docker.com/repository/docker/lospaulos/ascii-city/general):
```bash
docker pull lospaulos/ascii-city:latest
```

Run the image as a container with published port:
```bash
docker run -p 8000:80 lospaulos/ascii-city:latest
```

Then you can fetch an ascii render as explained above:
```bash
curl http://localhost:8000/Amsterdam
```

## Attribution
This project relies on OSMs Overpass API and Nominatim API. So, huge thanks to the OSM contributors and the whole community!
- [Overpass API](https://overpass-api.de)
- [Nominatim API](https://nominatim.org)

Data © [OpenStreetMap](https://www.openstreetmap.org/copyright)
