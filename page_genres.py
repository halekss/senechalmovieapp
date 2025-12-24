import streamlit as st

def show(df):
    # Titre Style "Ticket" simplifié
    st.markdown("<h1 style='text-align: center;'>📂 LE CATALOGUE</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- 1. ZONE DE FILTRES ---
    st.markdown("### 🔍 Affiner votre recherche")
    
    # --- Préparation des données (Langues & Genres) ---
    dico_langues = {
        'de': '🇩🇪 Allemand', 'en': '🇬🇧 Anglais', 'ar': '🇸🇦 Arabe', 'hy': '🇦🇲 Arménien',
        'eu': '🏞️ Basque', 'bs': '🇧🇦 Bosnien', 'cn': '🇭🇰 Cantonais', 'zh': '🇨🇳 Chinois (Mandarin)',
        'ko': '🇰🇷 Coréen', 'hr': '🇭🇷 Croate', 'da': '🇩🇰 Danois', 'es': '🇪🇸 Espagnol',
        'fi': '🇫🇮 Finnois', 'fr': '🇫🇷 Français', 'ka': '🇬🇪 Géorgien', 'he': '🇮🇱 Hébreu',
        'hi': '🇮🇳 Hindi', 'hu': '🇭🇺 Hongrois', 'id': '🇮🇩 Indonésien', 'is': '🇮🇸 Islandais',
        'it': '🇮🇹 Italien', 'ja': '🇯🇵 Japonais', 'ku': '🧣 Kurde', 'lv': '🇱🇻 Letton',
        'mk': '🇲🇰 Macédonien', 'ne': '🇳🇵 Népalais', 'no': '🇳🇴 Norvégien', 'ur': '🇵🇰 Ourdou',
        'fa': '🇮🇷 Persan', 'pl': '🇵🇱 Polonais', 'pt': '🇵🇹 Portugais', 'ro': '🇷🇴 Roumain',
        'ru': '🇷🇺 Russe', 'sr': '🇷🇸 Serbe', 'sv': '🇸🇪 Suédois', 'ta': '🇮🇳 Tamoul',
        'cs': '🇨🇿 Tchèque', 'th': '🇹🇭 Thaïlandais', 'tr': '🇹🇷 Turc', 'uk': '🇺🇦 Ukrainien',
        'vi': '🇻🇳 Vietnamien', 'xx': '❓ Inconnu'
    }

    codes_bruts = df['Langue Originale'].dropna().unique().tolist()
    
    # Tri alphabétique sur le NOM du pays
    liste_codes = sorted(
        codes_bruts, 
        key=lambda x: dico_langues.get(x, x).split(' ', 1)[1] if ' ' in dico_langues.get(x, x) else x
    )
    
    def format_langue(option): return dico_langues.get(option, option.upper()) if option != "Aucun" else "Indifférent"

    # Récupération des genres
    all_genres = set()
    for g_str in df['Genres_Filter'].fillna(""):
        parts = g_str.replace(',', ' ').split()
        for p in parts:
            if len(p) > 2:
                all_genres.add(p)
    liste_genres = sorted(list(all_genres))

    # --- Mise en page 2 Colonnes ---
    col_f1, col_f2 = st.columns(2)
    
    # COLONNE 1 : Genres + Langue
    with col_f1:
        genres_selection = st.multiselect(
            "🎭 Genres :",
            options=liste_genres,
            default=[],
            placeholder="Action, Drame..."
        )
        
        # Ajout du sélecteur de langue
        langue_sel = st.selectbox("🗣️ Pays d'origine", ["Aucun"] + liste_codes, format_func=format_langue)

    # COLONNE 2 : Année + Note
    with col_f2:
        min_year = int(df['Annee_sortie'].min())
        max_year = int(df['Annee_sortie'].max())
        
        annee_range = st.slider(
            "📅 Période :",
            min_value=min_year,
            max_value=max_year,
            value=(2000, max_year)
        )

        note_min = st.slider(
            "⭐ Note minimum :",
            min_value=4.0,
            max_value=10.0,
            value=6.0,
            step=0.5
        )

    # --- 2. APPLICATION DES FILTRES ---
    df_filtered = df.copy()

    # Filtre Genre
    if genres_selection:
        def check_genre(g_str):
            film_genres = set(g_str.replace(',', ' ').split())
            return not set(genres_selection).isdisjoint(film_genres)
        df_filtered = df_filtered[df_filtered['Genres_Filter'].apply(check_genre)]

    # Filtre Langue
    if langue_sel != "Aucun":
        df_filtered = df_filtered[df_filtered['Langue Originale'] == langue_sel]

    # Filtre Année
    df_filtered = df_filtered[
        (df_filtered['Annee_sortie'] >= annee_range[0]) & 
        (df_filtered['Annee_sortie'] <= annee_range[1])
    ]

    # Filtre Note
    df_filtered = df_filtered[df_filtered['Moyenne des votes'] >= note_min]

    # --- 2.5 AJOUT DU SÉLECTEUR DE TRI (ICI) ---
    st.markdown("<br>", unsafe_allow_html=True) # Petit espace
    col_tri, col_vide = st.columns([1, 2]) # On utilise une colonne pour ne pas que ça prenne toute la largeur
    
    with col_tri:
        mode_tri = st.radio(
            "Ordre d'affichage :", 
            ["🔥 Popularité", "🎲 Hasard"], 
            horizontal=True
        )

    # Application du tri selon le choix
    if mode_tri == "🎲 Hasard":
        # On mélange tout (frac=1 signifie 100% du dataframe)
        df_filtered = df_filtered.sample(frac=1).reset_index(drop=True)
    else:
        # On trie par popularité (du plus grand au plus petit)
        df_filtered = df_filtered.sort_values(by='Popularité', ascending=False)


    # --- 3. AFFICHAGE RÉSULTATS ---
    nb_films = len(df_filtered)
    st.markdown("---")
    st.markdown(f"**🎬 {nb_films} films correspondent à vos critères**")
    
    if nb_films == 0:
        st.warning("😕 Aucun film ne correspond à cette recherche. Essayez d'élargir les critères !")
    else:
        # Pagination légère
        if nb_films > 100:
            st.info("⚠️ Affichage des 100 premiers films de la sélection.")
            df_filtered = df_filtered.head(100)

        # GRILLE DE FILMS (5 colonnes)
        cols = st.columns(5)
        for i, (index, film) in enumerate(df_filtered.iterrows()):
            col = cols[i % 5]
            with col:
                # Préparation variables
                img_url = film.get('Affiche du Film', '')
                if not (isinstance(img_url, str) and "http" in img_url):
                    img_url = "https://via.placeholder.com/300x450"
                
                titre = film['Titre']
                if len(titre) > 20: titre = titre[:17] + "..."
                
                # CARTE HTML (Image + Titre intégré)
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{img_url}">
                    <div class="movie-card-title">{titre}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Infos supplémentaires en dessous
                st.caption(f"⭐ {film.get('Moyenne des votes', '-')}/10 | {int(film.get('Annee_sortie', 0))}")
                st.markdown("<br>", unsafe_allow_html=True)