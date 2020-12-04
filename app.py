from flask import Flask, request
import folium
import requests

app = Flask(__name__)

def get_lat_lon(address):
    url='https://nominatim.openstreetmap.org/search'
    response = requests.get(url, params={'q': address,'format': 'json'})
    if response.status_code != 200:
        return None, None
    data = response.json()
    return float(data[0]["lat"]), float(data[0]["lon"])

def get_radius(address, radius):
    lat_lon = get_lat_lon(address)
    m = folium.Map(location=lat_lon, zoom_start=8)
    folium.Marker(lat_lon, popup=address, tooltip= "You you are here").add_to(m)
    folium.Circle(
        radius= radius,
        location=lat_lon,
        color='green',
        fill=True,
    ).add_to(m)
    return m._repr_html_()

@app.route('/', methods=['POST'])
def call_method():
    address = request.form['address']
    radius = request.form['radius']
    return get_radius(address, radius)
@app.route('/')

def index():
    return '''
    <form method='POST'>
        <label for="address">Address:</label>
            <input type="text" id="address" name="address"><br><br>
        <label for="radius">Radius you can travel (in meters):</label>
            <input type="text" id="radius" name="radius"><br><br>
         <input type="submit" value="Submit">
    </form>
    '''
