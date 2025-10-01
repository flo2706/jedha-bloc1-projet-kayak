"""
Streamlit app — Top-N Hotels by City

Purpose:
    - Load the final enriched dataset (hotels + coordinates).
    - Let the user pick a city, minimum rating, and N hotels.
    - Display hotels on a Folium map with auto-center/zoom and colored markers.

Inputs:
    - CSV file: env var HOTELS_CSV or default ../Load/database/hotels_weather_final_ter.csv

Output:
    - Interactive map + UI (no file output)

Notes:
    - Dataset is cached with st.cache_data.
    - Marker color: 🟢 ≥ 9.0, 🟠 8.0–8.9, 🔴 < 8.0.
"""

import os
import html
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Config 
CSV_PATH = os.getenv(
    "HOTELS_CSV",
    "data/hotels_weather_final_ter.csv"  # default path
)

def color_by_rating(r: float) -> str:
    """Map rating to a Folium marker color."""
    if pd.isna(r):
        return "gray"
    if r >= 9.0:
        return "green"
    if r >= 8.0:
        return "orange"
    return "red"

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    """Load and lightly clean the hotels dataset."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    # Keep only rows with rating and valid coordinates
    df = df.dropna(subset=["hotel_rating", "hotel_latitude", "hotel_longitude"])
    df["hotel_rating"] = pd.to_numeric(df["hotel_rating"], errors="coerce")
    df = df.dropna(subset=["hotel_rating"])
    return df

# Load data 
df = load_data(CSV_PATH)

# Page title
st.markdown(
    "<h1 style='text-align:center; margin-top:0;'>Top Hotels by City (France)</h1>",
    unsafe_allow_html=True
)

# Sidebar filters 
with st.sidebar:
    st.markdown("### Filters")
    cities = sorted(df["city_name"].dropna().unique())
    selected_city = st.selectbox("Choose a city", cities, index=0)
    min_rating = st.slider("Minimum rating", 0.0, 10.0, 8.0, 0.1)
    top_n = st.slider("Number of hotels", min_value=5, max_value=30, value=20, step=5)

# Filter & sort 
city_df = (
    df[df["city_name"] == selected_city]
    .sort_values(by="hotel_rating", ascending=False)
)
city_df = city_df[city_df["hotel_rating"] >= min_rating].head(top_n)

# Empty state
if city_df.empty:
    st.warning(f"No hotels meeting the criteria in **{selected_city}**.")
    st.stop()

# City title 
nb_hotels = len(city_df)
st.markdown(
    f"<h2 style='text-align:center;'>Top {nb_hotels} Hotels in {html.escape(selected_city)}</h2>",
    unsafe_allow_html=True
)

# Build map (auto-center + auto-zoom) 
m = folium.Map(tiles="OpenStreetMap")
bounds = city_df[["hotel_latitude", "hotel_longitude"]].values.tolist()
m.fit_bounds(bounds)

# Cluster markers only if many points
cluster = MarkerCluster().add_to(m) if nb_hotels > 10 else m

for _, row in city_df.iterrows():
    name = row.get("hotel_name", "Unknown Hotel")
    rating = row.get("hotel_rating", None)
    url = row.get("hotel_url", "#")
    desc = row.get("hotel_description", "")

    safe_name = html.escape(str(name))
    safe_desc = html.escape(str(desc))[:300] + ("..." if len(str(desc)) > 300 else "")
    rating_txt = f"{rating:.1f}" if pd.notna(rating) else "N/A"

    popup_html = f"""
    <div style="font-size:13px; line-height:1.3;">
      <strong>{safe_name}</strong><br>
      <em>Rating:</em> {rating_txt}<br>
      <em>Description:</em> {safe_desc}<br>
      <a href="{html.escape(str(url))}" target="_blank" rel="noopener noreferrer">🔗 View on Booking</a>
    </div>
    """

    folium.Marker(
        location=[row["hotel_latitude"], row["hotel_longitude"]],
        popup=folium.Popup(popup_html, max_width=320),
        icon=folium.Icon(color=color_by_rating(row["hotel_rating"]), icon="info-sign")
    ).add_to(cluster)

# Render map 
st_folium(m, width=1000, height=600)

# Legend 
st.markdown("**Legend:** 🟢 ≥ 9.0 🟠 8.0–8.9 🔴 < 8.0")
