**PlantAdvisor :**

Trouve la plante faite pour toi, en moins de 2 minutes !

**Présentation de l'application :**

PlantAdvisor est une application développée par Élise et Édouard. Cette application a pour but de proposer à chaque utilisateur, qui prend le temps de répondre aux quelques questions qui lui sont posées, la plante qui corresponderait le plus à ses besoins et à ses contraintes. 

**Nos objectifs :**

L'objectif principal de PlantAdvisor est de permettre aux jardiniers 'en herbe' (donc aux personnes qui n'ont pas de connaissance en botanique) souhaitant acheter leurs première plante, de pouvoir découvrir en seulement 2 minutes quelle plante serait la plus à même de grandir et de s'épanouir chez eux. 

Bien évidemment, PlantAdvisor peut également être utilisé par des personnes qui s'y connaissent déjà bien en botanique, et qui souhaiteraient tout simplement decouvrir quelles autres plantes pourraient venir garnir leurs maisons ou jardins.



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

Critère -	Poids	- Description
Emplacement -	2	- Facteur déterminant pour la survie de la plante
Luminosité	- 1	- Niveau de lumière adapté
Type	- 1	- Style de plante souhaité
Température	- 1	- Tolérance thermique
Budget	- 1	- Prix compatible
Arrosage	- 1	- Fréquence d’entretien acceptable

La plante avec le score global le plus élevé (en %) est proposée à l’utilisateur.

**Technologies utilisées :**

- Python
- Streamlit (interface utilisateur)
- Pandas (traitement des données)
- CSV comme base de données de référence

**Exemple de résultat :** 

🏆 Monstera Deliciosa — Match : 92%
“Grande, élégante et facile à vivre, elle saura transformer ton salon en jungle urbaine.”
⚠️ Critères non remplis : Arrosage (prévoit un peu plus d’eau que prévu)

**Lancer l’application :**

1 - Cloner le projet : ***git clone https://github.com/votre-utilisateur/plantadvisor.git***
2 - Installer les dépendances : ***pip install -r requirements.txt***
3 - Lancer l’application Streamlit : ***streamlit run app.py***

PlantAdvisor est une application qui prend la forme d'un petit questionnaire interractif en 7 questions. Certaines sont des questions à choix multiples, d'autres à choix unique (radio button),
ou encore sous forme de curseur numérique (slider).

Pour déterminer quelle plante correspond le mieux à l'utilisateur, le calcul de score est basé sur 6 critères : emplacement, luminosite, type, temperature, budget, arrosage (il est important de noter que le critère “emplacement” a plus de poids que les autres, car il est souvent déterminant dans la survie de la plante).

La plante qui a le score le plus élevé sera donc proposée avec son score (en %), sa photo, ainsi qu'une courte description humoristique (mais toujours liée aux caractéristiques réelles de la plante).


En deux mots, PlantAdvisor transforme un vrai casse-tête en une expérience amusante et rapide.
