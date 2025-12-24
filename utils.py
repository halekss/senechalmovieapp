import pandas as pd
import streamlit as st
import os
import base64
from sklearn.neighbors import NearestNeighbors

# --- CONSTANTES ---
METADATA_COLS_SCALER = [
    'tconst', 'Id_TMDB', 'Titre', 'Titre Original', 'Résumé', 
    'Lien_vidéo', 'Affiche du Film', 'Logo', 'Langue Originale', 
    'Genres_List', 'Annee_sortie', 'Moyenne des votes', 'Nombre de votants', 'Popularité'
]

# --- CHARGEMENT DONNÉES ---
@st.cache_resource
def load_all_data():
    try:
        df_films = pd.read_csv("films.csv")
        
        # Sécurité Genres
        cols_fr = ['Genre Principal', 'Genre secondaire', 'Genre tertiaire']
        if all(col in df_films.columns for col in cols_fr):
            df_films['Genres_Filter'] = df_films[cols_fr].fillna('').astype(str).agg(' '.join, axis=1)
        elif 'Genres' in df_films.columns:
            df_films['Genres_Filter'] = df_films['Genres'].astype(str)
        else:
            df_films['Genres_Filter'] = ""

        df_scaler = pd.read_csv("df_films_scaler.csv")
        df_acteurs = pd.read_csv("intervenants_merge_total.csv")
        
        # Nettoyage Acteurs
        if not df_acteurs.empty:
            if 'Biographie' in df_acteurs.columns:
                df_acteurs = df_acteurs[df_acteurs['Biographie'] != 'Inconnu'].copy()
            if 'Photo de profil' in df_acteurs.columns:
                df_acteurs.rename(columns={'Photo de profil': 'photo'}, inplace=True)
            if 'photo' in df_acteurs.columns:
                df_acteurs['photo'] = df_acteurs['photo'].apply(
                    lambda x: "https://image.tmdb.org/t/p/w500"+x if isinstance(x, str) and not x.startswith('http') else x
                )

    except Exception as e:
        st.error(f"❌ Erreur critique chargement données : {e}")
        return None, None, None, None

    X = df_scaler.drop(columns=[c for c in METADATA_COLS_SCALER if c in df_scaler.columns], errors='ignore')
    X = X.select_dtypes(include=['number']).fillna(0)
    
    if not X.empty:
        model = NearestNeighbors(n_neighbors=6).fit(X)
    else:
        model = None

    return df_films, df_scaler, df_acteurs, model

def get_recommendations(df_films, df_scaler, model, film_title, n_reco=5):
    if df_films is None or film_title not in df_films['Titre'].values: return pd.DataFrame()
    try: idx = df_films[df_films['Titre'] == film_title].index[0]
    except: return pd.DataFrame()
    row_data = df_scaler.iloc[[idx]]
    X_input = row_data.drop(columns=[c for c in METADATA_COLS_SCALER if c in df_scaler.columns], errors='ignore')
    X_input = X_input.select_dtypes(include=['number']).fillna(0)
    if model:
        distances, indices = model.kneighbors(X_input, n_neighbors=n_reco+1)
        return df_films.iloc[indices[0][1:]]
    else: return pd.DataFrame()

# --- DESIGN (Correction ici !) ---
def get_img_as_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode()

def inject_custom_css():
    # On récupère le dossier où se trouve utils.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Charger le fichier CSS externe (style.css) avec un CHEMIN ABSOLU
    css_file = os.path.join(current_dir, "style.css") # <-- C'est ça la correction
    
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Si le fichier n'est pas trouvé, on force quand même un style minimal sombre
        st.markdown("""
        <style>
            .stApp { background-color: #0E1117; color: white; } 
            h1, h2, h3 { color: #E50914 !important; }
        </style>
        """, unsafe_allow_html=True)
    
    # 2. Gérer l'image de fond
    image_path = os.path.join(current_dir, "bandeau_senechal.png")
    img_b64 = get_img_as_base64(image_path)
    
    if img_b64:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_b64}");
            background-size: cover; 
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)