import folium
import webbrowser
from pathlib import Path
from math import sin, cos, sqrt, atan2, radians
from folium.features import DivIcon


# ---------------------------------------------------------
# Launch site: Space Launch Complex 40
# ---------------------------------------------------------

launch_site = {
    "name": "CCAFS SLC-40",
    "lat": 28.5620,
    "lon": -80.5772
}


# ---------------------------------------------------------
# Representative points of interest
# ---------------------------------------------------------

pois = [
    {
        "name": "Cape Canaveral City Hall",
        "type": "City",
        "lat": 28.384548,
        "lon": -80.605434
    },
    {
        "name": "FEC Railway — Titusville",
        "type": "Railway",
        "lat": 28.6077778,
        "lon": -80.8097778
    },
    {
        "name": "SR 401 Barge Canal Bridge",
        "type": "Highway",
        "lat": 28.40889,
        "lon": -80.63194
    }
]


# ---------------------------------------------------------
# Haversine distance
# ---------------------------------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# ---------------------------------------------------------
# Create map
# ---------------------------------------------------------

site_map = folium.Map(
    location=[launch_site["lat"], launch_site["lon"]],
    zoom_start=9,
    tiles=None
)

folium.TileLayer(
    tiles=(
        "https://server.arcgisonline.com/ArcGIS/rest/services/"
        "World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    ),
    attr="Esri",
    name="Esri World Street Map",
    overlay=False,
    control=False
).add_to(site_map)


# ---------------------------------------------------------
# Add launch-site marker
# ---------------------------------------------------------

launch_coordinate = [
    launch_site["lat"],
    launch_site["lon"]
]

folium.CircleMarker(
    location=launch_coordinate,
    radius=11,
    weight=3,
    fill=True,
    fill_opacity=0.9,
    tooltip=launch_site["name"],
    popup=launch_site["name"]
).add_to(site_map)

folium.Marker(
    location=launch_coordinate,
    icon=DivIcon(
        icon_size=(180, 30),
        icon_anchor=(-10, 15),
        html=f"""
        <div style="
            font-size:14px;
            font-weight:bold;
            background:white;
            padding:4px 7px;
            border-radius:4px;
            white-space:nowrap;
        ">
            {launch_site["name"]}
        </div>
        """
    )
).add_to(site_map)


# ---------------------------------------------------------
# Add POIs, distance lines, and labels
# ---------------------------------------------------------

for poi in pois:

    poi_coordinate = [
        poi["lat"],
        poi["lon"]
    ]

    distance = calculate_distance(
        launch_site["lat"],
        launch_site["lon"],
        poi["lat"],
        poi["lon"]
    )

    print(
        f"{poi['type']} — {poi['name']}: "
        f"{distance:.2f} km"
    )

    # POI marker
    folium.CircleMarker(
        location=poi_coordinate,
        radius=8,
        weight=2,
        fill=True,
        fill_opacity=0.9,
        tooltip=f"{poi['type']}: {poi['name']}",
        popup=(
            f"<b>{poi['name']}</b><br>"
            f"Type: {poi['type']}<br>"
            f"Distance: {distance:.2f} km"
        )
    ).add_to(site_map)

    # POI label
    folium.Marker(
        location=poi_coordinate,
        icon=DivIcon(
            icon_size=(220, 35),
            icon_anchor=(-10, 15),
            html=f"""
            <div style="
                font-size:13px;
                font-weight:bold;
                background:rgba(255,255,255,0.9);
                padding:3px 6px;
                border-radius:4px;
                white-space:nowrap;
            ">
                {poi['type']}: {poi['name']}
            </div>
            """
        )
    ).add_to(site_map)

    # Distance line
    folium.PolyLine(
        locations=[
            launch_coordinate,
            poi_coordinate
        ],
        weight=3,
        opacity=0.8,
        tooltip=f"{poi['type']}: {distance:.2f} km"
    ).add_to(site_map)

    # Midpoint distance label
    midpoint = [
        (launch_site["lat"] + poi["lat"]) / 2,
        (launch_site["lon"] + poi["lon"]) / 2
    ]

    folium.Marker(
        location=midpoint,
        icon=DivIcon(
            icon_size=(110, 30),
            icon_anchor=(25, 10),
            html=f"""
            <div style="
                font-size:12px;
                font-weight:bold;
                background:white;
                border:1px solid #555;
                padding:3px 5px;
                border-radius:4px;
                white-space:nowrap;
            ">
                {distance:.1f} km
            </div>
            """
        )
    ).add_to(site_map)


# ---------------------------------------------------------
# Fit map around all points
# ---------------------------------------------------------

all_coordinates = [
    launch_coordinate
] + [
    [poi["lat"], poi["lon"]]
    for poi in pois
]

site_map.fit_bounds(
    all_coordinates,
    padding=(80, 80)
)


# ---------------------------------------------------------
# Legend
# ---------------------------------------------------------

legend_html = """
<div style="
    position: fixed;
    bottom: 35px;
    left: 35px;
    width: 190px;
    background-color: white;
    border: 1px solid #777;
    z-index: 9999;
    font-size: 13px;
    padding: 10px 14px;
    border-radius: 5px;
">
    <b>Proximity Analysis</b><br>
    ● Launch Site<br>
    ● City<br>
    ● Railway<br>
    ● Highway<br>
    ━ Straight-line distance
</div>
"""

site_map.get_root().html.add_child(
    folium.Element(legend_html)
)


# ---------------------------------------------------------
# Save and open
# ---------------------------------------------------------

output_file = Path(
    "ccafs_slc40_poi_proximity.html"
).resolve()

site_map.save(str(output_file))

print(f"\nMap saved to:\n{output_file}")

webbrowser.open(output_file.as_uri())