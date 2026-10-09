import pandas as pd
import folium
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


# ---------------------------------------------------------
# Keep one coordinate per launch-site label
# ---------------------------------------------------------

launch_sites = (
    spacex_df[["Launch Site", "Lat", "Long"]]
    .drop_duplicates(subset="Launch Site")
    .reset_index(drop=True)
)

print(launch_sites)


# ---------------------------------------------------------
# Create map with Esri tiles
# ---------------------------------------------------------

site_map = folium.Map(
    location=[36.0, -100.0],
    zoom_start=4,
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
# Add launch-site markers
# ---------------------------------------------------------

for _, site in launch_sites.iterrows():

    coordinates = [site["Lat"], site["Long"]]

    folium.CircleMarker(
        location=coordinates,
        radius=9,
        weight=2,
        fill=True,
        fill_opacity=0.9,
        tooltip=site["Launch Site"],
        popup=folium.Popup(
            f"""
            <b>{site['Launch Site']}</b><br>
            Latitude: {site['Lat']:.4f}<br>
            Longitude: {site['Long']:.4f}
            """,
            max_width=250
        )
    ).add_to(site_map)

    # Permanent site label
    folium.Marker(
        location=coordinates,
        icon=folium.DivIcon(
            icon_size=(180, 30),
            icon_anchor=(-12, 12),
            html=f"""
                <div style="
                    font-size: 13px;
                    font-weight: bold;
                    white-space: nowrap;
                    background: rgba(255,255,255,0.8);
                    padding: 2px 4px;
                    border-radius: 3px;
                ">
                    {site['Launch Site']}
                </div>
            """
        )
    ).add_to(site_map)


# ---------------------------------------------------------
# Automatically frame all launch sites
# ---------------------------------------------------------

site_map.fit_bounds(
    launch_sites[["Lat", "Long"]].values.tolist(),
    padding=(50, 50)
)


# ---------------------------------------------------------
# Save and open map
# ---------------------------------------------------------

output_file = Path("spacex_launch_sites_map.html").resolve()

site_map.save(str(output_file))

print(f"\nMap saved to:\n{output_file}")

webbrowser.open(output_file.as_uri())