from flask import Flask, render_template
import folium
from folium.plugins import HeatMap
import csv
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    # Initialize map without tiles
    m = folium.Map(location=[39.255535, -76.711329],
                   zoom_start=16, tiles=None)
    
    # Add map tiles and store them in variables
    day_tile = folium.TileLayer(tiles="OpenStreetMap", name="Day Mode").add_to(m)
    night_tile = folium.TileLayer(
        tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
        attr="<a href=https://docs.stadiamaps.com/map-styles/alidade-smooth-dark/>Alidade Smooth Dark</a>",
        name="Night Mode", show=False
    ).add_to(m)

    # Add layers and get their names
    lamp_coords = []
    gradient = {.33: 'yellow', .66: 'orange', 1: 'white'}
    with open("lamps.csv", mode="r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            lamp_coords.append([float(line[1]), float(line[2])])
    lamp_layer = HeatMap(lamp_coords, name="Lamps", min_opacity=3,
                         gradient=gradient, radius=7, show=False).add_to(m)
    
    sos_layer = folium.FeatureGroup(name="Emergency Resources", show=False).add_to(m)
    with open("sos.csv", mode="r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup="SOS Phone",
                          icon=folium.Icon(color="blue",
                          icon="fa-solid fa-bell", prefix="fa")).add_to(sos_layer)
    folium.Marker([39.25984373757963, -76.71630620628858],
                  popup="Baltimore County Police Department",
                  icon=folium.Icon(color="darkblue",
                  icon="fa-solid fa-shield-dog", prefix="fa")).add_to(sos_layer)
    folium.Marker([39.25727885338491, -76.7141845789751],
                  popup="UMBC Campus Police Department",
                  icon=folium.Icon(color="darkblue",
                  icon="fa-solid fa-shield-dog", prefix="fa")).add_to(sos_layer)

    construction_layer = folium.FeatureGroup(name="Construction Closures", show=False).add_to(m)
    with open("construction.csv", mode="r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup="Closed for construction",
                          icon=folium.Icon(color="red",
                          icon="fa-solid fa-screwdriver-wrench", prefix="fa")).add_to(construction_layer)

    lactation_layer = folium.FeatureGroup(name="Lactation Rooms", show=False).add_to(m)
    with open("lactation_rooms.csv", mode="r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup=line[0],
                          tooltip="Click for the location in this building",
                          icon=folium.Icon(color="lightred",
                          icon="fa-solid fa-person-breastfeeding", prefix="fa")).add_to(lactation_layer)

    family_restrooms_layer = folium.FeatureGroup(name="Family Friendly Restrooms", show=False).add_to(m)
    with open("family_restrooms.csv", mode="r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup=line[0],
                          tooltip="Click for locations inside this building",
                          icon=folium.Icon(color="lightblue",
                          icon="fa-solid fa-baby", prefix="fa")).add_to(family_restrooms_layer)
            
    # reshapes csv into array of coordinates
    accessibility_layer = folium.FeatureGroup(name="Handicap Accessible Routes", show=False).add_to(m)
    locations = []
    location_lines = []
    with open("accessibility_routes.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            locations.append(line)

    for i in locations:
        location_lines.append(np.reshape(i, (-1,2)))

    # adds polylines to map for accessibility routes
    folium.PolyLine(
        locations=location_lines,
        line_cap="square",
        color="#167CB9",
        opacity=0.8,
        weight=2.5
    ).add_to(accessibility_layer)

    # Remove built-in LayerControl
    # folium.LayerControl().add_to(m)

    # Get layer and map names
    lamp_layer_name = lamp_layer.get_name()
    sos_layer_name = sos_layer.get_name()
    construction_layer_name = construction_layer.get_name()
    lactation_layer_name = lactation_layer.get_name()
    family_restrooms_layer_name = family_restrooms_layer.get_name()
    accessibility_layer_name = accessibility_layer.get_name()
    map_name = m.get_name()

    # Get tile layer names
    day_tile_name = day_tile.get_name()
    night_tile_name = night_tile.get_name()

    # Save and render the map
    m.save("map.html")
    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()
    
    return render_template(
        "index.html",
        header=header,
        body_html=body_html,
        script=script,
        lamp_layer_name=lamp_layer_name,
        sos_layer_name=sos_layer_name,
        construction_layer_name=construction_layer_name,
        lactation_layer_name=lactation_layer_name,
        family_restrooms_layer_name=family_restrooms_layer_name,
        accessibility_layer_name=accessibility_layer_name,
        day_tile_name=day_tile_name,
        night_tile_name=night_tile_name,
        map_name=map_name
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
