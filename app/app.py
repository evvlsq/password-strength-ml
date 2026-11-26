import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from zxcvbn import zxcvbn

RACINE = Path(__file__).resolve().parent.parent
sys.path.append(str(RACINE / "src"))

from features import extract_features
from suggestions import analyse


@st.cache_resource
def charger_modele():
    return joblib.load(RACINE / "models" / "model_rf.pkl")


model = charger_modele()

st.set_page_config(page_title="Analyseur de mots de passe", page_icon="🔐")
st.title("🔐 Analyseur intelligent de mots de passe")
st.caption("Aucun mot de passe n'est enregistré, ni écrit dans un fichier.")

pw = st.text_input("Saisissez un mot de passe à tester", type="password")

if pw:
    r = analyse(pw, model)

    if r["classe"] == 0:
        st.progress(0.33)
        st.error("Force : FAIBLE")
    elif r["classe"] == 1:
        st.progress(0.66)
        st.warning("Force : MOYENNE")
    else:
        st.progress(1.0)
        st.success("Force : FORTE")

    st.subheader("Suggestions pour l'améliorer")
    for c in r["conseils"]:
        st.write("- " + c)

    with st.expander("Comparaison avec zxcvbn (référence)"):
        z = zxcvbn(pw[:72])
        st.write(f"Score zxcvbn : {z['score']} sur 4")
        st.write(
            "Temps estimé pour le casser (attaque hors ligne rapide) : "
            + z["crack_times_display"]["offline_fast_hashing_1e10_per_second"]
        )

    with st.expander("Mesures utilisées par le modèle"):
        tableau = pd.DataFrame([extract_features(pw)]).T
        tableau.columns = ["valeur"]
        st.dataframe(tableau)

st.divider()
st.caption(
    "Limite : le modèle est entraîné sur un dataset dont les étiquettes suivent des règles simples. "
    "zxcvbn donne une estimation plus réaliste de la résistance réelle."
)