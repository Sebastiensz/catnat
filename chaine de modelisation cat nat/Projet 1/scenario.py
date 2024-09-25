import pandas as pd
from modules.alea_model import hazard_model
from modules.exposure_model import exposure_model
from modules.vulnerability_model import storm_vulnerability_model
from loss_calculation import calculate_losses

# Chargement des données météorologiques
weather_data = pd.read_csv('C:\\Users\\User\\Documents\\dev\\python\\Projets\\VScode\\cat nat modele\\data\\tempest_data.csv')

# Lire les données d'exposition depuis le fichier CSV
exposure_data = pd.read_csv('C:\\Users\\User\\Documents\\dev\\python\\Projets\\VScode\\cat nat modele\\data\\exposure_data.csv')

# Définir des scénarios de simulation
scenarios = {
    "scénario_baseline": {"wind_speed": 30},  # Vitesse du vent de base en km/h
    "scénario_augmentation": {"wind_speed": 45},  # Vitesse du vent augmentée à 45 km/h
    "scénario_extreme": {"wind_speed": 60},  # Vitesse du vent extrême à 60 km/h
}

# Fonction pour simuler des scénarios
def simulate_scenarios(weather_data, location):
    results = {}
    
    for scenario, params in scenarios.items():
        # Mock de la fonction hazard_model pour retourner la vitesse du vent simulée
        def mock_hazard_model(weather_data, location):
            return params["wind_speed"], None  # Retourne uniquement la vitesse du vent
        
        # Remplacer temporairement la fonction hazard_model par notre mock
        original_hazard_model = hazard_model
        globals()['hazard_model'] = mock_hazard_model
        
        # Calcul des pertes pour ce scénario
        total_loss = calculate_losses(exposure_data, weather_data, location, hazard_type='vent')
        results[scenario] = total_loss
        
        # Restauration de la fonction d'origine
        globals()['hazard_model'] = original_hazard_model
    
    return results

# Exemple d'utilisation
if __name__ == "__main__":
    location = 'Paris'  # Exemple de localisation

    # Simuler les scénarios et afficher les résultats
    results = simulate_scenarios(weather_data, location)
    
    for scenario, loss in results.items():
        print(f"{scenario} : Pertes totales estimées : {loss:.2f} €")
