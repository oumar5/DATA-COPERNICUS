import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
import plotly.graph_objects as go
from .service_api import get_weather_climate

def show():

    def get_weather_data(lat, lon, start_date, end_date):
        
        data = get_weather_climate(lat, lon, start_date, end_date)
                
        df = pd.DataFrame({
            'Date': data['Date'],
            'Temperature': data['Température Moyenne (°C)'],
            'Precipitation': data['Précipitations Moyenne (mm)'],
            'TempMax' : data['Température Max (°C)'],
            'TempMin' : data['Température Min (°C)']
        })   
            
        daily_df = df
        
        return daily_df
    
    # Style CSS personnalisé pour la navigation
    st.markdown("""
        <style>
            .nav-link {
                display: inline-block;
                padding: 10px 20px;
                background-color: #f0f2f6;
                border-radius: 5px;
                margin-right: 10px;
                text-decoration: none;
                color: #000000;
                text-align: center;
            }
            .nav-link:hover {
                background-color: #e0e2e6;
            }
            .nav-link.active {
                background-color: #00acb5;
                color: white;
            }
            .nav-container {
                display: flex;
                justify-content: center;
                padding: 10px 0;
                margin-bottom: 20px;
            }
            .st-emotion-cache-1ibsh2c {
                width: 100%;
                padding: 5rem 1rem 10rem;
                max-width: initial;
                min-width: auto;
            }
            .st-ak {
                gap: 10px;
            }
            
            .st-ae {
                display: flex;
                # background-color: darkgray;
                # padding: 2px;
            }
            
            #map_div{
                height: 453px !important;
                width: 1000px !important;
                position: relative;
                outline: none;
            }
        </style>
    """, unsafe_allow_html=True)

    
    st.title("Visualisation des données sur la région Auverne-Rhône-Alpes")

    # Carte pour sélectionner la zone
    m = folium.Map(location=[45.7578137, 4.8320114], zoom_start=8)
    draw = Draw(
        draw_options={
            'polyline': False,
            'rectangle': True,
            'polygon': True,
            'circle': False,
            'marker': False,
            'circlemarker': False
        },
        edit_options={'edit': False}
    )
    draw.add_to(m)

    col1, col2 = st.columns([3, 1])

    with col1:
        output = st_folium(m, width=1100, height=550, key="map_draw")
        drawn_data = output.get("last_active_drawing", None)

    with col2:
        if drawn_data:
            try:
                coordinates = drawn_data['geometry']['coordinates'][0]
                st.write(f"Coordonnées sélectionnées :\n\n {coordinates}")
                centroid = np.mean(coordinates, axis=0)
                lat, lon = centroid[1], centroid[0]
            except:
                st.write("Erreur dans la lecture des coordonnées")
                lat, lon = 45.7578137, 4.8320114
        else:
            st.write("Aucun tracé actif pour l'instant.")
            lat, lon = 45.7578137, 4.8320114

    # Date sliders
    start_reference = datetime(2024, 10, 6)  # Date de début fixe
    end_reference = datetime.now()
    days_diff = (end_reference - start_reference).days

    # Créer un slider pour sélectionner la plage de dates
    col1, col2 = st.columns(2)
    with col1:
        start_days = st.slider(
            "Date de début",
            min_value=0,
            max_value=days_diff,
            value=0,
            format="J+%d"
        )
        start_date = start_reference + timedelta(days=start_days)

    with col2:
        end_days = st.slider(
            "Date de fin",
            min_value=start_days,
            max_value=days_diff,
            value=min(start_days + 30, days_diff),
            format="J+%d"
        )
        end_date = start_reference + timedelta(days=end_days)

    # Afficher les dates sélectionnées
    st.write(f"Période sélectionnée : du {start_date.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}")

    # Formater les dates pour l'API
    start_date_formatted = start_date.strftime('%Y%m%d')
    end_date_formatted = end_date.strftime('%Y%m%d')

    weather_data = get_weather_data(lat, lon, start_date_formatted, end_date_formatted)

    _col1, _col2 = st.columns(2)
    with _col1:
        st.title("Dataset Metéo")
        st.dataframe(weather_data)
    with _col2:
        st.title("Sommaire Dataset")
        summary = weather_data.describe()  # Calcul des statistiques descriptives
        st.dataframe(summary)

    meteo_option = st.selectbox('Météo', ['Température', 'Précipitations'])

    if meteo_option == 'Température':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weather_data['Date'], y=weather_data['TempMax'], name='Temp Max'))
        fig.add_trace(go.Scatter(x=weather_data['Date'], y=weather_data['TempMin'], name='Temp Min'))
        fig.update_layout(title='Température', xaxis_title='Date', yaxis_title='Température (°C)')
        st.plotly_chart(fig)
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=weather_data['Date'], y=weather_data['Precipitation'], name='Précipitations'))
        fig.update_layout(title='Précipitations', xaxis_title='Date', yaxis_title='Précipitations (mm)')
        st.plotly_chart(fig)

