import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import pyvista as pv
from stpyvista import stpyvista

# Set page configuration
st.set_page_config(page_title="Stingless Bee Hive Thermal Simulator", layout="wide")

# Title and introduction
st.title("🍯 Stingless Bee Hive Thermal Simulator")
st.write("This app simulates and visualizes temperature distribution in stingless bee hives.")

# Sidebar: species selection and parameters
species_options = {"Melipona": {"ideal_temp": (30.0, 33.0), "humidity_range": (50.0, 70.0), "activity_profile": "Diurnal"},
                   "Scaptotrigona": {"ideal_temp": (31.0, 35.0), "humidity_range": (40.0, 70.0), "activity_profile": "Morning"}}

species_key = st.sidebar.selectbox("Select Bee Species", list(species_options.keys()))
species = species_options[species_key]

st.sidebar.markdown(f"**{species_key} Characteristics:**")
st.sidebar.write(f"Ideal Temperature: {species['ideal_temp'][0]}–{species['ideal_temp'][1]} °C")
st.sidebar.write(f"Humidity Range: {species['humidity_range'][0]}–{species['humidity_range'][1]} %")
st.sidebar.write(f"Activity Profile: {species['activity_profile']}")

colony_size_pct = st.sidebar.slider("Colony Size (%)", 0, 100, 50)
nest_thickness = st.sidebar.slider("Nest Wall Thickness (mm)", 1.0, 10.0, 5.0)
rain_intensity = st.sidebar.slider("Rain Intensity (0 to 1)", 0.0, 1.0, 0.0, step=0.1)

# Advanced hive configuration
with st.expander("Advanced Hive Configuration"):
    if species_key == "Melipona":
        default_boxes = [
            {"id": 1, "width": 23, "height": 6, "depth": 23, "cooling_effect": 1.0},
            {"id": 2, "width": 23, "height": 6, "depth": 23, "cooling_effect": 0.5},
            {"id": 3, "width": 23, "height": 6, "depth": 23, "cooling_effect": 2.0},
            {"id": 4, "width": 23, "height": 6, "depth": 23, "cooling_effect": 1.5}
        ]
    else:
        default_boxes = [
            {"id": 1, "width": 13, "height": 5, "depth": 13, "cooling_effect": 1.0},
            {"id": 2, "width": 13, "height": 5, "depth": 13, "cooling_effect": 0.5},
            {"id": 3, "width": 13, "height": 5, "depth": 13, "cooling_effect": 2.0},
            {"id": 4, "width": 13, "height": 5, "depth": 13, "cooling_effect": 1.5},
            {"id": 5, "width": 13, "height": 5, "depth": 13, "cooling_effect": 1.0}
        ]
    
    boxes = []
    for box in default_boxes:
        cols = st.columns(4)
        with cols[0]:
            box["width"] = st.number_input(f"Box {box['id']} Width (cm)", min_value=10, max_value=50, value=int(box["width"]))
        with cols[1]:
            box["height"] = st.number_input(f"Box {box['id']} Height (cm)", min_value=5, max_value=30, value=int(box["height"]))
        with cols[2]:
            box["depth"] = st.number_input(f"Box {box['id']} Depth (cm)", min_value=10, max_value=50, value=int(box["depth"]))
        with cols[3]:
            box["cooling_effect"] = st.number_input(f"Box {box['id']} Cooling Effect", min_value=0.0, max_value=5.0, value=box["cooling_effect"], step=0.1)
        boxes.append(box)

# GPS input and external data
gps_input = st.text_input("Enter GPS Coordinates (lat,lon)", "-3.4653,-62.2159")
lat, lon = map(float, gps_input.split(','))

altitude = 100  # Placeholder for altitude retrieval
st.write(f"Altitude: {altitude} m")

ambient_temp = st.slider("Ambient Temperature (°C)", 15.0, 40.0, 28.0)
is_daytime = st.toggle("Is it Daytime?", True)

# Simulation function (placeholder)
def simulate_hive_temperature(species, colony_size_pct, nest_thickness, boxes, ambient_temp, is_daytime, altitude, rain_intensity):
    # Placeholder simulation logic
    base_temp = ambient_temp + np.random.uniform(-2, 2)
    box_temps = [base_temp + np.random.uniform(-1, 1) for _ in boxes]
    return {
        "base_temp": base_temp,
        "box_temps": box_temps,
        "metabolic_heat": np.random.uniform(0.5, 2.0),
        "thermal_resistance": np.random.uniform(0.1, 0.5),
        "heat_gain": np.random.uniform(0.1, 1.0)
    }

# Run the simulation
results = simulate_hive_temperature(species, colony_size_pct, nest_thickness, boxes, ambient_temp, is_daytime, altitude, rain_intensity)

# Display results
st.subheader("Simulation Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("Base Hive Temperature", f"{results['base_temp']:.1f} °C")
    st.metric("Metabolic Heat Output", f"{results['metabolic_heat']:.2f} W")
with col2:
    st.write("Thermal Resistance:", f"{results['thermal_resistance']:.3f}")
    st.write("Heat Gain:", f"{results['heat_gain']:.3f}")

# 2D Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(np.array(results['box_temps']).reshape(-1, 1), annot=True, cmap='YlOrRd', ax=ax)
ax.set_title("Temperature Distribution in Hive Boxes")
ax.set_ylabel("Box ID")
st.pyplot(fig)

# 3D Visualization
plotter = pv.Plotter()
for i, box in enumerate(boxes):
    cube = pv.Cube(center=(i*1.5, 0, 0), x_length=box['width']/100, y_length=box['depth']/100, z_length=box['height']/100)
    plotter.add_mesh(cube, scalars=[results['box_temps'][i]], clim=[min(results['box_temps']), max(results['box_temps'])], cmap='coolwarm')

plotter.view_xy()
stpyvista(plotter, key="pv_plot")

# Correlation heatmap
df_col = pd.DataFrame({
    'ambient_temp': [ambient_temp],
    'base_temp': [results['base_temp']],
    'metabolic_heat': [results['metabolic_heat']],
    'thermal_resistance': [results['thermal_resistance']],
    'heat_gain': [results['heat_gain']]
})
for i, temp in enumerate(results['box_temps']):
    df_col[f'box_{i+1}_temp'] = temp

corr = df_col.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)

    # Run the simulation
    results = simulate_hive_temperature(
        species, colony_size_pct, nest_thickness, boxes,
        ambient_temp, is_daytime, altitude, rain_intensity
    )

    # Display results
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

    # Add debug output
    st.write("Box dimensions:", [(box.width, box.height, box.depth) for box in boxes])
    st.write("Calculated box temperatures:", results["box_temps"])

if __name__ == "__main__":
    main()
