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

def adjust_for_time_of_day(is_daytime, params, altitude):
    """Adjust parameters based on time of day and altitude in tropical conditions."""
    if is_daytime:
        # During the day, increase cooling effort due to higher activity and solar radiation
        params['ideal_hive_temperature'] += 1.0  # Slight increase in ideal temperature due to activity
        params['bee_metabolic_heat'] *= 1.1  # Increase metabolic heat slightly
    else:
        # At night, decrease ideal temp slightly due to less activity and clustering behavior
        params['ideal_hive_temperature'] -= 0.5  # Slight decrease due to less activity
        params['air_film_resistance_outside'] *= 1.1  # Slight increase in resistance due to less wind at night
    
    # Adjust for altitude
    oxygen_factor = calculate_oxygen_factor(altitude)
    params['bee_metabolic_heat'] *= oxygen_factor  # Adjust metabolic heat based on oxygen availability
    params['air_film_resistance_outside'] *= (1 + (altitude / 1000) * 0.05)  # Increase resistance slightly with altitude due to potential wind increase

    # Temperature decrease with altitude
    params['ideal_hive_temperature'] -= (altitude / 1000) * 0.5  # Decrease ideal temp by 0.5°C per 1000m
    
    return params

def adjust_for_time_of_day(is_daytime, params, altitude):
    """Adjust parameters based on time of day and altitude in tropical conditions."""
    if is_daytime:
        # During the day, increase cooling effort due to higher activity and solar radiation
        params['ideal_hive_temperature'] += 1.0  # Slight increase in ideal temperature due to activity
        params['bee_metabolic_heat'] *= 1.1  # Increase metabolic heat slightly
    else:
        # At night, decrease ideal temp slightly due to less activity and clustering behavior
        params['ideal_hive_temperature'] -= 0.5  # Slight decrease due to less activity
        params['air_film_resistance_outside'] *= 1.1  # Slight increase in resistance due to less wind at night
    
    # Adjust for altitude
    oxygen_factor = calculate_oxygen_factor(altitude)
    params['bee_metabolic_heat'] *= oxygen_factor  # Adjust metabolic heat based on oxygen availability
    params['air_film_resistance_outside'] *= (1 + (altitude / 1000) * 0.05)  # Increase resistance slightly with altitude due to potential wind increase

    # Temperature decrease with altitude
    params['ideal_hive_temperature'] -= (altitude / 1000) * 0.5  # Decrease ideal temp by 0.5°C per 1000m
    
    return params

def calculate_hive_temperature(params, boxes, ambient_temp_c, is_daytime, altitude):
    """Calculate hive temperature with adjustments for tropical conditions in Colombia including altitude."""
    params = adjust_for_time_of_day(is_daytime, params, altitude)
    
    ambient_temp_k, ideal_temp_k = ambient_temp_c + 273.15, params['ideal_hive_temperature'] + 273.15
    calculated_colony_size = 50000 * (params['colony_size'] / 100)
    oxygen_factor = calculate_oxygen_factor(altitude)
    colony_metabolic_heat = calculated_colony_size * params['bee_metabolic_heat'] * oxygen_factor

    total_volume = sum(
        (3 * math.sqrt(3) / 2) * ((box['width'] / (100 * math.sqrt(3))) ** 2) * (box['height'] / 100)
        for box in boxes
    )
    total_surface_area = sum(calculate_box_surface_area(box['width'], box['height']) for box in boxes)
    
    wood_resistance = (params['wood_thickness'] / 100) / params['wood_thermal_conductivity']
    total_resistance = wood_resistance + params['air_film_resistance_outside']

    if ambient_temp_c >= params['ideal_hive_temperature']:
        # In tropical conditions, cooling is more critical during the day
        cooling_effort = min(1.0, (ambient_temp_c - params['ideal_hive_temperature']) / 10)  # Less aggressive cooling due to high humidity
        temp_decrease = 2.0 * cooling_effort if is_daytime else 1.0 * cooling_effort  # More cooling during the day
        estimated_temp_c = max(params['ideal_hive_temperature'], ambient_temp_c - temp_decrease)
    else:
        # Minimal heating needed at night due to warm ambient conditions
        heat_contribution = min(
            params['ideal_hive_temperature'] - ambient_temp_c,
            (colony_metabolic_heat * total_resistance) / total_surface_area
        )
        # Since nights are warm, less heat is needed, but still some clustering effect
        heat_contribution = heat_contribution * 0.9 if not is_daytime else heat_contribution  # Slight increase for night clustering
        estimated_temp_c = ambient_temp_c + heat_contribution
    
    # Adjust for altitude's effect on temperature
    estimated_temp_c -= (altitude / 1000) * 0.5  # Decrease estimated temp by 0.5°C per 1000m
    
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
