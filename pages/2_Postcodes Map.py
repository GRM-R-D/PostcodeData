from __future__ import annotations

import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.write("## Dynamic layer control updates")

START_LOCATION = [53.134414, -1.871720]
START_ZOOM = 5

if "feature_group" not in st.session_state:
    st.session_state["feature_group"] = None

# Load GeoJSON data
geojson_file = "postcodes.geojson"
gdf = gpd.read_file(geojson_file)

# Example of properties to access
print(gdf.head())

# Define style function based on AVG PL_mea
def style_function_pl(x):
    return {
        "fillColor": "#1100f8",  # Example color
        "color": "#1100f8",      # Example color
        "fillOpacity": 0.3,      # Example opacity
        "weight": 2,
    }

# Define style function based on AVG LL_mea
def style_function_ll(x):
    return {
        "color": "#ff3939",      # Example color
        "fillOpacity": 0.3,      # Example opacity
        "weight": 3,
        "opacity": 1,
        "dashArray": "5, 5",
    }

# Create folium GeoJson objects
polygon_folium1 = folium.GeoJson(data=gdf,
                                  style_function=style_function_pl,
                                  name="AVG PL_mea")
polygon_folium2 = folium.GeoJson(data=gdf,
                                  style_function=style_function_ll,
                                  name="AVG LL_mea")

map = folium.Map(
    location=START_LOCATION,
    zoom_start=START_ZOOM,
    tiles="OpenStreetMap",
    max_zoom=5,
)

# Create FeatureGroups
fg1 = folium.FeatureGroup(name="AVG PL_mea")
fg1.add_child(polygon_folium1)

fg2 = folium.FeatureGroup(name="AVG LL_mea")
fg2.add_child(polygon_folium2)

fg_dict = {"AVG PL_mea": fg1, "AVG LL_mea": fg2, "None": None, "Both": [fg1, fg2]}

control = folium.LayerControl(collapsed=False)

# Streamlit interface
fg = st.radio("Feature Group", ["AVG PL_mea", "AVG LL_mea", "None", "Both"])
layer = st.radio("Layer Control", ["yes", "no"])

layer_dict = {"yes": control, "no": None}

st_folium(
    map,
    width=800,
    height=450,
    returned_objects=[],
    feature_group_to_add=fg_dict[fg],
    debug=True,
    layer_control=layer_dict[layer],
)
