import streamlit as st
import utils 

def show(df_films, df_scaler, model):
    
    # À mettre juste après "def show(...):"
    # Titre avec icône
    st.markdown("<h1 style='text-align: center;'>🎟️ SÉANCE & RECOMMANDATION</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- 1. GESTION DE LA MÉMOIRE (Session State) ---
    if 'film_focus' not in st.session_state: 
        st.session_state.film_focus = None
    if 'reco_cliquee' not in st.session_state: 
        st.session_state.reco_cliquee = None

    # Fonction pour déclencher le zoom sur une recommandation
    def activer_zoom(film_data):
        st.session_state.reco_cliquee = film_data

    # Fonction pour fermer le zoom
    def fermer_zoom():
        st.session_state.reco_cliquee = None

    liste_titres = sorted(df_films['Titre'].unique())
    
    # On retrouve l'index du film en mémoire pour le pré-selectionner
    index_actuel = None
    if st.session_state.film_focus in liste_titres:
        index_actuel = liste_titres.index(st.session_state.film_focus)

    # Barre de recherche centrée
    c_vide1, c_search, c_vide2 = st.columns([1, 2, 1])
    with c_search:
        film_actuel = st.selectbox(
            "Rechercher un film :", 
            options=liste_titres,
            index=index_actuel,
            placeholder="Tapez un titre...",
            label_visibility="collapsed"
        )
    
    # Mise à jour de la mémoire : Si on change la recherche principale, on reset le zoom
    if film_actuel != st.session_state.film_focus:
        st.session_state.film_focus = film_actuel
        st.session_state.reco_cliquee = None # On ferme le zoom précédent

    # --- 2. AFFICHAGE FICHE FILM PRINCIPAL (Sans Bande Annonce) ---
    if film_actuel:
        row = df_films[df_films['Titre'] == film_actuel]
        if not row.empty:
            info_film = row.iloc[0]
            
            col_infos, col_poster = st.columns([1.5, 1], gap="large")
            
            # --- COLONNE GAUCHE : INFOS ---
            with col_infos:
                st.markdown(f"## {info_film['Titre']}")
                
                # Petits badges pour Année / Durée / Note
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"📅 **{info_film.get('Date de sortie', info_film.get('Annee_sortie', 'N/A'))}**")
                c2.markdown(f"⏱️ **{info_film.get('Durée', '?')} min**")
                c3.markdown(f"⭐ **{info_film.get('Moyenne des votes', 'N/A')}/10**")
                
                st.markdown("### Synopsis")
                st.write(info_film.get('Résumé', 'Pas de résumé disponible.'))
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(f"🎭 **Genres :** {str(info_film.get('Genres_Filter', '')).replace(' ', ', ')}")

                # SUPPRESSION DE LA BANDE ANNONCE ICI (Consigne appliquée)

            # --- COLONNE DROITE : AFFICHE ---
            with col_poster:
                img = info_film.get('Affiche du Film', '')
                if isinstance(img, str) and "http" in img:
                    st.image(img, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/400x600?text=No+Poster", use_container_width=True)

            # --- 3. RECOMMANDATIONS (LA PELLICULE) ---
            st.markdown("---")
            st.subheader("POURSUIVRE LA SÉANCE AVEC...")
            
            recos = utils.get_recommendations(df_films, df_scaler, model, film_actuel, n_reco=5)
            
            if not recos.empty:
                cols = st.columns(5)
                for idx, (original_idx, film_reco) in enumerate(recos.iterrows()):
                    with cols[idx]:
                        # Préparation variables
                        img_url = film_reco.get('Affiche du Film', '')
                        if not (isinstance(img_url, str) and "http" in img_url):
                            img_url = "https://via.placeholder.com/300x450"

                        titre = film_reco['Titre']
                        if len(titre) > 20: titre = titre[:17] + "..."
                        
                        # CARTE HTML
                        st.markdown(f"""
                        <div class="movie-card">
                            <img src="{img_url}">
                            <div class="movie-card-title">{titre}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Espace avant le bouton
                        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

                        # Bouton Voir (Streamlit natif)
                        st.button(
                            "👉 Ça m'intéresse !", 
                            key=f"btn_{original_idx}", 
                            on_click=activer_zoom, 
                            args=(film_reco,), 
                            use_container_width=True
                        )

            # --- 4. ZONE DE ZOOM (S'affiche en dessous si un bouton est cliqué) ---
        if st.session_state.reco_cliquee is not None:
            film_detail = st.session_state.reco_cliquee
            
            st.markdown("---")
            # Le titre reste en doré car c'est un titre h3
            st.markdown(f"<h3 style='text-align: center; color: #D4AF37;'>🔎 Zoom sur : {film_detail['Titre']}</h3>", unsafe_allow_html=True)
            
            col_z1, col_z2 = st.columns([2, 1])
            
            with col_z1:
                # Bande annonce
                lien_video = film_detail.get('Lien_vidéo', '')
                if isinstance(lien_video, str) and "http" in lien_video:
                    st.video(lien_video)
                else:
                    st.warning("🔇 Pas de bande-annonce disponible pour ce film.")
            
            with col_z2:
                st.markdown(f"**⭐ Note :** {film_detail.get('Moyenne des votes', '-')}/10")
                st.write(f"**Année :** {int(film_detail.get('Annee_sortie', 0))}")
                
                # --- BUDGET & RECETTES (Texte blanc standard) ---
                def format_money(val):
                    try:
                        v = float(val)
                        if v > 0:
                            return f"{v:,.0f} $".replace(",", " ")
                    except: pass
                    return "Non communiqué"

                bud = format_money(film_detail.get('Budget', 0))
                rec = format_money(film_detail.get('Revenue', film_detail.get('Recettes', 0)))

                # On utilise simplement st.write ou st.markdown sans HTML de couleur
                st.markdown(f"💰 **Budget :** {bud}")
                st.markdown(f"💵 **Recettes :** {rec}")
                # ------------------------------------------------

                st.markdown("<br>", unsafe_allow_html=True) 
                st.write(film_detail.get('Résumé', 'Pas de résumé.'))
                
                st.markdown("<br>", unsafe_allow_html=True)
                # Bouton Fermer
                st.button("❌ Fermer", on_click=fermer_zoom, key="btn_fermer_zoom", use_container_width=True)