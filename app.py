import streamlit as st
import requests

# Set up the page title and layout
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Add a background image
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: ("bg.jpg");
    background-size: cover;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar for manual location input
st.sidebar.title("Location Input")
city = st.sidebar.text_input("Enter a city name", "Berlin")
latitude = st.sidebar.number_input("Latitude", value=52.52, format="%.2f")
longitude = st.sidebar.number_input("Longitude", value=13.41, format="%.2f")

# Fetch weather data from Meteo API
api_url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,rain,showers,snowfall&current=temperature_2m,is_day,showers,snowfall,rain"
response = requests.get(api_url)
data = response.json()

# Extract weather details
if "current" in data:
    temp = data["current"]["temperature_2m"]
    rain = data["current"].get("rain", 0)
    snowfall = data["current"].get("snowfall", 0)
    is_day = data["current"]["is_day"]

    # Determine weather condition and icon
    if rain > 0:
        weather_condition = "Rainy"
        icon = "🌧️"
    elif snowfall > 0:
        weather_condition = "Snowy"
        icon = "❄️"
    elif is_day:
        weather_condition = "Sunny"
        icon = "☀️"
    else:
        weather_condition = "Clear Night"
        icon = "🌙"

    # Display weather details
    st.markdown(f"## {icon} {weather_condition}")
    st.metric(label="🌡️ Temperature", value=f"{temp}°C")
    st.metric(label="🌧️ Rain", value=f"{rain} mm")
    st.metric(label="❄️ Snowfall", value=f"{snowfall} cm")
else:
    st.error("Failed to retrieve weather data. Check your location input.")

