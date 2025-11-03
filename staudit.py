# ==================================================
# 📊 Audit de flux produits - Version Dashboard Pro
# ==================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
from wordcloud import WordCloud

# ======================================
# 🎨 CONFIG GLOBALE DE L'APP
# ======================================
st.set_page_config(
    page_title="Audit de flux produits",
    page_icon="🧩",
    layout="wide"
)

# Style Streamlit custom (petit CSS sympa)
st.markdown("""
<style>
    .main {
        background-color: #F9FAFB;
        color: #111;
    }
    h1, h2, h3 {
        color: #333;
    }
    .stMetric {
        background: white;
        padding: 8px;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# 🏷️ 01. UPLOAD DU FLUX
# ======================================
st.title("🧩 Audit de flux produits")
st.markdown("Analyse automatique de la qualité et du contenu d’un flux e-commerce.")
st.divider()

st.subheader("📥 1. Import du flux produit")

uploaded_file = st.file_uploader("Charge ton flux (.csv)", type=["csv"])
if not uploaded_file:
    st.info("💡 En attente du fichier...")
    st.stop()

# Lecture intelligente du CSV avec détection du séparateur
try:
    flux = pd.read_csv(uploaded_file, sep=None, engine='python')
    st.success("✅ Fichier chargé avec succès !")
except Exception as e:
    st.error(f"Erreur de lecture du fichier : {e}")
    st.stop()

# ======================================
# 📊 02. PREMIÈRES ANALYSES
# ======================================
st.subheader("🔍 2. Premières analyses")
st.write(f"Le flux contient **{flux.shape[0]} produits** et **{flux.shape[1]} colonnes.**")

st.write("### Aperçu du flux")
st.dataframe(flux.head())

# --- Graph des valeurs manquantes ---
st.write("### Données manquantes")
col_graph1, _ = st.columns([1, 1])
with col_graph1:
    fig, ax = plt.subplots(figsize=(10, 3))
    msno.matrix(flux, ax=ax)
    st.pyplot(fig)

# --- Colonnes entièrement vides ---
fluxna = flux.loc[:, flux.isna().all()]
if fluxna.shape[1] == 0:
    st.success("Aucune colonne entièrement vide dans le flux 🎉")
else:
    st.warning("Colonnes vides détectées :")
    st.write(list(fluxna.columns))

st.divider()

# ======================================
# 🧠 03. ANALYSE DES TITRES
# ======================================
st.subheader("🧠 3. Analyse des titres produits")

# Vérifie la présence d'une colonne "title"
if "title" not in flux.columns:
    st.error("⚠️ Le flux ne contient pas de colonne 'title'. Analyse impossible.")
    st.stop()

# --- Doublons ---
nbtitre = len(flux['title'])
nbtitreunique = len(flux['title'].unique())
nbtitredoublon = nbtitre - nbtitreunique

st.write(f"Le flux comporte **{nbtitre}** titres, dont **{nbtitreunique}** uniques et **{nbtitredoublon}** doublons.")

col1, col2 = st.columns(2)

with col1:
    pourcentagetitre = {
        "Titres uniques": nbtitreunique,
        "Titres en doublon": nbtitredoublon
    }
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
    st.pyplot(fig)

with col2:
    st.write("📋 Répartition des titres")
    st.dataframe(pd.DataFrame(pourcentagetitre, index=["Quantité"]))

st.divider()

# --- Longueur des titres ---
st.subheader("📏 4. Longueur des titres")

dftitle = pd.DataFrame(flux['title'])
dftitle['nb_caracteres'] = dftitle['title'].astype(str).str.len()

titlemean = round(dftitle['nb_caracteres'].mean(), 2)
titlemedian = round(dftitle['nb_caracteres'].median(), 2)
titlemax = round(dftitle['nb_caracteres'].max(), 2)
titlemin = round(dftitle['nb_caracteres'].min(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Moyenne", f"{titlemean} car.")
col2.metric("Médiane", f"{titlemedian} car.")
col3.metric("Min", f"{titlemin} car.")
col4.metric("Max", f"{titlemax} car.")

col_graph, _ = st.columns([1, 1])
with col_graph:
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(dftitle['nb_caracteres'], bins=60, color='skyblue', edgecolor='black')
    ax.set_title("Distribution du nombre de caractères", fontsize=12, fontweight='bold')
    ax.set_xlabel("Nombre de caractères")
    ax.set_ylabel("Nombre de titres")
    plt.tight_layout()
    st.pyplot(fig)
