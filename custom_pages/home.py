import streamlit as st

def show():
    # En-tête
    st.markdown("# 🌍 HydroSense")
    st.markdown("Optimisez votre irrigation pour une agriculture durable")
    
    # Cartes des fonctionnalités principales
    st.markdown("## Fonctionnalités principales")

    # Créer deux colonnes pour afficher les images côte à côte
    col1, col2 = st.columns(2)

    # Fonctionnalité 1: Analyse Précise avec image
    with col1:
        st.markdown("### 📊 Analyse Précise")
        st.markdown("""
            Accédez à des données climatiques fiables et des analyses détaillées pour prendre les meilleures décisions.
        """)
        # Définir la taille fixe pour l'image
        st.image("assets/image4.jpg", caption="Analyse Précise", width=400)  # Ajuster la largeur ici

    # Fonctionnalité 2: Gestion Intelligente avec image
    with col2:
        st.markdown("### 💧 Gestion Intelligente")
        st.markdown("""
            Optimisez votre consommation d'eau grâce à nos recommandations personnalisées basées sur l'IA.
        """)
        # Définir la même taille fixe pour l'image
        st.image("assets/image2.jpg", caption="Gestion Intelligente", width=400)  # Ajuster la largeur ici

    # Fonctionnalité 3: Agriculture Durable
    st.markdown("### 🌱 Agriculture Durable")
    st.markdown("""
        Contribuez à la préservation des ressources tout en maximisant vos rendements agricoles.
    """)

    # Section des avantages avec métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Économie d'eau", value="30%", delta="vs méthodes traditionnelles")
    with col2:
        st.metric(label="Précision", value="95%", delta="fiabilité des données")
    with col3:
        st.metric(label="Productivité", value="+25%", delta="rendement agricole")

    # Bandeau d'astuce animé
    st.markdown("""
        💡 <strong>Astuce du jour :</strong> Consultez nos recommandations quotidiennes d'irrigation 
        pour optimiser votre consommation d'eau en fonction des prévisions météorologiques.
    """)

    # Section "Pour commencer" avec des étapes
    st.markdown("### 🚀 Pour commencer")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
            1. Sélectionnez votre parcelle sur la carte
            2. Analysez les données climatiques
            3. Suivez nos recommandations personnalisées
        """)
    
    with col2:
        st.success("""
            **Besoin d'aide ?**
            
            Consultez notre guide d'utilisation ou contactez notre équipe support pour un accompagnement personnalisé.
        """)
