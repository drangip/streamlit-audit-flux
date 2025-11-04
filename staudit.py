# ======================================
# Import des librairies
# ======================================

import streamlit as st
import pandas as pd
import numpy as np
import random
import requests
from matplotlib import pyplot as plt 
import seaborn as sns
import missingno as msno
from wordcloud import WordCloud

# ======================================
# Setup de la page
# ======================================


st.set_page_config(
    page_title="Shopping feed audit - sample", page_icon="🔍",
)

st.sidebar("Shopping feed audit - sample")

st.write("# Welcome to our automatic shopping feed audit!")

st.markdown(
    """
This is a sample Streamlit application that performs an automatic audit of a shopping feed (product data file).
"""
)


st.set_page_config(page_title="Import your csv fils", page_icon="📥")

st.markdown("Import your csv fils")
st.sidebar.header("Import your csv fils")
st.write(
    """You can upload your product feed in CSV format, and the application will analyze it and provide insights on data quality, missing values, and product title analysis."""
)


# =========================================================
# FONCTION : détection automatique du séparateur
# =========================================================
def detect_separator(uploaded_file):
    sample = uploaded_file.read(2048).decode("utf-8")
    uploaded_file.seek(0)
    dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "|"])
    return dialect.delimiter


# =========================================================
# FONCTION : chargement du fichier (mise en cache)
# =========================================================
@st.cache_data
def load_data(uploaded_file):
    sep = detect_separator(uploaded_file)
    df = pd.read_csv(uploaded_file, sep=sep)
    return df, sep


# =========================================================
# 🧮 UPLOAD DU FICHIER
# =========================================================

st.sidebar.header("Plotting Demo")
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

# ======================================
# 📊 02. PREMIÈRES ANALYSES
# ======================================
st.subheader("2. Premières analyses")
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