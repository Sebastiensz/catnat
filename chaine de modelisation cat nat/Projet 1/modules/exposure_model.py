def exposure_model(exposure_data, location, hazard_type=None):
    """
    Modèle d'exposition qui calcule la valeur totale des biens assurés dans une zone spécifique,
    avec des ajustements pour les types de biens et leur vulnérabilité.
    
    Args:
    - exposure_data (pd.DataFrame): Données d'exposition contenant des informations sur les biens assurés.
    - location (str): Lieu pour lequel on veut calculer la valeur des biens.
    - hazard_type (str, optionnel): Type d'aléa pour ajuster la vulnérabilité (par exemple, 'vent', 'inondation').
    
    Returns:
    - total_value (float): Valeur totale des biens assurés ajustée selon la vulnérabilité.
    """
    
    # Filtrer les données d'exposition pour le lieu spécifique
    exposure_at_location = exposure_data[exposure_data['location'] == location]
    
    if exposure_at_location.empty:
        raise ValueError(f"Aucune donnée d'exposition disponible pour le lieu {location}.")
    
    # Paramètres de vulnérabilité par type de bien et par type d'aléa (exemples)
    vulnerability_factors = {
        'Residential': {'vent': 0.8, 'inondation': 0.7},
        'Commercial': {'vent': 0.9, 'inondation': 0.6},
        'Industrial': {'vent': 0.7, 'inondation': 0.8}
    }
    
    # Calcule la valeur ajustée en fonction de la vulnérabilité
    total_value = 0
    for index, row in exposure_at_location.iterrows():
        asset_type = row['property_type']  # Exemple : résidentiel, commercial, industriel
        asset_value = row['value']      # Valeur du bien
        
        # Si un type d'aléa est spécifié, ajuster la valeur par la vulnérabilité
        if hazard_type and asset_type in vulnerability_factors:
            vulnerability = vulnerability_factors[asset_type].get(hazard_type, 1.0)
        else:
            vulnerability = 1.0  # Si aucune vulnérabilité n'est spécifiée
        
        # Ajustement de la valeur du bien en fonction de la vulnérabilité
        adjusted_value = asset_value * vulnerability
        total_value += adjusted_value
    
    return total_value


