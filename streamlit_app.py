import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests

# Set page config
st.set_page_config(
    page_title="Hive Thermal Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .stSlider > div > div > div > div {
        background-color: #4CAF50;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# API key for OpenWeatherMap (Replace with your actual API key)
OPENWEATHERMAP_API_KEY = 'your_api_key_here'

def get_temperature_from_coordinates(lat, lon):
    """Fetch current temperature from OpenWeatherMap API."""
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp']
    else:
        st.error(f"Failed to fetch weather data. Status code: {response.status_code}")
        return None

def calculate_oxygen_factor(altitude_m):
    # ... (previous functions remain unchanged)
    pass

def calculate_box_surface_area(width_cm, height_cm):
    # ... (previous functions remain unchanged)
    pass

def calculate_heat_transfer(temp_hive_k, temp_ambient_k, total_surface_area, total_resistance):
    # ... (previous functions remain unchanged)
    pass

def adjust_for_time_of_day(is_daytime, params):
    # ... (previous functions remain unchanged)
    pass

def calculate_hive_temperature(params, boxes, ambient_temp_c, is_daytime):
    # ... (previous functions remain unchanged)
    pass

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.boxes = [
        {'id': i+1, 'width': 22, 'length': 26, 'height': 9, 'cooling_effect': ce}
        for i, ce in enumerate([2, 0, 0, 8])
    ]

# Page header
st.title("🐝 Hive Thermal Dashboard")
st.markdown("---")

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Input Parameters")
    
    # User input for GPS coordinates
    gps_coordinates = st.text_input("Enter GPS Coordinates (lat, lon)", "4.6097, -74.0817")  # Default is Bogotá, Colombia
    try:
        lat, lon = map(float, gps_coordinates.split(','))
        ambient_temperature = get_temperature_from_coordinates(lat, lon)
        if ambient_temperature is None:
            ambient_temperature = 25.0  # Default temp if API fails
    except ValueError:
        st.error("Please enter valid coordinates in the format 'lat, lon'")
        ambient_temperature = 25.0  # Default temp if input is invalid
    
    # User selects whether it's day or night
    is_daytime = st.radio("Time of Day", ['Day', 'Night'], index=0, help="Select whether it's day or night")
    
    st.write(f"Current Ambient Temperature: {ambient_temperature}°C")
    
    colony_size = st.slider("Colony Size (%)", 0, 100, 50)
    altitude = st.slider("Altitude (meters)", 0, 3800, 0, 100)
    oxygen_factor = calculate_oxygen_factor(altitude)
    st.progress(oxygen_factor)
    st.caption(f"Oxygen Factor: {oxygen_factor:.2f}")

    st.subheader("📦 Box Configuration")
    for i, box in enumerate(st.session_state.boxes):
        with st.expander(f"Box {box['id']}", expanded=True):
            st.session_state.boxes[i]['cooling_effect'] = st.number_input(
                "Cooling Effect (°C)", 0.0, 20.0, float(box['cooling_effect']), 0.5, key=f"cooling_effect_{i}"
            )

# Parameters dictionary
params = {
    'colony_size': colony_size,
    'bee_metabolic_heat': 0.0040,  # Watts per bee
    'wood_thickness': 2.0,  # cm
    'wood_thermal_conductivity': 0.13,  # W/(m⋅K) for pine wood
    'air_film_resistance_outside': 0.04,  # m²K/W
    'altitude': altitude,  # meters
    'ideal_hive_temperature': 35.0  # °C
}

# Convert radio selection to boolean
is_daytime = is_daytime == 'Day'

# Calculate results
results = calculate_hive_temperature(params, st.session_state.boxes, ambient_temperature, is_daytime)

# Display results
with col2:
    st.subheader("📈 Analysis Results")
    
    col2a, col2b = st.columns(2)
    with col2a:
        st.metric("Base Hive Temperature", f"{results['base_temperature']:.1f}°C")
        st.metric("Ambient Temperature", f"{results['ambient_temperature']:.1f}°C")
    with col2b:
        st.metric("Colony Size", f"{int(results['calculated_colony_size']):,} bees")
        st.metric("Metabolic Heat", f"{results['colony_metabolic_heat']:.3f} kW")

    st.subheader("📊 Box Temperatures")
    for i, temp in enumerate(results['box_temperatures']):
        st.markdown(f"**Box {i+1}:** {temp:.1f}°C")
        progress_value = max(0.0, min(1.0, temp / 50))
        st.progress(progress_value)

    # Add a graph for temperature distribution
    fig, ax = plt.subplots()
    ax.bar([f'Box {i+1}' for i in range(len(results['box_temperatures']))], results['box_temperatures'])
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Distribution Across Hive Boxes')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    st.markdown(f'<img src="data:image/png;base64,{b64}"/>', unsafe_allow_html=True)
    
    with st.expander("🔍 Detailed Thermal Characteristics", expanded=True):
        st.markdown(f"""
        - **Total Volume:** {results['total_volume']:.4f} m³
        - **Total Surface Area:** {results['total_surface_area']:.4f} m²
        - **Thermal Resistance:** {results['thermal_resistance']:.4f} m²K/W
        - **Heat Transfer:** {results['heat_transfer']:.3f} kW
        """)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit • Thermal analysis for beekeeping with GPS-based temperature using Open-Meteo API*")
