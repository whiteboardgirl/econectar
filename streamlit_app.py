import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests
from dataclasses import dataclass
from typing import List, Tuple, Dict
import datetime
import pytz
import os
from timezonefinder import TimezoneFinder

# Data classes
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

# Bee species configuration
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

# Utility functions
def parse_gps_input(gps_str: str) -> Tuple[float, float] | None:
    try:
        lat, lon = map(float, gps_str.strip().split(','))
        return lat, lon
    except ValueError:
        return None

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"

@st.cache_data(show_spinner=False)
def get_weather_data(lat: float, lon: float) -> Dict | None:
    """
    Fetches weather data from Open-Meteo API.
    """
    url = OPEN_METEO_URL.format(lat=lat, lon=lon)
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
        else:
            st.warning("Weather data structure is unexpected.")
            return None
    except requests.RequestException as e:
        st.error(f"Failed to retrieve weather data: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

@st.cache_data(show_spinner=False)
def get_altitude(lat: float, lon: float) -> float | None:
    """
    Fetches altitude data from Open Elevation API.
    """
    url = OPEN_ELEVATION_URL.format(lat=lat, lon=lon)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = data.get("results")
        if results and isinstance(results, list):
            return results[0].get("elevation")
        else:
            st.warning("Altitude data structure is unexpected.")
            return None
    except requests.RequestException as e:
        st.error(f"Failed to retrieve altitude data: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def calculate_metabolic_heat(species: BeeSpecies, colony_size_pct: float, altitude: float) -> float:
    """
    Calculates the metabolic heat generated by the bee colony.
    """
    OXYGEN_ALTITUDE_SCALE = 7400
    oxygen_factor = max(0.5, np.exp(-altitude / OXYGEN_ALTITUDE_SCALE))
    colony_size = species.colony_size_factor * (colony_size_pct / 100.0)
    base_metabolic = colony_size * species.metabolic_rate * oxygen_factor
    ACTIVITY_MULTIPLIER = 2.5
    return base_metabolic * ACTIVITY_MULTIPLIER

def adjust_temperature(ambient_temp: float, altitude: float, species: BeeSpecies, is_daytime: bool) -> float:
    """
    Adjusts the ambient temperature based on altitude, bee species, and daytime.
    """
    ALTITUDE_TEMP_DROP = 6.5 / 1000  # Temperature drop per meter of altitude
    temp_adj = ambient_temp - (altitude * ALTITUDE_TEMP_DROP)

    if species.activity_profile == "Diurnal":
        temp_adj += 3 if is_daytime else -1
    elif species.activity_profile == "Morning":
        temp_adj += 4 if is_daytime else 0
    else:
        temp_adj += 2 if is_daytime else -0.5
    return temp_adj

def calculate_solar_heat_gain(lat: float, lon: float, is_daytime: bool, day_of_year: int) -> float:
    """
    Estimates solar heat gain in Watts based on location, time of day, and day of year.
    """
    if not is_daytime:
        return 0.0

    SOLAR_CONSTANT = 1367  # W/m^2
    # Simplified solar angle calculation
    solar_angle = np.cos(np.radians(23.45 * np.sin(np.radians(360 * (day_of_year + 284) / 365))))
    solar_radiation = SOLAR_CONSTANT * solar_angle * 0.7
    HIVE_SURFACE_AREA = 0.25  # m^2
    solar_heat_gain = solar_radiation * HIVE_SURFACE_AREA

    return solar_heat_gain

def simulate_hive_temperature(species: BeeSpecies, colony_size_pct: float, nest_thickness: float,
                              lid_thickness: float, boxes: List[HiveBox], ambient_temp: float,
                              is_daytime: bool, altitude: float, rain_intensity: float,
                              surface_area_exponent: float, lat: float, lon: float,
                              day_of_year: int) -> Dict:
    """
    Simulates the temperature inside the hive based on various parameters,
    including the effect of a closed lid that helps retain heat.
    """
    # Adjust ambient temperature for altitude, species behavior, and rain
    temp_adj = adjust_temperature(ambient_temp, altitude, species, is_daytime)
    temp_adj -= (rain_intensity * 3)

    # Calculate heat contributions from metabolism and solar gain
    metabolic_heat = calculate_metabolic_heat(species, colony_size_pct, altitude)
    solar_heat_gain = calculate_solar_heat_gain(lat, lon, is_daytime, day_of_year)
    total_heat = metabolic_heat + solar_heat_gain

    # Calculate thermal resistances: nest wall, propolis, and now lid resistance
    nest_resistance = (nest_thickness / 1000) / species.nest_conductivity
    propolis_resistance = sum(box.propolis_thickness * 0.015 for box in boxes)
    LID_CONDUCTIVITY = 0.05  # Assumed conductivity for the lid material
    lid_resistance = (lid_thickness / 1000) / LID_CONDUCTIVITY

    total_resistance = nest_resistance + propolis_resistance + lid_resistance + 0.08

    # Calculate total surface area of all boxes (in m^2)
    total_surface_area = sum(
        2 * ((box.width * box.height) + (box.width * box.depth) + (box.height * box.depth)) / 10000
        for box in boxes
    )
    adjusted_surface = total_surface_area ** surface_area_exponent
    adjusted_surface = max(adjusted_surface, 0.0001)  # Prevent division by zero

    heat_gain = (total_heat * total_resistance) / adjusted_surface
    heat_gain *= 1.5
    cooling = min(species.max_cooling * 0.7, heat_gain)

    # Determine the base hive temperature
    if temp_adj > species.ideal_temp[1]:
        hive_temp = temp_adj - cooling
    else:
        temp_difference = species.ideal_temp[1] - temp_adj
        hive_temp = temp_adj + min(heat_gain, temp_difference)

    # Calculate temperature for each hive box
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
        "solar_heat_gain": solar_heat_gain,
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

def plot_hive_3d_structure(boxes: List[HiveBox], box_temps: List[float], species: BeeSpecies) -> go.Figure:
    """
    Creates a 3D visualization of the hive boxes with temperature mapping.
    """
    fig = go.Figure()

    z_offset = 0
    for i, (box, temp) in enumerate(zip(boxes, box_temps)):
        # Calculate vertices for the box
        x = [-box.width/2, box.width/2, box.width/2, -box.width/2]
        y = [-box.depth/2, -box.depth/2, box.depth/2, box.depth/2]
        z = [z_offset] * 4

        # Add bottom face
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            i=[0], j=[1], k=[2],
            colorscale=[[0, 'blue'], [0.5, 'yellow'], [1, 'red']],
            intensity=[temp],
            name=f'Box {box.id}'
        ))

        # Add top face
        z_top = [z_offset + box.height] * 4
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z_top,
            colorscale=[[0, 'blue'], [0.5, 'yellow'], [1, 'red']],
            intensity=[temp],
            showscale=False
        ))

        z_offset += box.height + 2  # Spacing between boxes

    fig.update_layout(
        title="3D Hive Structure with Temperature Distribution",
        scene=dict(
            xaxis_title="Width (cm)",
            yaxis_title="Depth (cm)",
            zaxis_title="Height (cm)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        showlegend=True
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
            box.width = st.number_input(f"Box {box.id} Width (cm)", min_value=10, max_value=50, value=int(box.width))
        with cols[1]:
            box.height = st.number_input(f"Box {box.id} Height (cm)", min_value=5, max_value=30, value=int(box.height))
        with cols[2]:
            box.depth = st.number_input(f"Box {box.id} Depth (cm)", min_value=10, max_value=50, value=int(box.depth))
        with cols[3]:
            box.cooling_effect = st.number_input(f"Box {box.id} Cooling Effect", min_value=0.0, max_value=5.0, 
                                                   value=box.cooling_effect, step=0.1)
        boxes.append(box)
    return boxes

@st.cache_data(show_spinner=False)
def is_daytime_calc(lat: float, lon: float) -> bool:
    """
    Determine if it's daytime based on GPS coordinates.
    Uses the `suntime` library and local timezone for calculations.
    """
    try:
        from suntime import Sun, SunTimeException
        import datetime
        import pytz
        from timezonefinder import TimezoneFinder

        sun = Sun(lat, lon)
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        local_tz = pytz.timezone(timezone_str) if timezone_str else pytz.utc
        if not timezone_str:
            st.warning("Could not determine local timezone. Using UTC as default.")

        now = datetime.datetime.now(local_tz)
        today = now.date()

        try:
            sr = sun.get_local_sunrise_time(today)
            ss = sun.get_local_sunset_time(today)
            if sr.tzinfo is None:
                sr = local_tz.localize(sr)
            if ss.tzinfo is None:
                ss = local_tz.localize(ss)
            return sr < now < ss
        except SunTimeException as e:
            st.warning(f"Suntime calculation error: {e}. Assuming daytime.")
            return True

    except ImportError:
        st.warning("`suntime` library not found. Please install it for accurate daytime calculation.")
        return True
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return True

def main():
    st.set_page_config(page_title="Stingless Bee Hive Thermal Simulator", layout="wide")
    st.title("🍯 Stingless Bee Hive Thermal Simulator")

    # Sidebar: Bee species selection and parameters
    species_key = st.sidebar.selectbox("Select Bee Species", list(SPECIES_CONFIG.keys()))
    species = SPECIES_CONFIG[species_key]

    st.sidebar.markdown(f"**{species.name} Characteristics:**")
    st.sidebar.write(f"Ideal Temperature: {species.ideal_temp[0]}–{species.ideal_temp[1]} °C")
    st.sidebar.write(f"Humidity Range: {species.humidity_range[0]}–{species.humidity_range[1]} %")
    st.sidebar.write(f"Activity Profile: {species.activity_profile}")

    colony_size_pct = st.sidebar.slider("Colony Size (%)", 0, 100, 50)
    nest_thickness = st.sidebar.slider("Nest Wall Thickness (mm)", 1.0, 10.0, 5.0)
    # New slider for lid thickness
    lid_thickness = st.sidebar.slider("Lid Thickness (mm)", 1.0, 10.0, 5.0)
    rain_intensity = st.sidebar.slider("Rain Intensity (0 to 1)", 0.0, 1.0, 0.0, step=0.1)
    surface_area_exponent = st.sidebar.slider("Surface Area Exponent", 1.0, 2.0, 1.0, step=0.1)

    # Advanced hive configuration
    with st.expander("Advanced Hive Configuration"):
        boxes = create_hive_boxes(species)
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

        is_daytime = is_daytime_calc(lat, lon)
        st.write(f"It is daytime: {is_daytime}")

        weather = get_weather_data(lat, lon)
        if weather and weather.get("temperature") is not None:
            ambient_temp = weather["temperature"]
            st.write(f"Current Ambient Temperature: {ambient_temp} °C")
        else:
            st.warning("Weather data unavailable. Please use the slider below.")
            ambient_temp = st.slider("Ambient Temperature (°C)", 15.0, 40.0, 28.0)

    if st.button("Run Simulation"):
        day_of_year = datetime.datetime.now().timetuple().tm_yday

        results = simulate_hive_temperature(
            species=species,
            colony_size_pct=colony_size_pct,
            nest_thickness=nest_thickness,
            lid_thickness=lid_thickness,
            boxes=boxes,
            ambient_temp=ambient_temp,
            is_daytime=is_daytime,
            altitude=altitude,
            rain_intensity=rain_intensity,
            surface_area_exponent=surface_area_exponent,
            lat=lat,
            lon=lon,
            day_of_year=day_of_year
        )

        st.subheader("Simulation Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Hive Temperature", f"{results['base_temp']:.1f} °C")
            st.metric("Metabolic Heat Output", f"{results['metabolic_heat']:.2f} W")
        with col2:
            st.metric("Solar Heat Gain", f"{results['solar_heat_gain']:.2f} W")
        with col3:
            st.write("Thermal Resistance:", f"{results['thermal_resistance']:.3f}")
            st.write("Heat Gain:", f"{results['heat_gain']:.3f}")

        st.subheader("Temperature Status")
        if results['base_temp'] < species.ideal_temp[0]:
            st.error(f"⚠️ Alert: Hive is too cold! Current temperature ({results['base_temp']:.1f}°C) is below the ideal range ({species.ideal_temp[0]}-{species.ideal_temp[1]}°C).")
        elif results['base_temp'] > species.ideal_temp[1]:
            st.error(f"⚠️ Alert: Hive is too hot! Current temperature ({results['base_temp']:.1f}°C) is above the ideal range ({species.ideal_temp[0]}-{species.ideal_temp[1]}°C).")
        else:
            st.success(f"✅ Hive temperature ({results['base_temp']:.1f}°C) is within the ideal range ({species.ideal_temp[0]}-{species.ideal_temp[1]}°C).")

        st.plotly_chart(plot_box_temperatures(boxes, results["box_temps"], species), use_container_width=True)
        st.plotly_chart(plot_hive_3d_structure(boxes, results["box_temps"], species), use_container_width=True)

if __name__ == "__main__":
    main()
