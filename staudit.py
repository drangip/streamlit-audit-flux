import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
import csv

# =========================================================
# 🧩 CONFIGURATION DE L'APPLICATION
# =========================================================
st.set_page_config(
    page_title="Audit de flux produits",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🧠 Audit de flux produits")
st.markdown("Analyse automatique de la qualité de ton flux CSV (Google Merchant, Criteo, etc.)")
st.markdown("---")

# =========================================================
# ⚙️ FONCTION : détection automatique du séparateur
# =========================================================
def detect_separator(uploaded_file):
    sample = uploaded_file.read(2048).decode("utf-8")
    uploaded_file.seek(0)
    dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "|"])
    return dialect.delimiter


# =========================================================
# 🧠 FONCTION : chargement du fichier (mise en cache)
# =========================================================
@st.cache_data
def load_data(uploaded_file):
    sep = detect_separator(uploaded_file)
    df = pd.read_csv(uploaded_file, sep=sep)
    return df, sep


# =========================================================
# 🧮 UPLOAD DU FICHIER
# =========================================================
uploaded_file = st.file_uploader("📂 Charge ton flux produit", type=["csv"])

if not uploaded_file:
    st.info("⬆️ En attente du chargement du fichier CSV.")
    st.stop()

# Lecture + cache
try:
    flux, sep = load_data(uploaded_file)
    st.success(f"✅ Fichier chargé avec succès ! Séparateur détecté : `{sep}`")
except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")
    st.stop()


# =========================================================
# 🧭 NAVIGATION PAR ONGLETS
# =========================================================
tab1, tab2, tab3 = st.tabs(["📊 Aperçu & infos générales", "🔍 Qualité des données", "🧾 Analyse des titres"])

# =========================================================
# 🔹 ONGLET 1 : INFOS GÉNÉRALES
# =========================================================
with tab1:
    st.header("01. Aperçu du flux")
    st.write(f"Le flux contient **{flux.shape[0]} produits** et **{flux.shape[1]} colonnes.**")
    st.dataframe(flux.sample(min(5, len(flux))))

    with st.expander("Voir toutes les colonnes disponibles"):
        st.write(list(flux.columns))

# =========================================================
# 🔹 ONGLET 2 : QUALITÉ DES DONNÉES
# =========================================================
with tab2:
    st.header("02. Analyse de la qualité des données")

    st.subheader("Visualisation des données manquantes")
    fig, ax = plt.subplots(figsize=(25, 5))
    msno.matrix(flux, ax=ax)
    st.pyplot(fig)

    st.subheader("Colonnes entièrement vides")
    fluxna = flux.loc[:, flux.isna().all()]
    if fluxna.shape[1] == 0:
        st.success("🎉 Aucune colonne entièrement vide !")
    else:
        st.warning(f"{fluxna.shape[1]} colonnes entièrement vides :")
        st.write(list(fluxna.columns))

# =========================================================
# 🔹 ONGLET 3 : ANALYSE DES TITRES
# =========================================================
with tab3:
    st.header("03. Analyse des titres")

    if "title" not in flux.columns:
        st.error("❌ La colonne 'title' est introuvable dans le flux.")
        st.stop()

    # --- Doublons ---
    st.subheader("a. Doublons")
    nbtitre = len(flux['title'])
    nbtitreunique = len(flux['title'].unique())
    nbtitredoublon = nbtitre - nbtitreunique

    st.write(f"Le flux comporte **{nbtitre}** titres dont **{nbtitreunique}** uniques, soit **{nbtitredoublon}** doublons.")

    pourcentagetitre = {
        "Titres uniques": nbtitreunique,
        "Titres en doublon": nbtitredoublon
    }

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        pourcentagetitre.values(),
        labels=pourcentagetitre.keys(),
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'width': 0.4, 'edgecolor': 'white'},
        colors=[(0, 0.7, 0, 0.6), (1, 0, 0, 0.6)]
    )
    st.pyplot(fig)

    # --- Longueur des titres ---
    st.subheader("b. Longueur des titres")
    st.caption("*(La longueur maximale recommandée est de 150 caractères)*")

    dftitle = pd.DataFrame(flux['title'])
    dftitle['nb_caracteres'] = dftitle['title'].astype(str).str.len()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Moyenne", round(dftitle['nb_caracteres'].mean(), 2))
    col2.metric("Médiane", round(dftitle['nb_caracteres'].median(), 2))
    col3.metric("Min", round(dftitle['nb_caracteres'].min(), 2))
    col4.metric("Max", round(dftitle['nb_caracteres'].max(), 2))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(dftitle['nb_caracteres'], bins=80, color='skyblue', edgecolor='black')
    ax.set_title("Distribution du nombre de caractères des titres", fontsize=14)
    ax.set_xlabel("Nombre de caractères")
    ax.set_ylabel("Nombre de titres")
    st.pyplot(fig)