import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

def display_climate_indices(indices_list, time_labels):
    """
    Displays climate indices as separate charts and a table.
    """
    # Extract data for plots
    indices_vegetation = [indices["vegetation_index"] for indices in indices_list]
    indices_soil_moisture = [indices["soil_moisture"] for indices in indices_list]

    # Calculate statistics
    vegetation_mean = np.mean(indices_vegetation)
    vegetation_median = np.median(indices_vegetation)
    soil_moisture_mean = np.mean(indices_soil_moisture)
    soil_moisture_median = np.median(indices_soil_moisture)

    # Display statistics as a table with a green heading
    st.markdown("<h4 style='color:#27ae60;'>Statistiques des indices climatiques :</h4>", unsafe_allow_html=True)
    stats_table = {
        "Indice": ["Indice de végétation", "Humidité du sol (mm)"],
        "Moyenne": [f"{vegetation_mean:.2f}", f"{soil_moisture_mean:.2f}"],
        "Médiane": [f"{vegetation_median:.2f}", f"{soil_moisture_median:.2f}"]
    }
    st.table(stats_table)

    # Create separate plots for each index for clarity

    # Plot for Vegetation Index
    st.subheader("Indice de végétation")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(time_labels, indices_vegetation, marker='o', color='#27ae60')
    ax1.set_xlabel("Temps", fontsize=12, color='#2ecc71')
    ax1.set_ylabel("Indice de végétation", fontsize=12, color='#2ecc71')
    ax1.set_title("Évolution de l'indice de végétation", fontsize=14, color='#27ae60')
    ax1.grid(True, color='#90ee90')
    ax1.tick_params(axis='x', colors='#2ecc71')
    ax1.tick_params(axis='y', colors='#2ecc71')
    plt.xticks(rotation=45, ha="right")

    # Adjust x-axis labels if needed
    if len(time_labels) > 10:
        ax1.set_xticks(time_labels[::max(len(time_labels)//10, 1)])
    
    # Format dates on x-axis if needed
    if isinstance(time_labels[0], str) and len(time_labels[0]) == 8:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    st.pyplot(fig1)

    # Plot for Soil Moisture
    st.subheader("Humidité du sol (mm)")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(time_labels, indices_soil_moisture, marker='o', color='#2ecc71')
    ax2.set_xlabel("Temps", fontsize=12, color='#2ecc71')
    ax2.set_ylabel("Humidité du sol (mm)", fontsize=12, color='#2ecc71')
    ax2.set_title("Évolution de l'humidité du sol", fontsize=14, color='#27ae60')
    ax2.grid(True, color='#90ee90')
    ax2.tick_params(axis='x', colors='#2ecc71')
    ax2.tick_params(axis='y', colors='#2ecc71')
    plt.xticks(rotation=45, ha="right")

    # Adjust x-axis labels if needed
    if len(time_labels) > 10:
        ax2.set_xticks(time_labels[::max(len(time_labels)//10, 1)])

    # Format dates on x-axis if needed
    if isinstance(time_labels[0], str) and len(time_labels[0]) == 8:
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    st.pyplot(fig2)
