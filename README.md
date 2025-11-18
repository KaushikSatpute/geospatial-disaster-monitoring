# geospatial-disaster-monitoring

# 🌍 AI-Powered Geospatial Disaster Monitoring System

A real-time, interactive application developed using **Streamlit** to aggregate and visualize global disaster events, leveraging geospatial data APIs.

## ✨ Features

* **Real-time Data Integration:** Fetches up-to-the-minute data from multiple authoritative sources.
* **Interactive Mapping:** Visualizes disaster locations (e.g., wildfires, earthquakes) on a dynamic map.
* **Filtering & Analysis:** Allows users to filter events by type, region, or time, and view related trends.
* **Intuitive UI:** Built with Streamlit for easy accessibility and seamless data exploration.

## 🛠️ Technology Stack

* **Core Language:** Python
* **Front-End/Framework:** **Streamlit** (for the web application UI)
* **Geospatial Visualization:** **Folium**
* **Data Analysis & Charting:** **Plotly**
* **APIs Integrated:**
    * **USGS** (e.g., earthquake data)
    * **NASA EONET** (Earth Observatory Natural Event Tracker)
    * **News API** (for contextually relevant news articles)

## 🚀 Setup and Installation

### Prerequisites

You need **Python 3.8+** installed.

### 1. Clone the repository

```bash
git clone https://github.com/KaushikSatpute/geospatial-disaster-monitoring
cd ai_geospatial_disaster_monitoring
````

### 2\. Create and activate a virtual environment

It's highly recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate  # On Windows
```

### 3\. Install dependencies

```bash
pip install -r requirements.txt
```

### 4\. Configure API Keys (Crucial Step\!)

**You must set up your API keys as environment variables.**

1.  Obtain keys for your services (e.g., News API).

2.  Create a file named `.env` in the root directory (make sure it's ignored by Git, see the `.gitignore` section below).

3.  Add your keys to the `.env` file:

    ```
    NEWS_API_KEY="YOUR_NEWS_API_KEY_HERE"
    # Other potential keys (if applicable, e.g., MAPBOX_KEY)
    ```

4.  Modify the Python script to read these variables securely using the `dotenv` library.

### 5\. Run the Application

```bash
streamlit run app.py
```

The application will launch in your web browser.

## 📁 Project Structure

```
├── ai_geospatial_disaster_monitoring/
│   ├── app.py              # Main Streamlit application file
│   ├── data_fetcher.py     # Script to handle API calls (USGS, EONET, News)
│   ├── requirements.txt    # List of project dependencies
│   ├── .gitignore          # Specifies files/folders to ignore (e.g., .env, venv/)
├── README.md             # This file
```

## 🤝 Contribution

Feel free to open issues or submit pull requests to improve the project\!
