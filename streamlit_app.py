import streamlit as st

# 1. CONFIGURATION (Doit être la première commande Streamlit)
st.set_page_config(page_title="Senechal Movie", page_icon="🎬", layout="wide")

# 2. IMPORTS DES MODULES (C'est ce qui manquait !)
import utils          
import page_genres     
import page_reco       
import page_acteurs 
import page_accueil   

# 3. CHARGEMENT DONNÉES & STYLE
utils.inject_custom_css() 
df_films, df_scaler, df_acteurs, model = utils.load_all_data()

# 4. MISE EN PAGE : GAUCHE (MENU) | DROITE (ILLUSTRATION)
col_gauche, col_illustration = st.columns([0.8, 2], gap="large") 

# --- COLONNE GAUCHE : LOGO & MENU ---
with col_gauche:
    # Logo
    st.markdown("""
        <div style="text-align: left;">
            <span style="font-family: 'Bebas Neue'; font-size: 90px; color: white; line-height: 0.8;">SENECHAL<br>
            <span style="color: #D4AF37;">MOVIE</span></span>
        </div>
        <hr>
    """, unsafe_allow_html=True)
    
    if 'page' not in st.session_state: st.session_state.page = "accueil"

    # Espacement
    st.write("")
    
  
    
    # MENU VERTICAL
    if st.button("ACCUEIL", use_container_width=True): 
        st.session_state.page = "accueil"
        
    if st.button("CATALOGUE", use_container_width=True): 
        st.session_state.page = "genres"
        
    if st.button("RECOMMANDATION", use_container_width=True): 
        st.session_state.page = "reco"
        
    if st.button("ACTEURS", use_container_width=True): 
        st.session_state.page = "acteurs"

# --- COLONNE DROITE : ILLUSTRATION THÉMATIQUE ---
with col_illustration:
    # Petits sauts de ligne pour aligner l'image avec le logo
    st.write("") 
    st.write("")
    

    # Image Cinéma
    st.image("avatar_2.jpg", use_container_width=True)


# 5. AFFICHAGE DES PAGES
st.markdown("---") 

if st.session_state.page == "accueil":
    if df_films is not None:
        page_accueil.show(df_films)

elif st.session_state.page == "genres":
    if df_films is not None: page_genres.show(df_films)

elif st.session_state.page == "reco":
    if df_films is not None and df_scaler is not None: page_reco.show(df_films, df_scaler, model)

elif st.session_state.page == "acteurs":
    if df_acteurs is not None: page_acteurs.show(df_acteurs)