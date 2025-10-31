import streamlit as st
import pandas as pd

#Appearance personalization
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 18px !important;
    }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.pexels.com/photos/1072179/pexels-photo-1072179.jpeg?_gl=1*avezir*_ga*MjAxNDQzMTAyLjE3NjEwODUxODU.*_ga_8JE65Q40S6*czE3NjExNDQ0MDgkbzMkZzEkdDE3NjExNDUzMDgkajIxJGwwJGgw");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Application title and description
st.title("🌿 PlantAdvisor")
st.write("**Tu désires acheter une plante mais tu ne sais pas laquelle correspond le mieux à tes besoins et envies ? Pas de panique, PlantAdvisor est là pour t'éclairer.**")

# CSV loading and removing spaces
df_plantes = pd.read_csv("plants_clean.csv", sep=";", encoding="utf-8-sig")
df_plantes.columns = df_plantes.columns.str.strip()

# Temperature formatting
df_plantes['Température'] = df_plantes['Température'].astype(str)
df_plantes[['Temp_min', 'Temp_max']] = (
    df_plantes['Température']
    .str.replace('°C', '', regex=False)
    .str.replace(' ', '', regex=False)
    .str.split('-', expand=True)
)
df_plantes['Temp_min'] = pd.to_numeric(df_plantes['Temp_min'])
df_plantes['Temp_max'] = pd.to_numeric(df_plantes['Temp_max'])

#Question 1 : Plant location
emplacement = st.radio(
    "**🏡 Où souhaites-tu installer ta plante ?**", 
    ["A l'exterieur", "En interieur"]
)

# Transform answer into CSV compatible value
if emplacement == "A l'exterieur":
    emplacement = "Exterieur"
else:
    emplacement = "Interieur"
    
# Question 2 : Luminosity
luminosite = st.selectbox(
    "☀️ **Quelle sera la luminosité dont ta plante bénéficiera ?**",
    ['Beaucoup de luminosité (soleil direct)', 'Luminosité moyenne (pas de soleil direct)', 'Ombre ou sans lumière naturelle']
)
if luminosite == 'Beaucoup de luminosité (soleil direct)':
    luminosite = 'Fort'
elif luminosite == 'Luminosité moyenne (pas de soleil direct)':
    luminosite = 'Moyen'
else:
    luminosite = 'Faible'
    
# Question 3 : Plant type
type_plante = st.multiselect(
    "🪴 **Quel type de plante préfères-tu ?**",
    ["Plante grimpante", "Succulente", "Fleurie", "Tropicale", "Fougère", "Plante retombante", "Plante aromatique", "Plante aérienne", "Plante d’intérieur"]
)
# Question 4 : Average temperature
temp_piece = st.slider(
    "🌡️ **En moyenne, à quelle température sera exposée ta future plante ?**", 
    0, 35, 20)

# Question 5 : Watering
arrosage = st.selectbox(
    "**🚿 A quelle fréquence te sens-tu prêt à arroser ta plante ?**", 
    ["Tous les 2 à 3 jours", "Tous les 3 à 6 jours", "Tous les 7 à 12 jours", "Toutes les 2 à 3 semaines", "Toutes les 4 à 6 semaines"]
)

# User also accepts plants needing less watering
dico_arrosage = {
    "Tous les 2 à 3 jours": 1,
    "Tous les 3 à 6 jours": 2,
    "Tous les 7 à 12 jours": 3,
    "Toutes les 2 à 3 semaines": 4,
    "Toutes les 4 à 6 semaines": 5
}

# Question 6 : Allergen
allergene = st.radio(
    "🐕 **Veux-tu éviter les plantes allergènes pour tes animaux ?**", 
    ["Oui", "Non"])

# Sorting plants depending on allergen
if allergene == "Oui":
    df_plantes = df_plantes[df_plantes["Allergène animaux"] == "Non"]

# Question 7 : Budget
budget = st.number_input(
    "💰 **Quel est ton budget max ?** (entre 5€-40€)",
    )

# User submits his answers
if st.button("Je découvre ma plante"):

# Verify that at least 1 type of plant is selected and budget fits plant price
    if not type_plante:
        st.warning("⚠️ Veuillez sélectionner au moins un type de plante.")
    elif budget > 40:
        st.warning("⚠️ Veuillez saisir un montant inférieur ou égal à 40€.")
    elif budget < 5:
        st.warning("⚠️ Veuillez saisir un montant minimum de 5€.")
    else:

        # Score calculation
        def calcul_score(row, poids=None):
            # Criteria weigths
            if poids is None:
                poids = {"emplacement": 2, "luminosite": 1, "type": 1, "temperature": 1, "budget": 1, "arrosage": 1}
            
            score = 0
            total = sum(poids.values())

            # Plant location
            if str(row.get("emplacement")).lower() == emplacement.lower():
                score += poids["emplacement"]

            # Luminosity
            if str(row.get("Luminosité")).lower() == luminosite.lower():
                score += poids["luminosite"]

            # Plant type
            if str(row.get("Type")) in type_plante:
                score += poids["type"]

            # Temperature
            if pd.notna(row['Temp_min']) and pd.notna(row['Temp_max']):
                if row['Temp_min'] <= temp_piece <= row['Temp_max']:
                    score += poids["temperature"]

            # Budget
            if pd.notna(row.get("Budget")) and row["Budget"] <= budget:
                score += poids["budget"]

            # Watering
            user_arrosage_val = dico_arrosage.get(arrosage)
            plante_arrosage_val = dico_arrosage.get(str(row.get("Arrosage")), None)

            if plante_arrosage_val is not None:
                if plante_arrosage_val >= user_arrosage_val:
                    score += poids["arrosage"]

            return (score / total) * 100

        # Match calculation
        df_plantes["Match (%)"] = df_plantes.apply(calcul_score, axis=1)

        # Result sorting
        df_resultats = df_plantes.sort_values(by="Match (%)", ascending=False)
        
        # Result
        if df_resultats.empty or df_resultats["Match (%)"].max() < 25:
            st.warning("😕 Malheureusement, aucune plante ne semble correspondre à tes critères. Essaie d'ajuster tes réponses !")
        else:
            top1 = df_resultats.iloc[0]

            st.subheader(f"🏆 {top1['Nom']} - Match : {top1['Match (%)']:.0f}%")
            if pd.notna(top1.get("Photo")) and top1["Photo"]:
                st.image(top1["Photo"], width=300)
            st.write(f" **Allez, on fait les présentations ? 😉** Voici {top1['Description']}")
            st.markdown("---")

            # Unmet criteria
            details_non_remplis = []
            if str(top1.get("emplacement")).lower() != emplacement.lower():
                details_non_remplis.append(f"Emplacement : {top1.get('emplacement')}")
            if str(top1.get("Luminosité")).lower() != luminosite.lower():
                details_non_remplis.append(f"Luminosité : {top1.get('Luminosité')}")
            if str(top1.get("Type")) not in type_plante:
                details_non_remplis.append(f"Type : {top1.get('Type')}")
            if pd.notna(top1.get("Budget")) and top1["Budget"] > budget:
                details_non_remplis.append(f"Budget : {top1['Budget']} €")
            if pd.notna(top1.get("Arrosage")) and dico_arrosage.get(top1["Arrosage"]) < dico_arrosage.get(arrosage):
                details_non_remplis.append(f"Arrosage : {top1['Arrosage']}")
            if pd.notna(top1['Temp_min']) and pd.notna(top1['Temp_max']):
                if not (top1['Temp_min'] <= temp_piece <= top1['Temp_max']):
                    details_non_remplis.append(f"Température : {top1['Temp_min']}°C - {top1['Temp_max']}°C")

            if details_non_remplis:
                st.markdown("**⚠️ Critères non remplis :**")
                for critere in details_non_remplis:
                    st.markdown(f"- {critere}")
            else:
                st.markdown("**✅ C'est un match parfait !**")
