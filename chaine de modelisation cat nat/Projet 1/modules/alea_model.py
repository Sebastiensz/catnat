import pandas as pd
import numpy as np
from scipy.stats import weibull_min

# Chargement des données météorologiques


# Vérification de l'existence des colonnes nécessaires
#required_columns = ['location', 'wind_speed', 'pressure', 'precipitation', 'date']
#for col in required_columns:
  #  if col not in weather_data.columns:
   #     raise ValueError(f"Colonne manquante dans les données météo : {col}")

# Fonction du modèle d'aléa
def storm_hazard_model(weather_data, location, time_period=None):
    """
    Modèle d'aléa qui simule les vitesses de vent à un endroit donné, 
    basé sur une distribution de Weibull, en tenant compte de l'évolution temporelle.
    
    Args:
    - weather_data (pd.DataFrame): Données météo historiques.
    - location (str): Lieu pour lequel on veut simuler l'aléa.
    - time_period (tuple): Période temporelle optionnelle sous forme (start_year, end_year).
    
    Returns:
    - wind_speed (float): Vitesse du vent simulée à partir de la distribution de Weibull.
    """
    
    # Filtrer les données météo pour le lieu spécifique
    local_data = weather_data[weather_data['location'] == location]
    
    # Filtrer par période temporelle
    if time_period is not None:
        local_data['date'] = pd.to_datetime(local_data['date'])
        start_date = f"{time_period[0]}-01-01"
        end_date = f"{time_period[1]}-12-31"
        local_data = local_data[(local_data['date'] >= start_date) & (local_data['date'] <= end_date)]
    
    if local_data.empty:
        raise ValueError(f"Aucune donnée disponible pour le lieu {location} et la période donnée.")
    
    # Détermination des paramètres de Weibull à partir des données
    # Ajustez k (paramètre de forme) et lambda (paramètre d'échelle) en fonction des données historiques
    k = 2  # Ex: paramètre de forme (souvent entre 1.5 et 3 pour des vitesses de vent)
    lambda_ = local_data['wind_speed'].mean()  # Utilisation de la moyenne pour le paramètre d'échelle

    # Générer la vitesse du vent à partir de la distribution de Weibull
    wind_speed = weibull_min.rvs(k, scale=lambda_)
    
    return wind_speed

