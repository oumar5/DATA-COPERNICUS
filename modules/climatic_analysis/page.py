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

    
    st.title("Analyse climatique pour la région d'Auverne-Rhône-Alpes")

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

    # Date pickers
    start_reference = datetime(2024, 10, 6)  # Date de début fixe
    end_reference = datetime.now()

    # Créer des date pickers pour sélectionner la plage de dates
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Date de début",
            value=start_reference,
            max_value=end_reference
        )

    with col2:
        end_date = st.date_input(
            "Date de fin",
            value=min(start_reference + timedelta(days=30), end_reference),
            min_value=start_date,
            max_value=end_reference
        )

    # Afficher les dates sélectionnées
    st.write(f"Période sélectionnée : du {start_date.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}")

    # Formater les dates pour l'API
    start_date_formatted = start_date.strftime('%Y%m%d')
    end_date_formatted = end_date.strftime('%Y%m%d')

    weather_data = get_weather_data(lat, lon, start_date_formatted, end_date_formatted)

    # Ajout du bouton pour afficher/masquer le dataset
    show_dataset = st.button("Afficher/Masquer Dataset")

    # Variable de session pour suivre l'état d'affichage
    if 'show_dataset_state' not in st.session_state:
        st.session_state.show_dataset_state = False

    if show_dataset:
        st.session_state.show_dataset_state = not st.session_state.show_dataset_state

    if st.session_state.show_dataset_state:
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
        fig.add_trace(go.Scatter(x=weather_data['Date'], y=weather_data['TempMax'], name='Temp. Max'))
        fig.add_trace(go.Scatter(x=weather_data['Date'], y=weather_data['TempMin'], name='Temp. Min'))
        fig.add_trace(go.Scatter(x=weather_data['Date'], y=weather_data['Temperature'], name='Temp. Moyenne'))
        fig.update_layout(title='Température', xaxis_title='Date', yaxis_title='Température (°C)')
        st.plotly_chart(fig)
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=weather_data['Date'], y=weather_data['Precipitation'], name='Précipitations'))
        fig.update_layout(title='Précipitations', xaxis_title='Date', yaxis_title='Précipitations (mm)')
        st.plotly_chart(fig)

    # Créer la figure
    fig = go.Figure()

    # Ajouter la trace pour la température
    fig.add_trace(go.Scatter(
        x=weather_data['Date'],
        y=weather_data['Temperature'],
        name='Temp. Moyenne',
        line=dict(color='#3498db'),
        mode='lines'
    ))

    # Ajouter la trace pour les précipitations
    fig.add_trace(go.Bar(
        x=weather_data['Date'],
        y=weather_data['Precipitation'],
        name='Précipitations',
        marker_color='#2ecc71',
        yaxis='y2'  # Associer à l'axe y secondaire
    ))

    # Mettre à jour la disposition
    fig.update_layout(
        title='Température & Précipitation',
        xaxis_title='Date',
        yaxis=dict(
            title='Température (°C)',
            titlefont=dict(color='#3498db'),
            tickfont=dict(color='#3498db')
        ),
        yaxis2=dict(
            title='Précipitations (mm)',
            titlefont=dict(color='#2ecc71'),
            tickfont=dict(color='#2ecc71'),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(r=80)  # Ajuster si besoin pour afficher les étiquettes de l'axe secondaire
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

