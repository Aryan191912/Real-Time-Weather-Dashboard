import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from config import API_KEY

# Auto Refresh every 60 seconds
st_autorefresh(interval=60000, key="refresh")


st.set_page_config(
    page_title="Real-Time Weather Dashboard",
    page_icon="🌦️",
    layout="centered"
)

# Title
st.markdown(
    "<h1 style='text-align:center;color:#00BFFF;'>🌦️ Real-Time Weather Dashboard</h1>",
    unsafe_allow_html=True
)

# Last Updated Time
st.caption(f"🕒 Last Updated: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}")

# Sidebar
st.sidebar.title("🌍 Weather Dashboard")
st.sidebar.write("Search weather of any city in the world")


city = st.text_input("Enter City Name", "Delhi")

# API URL
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]

    weather = data["weather"][0]["main"]
    description = data["weather"][0]["description"]

    country = data["sys"]["country"]

    # Weather Icon
    icon = data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    st.success(f"🌍 Weather in {city}, {country}")

    st.image(icon_url, width=100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌡️ Temperature", f"{temperature} °C")
        st.metric("💧 Humidity", f"{humidity}%")

    with col2:
        st.metric("🌬️ Wind Speed", f"{wind} m/s")
        st.metric("📈 Pressure", f"{pressure} hPa")

    st.subheader("🌤️ Weather Condition")
    st.write(f"**{weather}**")
    st.write(description.title())

    # Data Table
    df = pd.DataFrame({
        "Parameter": [
            "Temperature",
            "Humidity",
            "Pressure",
            "Wind Speed"
        ],
        "Value": [
            temperature,
            humidity,
            pressure,
            wind
        ]
    })

    st.subheader("📋 Weather Data")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Weather Chart")
    st.bar_chart(df.set_index("Parameter"))

else:
    st.error("❌ Invalid City Name or API Key")

st.markdown("---")
st.markdown(
    "<center>Made with ❤️ by Aryan | Powered by OpenWeather API</center>",
    unsafe_allow_html=True
)