from modules.alea_model import storm_hazard_model
from modules.exposure_model import exposure_model
from modules.vulnerability_model import storm_vulnerability_model
import pandas as pd
import numpy as np

# Chargement des données météorologiques
weather_data = pd.read_csv('C:\\Users\\User\\Documents\\dev\\python\\Projets\\VScode\\cat nat modele\\data\\tempest_data.csv')

# Chargement des données d'exposition (biens assurés)
exposure_data = pd.read_csv('C:\\Users\\User\\Documents\\dev\\python\\Projets\\VScode\\cat nat modele\\data\\exposure_data.csv')


def calculate_losses(exposure_data, weather_data, location, hazard_type='vent'):
    """
    Calcule les pertes totales pour un lieu donné en fonction des données d'exposition et des conditions météorologiques.
    
    Args:
    - exposure_data (pd.DataFrame): Données sur les biens assurés.
    - weather_data (pd.DataFrame): Données météorologiques historiques.
    - location (str): Lieu pour lequel on veut estimer les pertes.
    - hazard_type (str): Type d'aléa (ex. 'vent', 'inondation').
    
    Returns:
    - total_loss (float): Pertes totales estimées en euros.
    """
    
    # Récupère l'intensité de l'aléa (vitesse du vent dans cet exemple)
    wind_speed = storm_hazard_model(weather_data, location)  # Hypothèse : modèle aléa basé sur le vent
    
    # Récupère la valeur totale des biens assurés dans la zone
    total_value = exposure_model(exposure_data, location, hazard_type=hazard_type)
    
    # Calcule les pertes totales en fonction des vulnérabilités des biens
    total_loss = 0
    exposure_at_location = exposure_data[exposure_data['location'] == location]
    
    # Parcourt chaque bien dans la zone pour calculer les pertes individuelles
    for index, row in exposure_at_location.iterrows():
        asset_value = row['value']
        #print(f"assetvalue {asset_value} ")
        asset_type = row['property_type']  # Exemple : résidentiel, commercial, industriel
        #print(f"asset_type {asset_type} ")
        building_quality = row['building_quality']  # Qualité des constructions (Low, Medium, High)
        #print(f"building_quality {building_quality} ")
        exposure_duration = row['exposure_duration']  # Durée d'exposition aux vents forts (en heures)
        #print(f"exposure_duration {exposure_duration} ")
        #print(f"\n ")
        
        # Utilisation du modèle de vulnérabilité amélioré
        print(f"wind_speed {wind_speed} ")
        damage_ratio = storm_vulnerability_model(wind_speed, asset_type, building_quality, exposure_duration)
        #print(f"damage_ratio {damage_ratio} ")
        
        # Calcul des pertes pour ce bien
        loss = asset_value * damage_ratio
        total_loss += loss
    
    return total_loss

# Exemple de calcul des pertes pour une tempête à Paris
total_loss = calculate_losses(exposure_data, weather_data, 'Paris', hazard_type='vent')
print(f"Pertes totales estimées à Paris : {total_loss} €")
