from flask import Flask, render_template_string
import folium
from folium.plugins import HeatMap
import csv

app = Flask(__name__)

@app.route("/")
def home():
    # initialize map
    m = folium.Map(location=[39.255535, -76.711329],
                    zoom_start=15.5, width=1200, height=630)
    # m = folium.Map(location=[39.255535, -76.711329],
    #                 zoom_start=15.5, width=800, height=500, tiles="CartoDB Voyager")

    # m = folium.Map(location=[39.255535, -76.711329],
    # zoom_start=15.5, width=800, height=500, tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/0/20/{y}{r}.png}",
    # attr = '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
    
    # adds lamps layer
    lamps = folium.FeatureGroup(name="Lamps", show=False).add_to(m)
    lamp_coords = []
    gradient = {.33: 'yellow', .66: 'orange', 1: 'white'}
    with open("lamps.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            lamp_coords.append([float(line[1]), float(line[2])])
            folium.Marker([line[1], line[2]], popup="lamp", icon=folium.Icon(color="beige",icon="fa-solid fa-lightbulb",prefix="fa")).add_to(lamps)
            # folium.Marker([line[1], line[2]], popup="lamp", icon=lamp_icon).add_to(lamps)
    HeatMap(lamp_coords, name="Lamp Light", min_opacity=3, gradient=gradient, radius=7, show=False).add_to(m)

    # add sos emergency lamps layer
    sos = folium.FeatureGroup(name="SOS Lamps", show=False).add_to(m)
    with open("sos.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup="SOS Lamp", icon=folium.Icon(color="lightblue",icon="fa-regular fa-bell",prefix="fa")).add_to(sos)

    # adds layer controls to map
    folium.LayerControl().add_to(m)


    # convert folium map to html
    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        {{header|safe}}
        <body>
            <h1>RetrieverSafe</h1>
            {{body_html|safe}}
            <script>
                {{script|safe}}
            </script>
        <body>
    </html>
    """, header=header, body_html=body_html, script=script)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)