Projet de Modélisation des Pertes Assurantielles dues aux Aléas Climatiques
Introduction
Ce projet a pour objectif de modéliser les pertes assurantielles causées par divers aléas climatiques, en particulier les tempêtes. En utilisant des données d'exposition et des modèles de vulnérabilité, nous pouvons estimer les pertes potentielles dans différentes régions et sous différents scénarios climatiques.

Structure du Projet
Le projet est organisé de la manière suivante :

modules/ : Dossier contenant les différents modules Python nécessaires au calcul des pertes.

storm_alea_modele.py : Module pour modéliser les aléas liés aux tempêtes (ex. vitesse du vent).
exposure_modele.py : Module pour gérer les données d'exposition des biens assurés.
vulnerability_model.py : Module pour modéliser la vulnérabilité des biens face aux aléas.
loss_calculation.py : Script principal pour calculer les pertes en fonction des données d'exposition et des conditions météorologiques.

main.py : Script qui simule plusieurs scénarios de pertes en utilisant les modèles et données disponibles.

data/ : Dossier contenant les fichiers CSV pour les données d'exposition et les données météorologiques.

exposure_data.csv : Données sur les biens assurés (valeurs, types, etc.).
tempest_data.csv : Données météorologiques pour le modèle.
Démarche
Chargement des Données :

Nous chargeons les données d'exposition et les données météorologiques à partir de fichiers CSV à l'aide de la bibliothèque pandas.
Définition des Scénarios :

Nous définissons plusieurs scénarios de simulation pour évaluer l'impact des changements climatiques, notamment une augmentation de la vitesse du vent.
Simulation des Scénarios :

Pour chaque scénario, nous utilisons un modèle "mock" pour simuler la vitesse du vent, puis nous appelons la fonction calculate_losses pour estimer les pertes totales.
Les résultats sont stockés dans un dictionnaire et affichés à l'utilisateur.
Fonctionnalités du Code :

Le code est structuré de manière modulaire, facilitant la maintenance et les futures extensions.
La simulation permet d'évaluer l'impact potentiel des aléas climatiques sous différents scénarios.
Instructions d'Utilisation
Pré-requis :

Installer Python et la bibliothèque pandas.
Exécution du Code :

Cloner le dépôt depuis GitHub.
Naviguer dans le dossier du projet.
Exécuter le script principal avec la commande :
bash
Copier le code
python main.py
Résultats :

Les pertes totales estimées pour chaque scénario seront affichées dans le terminal.
Conclusion
Ce projet fournit une base pour modéliser et comprendre l'impact des aléas climatiques sur les pertes assurantielles. Les résultats peuvent être utilisés pour éclairer la prise de décision en matière d'assurance et de gestion des risques.
