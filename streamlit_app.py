import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import requests
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

@dataclass
class MeliponaSpecies:
    name: str
    metabolic_rate: float
    colony_size_factor: int
    ideal_temp: tuple
    humidity_range: tuple
    nest_conductivity: float
    max_cooling: float
    activity_profile: str

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

@dataclass
class Box:
    id: int
    width: float
    height: float
    depth: float
    cooling_effect: float
    propolis_thickness: float = 1.5

def calculate_box_surface_area(width_cm: float, height_cm: float, depth_cm: float) -> float:
    width_m, height_m, depth_m = width_cm / 100, height_cm / 100, depth_cm / 100
    return 2 * (width_m * depth_m + width_m * height_m + depth_m * height_m)

def calculate_metabolic_heat(species: MeliponaSpecies, colony_size_pct: float, altitude: float) -> float:
    oxygen_factor = max(0.5, math.exp(-altitude/7400))
    colony_size = species.colony_size_factor * colony_size_pct
    return colony_size * species.metabolic_rate * oxygen_factor

def adjust_for_species_activity(temp: float, species: MeliponaSpecies, is_daytime: bool) -> float:
    if species.activity_profile == "Diurnal":
        return temp + (3 if is_daytime else -3)
    elif species.activity_profile == "Morning":
        return temp + (4 if is_daytime else -2)
    else:
        return temp + (2 if is_daytime else -4)

def calculate_hive_temperature(species: MeliponaSpecies, params: dict, boxes: List[Box], ambient_temp: float,
                               is_daytime: bool, altitude: float) -> dict:
    adj_temp = ambient_temp - (altitude * 6.5 / 1000)
    adj_temp = adjust_for_species_activity(adj_temp, species, is_daytime)
    metabolic_heat = calculate_metabolic_heat(species, params['colony_size'], altitude)
    nest_resistance = (params['nest_thickness']/1000)/species.nest_conductivity
    total_resistance = nest_resistance + 0.04
    surface_area = sum(calculate_box_surface_area(b.width, b.height, b.depth) for b in boxes)
    if adj_temp > species.ideal_temp[1]:
        cooling = min(species.max_cooling, (adj_temp - species.ideal_temp[1]) * 0.3)
        hive_temp = adj_temp - cooling
    else:
        heat_gain = (metabolic_heat * total_resistance) / surface_area
        hive_temp = adj_temp + min(heat_gain, species.ideal_temp[1] - adj_temp)
    box_temps = []
    for box in boxes:
        propolis_effect = box.propolis_thickness * 0.02
        box_temp = hive_temp - box.cooling_effect + propolis_effect
        box_temps.append(max(species.ideal_temp[0], min(species.ideal_temp[1], box_temp)))
    return {
        'base_temp': hive_temp,
        'box_temps': box_temps,
        'metabolic_heat': metabolic_heat,
        'thermal_resistance': total_resistance
    }

def plot_organic_hive_structure(boxes, temperatures):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    x, y, z, sizes, colors = [], [], [], [], []
    for box, temp in zip(boxes, temperatures):
        num_pots = int(temp * 5)  # Arbitrary scaling for visualization
        x.extend(np.random.uniform(0, box.width, num_pots))
        y.extend(np.random.uniform(0, box.depth, num_pots))
        z.extend(np.random.uniform(0, box.height, num_pots))
        sizes.extend(np.random.uniform(10, 30, num_pots))
        colors.extend([temp] * num_pots)
    
    scatter = ax.scatter(x, y, z, s=sizes, alpha=0.6, c=colors, cmap='YlOrRd')
    
    ax.set_xlabel('Width (cm)')
    ax.set_ylabel('Depth (cm)')
    ax.set_zlabel('Height (cm)')
    ax.set_title('Stingless Bee Hive - Organic Structure')
    
    fig.colorbar(scatter, label='Temperature (°C)')
    
    return fig


def plot_curved_hive_surface(boxes):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for box in boxes:
        x = np.linspace(0, box.width, 50)
        y = np.linspace(0, box.depth, 50)
        X, Y = np.meshgrid(x, y)
        
        Z = 5 * np.sin(X/10) + 5 * np.cos(Y/10)
        
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    
    ax.set_xlabel('Width (cm)')
    ax.set_ylabel('Depth (cm)')
    ax.set_zlabel('Height (cm)')
    ax.set_title('Stingless Bee Hive - Curved Interior Surface')
    
    return fig

def render_species_controls():
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

def main():
    st.set_page_config(page_title="Meliponini Thermal Sim", layout="wide")
    st.title("🍯 Stingless Bee Hive Thermal Simulator")

    species, params = render_species_controls()

    if 'boxes' not in st.session_state:
        if species.name == "Melipona":  # INPA type
            st.session_state.boxes = [
                Box(1, 23, 6, 23, 1.0),
                Box(2, 23, 6, 23, 0.5),
                Box(3, 23, 6, 23, 2.0),
                Box(4, 23, 6, 23, 1.5)
            ]
        else:  # AF type for smaller bees
            st.session_state.boxes = [
                Box(1, 13, 5, 13, 1.0),
                Box(2, 13, 5, 13, 0.5),
                Box(3, 13, 5, 13, 2.0),
                Box(4, 13, 5, 13, 1.5),
                Box(5, 13, 5, 13, 1.0)
            ]

    col1, col2 = st.columns(2)
    with col1:
        lat, lon = map(float, st.text_input("GPS Coordinates", "-3.4653,-62.2159").split(','))
        altitude = get_altitude(lat, lon) or st.slider("Altitude (m)", 0, 1000, 100)
    with col2:
        ambient_temp = get_temperature(lat, lon) or st.slider("Temperature (°C)", 15.0, 40.0, 28.0)
        is_daytime = st.toggle("Daytime", True)

    results = calculate_hive_temperature(species, params, st.session_state.boxes, ambient_temp, is_daytime, altitude)

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

    with st.expander("Advanced Hive Configuration"):
        for box in st.session_state.boxes:
            cols = st.columns(5)
            with cols[0]: box.width = st.number_input(f"Width Box {box.id}", 10, 30, int(box.width))
            with cols[1]: box.height = st.number_input(f"Height Box {box.id}", 5, 20, int(box.height))
            with cols[2]: box.depth = st.number_input(f"Depth Box {box.id}", 10, 30, int(box.depth))
            with cols[3]: box.cooling_effect = st.number_input(f"Cooling Box {box.id}", 0.0, 5.0, box.cooling_effect)
            with cols[4]: box.propolis_thickness = st.number_input(f"Propolis Box {box.id}", 0.0, 5.0, box.propolis_thickness)

    st.subheader("3D Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_organic_hive_structure(st.session_state.boxes, results['box_temps']))
    with col2:
        st.pyplot(plot_curved_hive_surface(st.session_state.boxes))

@st.cache_data
def get_temperature(lat: float, lon: float) -> float:
    try:
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
        return response.json()['current_weather']['temperature']
    except:
        return None

@st.cache_data
def get_weather_data(lat: float, lon: float) -> Dict[str, Any]:
    try:
        api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'] if 'wind' in data else 0,
            'cloudiness': data['clouds']['all'] if 'clouds' in data else 0
        }
    except requests.RequestException:
        return None

# Then use this in main():
weather_data = get_weather_data(lat, lon)
if weather_data:
    ambient_temp = weather_data['temperature']
    # You can now adjust other parameters based on this data
else:
    ambient_temp = st.slider("Temperature (°C)", 15.0, 40.0, 28.0)  # Fallback to manual input

if __name__ == "__main__":
    main()
