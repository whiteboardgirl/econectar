import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import requests
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# ========================
# Species Configuration
# ========================

@dataclass
class MeliponaSpecies:
    name: str
    metabolic_rate: float # W/bee
    colony_size_factor: int # Bees per percentage
    ideal_temp: tuple # (min, max) in °C
    humidity_range: tuple # optimal RH range
    nest_conductivity: float # W/m·K
    max_cooling: float # Max cooling capacity (°C)
    activity_profile: str # Diurnal pattern

SPECIES_CONFIG = {
    "Small (e.g., Tetragonula)": MeliponaSpecies(
        name="Tetragonula",
        metabolic_rate=0.0028,
        colony_size_factor=400,
        ideal_temp=(28, 31),
        humidity_range=(60, 80),
        nest_conductivity=0.07,
        max_cooling=1.2,
        activity_profile="Evening"
    ),
    "Medium (e.g., Melipona)": MeliponaSpecies(
        name="Melipona",
        metabolic_rate=0.0035,
        colony_size_factor=700,
        ideal_temp=(30, 33),
        humidity_range=(50, 75),
        nest_conductivity=0.09,
        max_cooling=1.5,
        activity_profile="Diurnal"
    ),
    "Large (e.g., Scaptotrigona)": MeliponaSpecies(
        name="Scaptotrigona",
        metabolic_rate=0.0042,
        colony_size_factor=1000,
        ideal_temp=(31, 35),
        humidity_range=(40, 70),
        nest_conductivity=0.11,
        max_cooling=1.8,
        activity_profile="Morning"
    )
}

# ========================
# Core Models
# ========================

@dataclass
class Box:
    id: int
    width: float # cm
    height: float # cm
    cooling_effect: float
    propolis_thickness: float = 1.5 # mm

# ========================
# Thermal Calculations
# ========================

def calculate_box_surface_area(width_cm: float, height_cm: float) -> float:
    """
    Calculate the total surface area for a hexagonal box in square meters.
    Assumes a hexagon-based design where the width defines the distance between parallel sides.
    """
    width_m, height_m = width_cm / 100, height_cm / 100
    side_length = width_m / math.sqrt(3)
    hexagon_area = (3 * math.sqrt(3) / 2) * (side_length ** 2)
    sides_area = 6 * side_length * height_m
    return (2 * hexagon_area) + sides_area

def calculate_metabolic_heat(species: MeliponaSpecies, colony_size_pct: float, altitude: float) -> float:
    """Calculate colony metabolic heat with altitude compensation."""
    oxygen_factor = max(0.5, math.exp(-altitude/7400))
    colony_size = species.colony_size_factor * colony_size_pct
    return colony_size * species.metabolic_rate * oxygen_factor

def adjust_for_species_activity(temp: float, species: MeliponaSpecies, is_daytime: bool) -> float:
    """Apply species-specific diurnal adjustments."""
    if species.activity_profile == "Diurnal":
        return temp + (3 if is_daytime else -3)
    elif species.activity_profile == "Morning":
        return temp + (4 if is_daytime else -2)
    else: # Evening
        return temp + (2 if is_daytime else -4)

def calculate_hive_temperature(species: MeliponaSpecies, params: dict, boxes: List[Box], ambient_temp: float,
                               is_daytime: bool, altitude: float) -> dict:
    """Core thermal model adapted for stingless bees."""
    # Environmental adjustments
    adj_temp = ambient_temp - (altitude * 6.5 / 1000)
    adj_temp = adjust_for_species_activity(adj_temp, species, is_daytime)

    # Metabolic calculations
    metabolic_heat = calculate_metabolic_heat(species, params['colony_size'], altitude)

    # Nest material properties
    nest_resistance = (params['nest_thickness']/1000)/species.nest_conductivity
    total_resistance = nest_resistance + 0.04 # Air film resistance

    # Thermal equilibrium calculation
    surface_area = sum(calculate_box_surface_area(b.width, b.height) for b in boxes)
    if adj_temp > species.ideal_temp[1]:
        cooling = min(species.max_cooling, (adj_temp - species.ideal_temp[1]) * 0.3)
        hive_temp = adj_temp - cooling
    else:
        heat_gain = (metabolic_heat * total_resistance) / surface_area
        hive_temp = adj_temp + min(heat_gain, species.ideal_temp[1] - adj_temp)

    # Box temperature adjustments
    box_temps = []
    for box in boxes:
        propolis_effect = box.propolis_thickness * 0.02 # 0.02°C/mm insulation
        box_temp = hive_temp - box.cooling_effect + propolis_effect
        box_temps.append(max(species.ideal_temp[0], min(species.ideal_temp[1], box_temp)))

    return {
        'base_temp': hive_temp,
        'box_temps': box_temps,
        'metabolic_heat': metabolic_heat,
        'thermal_resistance': total_resistance
    }

# ========================
# 3D Visualization Functions
# ========================

def plot_hive_honey_distribution(boxes, honey_volumes):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for box, honey_volume in zip(boxes, honey_volumes):
        # Generate random positions for honey pots within the box dimensions
        num_pots = int(honey_volume / 10)  # Assume each pot holds about 10 ml
        x = np.random.uniform(0, box.width, num_pots)
        y = np.random.uniform(0, box.height, num_pots)
        z = np.random.uniform(0, honey_volume, num_pots)
        
        ax.scatter(x, y, z, s=50, alpha=0.6)
    
    ax.set_xlabel('Width (cm)')
    ax.set_ylabel('Height (cm)')
    ax.set_zlabel('Honey Volume (ml)')
    ax.set_title('Stingless Bee Honey Pot Distribution')
    
    return fig

def plot_box_characteristics_3d(boxes, temperatures):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    x = [box.width for box in boxes]
    y = [box.height for box in boxes]
    z = [box.cooling_effect for box in boxes]
    
    scatter = ax.scatter(x, y, z, c=temperatures, cmap='coolwarm', s=100)
    
    ax.set_xlabel('Width (cm)')
    ax.set_ylabel('Height (cm)')
    ax.set_zlabel('Cooling Effect')
    ax.set_title('Box Characteristics and Temperature')
    
    fig.colorbar(scatter, label='Temperature (°C)')
    
    return fig

def plot_box_temperatures_3d(boxes, temperatures):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    x = [box.width for box in boxes]
    y = [box.height for box in boxes]
    z = np.zeros_like(x)
    
    dx = dy = 1  # Width of each bar
    dz = temperatures
    
    ax.bar3d(x, y, z, dx, dy, dz, shade=True)
    
    ax.set_xlabel('Width (cm)')
    ax.set_ylabel('Height (cm)')
    ax.set_zlabel('Temperature (°C)')
    ax.set_title('Box Temperatures')
    
    return fig

# ========================
# UI Components
# ========================

def render_species_controls():
    """Species selection and configuration."""
    species_name = st.sidebar.selectbox("Bee Species", list(SPECIES_CONFIG.keys()))
    species = SPECIES_CONFIG[species_name]
    st.sidebar.markdown(f"**{species.name} Characteristics:**")
    st.sidebar.write(f"- Ideal Temp: {species.ideal_temp[0]}–{species.ideal_temp[1]}°C")
    st.sidebar.write(f"- Humidity Range: {species.humidity_range[0]}–{species.humidity_range[1]}% RH")
    st.sidebar.write(f"- Activity Pattern: {species.activity_profile}")
    params = {
        'colony_size': st.sidebar.slider("Colony Size (%)", 0, 100, 50),
        'nest_thickness': st.sidebar.slider("Nest Wall Thickness (mm)", 1.0, 10.0, 5.0),
        'rain_intensity': st.sidebar.slider("Rain Intensity", 0.0, 1.0, 0.0)
    }
    return species, params

# ========================
# Main Application
# ========================

def main():
    st.set_page_config(page_title="Meliponini Thermal Sim", layout="wide")
    st.title("🍯 Stingless Bee Hive Thermal Simulator")

    # Initialize session state
    if 'boxes' not in st.session_state:
        st.session_state.boxes = [
            Box(1, 18, 8, 1.0),
            Box(2, 18, 8, 0.5),
            Box(3, 22, 10, 2.0),
            Box(4, 20, 9, 1.5)
        ]
    elif len(st.session_state.boxes) != 4:
        while len(st.session_state.boxes) < 4:
            new_id = len(st.session_state.boxes) + 1
            st.session_state.boxes.append(Box(new_id, 20, 9, 1.5))
        st.session_state.boxes = st.session_state.boxes[:4]

    # Species configuration
    species, params = render_species_controls()

    # Environmental inputs
    col1, col2 = st.columns(2)
    with col1:
        lat, lon = map(float, st.text_input("GPS Coordinates", "-3.4653,-62.2159").split(','))
        altitude = get_altitude(lat, lon) or st.slider("Altitude (m)", 0, 1000, 100)
    with col2:
        ambient_temp = get_temperature(lat, lon) or st.slider("Temperature (°C)", 15.0, 40.0, 28.0)
        is_daytime = st.toggle("Daytime", True)

    # Thermal calculations
    results = calculate_hive_temperature(species, params, st.session_state.boxes, ambient_temp, is_daytime, altitude)

    # Results display
    st.subheader("Thermal Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Hive Core Temperature", f"{results['base_temp']:.1f}°C")
        st.metric("Metabolic Heat Output", f"{results['metabolic_heat']:.2f} W")
    with col2:
        fig, ax = plt.subplots()
        ax.bar([f"Box {i+1}" for i in range(len(results['box_temps']))], results['box_temps'])
        ax.set_ylim(species.ideal_temp[0]-2, species.ideal_temp[1]+2)
        st.pyplot(fig)

    # Box configuration
    with st.expander("Advanced Hive Configuration"):
        for box in st.session_state.boxes:
            cols = st.columns(4)
            with cols[0]: box.width = st.number_input(f"Width Box {box.id}", 10, 30, int(box.width))
            with cols[1]: box.height = st.number_input(f"Height Box {box.id}", 5, 20, int(box.height))
            with cols[2]: box.cooling_effect = st.number_input(f"Cooling Box {box.id}", 0.0, 5.0, box.cooling_effect)
            with cols[3]: box.propolis_thickness = st.number_input(f"Propolis Box {box.id}", 0.0, 5.0, box.propolis_thickness)

    # 3D Visualizations
    st.subheader("3D Visualizations")
    col1, col2 = st.columns(2)

    with col1:
        fig_surface = plot_hive_temperature_surface(st.session_state.boxes, results['box_temps'])
        st.pyplot(fig_surface)

    with col2:
        fig_scatter = plot_box_characteristics_3d(st.session_state.boxes, results['box_temps'])
        st.pyplot(fig_scatter)

    st.subheader("Box Temperature Comparison")
    fig_bar = plot_box_temperatures_3d(st.session_state.boxes, results['box_temps'])
    st.pyplot(fig_bar)

# Helper functions for API calls
@st.cache_data
def get_temperature(lat: float, lon: float) -> float:
    try:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
        return response.json()['current_weather']['temperature']
    except:
        return None

@st.cache_data
def get_altitude(lat: float, lon: float) -> float:
    try:
        response = requests.get(f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}")
        return response.json()['results'][0]['elevation']
    except:
        return None

if __name__ == "__main__":
    main()
