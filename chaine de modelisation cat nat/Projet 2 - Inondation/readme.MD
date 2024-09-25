# Modélisation Simplifiée des Dommages en Inondation
![app1](images/app1.png)
![app2](images/app2.png)
![app3](images/app3.png)
## Introduction

Ce document présente le modèle que j’ai développé pour simuler les dommages causés par des inondations. J'ai choisi de réaliser cet exercice en utilisant le langage R, avec le package `data.table` pour la manipulation des données. Ce choix permet des calculs plus performants tout en consommant moins de ressources.

## Grille d'Aléa

La grille d’aléa est constituée de 1740 colonnes de 25 mètres et de 896 lignes de 25 mètres, formant ainsi une grille de 43,5 km par 22,4 km. Nous opérons à une échelle relativement faible, ce qui nous amène à rester en Lambert 93 pour le calcul des coordonnées.

## Calcul de la Hauteur d'Eau

Pour obtenir la hauteur d'eau pour chaque police du portefeuille, nous utilisons les coordonnées de la maille en bas à gauche de notre matrice d'aléa pour calculer les distances X et Y par rapport à chaque police. Ces distances déterminent la position de la police dans la matrice d'aléa :

- La distance X divisée par 25m représente le nombre de colonnes entre la police et la maille.
- La distance Y divisée par 25m représente le nombre de lignes au-dessus de la maille.

La formule finale pour calculer la hauteur d'eau est : alea_matrix[896 - floor(distance_Y / 25), floor(distance_X / 25)].


## Taux de Destruction et Montant des Dommages

Lorsque j’obtiens la hauteur d’eau, je dois lui associer un taux de destruction. J’ai créé une fonction d’interpolation linéaire qui permet, pour chaque hauteur d’eau \( H_1 \), de se baser sur les taux de destruction des hauteurs d’eau voisines connues dans la table `CourbeDommage` pour déduire linéairement le taux de destruction associé à cette hauteur d’eau \( H_1 \). 

Je peux alors calculer le coût comme étant le produit entre le taux de destruction et la valeur assurée. Voici les résultats obtenus pour chaque police :

| ID | X      | Y        | Risque     | Étage | Usage       | Valeur Assurée (€) | Hauteur Eau (m) | Tx Destruction | Montant Dommage (€) |
|----|--------|----------|------------|-------|-------------|--------------------|------------------|----------------|---------------------|
| 1  | 994335 | 6267603  | Maison     | 2     | Propriétaire | 236021             | 0,407461         | 0,043059575    | 10162,96            |
| 2  | 994406 | 6267578  | Villa      | 3     | Propriétaire | 531240             | 1,02563          | 0,105126       | 55847,14            |
| 3  | 994431 | 6267425  | Maison     | 1     | Locataire   | 200069             | 0                | 0              | 0                   |
| 4  | 994516 | 6267416  | Appartement | 4     | Locataire   | 15032              | 0                | 0              | 0                   |
| 5  | 995414 | 6267213  | Entreprise  | 2     | Propriétaire | 1022606            | 1,00937          | 0,101874       | 104176,96           |
| 6  | 994522 | 6266847  | Maison     | 2     | Propriétaire | 260023             | 0                | 0              | 0                   |
| 7  | 997958 | 6268622  | Appartement | 6     | Propriétaire | 54221              | 0                | 0              | 0                   |
| 8  | 997987 | 6268622  | Maison     | 1     | Locataire   | 262654             | 0                | 0              | 0                   |
| 9  | 998004 | 6268782  | Maison     | 2     | Propriétaire | 287964             | 0                | 0              | 0                   |
| 10 | 997863 | 6268698  | Entreprise  | 3     | Propriétaire | 25000056           | 0,367865         | 0,040089875    | 1002249,12          |

Au total, nous avons 4 polices touchées sur 10, dont 2 entreprises pour un montant de plus de 1 106 426,08 € et une villa et une maison pour un montant de 66 010,10 €. Le montant total des dommages est 1 172 436 €, dont plus de 94,3 % proviennent des entreprises.

## Améliorations Possibles

Pour améliorer ce modèle, plusieurs pistes peuvent être envisagées :

- **Répartition des Valeurs Assurées** : Prendre en compte la répartition différente des valeurs assurées par étage, car en général, les appartements situés en hauteur ont plus de valeur que ceux du bas.
- **Date de Construction** : Intégrer la date de construction pourrait apporter des informations pertinentes sur la vulnérabilité des bâtiments.
- **Mesures de Prévention** : Considérer les mesures de prévention prises, telles que le déplacement des principales installations en hauteur pour éviter les dégâts au rez-de-chaussée.
  
## Mesures Communales

Au niveau communal, des mesures de prévention peuvent être mises en place, incitant les résidents à effectuer des actions préventives, telles que le déplacement de meubles en hauteur. Ces efforts sont promus par les Plans de Prévention des Risques Naturels (PPRN), visant à préparer les résidents exposés aux risques afin de réduire les dommages.

## Conclusion

Ce modèle fournit une approche initiale pour estimer les dommages en cas d’inondation, mais plusieurs aspects pourraient être optimisés. En tenant compte des facteurs mentionnés ci-dessus, il serait possible d’affiner les estimations et de mieux préparer les communautés face aux inondations.


