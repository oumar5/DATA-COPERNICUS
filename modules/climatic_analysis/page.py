import streamlit as st
from .service import get_climate_data
from .components import display_climate_data

def show():
    """
    Displays a climate analysis page in Streamlit with default coordinates set to Lyon.
    """
    st.title("Analyse climatique (Lyon par défaut)")
    
    # User input for latitude and longitude (default: Lyon)
    lat = st.number_input("Latitude", value=45.7640, format="%.6f")
    lon = st.number_input("Longitude", value=4.8357, format="%.6f")
    
    # User input for start and end dates
    start_date = st.text_input("Date de début (format YYYYMMDD)", value="20230101")
    end_date = st.text_input("Date de fin (format YYYYMMDD)", value="20230131")
    
    # Button to trigger the analysis
    if st.button("Analyser"):
        with st.spinner("Récupération des données climatiques..."):
            climate_data = get_climate_data(lat, lon, start_date, end_date)
        
        # Display the retrieved climate data
        display_climate_data(climate_data)
