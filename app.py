import streamlit as st
import pandas as pd

#Me permet d'injecter du CSS pour modifier l'apparence :
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 17px !important;
    }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.pexels.com/photos/1072179/pexels-photo-1072179.jpeg?_gl=1*avezir*_ga*MjAxNDQzMTAyLjE3NjEwODUxODU.*_ga_8JE65Q40S6*czE3NjExNDQ0MDgkbzMkZzEkdDE3NjExNDUzMDgkajIxJGwwJGgw");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        filter: brightness(100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre de l'app
st.title("🌿 PlantAdvisor")
st.write("Tu désires acheter une plante mais tu ne sais pas laquelle correspond le mieux à tes besoins et envies ? Pas de panique, PlantAdvisor est là pour t'éclairer.")

# Charger CSV et nettoyer les colonnes
df_plantes = pd.read_csv("plants.csv", sep=";", encoding="utf-8-sig")
df_plantes.columns = df_plantes.columns.str.strip() # Supprimer les espaces dans les noms de colonnes

# Séparer et nettoyer la température
df_plantes['Température'] = df_plantes['Température'].astype(str) # Assure que toutes les valeurs sont des chaînes
df_plantes[['Temp_min', 'Temp_max']] = (
    df_plantes['Température']
    .str.replace('°C', '', regex=False) # Supprime le symbole °C
    .str.replace(' ', '', regex=False)# Supprime les espaces
    .str.split('-', expand=True)# Sépare min et max en deux colonnes
)
df_plantes['Temp_min'] = pd.to_numeric(df_plantes['Temp_min'], errors='coerce') # Convertit en nombres, NaN si erreur
df_plantes['Temp_max'] = pd.to_numeric(df_plantes['Temp_max'], errors='coerce')

#Question 1 : Emplacement
emplacement = st.radio(
    "**🏡 Où souhaites-tu installer ta plante ?**", 
    ["Une plante d'exterieur", "Une plante d'interieur"]
)

# Transformer en valeur CSV
if emplacement == "Une plante d'exterieur":
    emplacement = "Exterieur"
else:
    emplacement = "Interieur"
    
# Question 2 : Luminosité
luminosite = st.selectbox(
    "☀️ **Quelle sera la luminosité dont ta plante bénéficiera ?**",
    ['Beaucoup de luminosité (soleil direct)', 'Luminosité moyenne (pas de soleil direct)', 'Ombre ou sans sans lumière naturelle']
)
if luminosite == 'Beaucoup de luminosité (soleil direct)':
    luminosite = 'Forte'
elif luminosite == 'Luminosité moyenne (pas de soleil direct)':
    luminosite = 'Moyen'
else:
    luminosite = 'Faible'
    
# Question 3 : Type de plante
type_plante = st.multiselect(
    "🪴 **Quel type de plante préfères-tu ?**",
    ["Plante grimpante", "Succulente", "Fleurie", "Tropicale", "Fougère", "Plante retombante", "Plante aromatique", "Plante aérienne"]
)
# Question 4 : Température moyenne
temp_piece = st.slider(
    "🌡️ **En moyenne, à quelle température chauffez-vous votre pièce ?**", 
    10, 40, 20)

# Question 5 : Arrosage
arrosage = st.slider(
    "**🚿 A quelle fréquence te sens-tu prêt à arroser ta plante par mois ?**", 
    1, 10, 5)

# Question 6 : Allergène
allergene = st.radio(
    "🐕 **Veux-tu éviter les plantes allergènes pour tes animaux ?**", 
    ["Oui", "Non"])

# Question 7 : Budget
budget = st.number_input(
    "💰 **Quel est ton budget max ?**",
    )

# Filtrer les plantes allergènes si l’utilisateur dit “Oui”
if allergene == "Oui":
    df_plantes = df_plantes[df_plantes["Allergène animaux"].str.lower() == "non"]

# Quand l’utilisateur clique sur "Je découvre ma plante"
if st.button("Je découvre ma plante"):
# Vérification : au moins un type doit être sélectionné
    if not type_plante:
        st.warning("⚠️ Veuillez sélectionner au moins un type de plante.")
    else:

        # Fonction calcul score
        def calcul_score(row, poids=None):
            # Poids des critères pour calculer le score (type = 2 pour plus d'importance)
            if poids is None:
                poids = {"emplacement": 1, "luminosite": 1, "allergene": 1, "type": 2, "temperature": 1, "budget": 1, "arrosage": 1}
            
            score = 0
            total = sum(poids.values())

            # Emplacement
            if str(row.get("emplacement")).lower() == emplacement.lower():
                score += poids["emplacement"]

            # Luminosité
            if str(row.get("Luminosité")).lower() == luminosite.lower():
                score += poids["luminosite"]

            # Allergène
            score += poids["allergene"]

            # Type
            if str(row.get("Type")) in type_plante:
                score += poids["type"]

            # Température
            if pd.notna(row['Temp_min']) and pd.notna(row['Temp_max']):
                if row['Temp_min'] <= temp_piece <= row['Temp_max']:
                    score += poids["temperature"]

            # Budget— inclut les plantes moins chères que le budget max
            if pd.notna(row.get("Budget")) and row["Budget"] <= budget:
                score += poids["budget"]

            # Arrosage — inclut les plantes demandant moins d’arrosage que souhaité

            if pd.notna(row.get("Arrosage")) and row["Arrosage"] <= arrosage:
                score += poids["arrosage"]

            return (score / total) * 100

        # Calculer Match
        df_plantes["Match (%)"] = df_plantes.apply(calcul_score, axis=1)

        # Trier résultats
        df_resultats = df_plantes.sort_values(by="Match (%)", ascending=False)
        
        # Afficher les recommandations
        if df_resultats.empty or df_resultats["Match (%)"].max() < 25:
            st.warning("😕 Malheureusement, aucune plante ne semble correspondre à tes critères. Essaie d'ajuster tes réponses !")
        else:
            top1 = df_resultats.iloc[0]

            # Affichage nom + photo
            st.subheader(f"🏆 {top1['Nom']} - Match : {top1['Match (%)']:.0f}%")
            if pd.notna(top1.get("Photo")) and top1["Photo"]:
                st.image(top1["Photo"], width=300)
            st.markdown("---")

            # Critères non remplis
            details_non_remplis = []
            if str(top1.get("emplacement")).lower() != emplacement.lower():
                details_non_remplis.append("Emplacement")
            if str(top1.get("Luminosité")).lower() != luminosite.lower():
                details_non_remplis.append("Luminosité")
            if str(top1.get("Type")) not in type_plante:
                details_non_remplis.append("Type")
            if pd.notna(top1.get("Budget")) and top1["Budget"] > budget:
                details_non_remplis.append("Budget")
            if pd.notna(top1.get("Arrosage")) and top1["Arrosage"] > arrosage:
                details_non_remplis.append("Arrosage")
            if pd.notna(top1['Temp_min']) and pd.notna(top1['Temp_max']):
                if not (top1['Temp_min'] <= temp_piece <= top1['Temp_max']):
                    details_non_remplis.append("Température")

            if details_non_remplis:
                st.markdown("⚠️ Critères non remplis :")
                for critere in details_non_remplis:
                    st.markdown(f"- {critere}")
            else:
                st.markdown("✅ Tous les critères correspondent parfaitement !")
