import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno

# --- Config générale ---
st.set_page_config(page_title="Audit de flux produits", page_icon="🧩", layout="wide")

# --- Sidebar navigation ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Aller à :", [
    "🏠 Accueil",
    "📊 Analyse du flux",
    "🧠 Analyse des titres"
])

# --- CSS pour centrer les graphiques ---
st.markdown("""
    <style>
        .main {
            background-color: #F9FAFB;
        }
        div.block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .centered {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil":
    st.title("🧩 Audit de flux produits")
    st.markdown("""
    Bienvenue dans ton outil d’audit de flux produits !  
    Utilise la barre de gauche pour naviguer entre les sections :
    - **📊 Analyse du flux** pour voir la structure et les données manquantes  
    - **🧠 Analyse des titres** pour vérifier les doublons et la longueur
    """)
    st.info("Commence par aller dans l’onglet **Analyse du flux** pour uploader ton fichier CSV.")

# --- PAGE 2 : ANALYSE DU FLUX ---
elif page == "📊 Analyse du flux":
    st.header("📥 Upload du flux produit")

    uploaded_file = st.file_uploader("Charge ton flux (.csv)", type=["csv"])
    if not uploaded_file:
        st.info("💡 En attente du fichier...")
        st.stop()

    flux = pd.read_csv(uploaded_file, sep=None, engine='python')
    st.success("✅ Fichier chargé avec succès !")

    st.subheader("Aperçu du flux")
    st.dataframe(flux.head())

    st.subheader("Visualisation des données manquantes")
    fig, ax = plt.subplots(figsize=(10, 3))
    msno.matrix(flux, ax=ax)
    # ✅ Centrage du graphique
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 3 : ANALYSE DES TITRES ---
elif page == "🧠 Analyse des titres":
    st.header("Analyse des titres produits")

    uploaded_file = st.file_uploader("Recharger ton flux (.csv)", type=["csv"])
    if not uploaded_file:
        st.info("💡 En attente du fichier...")
        st.stop()

    flux = pd.read_csv(uploaded_file, sep=None, engine='python')

    if "title" not in flux.columns:
        st.error("⚠️ Le flux ne contient pas de colonne 'title'.")
        st.stop()

    nbtitre = len(flux['title'])
    nbtitreunique = len(flux['title'].unique())
    nbtitredoublon = nbtitre - nbtitreunique

    st.write(f"Le flux comporte **{nbtitre}** titres dont **{nbtitreunique}** uniques et **{nbtitredoublon}** doublons.")

    # --- Graph ---
    pourcentagetitre = {"Titres uniques": nbtitreunique, "Titres en doublon": nbtitredoublon}
    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        pourcentagetitre.values(),
        labels=pourcentagetitre.keys(),
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'width': 0.4, 'edgecolor': 'white'},
        colors=[(0, 0.7, 0, 0.6), (1, 0, 0, 0.6)]
    )
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(9)
    
    # ✅ Centrer le graphique
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
