import streamlit as st
import random
import folium
from streamlit_folium import st_folium

def show(df):
     # --- 2. TEXTE D'INTRO ---
    # Création de deux colonnes
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown("### 🍿 BIENVENUE DANS VOTRE ESPACE")
        st.write("""
        Un nouveau souffle pour vos soirées cinéma.
        Notre application inédite est là pour transformer la façon dont vous choisissez vos films.

        Ici, vous reprenez le contrôle : c'est vous le maître de votre prochaine séance. Que vous ayez une envie ciblée par genre ou que vous cherchiez une recommandation précise basée sur un film que vous avez déjà aimé, tout est conçu pour vous guider.

        Laissez-vous porter par cette nouvelle expérience et trouvez le film parfait, sans effort.
        """)

    # Colonne de droite : Infos pratiques et carte
    with col2:
        st.markdown("""
        <small>
        Cinéma Le Sénéchal<br>
        1 Rue du Sénéchal, 23000 Guéret<br>
        05 55 52 26 44<br>
        cinema.senechal@gmail.com<br>
        <a href="https://www.cinema-senechal.com/" target="_blank" style="color: #D4AF37;">Notre site direct</a><br>
        <a href="https://www.facebook.com/cinema.lesenechal/?locale=fr_FR" target="_blank" style="color: #D4AF37;">Notre Facebook pour suivre nos actualités</a>
        </small>
        """, unsafe_allow_html=True)   
         
        # Carte Folium
        map_center = [46.1707, 1.8687]
        m = folium.Map(location=map_center, zoom_start=15)
        folium.Marker(
            map_center, 
            popup="Le Sénéchal", 
            tooltip="Le Sénéchal",
            icon=folium.Icon(color='red', icon='film')
        ).add_to(m)
        
        st_folium(m, width=400, height=300)
        
    # --- 3. FILMS À L'AFFICHE ---
    st.markdown("---")
    st.subheader("🔥 ACTUELLEMENT À L'AFFICHE")
    
    if df is not None and not df.empty:
        # Sélection aléatoire de 5 films parmi les populaires
        top_films = df.sort_values(by='Popularité', ascending=False).head(100)
        selection = top_films.sample(n=5)
        
        cols = st.columns(5)
        for idx, (index, film) in enumerate(selection.iterrows()):
            with cols[idx]:
                # Préparation des variables
                img_url = film.get('Affiche du Film', '')
                if not (isinstance(img_url, str) and "http" in img_url):
                    img_url = "https://via.placeholder.com/300x450"
                
                titre = film['Titre']
                if len(titre) > 20: titre = titre[:17] + "..."

                # ON CRÉE LA CARTE HTML UNIQUE
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{img_url}" alt="{titre}">
                    <div class="movie-card-title">{titre}</div>
                </div>
                """, unsafe_allow_html=True)