import streamlit as st 
import requests
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import plotly.express as px
import datetime

# News API Key
api_key = 'ba4ae72940a44ff69bc820c01fdf9a90'  # Replace with your actual key

if not api_key:
    st.error("API key is missing! Please set it in the script.")
    st.stop()

# Function to fetch earthquake data from USGS
def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    today = datetime.datetime.now(datetime.timezone.utc).date()
    start_date = today - datetime.timedelta(days=30)
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": today,
        "minmagnitude": 4.5,
        "orderby": "time"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch earthquake data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching earthquake data: {e}")
        return None

# Function to fetch disasters from NASA EONET
def fetch_eonet_disasters():
    url = "https://eonet.gsfc.nasa.gov/api/v3/events"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch EONET disaster data. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching EONET disaster data: {e}")
        return None

# Function to fetch disaster-related news
def fetch_disaster_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "earthquake OR wildfire OR storm",  # Only focused disasters
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch disaster news. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching disaster news: {e}")
        return None

# Function to create a map with disaster locations
def create_disaster_map(earthquake_data, eonet_data, selected_disaster):
    disaster_map = folium.Map(location=[20, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(disaster_map)

    # Earthquake markers
    if earthquake_data and selected_disaster in ("All", "Earthquake"):
        for feature in earthquake_data['features']:
            coordinates = feature['geometry']['coordinates']
            magnitude = feature['properties']['mag']
            place = feature['properties']['place']
            folium.Marker(
                [coordinates[1], coordinates[0]],
                popup=f"<b>Earthquake</b><br>{place}<br>Magnitude: {magnitude}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(marker_cluster)

    # Other disasters from EONET
    if eonet_data and "events" in eonet_data:
        for event in eonet_data["events"]:
            if event["geometry"]:
                coords = event["geometry"][0]["coordinates"]
                lon, lat = coords[0], coords[1]
                title = event["title"]
                category = event["categories"][0]["title"]

                if selected_disaster == "All" or selected_disaster.lower() in category.lower():
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"<b>{category}</b><br>{title}",
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(marker_cluster)

    return disaster_map

# --- Streamlit UI ---
st.set_page_config(page_title="Global Disaster Monitor", layout="wide")

st.title("🌎 Global Disaster Monitoring & Visualization System")
st.write("This system provides real-time information on earthquakes, wildfires, storms, and more across the globe.")

# Sidebar
st.sidebar.title("Filters")
selected_disaster = st.sidebar.selectbox(
    "Select Disaster Type",
    ["All", "Earthquake", "Wildfire", "Storm"]  # Only available working types
)

# Fetch Data
earthquake_data = fetch_earthquake_data()
eonet_data = fetch_eonet_disasters()
news_data = fetch_disaster_news()

# Sidebar: Key Events News (with disaster-related filter)
st.sidebar.markdown("""<h3 style="font-size: 18px; color: #FFFFFF; margin-top: 20px;">Key Events</h3>""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <style>
    .marquee-container { height: 300px; overflow: hidden; position: relative; background-color: #f9f9f9; color: #333; padding: 10px; border-radius: 10px; }
    .marquee-content { display: flex; flex-direction: column; animation: moveUp 20s linear infinite; }
    .marquee-item { margin-bottom: 10px; font-size: 16px; font-weight: bold; color: #2e3b4e; animation: flash 2s infinite; }
    @keyframes moveUp { 0% { transform: translateY(100%); } 100% { transform: translateY(-100%); } }
    @keyframes flash { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    .marquee-content:hover { animation-play-state: paused; }
    </style>
""", unsafe_allow_html=True)

marquee_content = ""
if news_data and news_data.get('articles'):
    for article in news_data['articles']:
        if any(keyword in article['title'].lower() for keyword in ['earthquake', 'wildfire', 'storm']):
            marquee_content += f'<div class="marquee-item"><a href="{article["url"]}" target="_blank" style="color: #2e3b4e; text-decoration: none;">{article["title"]}</a></div>'
else:
    marquee_content += "<div class='marquee-item'>No disaster news available at the moment.</div>"

st.sidebar.markdown(f'<div class="marquee-container"><div class="marquee-content">{marquee_content}</div></div>', unsafe_allow_html=True)

# Display Disaster Map
st.header("📍 Disaster Locations on Map")
disaster_map = create_disaster_map(earthquake_data, eonet_data, selected_disaster)
st.components.v1.html(disaster_map._repr_html_(), height=600)

# Real-time Disaster Details Table
st.header("🗂️ Real-time Disaster Details")

# Prepare earthquake data
earthquake_records = []
if earthquake_data and "features" in earthquake_data:
    for feature in earthquake_data["features"]:
        coords = feature['geometry']['coordinates']
        earthquake_records.append({
            "Type": "Earthquake",
            "Location": feature["properties"]["place"],
            "Magnitude/Title": f"Magnitude {feature['properties']['mag']}",
            "Date": datetime.datetime.utcfromtimestamp(feature["properties"]["time"] / 1000).strftime('%Y-%m-%d %H:%M UTC')
        })

# Prepare wildfire and storm data
eonet_records = []
wildfire_data = []  # To collect wildfire data for histogram
if eonet_data and "events" in eonet_data:
    for event in eonet_data["events"]:
        category = event["categories"][0]["title"]
        if category.lower() in ["wildfires", "storms"]:
            event_time = event["geometry"][0]["date"]
            coords = event["geometry"][0]["coordinates"]
            eonet_records.append({
                "Type": category[:-1] if category.endswith('s') else category,  # Remove 's' from Wildfires -> Wildfire
                "Location": f"Lat: {coords[1]}, Lon: {coords[0]}",
                "Magnitude/Title": event["title"],
                "Date": datetime.datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M UTC')
            })
            if category.lower() == "wildfires":
                wildfire_data.append(event)

# Combine all records
all_disasters = earthquake_records + eonet_records

# Create DataFrame
if all_disasters:
    disaster_df = pd.DataFrame(all_disasters)
    st.dataframe(disaster_df, use_container_width=True)
else:
    st.write("No real-time disasters to display currently.")

# Earthquake Histogram
if earthquake_data and "features" in earthquake_data:
    magnitudes = [feature["properties"]["mag"] for feature in earthquake_data["features"]]

    # Create histogram
    st.header("🌍 Earthquake Magnitude Trend Over Time")
    fig = px.histogram(
        x=magnitudes,
        labels={"x": "Magnitude", "y": "Count of Earthquakes"},
        title="Distribution of Earthquake Magnitudes",
        nbins=30
    )
    st.plotly_chart(fig)



# Wildfire Histogram
if wildfire_data:
    wildfire_dates = [event["geometry"][0]["date"] for event in wildfire_data]
    wildfire_dates = [datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for date in wildfire_dates]

    # Create histogram
    st.header("🔥 Wildfire Trend Over Time")
    fig = px.histogram(
        x=wildfire_dates,
        labels={"x": "Date of Wildfire", "y": "Count of Wildfires"},
        title="Distribution of Wildfires Over Time",
        nbins=30
    )
    st.plotly_chart(fig)

# --- Overview Section ---
st.header("📝 Overview and Summary")

st.markdown("""
- **Data Sources**: Earthquake data from USGS, Disaster events from NASA EONET.
- **Disasters Covered**: Earthquakes, Wildfires, Storms.
- **Visualization**: Real-time interactive map and disaster magnitude distribution.
- **Live News**: Latest disaster-related news headlines scrolling on the sidebar.

> Stay aware. Stay safe. 🌍
""")
