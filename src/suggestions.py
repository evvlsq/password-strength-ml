import pandas as pd
from features import extract_features

MOTS_COURANTS = [
    "password", "motdepasse", "azerty", "qwerty", "admin", "welcome",
    "iloveyou", "letmein", "123456", "abc123", "football", "soleil",
]

NOMS_CLASSES = ["faible", "moyen", "fort"]


def get_suggestions(pw):
    """Analyse le mot de passe avec les features et renvoie une liste de conseils."""
    f = extract_features(pw)
    conseils = []

    if f["length"] < 12:
        conseils.append("Allongez-le : visez au moins 12 caractères.")
    if f["n_upper"] == 0:
        conseils.append("Ajoutez des majuscules.")
    if f["n_lower"] == 0:
        conseils.append("Ajoutez des minuscules.")
    if f["n_digit"] == 0:
        conseils.append("Ajoutez des chiffres.")
    if f["n_symbol"] == 0:
        conseils.append("Ajoutez des symboles (par exemple ! # $ % @).")
    if f["has_sequence"]:
        conseils.append("Évitez les suites logiques (123, abc, qwerty...).")
    if f["has_repeat"]:
        conseils.append("Évitez les caractères répétés (aaa, 111...).")
    if f["length"] >= 6 and f["n_unique"] < 0.6 * f["length"]:
        conseils.append("Variez davantage les caractères : beaucoup se répètent.")
    if any(mot in pw.lower() for mot in MOTS_COURANTS):
        conseils.append("Évitez les mots courants et les mots de passe connus.")

    if not conseils:
        conseils.append("Excellent ! Pensez à utiliser un gestionnaire de mots de passe.")
    return conseils


def analyse(pw, model):
    """Prédit la classe avec le modèle ML et renvoie aussi les conseils."""
    features = pd.DataFrame([extract_features(pw)])
    classe = int(model.predict(features)[0])
    conseils = get_suggestions(pw)

    # Un mot de passe faible ou moyen doit toujours recevoir au moins un conseil utile
    if classe < 2 and conseils[0].startswith("Excellent"):
        conseils = ["Allongez-le encore ou utilisez une phrase de passe plus longue."]

    return {"classe": classe, "nom": NOMS_CLASSES[classe], "conseils": conseils}