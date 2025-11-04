import streamlit as st
import pandas as pd

st.set_page_config(page_title="Audit de flux produits", page_icon="🧩", layout="wide")

st.title("Audit de flux produits")

st.markdown("""
Bienvenue dans ton outil d’audit de flux produits !  
Voici comment ça fonctionne :
1. **Upload ton flux** sur cette page  
2. Accède ensuite à :
   - 📊 *Analyse du flux* (structure, champs manquants, etc.)
   - 🧠 *Analyse des titres* (doublons, longueur, qualité)
""")

# --- Upload du fichier ---
uploaded_file = st.file_uploader("📥 Charge ton flux produit (.csv)", type=["csv"])

if uploaded_file:
    try:
        flux = pd.read_csv(uploaded_file, sep=None, engine='python')
        st.session_state["flux_data"] = flux  # 🔹 Stockage dans la session
        st.success("✅ Flux chargé et enregistré en mémoire.")
        st.dataframe(flux.head())
        st.info("Tu peux maintenant aller dans les pages d’analyse via la barre latérale.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("💡 En attente d’un fichier CSV.")
