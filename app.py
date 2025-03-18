import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Set up the page title and layout
st.set_page_config(page_title="Weather Dashboard", layout="wide")


# Add a faded background image using custom CSS
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://eg5c9vcv2j9.exactdn.com/wp-content/uploads/2023/07/AdobeStock_440069937-scaled.jpeg?lossy=1&ssl=1');
    background-size: cover;
    background-position: center;
    position: relative;
    overflow-y: scroll;  /* Ensure scrolling is allowed */
    min-height: 100vh;  /* Ensure the content is tall enough to fill the page */
}
[data-testid="stAppViewContainer"]:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);  /* Faded overlay */
    z-index: -1;
}
body {
    overflow-y: auto;  /* Ensure that the body itself is scrollable */
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar for manual location input
st.sidebar.title("Location Input")
city = st.sidebar.text_input("Enter a city name", "Berlin")
latitude = st.sidebar.number_input("Latitude", value=52.52, format="%.2f")
longitude = st.sidebar.number_input("Longitude", value=13.41, format="%.2f")

# Fetch weather data from Meteo API using dynamic latitude and longitude
api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain,showers,snowfall&current=temperature_2m,showers,snowfall,rain"
response = requests.get(api_url)
data = response.json()

# Extract weather details
if "current" in data:
    temp = data["current"]["temperature_2m"]
    rain = data["current"].get("rain", 0)
    snowfall = data["current"].get("snowfall", 0)

    # Determine weather condition and icon
    if rain > 0:
        weather_condition = "Rainy"
        icon = "🌧️"
    elif snowfall > 0:
        weather_condition = "Snowy"
        icon = "❄️"
    else:
        weather_condition = "Sunny"
        icon = "☀️"

    # Display weather details
    st.markdown(f"## {icon} {weather_condition}")
    st.metric(label="🌡️ Temperature", value=f"{temp}°C")
    st.metric(label="🌧️ Rain", value=f"{rain} mm")
    st.metric(label="❄️ Snowfall", value=f"{snowfall} cm")

    if "hourly" in data:
        hourly_data = data["hourly"]
        times = hourly_data["time"]
        temperatures = hourly_data["temperature_2m"]

        # Convert time to pandas datetime
        times = pd.to_datetime(times)

        # Plot the temperature over time
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(times, temperatures, label="Temperature (°C)", color="tab:red")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(f"Temperature vs Time for {city}")
        ax.grid(True)
        ax.legend()
        
        # Show plot in Streamlit
        st.pyplot(fig)

else:
    st.error("Failed to retrieve weather data. Check your location input.")
