import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse des titres", layout="wide")

st.header("🧠 Analyse des titres produits")

# Vérifie si le flux est déjà chargé
if "flux_data" not in st.session_state:
    st.error("⚠️ Aucun flux détecté. Reviens sur la page d’accueil pour charger ton fichier.")
    st.stop()

flux = st.session_state["flux_data"]

# --- Vérification colonne titre ---
if "title" not in flux.columns:
    st.error("⚠️ La colonne 'title' est absente du flux.")
    st.stop()

# --- Statistiques de titres ---
nbtitre = len(flux['title'])
nbtitreunique = len(flux['title'].unique())
nbtitredoublon = nbtitre - nbtitreunique

st.write(f"Le flux comporte **{nbtitre}** titres dont **{nbtitreunique}** uniques et **{nbtitredoublon}** doublons.")

# --- Graphique ---
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

# Centrage
st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)