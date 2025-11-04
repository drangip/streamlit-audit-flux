import streamlit as st
import matplotlib.pyplot as plt
import missingno as msno

st.set_page_config(page_title="Analyse global du flux", layout="wide")

st.header("📊 Analyse global du flux")

# Vérifie si le flux existe dans la session
if "flux_data" not in st.session_state:
    st.error("⚠️ Aucun flux détecté. Reviens sur la page d’accueil pour charger ton fichier.")
    st.stop()

flux = st.session_state["flux_data"]

# --- Aperçu ---
st.subheader("Aperçu du flux")
st.dataframe(flux.head())

# --- Données manquantes ---
st.subheader("Visualisation des données manquantes")
fig, ax = plt.subplots(figsize=(10, 3))
msno.matrix(flux, ax=ax)
st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)