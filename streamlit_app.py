import streamlit as st
import numpy as np
import math

# Set page config
st.set_page_config(
    page_title="ECONECTAR Hive Thermal Dashboard",
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

def calculate_hexagonal_surface_area(width_cm, height_cm):
    """
    Calculate surface area for a hexagonal box
    Args:
        width_cm: Width in centimeters
        height_cm: Height in centimeters
    Returns:
        Surface area in square meters
    """
    # Convert dimensions to meters
    width_m = width_cm / 100
    height_m = height_cm / 100
    
    # Calculate hexagon geometry
    apothem = width_m / 2
    side_length = (2 * apothem) / math.sqrt(3)
    
    # Calculate areas (in square meters)
    base_area = 6 * (0.5 * side_length * apothem)  # Area of one hexagonal face
    side_area = 6 * (side_length * height_m)  # Area of all rectangular sides
    
    total_area = 2 * base_area + side_area  # Two hexagonal faces + all side faces
    return total_area

def calculate_hive_temperature(params, boxes, ambient_temp_c):
    """
    Calculate hive temperature and related metrics using SI units
    Args:
        params: Dictionary of parameters
        boxes: List of box dimensions
        ambient_temp_c: Ambient temperature in Celsius
    """
    # Convert temperatures to Kelvin for calculations
    ambient_temp_k = ambient_temp_c + 273.15
    ideal_temp_k = params['ideal_hive_temperature'] + 273.15
    
    # Calculate colony parameters
    calculated_colony_size = 50000 * (params['colony_size'] / 100)
    oxygen_factor = calculate_oxygen_factor(params['altitude'])
    
    # Calculate metabolic heat (W)
    # bee_metabolic_heat is in Watts per bee
    colony_metabolic_heat = (
        calculated_colony_size 
        * params['bee_metabolic_heat'] 
        * oxygen_factor
    )
    
    # Calculate thermal resistance (K⋅m²/W)
    # Convert thickness from cm to m and ensure thermal conductivity is in W/(m⋅K)
    middle_layer_resistance = (
        (params['middle_layer_thickness'] / 100) 
        / params['middle_layer_thermal_conductivity']
    )
    total_thermal_resistance = middle_layer_resistance
    
    # Calculate volumes and surface areas
    total_volume = sum(
        (box['width'] / 100) * (box['length'] / 100) * (box['height'] / 100) 
        for box in boxes
    )  # in cubic meters
    
    total_surface_area = sum(
        calculate_hexagonal_surface_area(box['width'], box['height']) 
        for box in boxes
    )  # in square meters
    
    def calculate_heat_transfer(temp_difference_k):
        """Calculate heat transfer in Watts"""
        return total_surface_area * temp_difference_k / total_thermal_resistance
    
    # Temperature calculation with improved convergence
    # Work in Kelvin for calculations
    lower_bound = ambient_temp_k
    upper_bound = ideal_temp_k
    tolerance = 0.01
    
    while (upper_bound - lower_bound) > tolerance:
        estimated_temp_k = (lower_bound + upper_bound) / 2
        temp_difference = abs(estimated_temp_k - ambient_temp_k)
        heat_transfer = calculate_heat_transfer(temp_difference)
        
        if heat_transfer > colony_metabolic_heat:
            upper_bound = estimated_temp_k
        else:
            lower_bound = estimated_temp_k
    
    # Convert final temperature back to Celsius
    estimated_hive_temp_c = estimated_temp_k - 273.15
    
    # Calculate box temperatures (in Celsius)
    box_temperatures = [
        estimated_hive_temp_c - box['cooling_effect'] 
        for box in boxes
    ]
    
    # Calculate final heat transfer
    final_temp_difference = abs(estimated_temp_k - ambient_temp_k)
    final_heat_transfer = calculate_heat_transfer(final_temp_difference)

    return {
        'calculated_colony_size': calculated_colony_size,
        'colony_metabolic_heat': colony_metabolic_heat / 1000,  # Convert to kW
        'base_temperature': estimated_hive_temp_c,
        'box_temperatures': box_temperatures,
        'total_volume': total_volume,
        'total_surface_area': total_surface_area,
        'thermal_resistance': total_thermal_resistance,
        'ambient_temperature': ambient_temp_c,
        'oxygen_factor': oxygen_factor,
        'heat_transfer': final_heat_transfer / 1000  # Convert to kW
    }

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.boxes = [
        {'id': i+1, 'width': 22, 'length': 26, 'height': 9, 'cooling_effect': ce}
        for i, ce in enumerate([2, 0, 0, 8])  # Default cooling effects
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
        min_value=-10.0,
        max_value=45.0,
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
        min_value=-500, 
        max_value=5000, 
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
    'middle_layer_material': 'Papier-mâché & Terracotta Composite',
    'middle_layer_thickness': 1.0,  # cm (will be converted to m in calculations)
    'middle_layer_thermal_conductivity': 0.2,  # W/(m⋅K)
    'altitude': altitude,  # meters
    'ideal_hive_temperature': 35.0  # °C
}

# Calculate results with user-defined ambient temperature
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
        st.progress(min(1.0, temp / 40))  # Normalize to 40°C max for progress bar
    
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
