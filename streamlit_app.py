import streamlit as st
import numpy as np
import math

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

def calculate_oxygen_factor(altitude_m):
    """Calculate oxygen factor based on altitude"""
    factor = 1 - (0.1 * (abs(altitude_m) / 1000))
    return max(0.5, factor)

def calculate_box_surface_area(width_cm, length_cm, height_cm):
    """Calculate surface area for a rectangular box"""
    # Convert dimensions to meters
    width_m = width_cm / 100
    length_m = length_cm / 100
    height_m = height_cm / 100
    
    # Calculate areas (in square meters)
    top_bottom_area = 2 * (width_m * length_m)
    front_back_area = 2 * (width_m * height_m)
    left_right_area = 2 * (length_m * height_m)
    
    return top_bottom_area + front_back_area + left_right_area

def calculate_heat_transfer(temp_hive_k, temp_ambient_k, total_surface_area, total_resistance):
    """Calculate heat transfer"""
    temp_difference = abs(temp_hive_k - temp_ambient_k)
    heat_transfer = (total_surface_area * temp_difference) / total_resistance
    return heat_transfer

def calculate_hive_temperature(params, boxes, ambient_temp_c):
    """Calculate hive temperature and related metrics"""
    # Convert temperatures to Kelvin
    ambient_temp_k = ambient_temp_c + 273.15
    ideal_temp_k = params['ideal_hive_temperature'] + 273.15
    
    # Calculate colony parameters
    calculated_colony_size = 50000 * (params['colony_size'] / 100)
    oxygen_factor = calculate_oxygen_factor(params['altitude'])
    colony_metabolic_heat = calculated_colony_size * params['bee_metabolic_heat'] * oxygen_factor
    
    # Calculate total surface area and volume
    total_volume = sum(
        (box['width'] / 100) * (box['length'] / 100) * (box['height'] / 100) 
        for box in boxes
    )
    total_surface_area = sum(
        calculate_box_surface_area(box['width'], box['length'], box['height']) 
        for box in boxes
    )
    
    # Calculate thermal resistance
    wood_resistance = (params['wood_thickness'] / 100) / params['wood_thermal_conductivity']
    total_resistance = wood_resistance + params['air_film_resistance_outside']
    
    # Temperature calculation with convergence
    lower_bound = ambient_temp_k
    upper_bound = ideal_temp_k
    tolerance = 0.01
    
    while (upper_bound - lower_bound) > tolerance:
        estimated_temp_k = (lower_bound + upper_bound) / 2
        heat_transfer = calculate_heat_transfer(
            estimated_temp_k, 
            ambient_temp_k, 
            total_surface_area, 
            total_resistance
        )
        
        if heat_transfer > colony_metabolic_heat:
            upper_bound = estimated_temp_k
        else:
            lower_bound = estimated_temp_k
    
    # Convert final temperature back to Celsius
    estimated_hive_temp_c = estimated_temp_k - 273.15
    
    # Calculate box temperatures with bounds
    box_temperatures = [
        max(0, min(50, estimated_hive_temp_c - box['cooling_effect']))
        for box in boxes
    ]
    
    final_heat_transfer = calculate_heat_transfer(
        estimated_temp_k,
        ambient_temp_k,
        total_surface_area,
        total_resistance
    )

    return {
        'calculated_colony_size': calculated_colony_size,
        'colony_metabolic_heat': colony_metabolic_heat / 1000,  # Convert to kW
        'base_temperature': estimated_hive_temp_c,
        'box_temperatures': box_temperatures,
        'total_volume': total_volume,
        'total_surface_area': total_surface_area,
        'thermal_resistance': total_resistance,
        'ambient_temperature': ambient_temp_c,
        'oxygen_factor': oxygen_factor,
        'heat_transfer': final_heat_transfer / 1000  # Convert to kW
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

# Create main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Input Parameters")
    
    # Ambient Temperature Control
    ambient_temperature = st.slider(
        "Ambient Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=20.0,
        step=0.1,
        help="Set the current ambient temperature"
    )
    
    # Colony Parameters
    colony_size = st.slider(
        "Colony Size (%)", 
        min_value=0, 
        max_value=100, 
        value=50,
        help="Percentage of maximum colony size (50,000 bees)"
    )
    
    # Altitude Parameters with progress bar for oxygen factor
    altitude = st.slider(
        "Altitude (meters)", 
        min_value=0, 
        max_value=3800, 
        value=0,
        step=100,
        help="Height above sea level affects oxygen availability"
    )
    oxygen_factor = calculate_oxygen_factor(altitude)
    st.progress(oxygen_factor)
    st.caption(f"Oxygen Factor: {oxygen_factor:.2f}")
    
    # Box Parameters in expanders
    st.subheader("📦 Box Configuration")
    for i, box in enumerate(st.session_state.boxes):
        with st.expander(f"Box {box['id']}", expanded=True):
            st.session_state.boxes[i]['cooling_effect'] = st.number_input(
                "Cooling Effect (°C)",
                min_value=0.0,
                max_value=20.0,
                value=float(box['cooling_effect']),
                step=0.5,
                key=f"cooling_effect_{i}",
                help="Additional cooling effect applied to this box"
            )

# Parameters dictionary with SI units
params = {
    'colony_size': colony_size,
    'bee_metabolic_heat': 0.0040,  # Watts per bee
    'wood_thickness': 2.0,  # cm
    'wood_thermal_conductivity': 0.13,  # W/(m⋅K) for pine wood
    'air_film_resistance_outside': 0.04,  # m²K/W
    'altitude': altitude,  # meters
    'ideal_hive_temperature': 35.0  # °C
}

# Calculate results
results = calculate_hive_temperature(params, st.session_state.boxes, ambient_temperature)

# Display results in second column
with col2:
    st.subheader("📈 Analysis Results")
    
    # Create metrics for key values
    col2a, col2b = st.columns(2)
    with col2a:
        st.metric("Base Hive Temperature", f"{results['base_temperature']:.1f}°C")
        st.metric("Ambient Temperature", f"{results['ambient_temperature']:.1f}°C")
    with col2b:
        st.metric("Colony Size", f"{int(results['calculated_colony_size']):,} bees")
        st.metric("Metabolic Heat", f"{results['colony_metabolic_heat']:.3f} kW")
    
    # Box temperatures
    st.subheader("📊 Box Temperatures")
    for i, temp in enumerate(results['box_temperatures']):
        st.markdown(f"**Box {i+1}:** {temp:.1f}°C")
        # Ensure progress value is between 0 and 1
        progress_value = max(0.0, min(1.0, temp / 50))  # Normalize to 50°C max
        st.progress(progress_value)
    
    # Thermal characteristics in an expander
    with st.expander("🔍 Detailed Thermal Characteristics", expanded=True):
        st.markdown(f"""
        - **Total Volume:** {results['total_volume']:.4f} m³
        - **Total Surface Area:** {results['total_surface_area']:.4f} m²
        - **Thermal Resistance:** {results['thermal_resistance']:.4f} m²K/W
        - **Heat Transfer:** {results['heat_transfer']:.3f} kW
        """)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit • Thermal analysis for beekeeping*")
