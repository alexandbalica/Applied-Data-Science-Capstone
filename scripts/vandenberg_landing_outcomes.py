import pandas as pd
import folium
from folium.plugins import MarkerCluster
import webbrowser
from pathlib import Path


# ---------------------------------------------------------
# Load SpaceX geospatial dataset
# ---------------------------------------------------------

DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
)

spacex_df = pd.read_csv(DATA_URL)

# Keep the columns used in the original Coursera Folium notebook
spacex_df = spacex_df[
    ["Launch Site", "Lat", "Long", "class"]
].copy()


# ---------------------------------------------------------
# Translate class into meaningful landing outcomes
# ---------------------------------------------------------

spacex_df["Landing Outcome"] = spacex_df["class"].map({
    1: "Success",
    0: "Failed"
})

spacex_df["marker_color"] = spacex_df["class"].map({
    1: "green",
    0: "red"
})


# ---------------------------------------------------------
# Focus on Vandenberg / California
# ---------------------------------------------------------

SITE = "VAFB SLC-4E"

site_df = spacex_df[
    spacex_df["Launch Site"] == SITE
].copy()

site_lat = site_df["Lat"].iloc[0]
site_lon = site_df["Long"].iloc[0]


# ---------------------------------------------------------
# Create focused map using Esri tiles
# ---------------------------------------------------------

site_map = folium.Map(
    location=[site_lat, site_lon],
    zoom_start=10,
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
# Highlight the launch site
# ---------------------------------------------------------

folium.Circle(
    location=[site_lat, site_lon],
    radius=1500,
    color="#333333",
    weight=2,
    fill=False,
    popup=SITE
).add_to(site_map)

folium.Marker(
    location=[site_lat, site_lon],
    icon=folium.DivIcon(
        icon_size=(180, 30),
        icon_anchor=(-10, 15),
        html=f"""
        <div style="
            font-size:14px;
            font-weight:bold;
            white-space:nowrap;
            background:rgba(255,255,255,0.85);
            padding:3px 6px;
            border-radius:4px;
        ">
            {SITE}
        </div>
        """
    )
).add_to(site_map)


# ---------------------------------------------------------
# Add success / failure launch markers
# ---------------------------------------------------------

marker_cluster = MarkerCluster(
    name="Landing Outcomes"
).add_to(site_map)

for index, record in site_df.iterrows():

    folium.Marker(
        location=[record["Lat"], record["Long"]],
        popup=folium.Popup(
            f"""
            <b>{record['Launch Site']}</b><br>
            Landing Outcome: <b>{record['Landing Outcome']}</b>
            """,
            max_width=250
        ),
        tooltip=record["Landing Outcome"],
        icon=folium.Icon(
            color=record["marker_color"],
            icon="info-sign"
        )
    ).add_to(marker_cluster)


# ---------------------------------------------------------
# Add a simple legend
# ---------------------------------------------------------

legend_html = """
<div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    width: 155px;
    background-color: white;
    border: 2px solid #999;
    z-index: 9999;
    font-size: 14px;
    padding: 10px;
">
    <b>Landing Outcome</b><br>
    <span style="color:green;">●</span> Success<br>
    <span style="color:red;">●</span> Failed
</div>
"""

site_map.get_root().html.add_child(
    folium.Element(legend_html)
)


# ---------------------------------------------------------
# Save and open
# ---------------------------------------------------------

output_file = Path(
    "vandenberg_landing_outcomes_map.html"
).resolve()

site_map.save(str(output_file))

print(f"Map saved to:\n{output_file}")
print(f"\nVandenberg records: {len(site_df)}")
print(site_df["Landing Outcome"].value_counts())

webbrowser.open(output_file.as_uri())