import streamlit as st
import pandas as pd

# Titre de l'app
st.title("🌿 Trouve ta plante idéale !")

# Charger le CSV et nettoyer les colonnes
df_plantes = pd.read_csv("plants.csv", sep=";", encoding="utf-8-sig")
df_plantes.columns = df_plantes.columns.str.strip() #on enleve les espaces

# Séparer et nettoyer la température
df_plantes['Température'] = df_plantes['Température'].astype(str)  # sécurité si certains sont NaN
df_plantes[['Temp_min', 'Temp_max']] = (
    df_plantes['Température']
    .str.replace('°C', '', regex=False)# enlève les °C
    .str.replace(' ', '', regex=False)  # enlève les espaces
    .str.split('-', expand=True) # enlève les -
)
df_plantes['Temp_min'] = pd.to_numeric(df_plantes['Temp_min'], errors='coerce') #conversion en nombre, si erreur NaN
df_plantes['Temp_max'] = pd.to_numeric(df_plantes['Temp_max'], errors='coerce')

# Question 1 : Luminosité
luminosite = st.selectbox("Quelle est la luminosité de ta pièce ?", ["Faible", "Moyen", "Fort"])

# Question 2 : Allergène
allergene = st.radio("Veux-tu éviter les plantes allergènes pour tes animaux ?", ["Oui", "Non"])

# Question 3 : Type de plante
type_plante = st.selectbox(
    "Quel type de plante préfères-tu ?",
    [
        "Plante grimpante", "Succulente", "Plante d'intérieur", "Fleurie",
        "Tropicale", "Fougère", "Plante retombante", "Plante aromatique", "Plante aérienne"
    ]
)

# Question 4 : Température moyenne
temp_piece = st.slider(
    "En moyenne, à quelle température chauffez-vous votre pièce ?",
    min_value=10, max_value=35, value=20
)

# Filtrer les plantes allergènes si l’utilisateur dit “Oui”
if allergene == "Oui":
    df_plantes = df_plantes[df_plantes["Allergène animaux"] == "Non"]

# Quand l’utilisateur clique sur “Valider”
if st.button("Valider"):

    def calcul_score(row, poids=None):
        if poids is None:
            poids = {"luminosite": 1, "allergene": 1, "type": 1, "temperature": 1}
        score = 0
        total = sum(poids.values())

        # Luminosité
        if row.get("Luminosité") == luminosite:
            score += poids["luminosite"]

        # Allergène animaux (tout le monde est non allergène ici si allergene == Oui)
        score += poids["allergene"]

        # Type
        if row.get("Type") == type_plante:
            score += poids["type"]

        # Température : vérifier si la température de la pièce est dans la plage
        if pd.notna(row['Temp_min']) and pd.notna(row['Temp_max']): #verifie que la plante a bien des valeurs temp
            if row['Temp_min'] <= temp_piece <= row['Temp_max']: #condition pour encadrer
                score += poids["temperature"]

        return (score / total) * 100

    # Calcul du score pour chaque plante
    df_plantes["Match (%)"] = df_plantes.apply(calcul_score, axis=1)

    # Trier les résultats
    df_resultats = df_plantes.sort_values(by="Match (%)", ascending=False)

    # Afficher les recommandations
    if df_resultats.empty or df_resultats["Match (%)"].max() < 25: 
        st.warning("😕 Aucune plante ne correspond vraiment à tes critères. Essaie d'ajuster tes réponses !")
    else:
        st.subheader("🏆 Top plante recommandée")
        top1 = df_resultats.iloc[0]
        st.markdown(f"**{top1['Nom']}** - Match : {top1['Match (%)']:.0f}%")
        st.markdown(f"{top1['Description']}")
        if pd.notna(top1.get("Photo")) and top1["Photo"]:
            st.image(top1["Photo"], width=300)
        st.markdown("---")

        st.subheader("🌿 Autres plantes recommandées")
        for _, row in df_resultats.iloc[1:5].iterrows():
            st.markdown(f"**{row['Nom']}** - Match : {row['Match (%)']:.0f}%")
            st.markdown(f"{row['Description']}")
            if pd.notna(row.get("Photo")) and row["Photo"]:
                st.image(row["Photo"], width=200)
            st.markdown("---")
