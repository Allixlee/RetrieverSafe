from flask import Flask, render_template_string
import folium
from folium.plugins import HeatMap
import csv

app = Flask(__name__)

@app.route("/")
def home():

    m = folium.Map(location=[39.255535, -76.711329],
                    zoom_start=15.5, width=1200, height=630)
    # m = folium.Map(location=[39.255535, -76.711329],
    #                 zoom_start=15.5, width=800, height=500, tiles="CartoDB Voyager")

    # m = folium.Map(location=[39.255535, -76.711329],
    # zoom_start=15.5, width=800, height=500, tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/0/20/{y}{r}.png}",
    # attr = '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
    
    
    lamps = folium.FeatureGroup(name="Lamps", show=False).add_to(m)
    lamp_coords = []
    gradient = {.33: 'purple', .66: 'blue', 1: 'white'}

    with open("lamps.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            print(line)
            lamp_coords.append([float(line[1]), float(line[2])])
            folium.Marker([line[1], line[2]], popup="<i>Center of UMBC").add_to(lamps)

    
    HeatMap(lamp_coords, name="Lamp Light", min_opacity=3, gradient=gradient, radius=7, show=False).add_to(m)
    folium.LayerControl().add_to(m)


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