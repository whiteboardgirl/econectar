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

def get_temperature_from_coordinates(lat, lon):
    """Fetch current temperature from Open-Meteo API with enhanced error handling."""
    # Validate coordinates
    if not (-90 <= lat <= 90):
        st.error("Invalid latitude. Must be between -90 and 90.")
        return None
    if not (-180 <= lon <= 180):
        st.error("Invalid longitude. Must be between -180 and 180.")
        return None
    
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}¤t_weather=true'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['current_weather']['temperature']
    else:
        error_data = response.json()
        st.error(f"Failed to fetch weather data. Status code: {response.status_code}. Error: {error_data.get('error', 'Unknown error')}")
        st.write(f"Debug Info - URL: {url}")  # This will show the exact URL used in the request
    return None

def calculate_oxygen_factor(altitude_m):
    """Calculate oxygen factor based on altitude."""
    P0 = 1013.25  # Standard atmospheric pressure at sea level (hPa)
    H = 7400  # Scale height for Earth's atmosphere (m)
    pressure_ratio = math.exp(-altitude_m / H)
    return max(0.6, pressure_ratio)

def calculate_box_surface_area(width_cm, height_cm):
    """Calculate surface area for a hexagonal box in square meters."""
    width_m, height_m = width_cm / 100, height_cm / 100
    side_length = width_m / math.sqrt(3)
    hexagon_area = (3 * math.sqrt(3) / 2) * (side_length ** 2)
    sides_area = 6 * side_length * height_m
    return (2 * hexagon_area) + sides_area

def calculate_heat_transfer(temp_hive_k, temp_ambient_k, total_surface_area, total_resistance):
    """Calculate heat transfer in Watts."""
    return (total_surface_area * abs(temp_hive_k - temp_ambient_k)) / total_resistance

def adjust_for_time_of_day(is_daytime, params):
    """Adjust parameters based on time of day in tropical conditions."""
    if is_daytime:
        params['ideal_hive_temperature'] += 0.5  # Slight increase in ideal temperature due to activity
    else:
        params['ideal_hive_temperature'] -= 0.5  # Slight decrease due to less activity
    return params

def calculate_hive_temperature(params, boxes, ambient_temp_c, is_daytime):
    """Calculate hive temperature with adjustments for tropical conditions in Colombia."""
    params = adjust_for_time_of_day(is_daytime, params)
    
    ambient_temp_k, ideal_temp_k = ambient_temp_c + 273.15, params['ideal_hive_temperature'] + 273.15
    calculated_colony_size = 50000 * (params['colony_size'] / 100)
    oxygen_factor = calculate_oxygen_factor(params['altitude'])
    colony_metabolic_heat = calculated_colony_size * params['bee_metabolic_heat'] * oxygen_factor

    total_volume = sum(
        (3 * math.sqrt(3) / 2) * ((box['width'] / (100 * math.sqrt(3))) ** 2) * (box['height'] / 100)
        for box in boxes
    )
    total_surface_area = sum(calculate_box_surface_area(box['width'], box['height']) for box in boxes)
    
    wood_resistance = (params['wood_thickness'] / 100) / params['wood_thermal_conductivity']
    total_resistance = wood_resistance + params['air_film_resistance_outside']

    # Adjustments for tropical conditions
    if ambient_temp_c >= params['ideal_hive_temperature']:
        # In tropical conditions, cooling is more critical during the day
        cooling_effort = min(1.0, (ambient_temp_c - params['ideal_hive_temperature']) / 10)  # Less aggressive cooling due to high humidity
        temp_decrease = 1.5 * cooling_effort if is_daytime else 0.5 * cooling_effort  # More cooling during the day
        estimated_temp_c = max(params['ideal_hive_temperature'], ambient_temp_c - temp_decrease)
    else:
        # Minimal heating needed at night due to warm ambient conditions
        heat_contribution = min(
            params['ideal_hive_temperature'] - ambient_temp_c,
            (colony_metabolic_heat * total_resistance) / total_surface_area
        )
        # Since nights are warm, less heat is needed
        heat_contribution = heat_contribution * 0.8  # reducing heat contribution
        estimated_temp_c = ambient_temp_c + heat_contribution
    
    estimated_temp_c = min(50, max(0, estimated_temp_c))
    estimated_temp_k = estimated_temp_c + 273.15

    final_heat_transfer = calculate_heat_transfer(
        estimated_temp_k,
        ambient_temp_k,
        total_surface_area,
        total_resistance
    )

    box_temperatures = [
        max(0, min(50, estimated_temp_c - box['cooling_effect']))
        for box in boxes
    ]

    return {
        'calculated_colony_size': calculated_colony_size,
        'colony_metabolic_heat': colony_metabolic_heat / 1000,
        'base_temperature': estimated_temp_c,
        'box_temperatures': box_temperatures,
        'total_volume': total_volume,
        'total_surface_area': total_surface_area,
        'thermal_resistance': total_resistance,
        'ambient_temperature': ambient_temp_c,
        'oxygen_factor': oxygen_factor,
        'heat_transfer': final_heat_transfer / 1000
    }

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
    
    # User input for GPS coordinates with enhanced guidance
    gps_coordinates = st.text_input("Enter GPS Coordinates (lat, lon)", "4.6097, -74.0817", help="Enter in decimal degrees format, e.g., '4.6097, -74.0817' for Bogotá, Colombia")
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
    
    # Ensure oxygen_factor is between 0 and 1 for st.progress()
    progress_value = (oxygen_factor - 0.6) / (1.0 - 0.6)  # Normalize to 0-1 range if oxygen_factor is between 0.6 and 1.0
    
    st.progress(progress_value)
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
