import streamlit as st
import pandas as pd

# Titre de l'app
st.title("🌿 Trouve ta plante idéale !")

# Charger le CSV avec nettoyage
df_plantes = pd.read_csv("plants.csv", sep=";", encoding="utf-8-sig")
df_plantes.columns = df_plantes.columns.str.strip()

# Séparer et nettoyer la température
df_plantes[['Temp_min', 'Temp_max']] = df_plantes['Température'].str.replace('°C','').str.split('-', expand=True)
df_plantes['Temp_min'] = pd.to_numeric(df_plantes['Temp_min'], errors='coerce')
df_plantes['Temp_max'] = pd.to_numeric(df_plantes['Temp_max'], errors='coerce')

# 1️⃣ Question Luminosité
luminosite = st.selectbox("Quelle est la luminosité de ta pièce ?", ["Faible", "Moyenne", "Forte"])

# 2️⃣ Question Allergène pour animaux
allergene = st.radio("Veux-tu éviter les plantes allergènes pour tes animaux ?", ["Oui", "Non"])

# 3️⃣ Question Type de plante
type_plante = st.selectbox(
    "Quel type de plante préfères-tu ?", 
    ["Plante grimpante", "Succulente", "Plante d'intérieur", "Fleurie", "Tropicale", "Fougère", "Plante retombante", "Plante aromatique", "Plante aérienne"]
)

# 4️⃣ Température de la pièce
temp_piece = st.slider(
    "En moyenne, à quelle température chauffez-vous votre pièce ?",
    min_value=10, max_value=35, value=20
)

# Bouton Valider
if st.button("Valider"):

    # Fonction de calcul du score
    def calcul_score(row, poids=None):
        if poids is None:
            poids = {"luminosite":1, "allergene":1, "type":1, "temperature":1}
        score = 0
        total = sum(poids.values())

        # Luminosité
        if row["Luminosité"] == luminosite:
            score += poids["luminosite"]

        # Allergène animaux
        if allergene == "Oui" and row["Allergène animaux"] == "Non":
            score += poids["allergene"]
        elif allergene == "Non":
            score += poids["allergene"]

        # Type
        if row["Type"] == type_plante:
            score += poids["type"]

        # Température
        if pd.notna(row['Temp_min']) and pd.notna(row['Temp_max']):
            if row['Temp_min'] <= temp_piece <= row['Temp_max']:
                score += poids["temperature"]

        return (score / total) * 100

    # Calculer le pourcentage de correspondance
    df_plantes["Match (%)"] = df_plantes.apply(calcul_score, axis=1)

    # Trier par match décroissant
    df_resultats = df_plantes.sort_values(by="Match (%)", ascending=False)

    # Vérifier si au moins une plante correspond à plus de 25%
    if df_resultats["Match (%)"].max() < 25:
        st.warning("😕 Aucune plante ne correspond vraiment à tes critères. Essaie d'ajuster tes réponses !")
    else:
        # 🔝 Top 1
        st.subheader("🏆 Top plante recommandée")
        top1 = df_resultats.iloc[0]
        st.markdown(f"**{top1['Nom']}** - Match : {top1['Match (%)']:.0f}%")
        st.markdown(f"{top1['Description']}")
        if pd.notna(top1["Photo"]) and top1["Photo"]:
            st.image(top1["Photo"], width=300)
        st.markdown("---")

        # 👑 Top 2 à 5
        st.subheader("🌿 Autres plantes recommandées")
        for idx, row in df_resultats.iloc[1:5].iterrows():
            st.markdown(f"**{row['Nom']}** - Match : {row['Match (%)']:.0f}%")
            st.markdown(f"{row['Description']}")
            if pd.notna(row["Photo"]) and row["Photo"]:
                st.image(row["Photo"], width=200)
            st.markdown("---")

