import streamlit as st
import pandas as pd
import numpy as np
import random
import requests
from matplotlib import pyplot as plt
import seaborn as sns

import missingno as msno

from wordcloud import WordCloud

# 🏷️ Titre de ton app
st.title("Audit de flux produits")

st.markdown("## 01. Upload du flux à analyser")
st.markdown("---")


# 📂 Import des données
uploaded_file = st.file_uploader("Charge ton ton flux produit", type=["csv"])
if uploaded_file:
    flux = pd.read_csv(uploaded_file, sep=",")
    st.success("Fichier chargé avec succès !")
else:
    st.info("En attente du chargement du fichier...")
    st.stop() 


st.markdown("## 02. Premières analyses")
st.markdown("---")


st.write(f"Le flux comprend {flux.shape[0]} lignes (produits) et {flux.shape[1]} colonnes.")

st.write("Vous trouverez ci-dessous un aperçu du flux :", flux.sample(5))

st.write("Visualisation des données manquantes :")

# Création du graphique missingno
fig, ax = plt.subplots(figsize=(25, 5))
msno.matrix(flux, ax=ax)

# Affichage dans Streamlit
st.pyplot(fig)


st.write("Les colonnes suivantes du flux sont vides :")

fluxna = flux.loc[:, flux.isna().all()]

if fluxna.shape[1] == 0:
    st.success("Aucune colonne entièrement vide dans le flux.")
else:
    st.write(list(fluxna.columns))


st.markdown("## 03.Analyse des éléments du flux")
st.markdown("---")


st.markdown("### a. Analyse des doublons")


# --- Calculs ---
nbtitre = round(len(flux['title']), 2)
nbtitreunique = round(len(flux['title'].unique()), 2)
nbtitredoublon = nbtitre - nbtitreunique

# --- Affichage texte Streamlit ---
st.write(f"Le flux comporte **{nbtitre}** titres dont **{nbtitreunique}** sont uniques, soit **{nbtitredoublon}** doublons.")

# --- DataFrame récap ---
pourcentagetitre = {
    "Titres uniques": nbtitreunique,
    "Titres en doublon": nbtitredoublon
}
st.dataframe(pd.DataFrame(pourcentagetitre, index=["Quantité"]))

# --- Création du graphique ---
fig, ax = plt.subplots(figsize=(5, 5))

# 🔹 Couleurs personnalisées avec opacité
colors = []
for label in pourcentagetitre.keys():
    if "doublon" in label.lower():
        colors.append((1, 0, 0, 0.6))  # rouge semi-transparent
    elif "unique" in label.lower():
        colors.append((0, 0.7, 0, 0.6))  # vert semi-transparent
    else:
        colors.append((0.6, 0.6, 0.6, 0.5))  # gris clair par défaut

# 🔹 Camembert (donut)
wedges, texts, autotexts = ax.pie(
    pourcentagetitre.values(),
    labels=pourcentagetitre.keys(),
    autopct='%1.1f%%',
    startangle=90,
    counterclock=False,
    wedgeprops={'width': 0.4, 'edgecolor': 'white'},
    colors=colors,
    pctdistance=0.7
)

# 🔹 Style du texte
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(6)
    autotext.set_fontweight('bold')

plt.tight_layout()

# --- Affichage dans Streamlit ---
st.pyplot(fig)

# --- Calculs de longueur de titres ---
dftitle = pd.DataFrame(flux['title'])
dftitle['nb_caracteres'] = dftitle['title'].astype(str).str.len()

titlemean = round(dftitle['nb_caracteres'].mean(), 2)
titlemedian = round(dftitle['nb_caracteres'].median(), 2)
titlemax = round(dftitle['nb_caracteres'].max(), 2)
titlemin = round(dftitle['nb_caracteres'].min(), 2)

# --- Bloc de texte Streamlit ---
st.markdown("### b. Analyse de la taille des titres")
st.write("*(La longueur maximale recommandée est de **150 caractères**)*")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Moyenne", f"{titlemean} car.")
col2.metric("Médiane", f"{titlemedian} car.")
col3.metric("Min", f"{titlemin} car.")
col4.metric("Max", f"{titlemax} car.")

# --- Histogramme Streamlit ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(
    dftitle['nb_caracteres'],
    bins=80,
    color='skyblue',
    edgecolor='black'
)

# Titre et axes
ax.set_title("Distribution du nombre de caractères des titres", fontsize=14, fontweight='bold')
ax.set_xlabel("Nombre de caractères")
ax.set_ylabel("Nombre de titres")
ax.legend()

plt.tight_layout()
st.pyplot(fig)
