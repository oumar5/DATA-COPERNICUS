import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
import plotly.graph_objects as go
from .service_api import calculate_soil_moisture_and_vegetation_index

def set_green_theme():
    st.markdown(
        """
        <style>
        /* Set background color for the entire app */
        .reportview-container {
            background-color: #eaffea;
        }
        /* Style the buttons with a green background */
        .stButton>button {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 0.5em 1em;
            border-radius: 5px;
        }
        /* Change text input background color */
        .stTextInput>div>div>input {
            background-color: #f0fff0;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show():


    def get_soil_data(lat, lon, start_date, end_date):
        
        data = calculate_soil_moisture_and_vegetation_index(lat, lon, start_date, end_date)
        
        df = pd.DataFrame({
            'Date': data["Date"],
            'Humidité du sol': data['Humidité du sol'],
            'VegetationIndex': data['Indice de végétation']
        })
        
        return df
 

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

    
    st.title("Analyse du sol de la région Auvergne-Rhône-Alpes")

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

    # weather_data = get_weather_data(lat, lon, start_date_formatted, end_date_formatted)
    # weather_data = get_weather_data(lat, lon, start_date_formatted, end_date_formatted)
    soil_data = get_soil_data(lat, lon, start_date_formatted, end_date_formatted)

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
            st.title("Dataset du Sol")
            st.dataframe(soil_data)
        with _col2:
            st.title("Sommaire")
            summary = soil_data.describe()  # Calcul des statistiques descriptives
            st.dataframe(summary)

    # col1, col2 = st.columns(2)
    # with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=soil_data['Date'], 
        y=soil_data['Humidité du sol'], 
        name='Humidité du sol'),           
    )
    fig.update_layout(title='Humidité du sol', xaxis_title='Date', yaxis_title='Humidité (%)')
    st.plotly_chart(fig)

    # with col2:
     # Deuxième graphique - Indice de végétation (en vert)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=soil_data['Date'],
        y=soil_data['VegetationIndex'],
        name='Indice de végétation',
        line=dict(color='#2ecc71')  # Couleur verte
    ))
    fig2.update_layout(
        title='Indice de végétation',
        xaxis_title='Date',
        yaxis_title='Indice',
        height=400  # Hauteur fixe pour le graphique
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Troisième graphique - Graphique combiné avec deux axes y
    fig3 = go.Figure()
    
    # Ajout des barres pour l'humidité du sol (axe y principal)
    fig3.add_trace(go.Bar(
        x=soil_data['Date'],
        y=soil_data['Humidité du sol'],
        name='Humidité du sol',
        marker_color='#3498db',  # Bleu
        opacity=0.7,
        yaxis='y'
    ))
    
    # Ajout des barres pour l'indice de végétation (axe y secondaire)
    fig3.add_trace(go.Scatter(
        x=soil_data['Date'],
        y=soil_data['VegetationIndex'],
        name='Indice de végétation',
        marker_color='#2ecc71',  # Vert
        opacity=0.7,
        yaxis='y2'
    ))
    
    # Mise en page du graphique avec deux axes y
    fig3.update_layout(
        title='Comparaison Humidité du sol et Indice de végétation',
        xaxis_title='Date',
        yaxis=dict(
            title='Humidité du sol (%)',
            titlefont=dict(color='#3498db'),
            tickfont=dict(color='#3498db')
        ),
        yaxis2=dict(
            title='Indice de végétation',
            titlefont=dict(color='#2ecc71'),
            tickfont=dict(color='#2ecc71'),
            overlaying='y',
            side='right'
        ),
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        # Ajuster les marges pour accommoder le deuxième axe y
        margin=dict(r=50)
    )
    
    st.plotly_chart(fig3, use_container_width=True)
