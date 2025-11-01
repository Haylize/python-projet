**PlantAdvisor :**

Trouve la plante faite pour toi, en moins de 2 minutes !


**Présentation de l'application :**

PlantAdvisor est une application développée par Élise et Édouard.  
Elle permet à chaque utilisateur, prenant le temps de répondre aux quelques questions qui lui sont posées, de découvrir la plante qui correspond le mieux à ses besoins et contraintes. 


**Nos objectifs :**

L'objectif principal de PlantAdvisor est de permettre aux jardiniers 'en herbe' (donc aux personnes qui n'ont pas de connaissance en botanique) souhaitant acheter leur première plante, de pouvoir découvrir en seulement 2 minutes quelle plante serait la plus à même de grandir et de s'épanouir chez eux. 

Bien évidemment, PlantAdvisor peut également être utilisé par des personnes qui s'y connaissent déjà bien en botanique, et qui souhaiteraient tout simplement découvrir quelles autres plantes pourraient venir garnir leurs maisons ou leurs jardins.


**Les principales fonctionnalités :**

  PlantAdvisor repose sur un questionnaire de 7 questions, combinant différents types d’interactions :

  - Sélection simple (radio buttons)
  - Sélection multiple (multiselect)
  - Curseur numérique (slider)
  - Champ de saisie (input)

  Les questions portent sur :

  - L’emplacement (intérieur / extérieur)
  - La luminosité disponible
  - Le type de plante souhaité
  - La température moyenne de la pièce
  - La fréquence d’arrosage souhaitée
  - La présence éventuelle d’animaux (plantes non allergènes)
  - Le budget maximal

**Méthode de calcul :**

Le score de correspondance est basé sur 6 critères pondérés :

`*Critère -	Poids	- Description*
Emplacement -	2	- Facteur déterminant pour la survie de la plante
Luminosité	- 1	- Niveau de lumière adapté
Type	- 1	- Style de plante souhaité
Température	- 1	- Tolérance thermique
Budget	- 1	- Prix compatible
Arrosage	- 1	- Fréquence d’entretien acceptable`

La plante avec le score global le plus élevé (en %) est proposée à l’utilisateur.

**Technologies utilisées :**

- Python
- Streamlit (interface utilisateur)
- Pandas (traitement des données)
- CSV comme base de données de référence
- CSS pour la personnalisation de l’apparence

**Exemple de résultat :** 

🏆 Aloe Vera (Match : 92%)  
“le médecin de poche. Soigne tes coups de soleil, ton égo et ton appart sec comme le Sahara. Attention, il déteste le trop-plein d’eau.”  
⚠️ Critères non remplis : Arrosage (prévoit moins d’eau que prévu)

**Lancer l’application :**

- Cloner le projet : ***git clone git clone https://github.com/Haylize/python-projet.git***
- Installer les dépendances : ***pip install -r requirements.txt***
- Lancer l’application Streamlit : ***streamlit run app.py***

**En deux mots, PlantAdvisor transforme un vrai casse-tête en une expérience amusante et rapide.**
