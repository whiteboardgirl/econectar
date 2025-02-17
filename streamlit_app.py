import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go
import requests
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class BeeSpecies:
    name: str
    metabolic_rate: float  # W per bee (arbitrary unit)
    colony_size_factor: int  # base colony size number
    ideal_temp: Tuple[float, float]  # ideal temperature range (min, max) in °C
    humidity_range: Tuple[float, float]  # ideal humidity range in %
    nest_conductivity: float  # thermal conductivity (W/m·K)
    max_cooling: float  # maximum cooling capacity in °C
    activity_profile: str  # e.g., "Diurnal", "Morning", etc.

@dataclass
class HiveBox:
    id: int
    width: float  # in cm
    height: float  # in cm
    depth: float  # in cm
    cooling_effect: float  # cooling factor specific to the box
    propolis_thickness: float = 1.5  # in mm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SPECIES_CONFIG: Dict[str, BeeSpecies] = {
    "Melipona": BeeSpecies(
        name="Melipona",
        metabolic_rate=0.0035,
        colony_size_factor=700,
        ideal_temp=(30.0, 33.0),
        humidity_range=(50.0, 70.0),
        nest_conductivity=0.09,
        max_cooling=1.5,
        activity_profile="Diurnal"
    ),
    "Scaptotrigona": BeeSpecies(
        name="Scaptotrigona",
        metabolic_rate=0.0042,
        colony_size_factor=1000,
        ideal_temp=(31.0, 35.0),
        humidity_range=(40.0, 70.0),
        nest_conductivity=0.11,
        max_cooling=1.8,
        activity_profile="Morning"
    )
}

# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------
def parse_gps_input(gps_str: str) -> Optional[Tuple[float, float]]:
    """
    Parse a comma-separated GPS string into (latitude, longitude).
    Returns None if parsing fails.
    """
    try:
        parts = gps_str.split(',')
        if len(parts) != 2:
            return None
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        return lat, lon
    except ValueError:
        return None

@st.cache_data(show_spinner=False)
def get_weather_data(lat: float, lon: float) -> Optional[Dict]:
    """
    Retrieve current weather data from Open-Meteo API.
    Returns a dictionary with 'temperature' (°C) and 'windspeed' if available.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        current = data.get("current_weather")
        if current:
            return {
                "temperature": current.get("temperature"),
                "windspeed": current.get("windspeed")
            }
    except requests.RequestException:
        return None
    return None

@st.cache_data(show_spinner=False)
def get_altitude(lat: float, lon: float) -> Optional[float]:
    """
    Retrieve altitude using the Open-Elevation API.
    """
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = data.get("results")
        if results and isinstance(results, list):
            return results[0].get("elevation")
    except requests.RequestException:
        return None
    return None

# ---------------------------------------------------------------------------
# Thermal Simulation Functions
# ---------------------------------------------------------------------------
def calculate_metabolic_heat(species: BeeSpecies, colony_size_pct: float, altitude: float) -> float:
    """
    Calculate the metabolic heat output.
    A simple model: (colony size * metabolic_rate * oxygen_factor).
    Oxygen factor decreases with altitude.
    """
    oxygen_factor = max(0.5, math.exp(-altitude / 7400))
    colony_size = species.colony_size_factor * (colony_size_pct / 100.0)
    return colony_size * species.metabolic_rate * oxygen_factor

def adjust_temperature(ambient_temp: float, altitude: float, species: BeeSpecies, is_daytime: bool) -> float:
    """
    Adjust ambient temperature for altitude effects and species activity.
    Altitude: lapse rate ~6.5°C per 1000 m.
    Activity profile adjustments: simple additive modifications.
    """
    temp_adj = ambient_temp - (altitude * 6.5 / 1000)
    if species.activity_profile == "Diurnal":
        temp_adj += 2 if is_daytime else -2
    elif species.activity_profile == "Morning":
        temp_adj += 3 if is_daytime else -1
    else:
        temp_adj += 1 if is_daytime else -1
    return temp_adj

def simulate_hive_temperature(species: BeeSpecies, colony_size_pct: float, nest_thickness: float,
                              boxes: List[HiveBox], ambient_temp: float, is_daytime: bool,
                              altitude: float, rain_intensity: float, surface_area_exponent: float) -> Dict:
    """
    Simulate the hive's thermal behavior.
    
    Parameters:
      - surface_area_exponent: exponent applied to total surface area for sensitivity.
    
    Returns a dictionary containing:
      - base_temp: core hive temperature.
      - box_temps: list of temperatures per hive box.
      - metabolic_heat, thermal_resistance, heat_gain.
    """
    # Ensure numeric types
    ambient_temp = float(ambient_temp)
    nest_thickness = float(nest_thickness)
    rain_intensity = float(rain_intensity)
    surface_area_exponent = float(surface_area_exponent)

    # Adjust ambient temperature for altitude and species activity
    temp_adj = adjust_temperature(ambient_temp, altitude, species, is_daytime)
    # Apply rain cooling effect: each 0.1 rain intensity reduces ~0.5°C.
    temp_adj -= (rain_intensity * 5)

    metabolic_heat = calculate_metabolic_heat(species, colony_size_pct, altitude)
    nest_resistance = (nest_thickness / 1000) / species.nest_conductivity
    total_resistance = nest_resistance + 0.04

    # Compute total surface area from all boxes (cm^2 -> m^2)
    total_surface_area = sum(
        2 * ((box.width * box.height) + (box.width * box.depth) + (box.height * box.depth)) / 10000
        for box in boxes
    )
    # Debug: output total surface area
    st.write("Total Surface Area (m^2):", total_surface_area)

    # Increase sensitivity by raising total surface area to the specified exponent.
    try:
        adjusted_surface = total_surface_area ** surface_area_exponent
    except Exception as e:
        st.error("Error computing adjusted surface area: " + str(e))
        adjusted_surface = total_surface_area  # fallback

    heat_gain = (metabolic_heat * total_resistance) / adjusted_surface
    cooling = min(species.max_cooling, heat_gain)

    if temp_adj > species.ideal_temp[1]:
        hive_temp = temp_adj - cooling
    else:
        hive_temp = temp_adj + min(heat_gain, species.ideal_temp[1] - temp_adj)

    # Calculate box temperatures
    box_temps = []
    for box in boxes:
        box_temp = hive_temp - box.cooling_effect + (box.propolis_thickness * 0.02)
        box_temp = max(species.ideal_temp[0], min(species.ideal_temp[1], box_temp))
        box_temps.append(box_temp)

    # Debug: output key computed values
    st.write("Adjusted Ambient Temp:", temp_adj)
    st.write("Metabolic Heat:", metabolic_heat)
    st.write("Total Thermal Resistance:", total_resistance)
    st.write("Heat Gain:", heat_gain)
    st.write("Core Hive Temperature:", hive_temp)

    return {
        "base_temp": hive_temp,
        "box_temps": box_temps,
        "metabolic_heat": metabolic_heat,
        "thermal_resistance": total_resistance,
        "heat_gain": heat_gain
    }

# ---------------------------------------------------------------------------
# Visualization Functions (using Plotly)
# ---------------------------------------------------------------------------
def plot_box_temperatures(boxes: List[HiveBox], box_temps: List[float], species: BeeSpecies) -> go.Figure:
    """
    Create an interactive bar chart showing temperatures in each hive box.
    """
    labels = [f"Box {box.id}" for box in boxes]
    fig = go.Figure(data=[go.Bar(x=labels, y=box_temps, marker_color='indianred')])
    fig.update_layout(
        title="Temperature in Hive Boxes",
        xaxis_title="Box ID",
        yaxis_title="Temperature (°C)",
        yaxis=dict(range=[species.ideal_temp[0] - 2, species.ideal_temp[1] + 2])
    )
    return fig

def plot_hive_3d_structure(boxes: List[HiveBox], box_temps: List[float]) -> go.Figure:
    """
    Create a 3D scatter plot to visualize the hive structure.
    """
    x, y, z, temp_values = [], [], [], []
    for box, temp in zip(boxes, box_temps):
        num_points = 50  # number of points per box
        xs = np.random.uniform(0, box.width, num_points)
        ys = np.random.uniform(0, box.depth, num_points)
        zs = np.random.uniform(0, box.height, num_points)
        x.extend(xs)
        y.extend(ys)
        z.extend(zs)
        temp_values.extend([temp] * num_points)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=4,
            color=temp_values,
            colorscale='YlOrRd',
            colorbar=dict(title="Temp (°C)")
        )
    )])
    fig.update_layout(
        title="3D Visualization of Hive Structure",
        scene=dict(
            xaxis_title="Width (cm)",
            yaxis_title="Depth (cm)",
            zaxis_title="Height (cm)"
        )
    )
    return fig

# ---------------------------------------------------------------------------
# Main Application Function
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Stingless Bee Hive Thermal Simulator", layout="wide")
    st.title("🍯 Stingless Bee Hive Thermal Simulator")

    # Sidebar: species selection and parameters
    species_key = st.sidebar.selectbox("Select Bee Species", list(SPECIES_CONFIG.keys()))
    species = SPECIES_CONFIG[species_key]
    st.sidebar.markdown(f"**{species.name} Characteristics:**")
    st.sidebar.write(f"Ideal Temperature: {species.ideal_temp[0]}–{species.ideal_temp[1]} °C")
    st.sidebar.write(f"Humidity Range: {species.humidity_range[0]}–{species.humidity_range[1]} %")
    st.sidebar.write(f"Activity Profile: {species.activity_profile}")

    colony_size_pct = st.sidebar.slider("Colony Size (%)", 0, 100, 50)
    nest_thickness = st.sidebar.slider("Nest Wall Thickness (mm)", 1.0, 10.0, 5.0)
    rain_intensity = st.sidebar.slider("Rain Intensity (0 to 1)", 0.0, 1.0, 0.0, step=0.1)
    surface_area_exponent = st.sidebar.slider("Surface Area Exponent", 1.0, 2.0, 1.0, step=0.1)

    # Advanced hive configuration for boxes
    with st.expander("Advanced Hive Configuration"):
        if species.name == "Melipona":
            default_boxes = [
                HiveBox(1, 23, 6, 23, 1.0),
                HiveBox(2, 23, 6, 23, 0.5),
                HiveBox(3, 23, 6, 23, 2.0),
                HiveBox(4, 23, 6, 23, 1.5)
            ]
        else:
            default_boxes = [
                HiveBox(1, 13, 5, 13, 1.0),
                HiveBox(2, 13, 5, 13, 0.5),
                HiveBox(3, 13, 5, 13, 2.0),
                HiveBox(4, 13, 5, 13, 1.5),
                HiveBox(5, 13, 5, 13, 1.0)
            ]
        boxes = []
        for box in default_boxes:
            cols = st.columns(4)
            with cols[0]:
                box.width = st.number_input(f"Box {box.id} Width (cm)", min_value=10, max_value=50, value=int(box.width))
            with cols[1]:
                box.height = st.number_input(f"Box {box.id} Height (cm)", min_value=5, max_value=30, value=int(box.height))
            with cols[2]:
                box.depth = st.number_input(f"Box {box.id} Depth (cm)", min_value=10, max_value=50, value=int(box.depth))
            with cols[3]:
                box.cooling_effect = st.number_input(f"Box {box.id} Cooling Effect", min_value=0.0, max_value=5.0, value=box.cooling_effect, step=0.1)
            boxes.append(box)

    # GPS input and external data
    gps_input = st.text_input("Enter GPS Coordinates (lat,lon)", "-3.4653,-62.2159")
    gps = parse_gps_input(gps_input)
    if gps is None:
        st.error("Invalid GPS input. Please enter coordinates as 'lat,lon'.")
        return
    lat, lon = gps

    altitude = get_altitude(lat, lon)
    if altitude is None:
        st.warning("Could not retrieve altitude. Please enter altitude manually.")
        altitude = st.slider("Altitude (m)", 0, 5000, 100)
    else:
        st.write(f"Altitude: {altitude} m")

    weather = get_weather_data(lat, lon)
    if weather and weather.get("temperature") is not None:
        ambient_temp = weather["temperature"]
        st.write(f"Current Ambient Temperature: {ambient_temp} °C")
    else:
        st.warning("Weather data unavailable. Please use the slider below.")
        ambient_temp = st.slider("Ambient Temperature (°C)", 15.0, 40.0, 28.0)

    is_daytime = st.toggle("Is it Daytime?", True)

    # Run the simulation
    results = simulate_hive_temperature(
        species, colony_size_pct, nest_thickness, boxes,
        ambient_temp, is_daytime, altitude, rain_intensity, surface_area_exponent
    )

    st.subheader("Simulation Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Base Hive Temperature", f"{results['base_temp']:.1f} °C")
        st.metric("Metabolic Heat Output", f"{results['metabolic_heat']:.2f} W")
    with col2:
        st.write("Thermal Resistance:", f"{results['thermal_resistance']:.3f}")
        st.write("Heat Gain:", f"{results['heat_gain']:.3f}")

    # Display interactive plots
    st.plotly_chart(plot_box_temperatures(boxes, results["box_temps"], species), use_container_width=True)
    st.plotly_chart(plot_hive_3d_structure(boxes, results["box_temps"]), use_container_width=True)

if __name__ == "__main__":
    main()
