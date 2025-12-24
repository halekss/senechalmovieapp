import streamlit as st

def show(df):
    # Titre Doré Spécifique
    st.markdown("<h1 style='text-align: center; color: #D4AF37 !important;'>🌟 HALL OF FAME 🌟</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Découvrez les stars du Cinéma Senechal</p>", unsafe_allow_html=True)
    
    acteurs = sorted(df['Identité'].unique())
    
    # Barre de recherche centrée
    c_vide1, c_search, c_vide2 = st.columns([1, 2, 1])
    with c_search:
        choix = st.selectbox("Rechercher une star :", acteurs, label_visibility="collapsed")

    if choix:
        info = df[df['Identité'] == choix].iloc[0]
        
        st.markdown("---")
        
        # Mise en page : Photo (1/3) | Biographie (2/3)
        col_photo, col_bio = st.columns([1, 2], gap="medium")
        
        with col_photo:
            st.markdown(f"<h2 style='text-align: center; color: white !important;'>{info['Identité']}</h2>", unsafe_allow_html=True)
            
            p = info['photo']
            # Affichage de l'image
            st.image(p if isinstance(p, str) and "http" in p else "https://via.placeholder.com/300?text=No+Photo", use_container_width=True)
            
            if 'Métier' in info and info['Métier']:
                st.markdown(f"<div style='text-align:center; padding: 10px; border: 1px solid #D4AF37; border-radius: 5px; margin-top: 10px;'>🎥 {info['Métier']}</div>", unsafe_allow_html=True)
        
        with col_bio:
            # Boite de Biographie Stylisée (CSS injecté localement pour faire le cadre)
            st.markdown(f"""
            <div style='
                background-color: rgba(255, 255, 255, 0.05); 
                padding: 25px; 
                border-radius: 10px; 
                border-left: 5px solid #D4AF37;
                height: 100%;
            '>
                <h3 style='margin-top: 0; color: #D4AF37 !important;'>Biographie</h3>
                <p style='line-height: 1.8; font-size: 1.1em; text-align: justify;'>
                    {info['Biographie']}
                </p>
            </div>
            """, unsafe_allow_html=True)