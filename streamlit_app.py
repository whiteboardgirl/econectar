import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests
from dataclasses import dataclass
from typing import List, Tuple, Dict
import math

@dataclass
class BeeSpecies:
    name: str
    metabolic_rate: float
    colony_size_factor: int
    ideal_temp: Tuple[float, float]
    humidity_range: Tuple[float, float]
    nest_conductivity: float
    max_cooling: float
    activity_profile: str

@dataclass
class HiveBox:
    id: int
    width: float
    height: float
    depth: float
    cooling_effect: float
    propolis_thickness: float = 1.5

SPECIES_CONFIG: Dict[str, BeeSpecies] = {
    "Melipona": BeeSpecies(
        name="Melipona",
        metabolic_rate=0.0088,
        colony_size_factor=700,
        ideal_temp=(30.0, 33.0),
        humidity_range=(50.0, 70.0),
        nest_conductivity=0.09,
        max_cooling=1.5,
        activity_profile="Diurnal"
    ),
    "Scaptotrigona": BeeSpecies(
        name="Scaptotrigona",
        metabolic_rate=0.0105,
        colony_size_factor=1000,
        ideal_temp=(31.0, 35.0),
        humidity_range=(40.0, 70.0),
        nest_conductivity=0.11,
        max_cooling=1.8,
        activity_profile="Morning"
    ),
    "Tetragonisca angustula": BeeSpecies(
        name="Tetragonisca angustula",
        metabolic_rate=0.0070,
        colony_size_factor=300,
        ideal_temp=(28.0, 31.0),
        humidity_range=(60.0, 80.0),
        nest_conductivity=0.07,
        max_cooling=1.2,
        activity_profile="Diurnal"
    ),
    "Frieseomelitta nigra": BeeSpecies(
        name="Frieseomelitta nigra",
        metabolic_rate=0.0120,
        colony_size_factor=500,
        ideal_temp=(32.0, 36.0),
        humidity_range=(45.0, 65.0),
        nest_conductivity=0.10,
        max_cooling=1.7,
        activity_profile="Morning"
    ),
    "Trigona fulviventris": BeeSpecies(
        name="Trigona fulviventris",
        metabolic_rate=0.0095,
        colony_size_factor=800,
        ideal_temp=(32.0, 36.0),
        humidity_range=(45.0, 65.0),
        nest_conductivity=0.10,
        max_cooling=1.6,
        activity_profile="Diurnal"
    ),
    "Cephalotrigona femorata": BeeSpecies(
        name="Cephalotrigona femorata",
        metabolic_rate=0.0110,
        colony_size_factor=600,
        ideal_temp=(29.0, 33.0),
        humidity_range=(50.0, 70.0),
        nest_conductivity=0.095,
        max_cooling=1.55,
        activity_profile="Diurnal"
    ),
    # Additional Colombian species:
    "Melipona eburnea": BeeSpecies(
        name="Melipona eburnea",
        metabolic_rate=0.0090,
        colony_size_factor=750,
        ideal_temp=(30.5, 33.5),
        humidity_range=(50.0, 70.0),
        nest_conductivity=0.085,
        max_cooling=1.6,
        activity_profile="Diurnal"
    ),
    "Melipona compressipes": BeeSpecies(
        name="Melipona compressipes",
        metabolic_rate=0.0100,
        colony_size_factor=800,
        ideal_temp=(31.0, 34.0),
        humidity_range=(50.0, 68.0),
        nest_conductivity=0.088,
        max_cooling=1.7,
        activity_profile="Diurnal"
    ),
    "Trigona spinipes": BeeSpecies(
        name="Trigona spinipes",
        metabolic_rate=0.0092,
        colony_size_factor=850,
        ideal_temp=(31.0, 35.0),
        humidity_range=(45.0, 65.0),
        nest_conductivity=0.095,
        max_cooling=1.65,
        activity_profile="Diurnal"
    )
}

def parse_gps_input(gps_str: str) -> Tuple[float, float] | None:
    try:
        lat, lon = map(float, gps_str.strip().split(','))
        return lat, lon
    except ValueError:
        return None

@st.cache_data(show_spinner=False)
def get_weather_data(lat: float, lon: float) -> Dict | None:
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
        pass
    return None

@st.cache_data(show_spinner=False)
def get_altitude(lat: float, lon: float) -> float | None:
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = data.get("results")
        if results and isinstance(results, list):
            return results[0].get("elevation")
    except requests.RequestException:
        pass
    return None

def calculate_metabolic_heat(species: BeeSpecies, colony_size_pct: float, altitude: float) -> float:
    oxygen_factor = max(0.5, np.exp(-altitude / 7400))
    colony_size = species.colony_size_factor * (colony_size_pct / 100.0)
    base_metabolic = colony_size * species.metabolic_rate * oxygen_factor
    activity_multiplier = 2.5
    return base_metabolic * activity_multiplier

def adjust_temperature(ambient_temp: float, altitude: float, species: BeeSpecies, is_daytime: bool) -> float:
    temp_adj = ambient_temp - (altitude * 6.5 / 1000)
    if species.activity_profile == "Diurnal":
        temp_adj += 3 if is_daytime else -1
    elif species.activity_profile == "Morning":
        temp_adj += 4 if is_daytime else 0
    else:
        temp_adj += 2 if is_daytime else -0.5
    return temp_adj

def simulate_hive_temperature(species: BeeSpecies, colony_size_pct: float, nest_thickness: float,
                              boxes: List[HiveBox], ambient_temp: float, is_daytime: bool,
                              altitude: float, rain_intensity: float, surface_area_exponent: float) -> Dict:
    temp_adj = adjust_temperature(ambient_temp, altitude, species, is_daytime)
    temp_adj -= (rain_intensity * 3)

    metabolic_heat = calculate_metabolic_heat(species, colony_size_pct, altitude)

    nest_resistance = (nest_thickness / 1000) / species.nest_conductivity
    propolis_resistance = sum(box.propolis_thickness * 0.015 for box in boxes)
    total_resistance = nest_resistance + propolis_resistance + 0.08

    total_surface_area = sum(
        2 * ((box.width * box.height) + (box.width * box.depth) + (box.height * box.depth)) / 10000
        for box in boxes
    )

    adjusted_surface = total_surface_area ** surface_area_exponent
    heat_gain = (metabolic_heat * total_resistance) / adjusted_surface
    heat_gain *= 1.5

    cooling = min(species.max_cooling * 0.7, heat_gain)

    if temp_adj > species.ideal_temp[1]:
        hive_temp = temp_adj - cooling
    else:
        temp_difference = species.ideal_temp[1] - temp_adj
        hive_temp = temp_adj + min(heat_gain, temp_difference)

    box_temps = []
    for box in boxes:
        box_temp = hive_temp - (box.cooling_effect * 0.7)
        propolis_heating = box.propolis_thickness * 0.03
        box_temp += propolis_heating
        box_temp = max(species.ideal_temp[0], min(species.ideal_temp[1], box_temp))
        box_temps.append(box_temp)

    return {
        "base_temp": hive_temp,
        "box_temps": box_temps,
        "metabolic_heat": metabolic_heat,
        "thermal_resistance": total_resistance,
        "heat_gain": heat_gain
    }

def plot_box_temperatures(boxes: List[HiveBox], box_temps: List[float], species: BeeSpecies) -> go.Figure:
    labels = [f"Box {box.id}" for box in boxes]
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=box_temps,
        marker_color='indianred',
        text=[f"{temp:.1f}°C" for temp in box_temps],
        textposition='auto',
    )])
    fig.update_layout(
        title="Temperature in Hive Boxes",
        xaxis_title="Box ID",
        yaxis_title="Temperature (°C)",
        yaxis=dict(range=[species.ideal_temp[0] - 2, species.ideal_temp[1] + 2])
    )
    return fig

def plot_hive_3d_structure(boxes: List[HiveBox], box_temps: List[float]) -> go.Figure:
    x, y, z, temp_values = [], [], [], []
    for box, temp in zip(boxes, box_temps):
        num_points = 50
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

def create_hive_boxes(species):
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
            box.width = st.number_input(f"Box {box.id} Width (cm)", min_value=10, max_value=50, value=int(box.width), key=f"width_{box.id}")
        with cols[1]:
            box.height = st.number_input(f"Box {box.id} Height (cm)", min_value=5, max_value=30, value=int(box.height), key=f"height_{box.id}")
        with cols[2]:
            box.depth = st.number_input(f"Box {box.id} Depth (cm)", min_value=10, max_value=50, value=int(box.depth), key=f"depth_{box.id}")
        with cols[3]:
            box.cooling_effect = st.number_input(f"Box {box.id} Cooling Effect", min_value=0.0, max_value=5.0, value=box.cooling_effect, step=0.1, key=f"cooling_{box.id}")
        boxes.append(box)
    return boxes

def main():
    st.set_page_config(page_title="Stingless Bee Hive Thermal Simulator", layout="wide")

    st.title("🍯 Stingless Bee Hive Thermal Simulator")

    species_key = st.sidebar.selectbox("Select Bee Species", list(SPECIES_CONFIG.keys()), key="species_select")
    species = SPECIES_CONFIG[species_key]

    st.sidebar.markdown(f"**{species.name} Characteristics:**", key="species_header")
    st.sidebar.write(f"Ideal Temperature: {species.ideal_temp[0]}–{species.ideal_temp[1]} °C", key="ideal_temp_side")
    st.sidebar.write(f"Humidity Range: {species.humidity_range[0]}–{species.humidity_range[1]} %", key="humidity_side")
    st.sidebar.write(f"Activity Profile: {species.activity_profile}", key="activity_side")

    colony_size_pct = st.sidebar.slider("Colony Size (%)", 0, 100, 50, key="colony_size")
    nest_thickness = st.sidebar.slider("Nest Wall Thickness (mm)", 1.0, 10.0, 5.0, key="nest_thickness")
    rain_intensity = st.sidebar.slider("Rain Intensity (0 to 1)", 0.0, 1.0, 0.0, step=0.1, key="rain_intensity")
    surface_area_exponent = st.sidebar.slider("Surface Area Exponent", 1.0, 2.0, 1.0, step=0.1, key="surface_area_exponent")

    with st.expander("Advanced Hive Configuration", key="hive_config_expander"):
        boxes = create_hive_boxes(species)

    gps_input = st.text_input("Enter GPS Coordinates (lat,lon)", "-3.4653,-62.2159", key="gps_input")
    gps = parse_gps_input(gps_input)

    if gps is None:
        st.error("Invalid GPS input. Please enter coordinates as 'lat,lon'.", key="gps_error")
        return

    lat, lon = gps
    altitude = get_altitude(lat, lon)

    if altitude is None:
        st.warning("Could not retrieve altitude. Please enter altitude manually.", key="altitude_warning")
        altitude = st.slider("Altitude (m)", 0, 5000, 100, key="manual_altitude")
    else:
        st.write(f"Altitude: {altitude} m", key="altitude_write")

    weather = get_weather_data(lat, lon)
    if weather and weather.get("temperature") is not None:
        ambient_temp = weather["temperature"]
        st.write(f"Current Ambient Temperature: {ambient_temp} °C", key="ambient_temp_write")
    else:
        st.warning("Weather data unavailable. Please use the slider below.", key="weather_warning")
        ambient_temp = st.slider("Ambient Temperature (°C)", 15.0, 40.0, 28.0, key="manual_temp")

    is_daytime = st.toggle("Is it Daytime?", True, key="is_daytime")

    if st.button("Run Simulation", key="run_simulation_button"):
        results = simulate_hive_temperature(
            species, colony_size_pct, nest_thickness, boxes,
            ambient_temp, is_daytime, altitude, rain_intensity, surface_area_exponent
        )

        st.subheader("Simulation Results", key="sim_results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Base Hive Temperature", f"{results['base_temp']:.1f} °C", key="base_temp_metric")
            st.metric("Metabolic Heat Output", f"{results['metabolic_heat']:.2f} W", key="metabolic_heat_metric")
        with col2:
            st.write("Thermal Resistance:", f"{results['thermal_resistance']:.3f}", key="thermal_resistance_write")
            st.write("Heat Gain:", f"{results['heat_gain']:.3f}", key="heat_gain_write")

        st.subheader("Temperature Status", key="temperature_status")
        if results['base_temp'] < species.ideal_temp[0]:
            st.error(f"⚠️ Alert: Hive is too cold! Current temperature ({results['base_temp']:.1f}°C) is below the ideal range ({species.ideal_temp[0]}-{species.ideal_temp[1]}°C).", key="too_cold_alert")
        elif results['base_temp'] > species.ideal_temp[1]:
            st.error(f"⚠️ Alert: Hive is too hot! Current temperature ({results['base_temp']:.1f}°C) is above the ideal range ({species.ideal_temp[0]}-{species.ideal_temp[1]}°C).", key="too_hot_alert")
        else:
            st.success(f"✅ Hive temperature ({results['base_temp']:.1f}°C) is within the ideal range ({species.ideal_temp[0]}-{species.ideal_temp[1]}°C).", key="temp_within_range")

        st.plotly_chart(plot_box_temperatures(boxes, results["box_temps"], species), use_container_width=True, key="box_temp_chart")
        st.plotly_chart(plot_hive_3d_structure(boxes, results["box_temps"]), use_container_width=True, key="hive_3d_chart")

if __name__ == "__main__":
    main()
