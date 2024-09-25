from random import sample, choices, randint
from tkinter import Tk, Canvas, Scale, Button, Label, Entry, StringVar, OptionMenu
import matplotlib.pyplot as plt
import numpy as np
from noise import snoise2

# Types d'arbres et de bâtiments avec leurs propriétés combinées
PROPERTIES = {
    'Chêne': {'color': 'forest green', 'inflammability': 0.4},
    'Pin': {'color': 'dark green', 'inflammability': 0.9},
    'Épicéa': {'color': 'medium sea green', 'inflammability': 0.7},
    'Bouleau': {'color': 'light green', 'inflammability': 0.6},
    'Maison': {'color': 'light gray', 'inflammability': 0.8, 'insurance_value': 50000},
    'Bureau': {'color': 'dark gray', 'inflammability': 0.9, 'insurance_value': 100000},
    'École': {'color': 'light blue', 'inflammability': 0.85, 'insurance_value': 75000},
    'Hôpital': {'color': 'light pink', 'inflammability': 0.95, 'insurance_value': 150000}
}

COLORS = ["ivory", "lime green", "red", "gray75"]

# Paramètres météorologiques
wind_speed = 0.1
humidity = 0.5
temperature = 30
wind_direction = 'N'

def generate_slope_field(n, num_hills=3):
    """ Génère un champ de pente avec des collines """
    field = np.zeros((n, n))
    
    for _ in range(num_hills):
        center_x = np.random.randint(0, n)
        center_y = np.random.randint(0, n)
        max_height = np.random.uniform(0.5, 1.0)
        sigma = np.random.uniform(n / 10, n / 5)
        
        for i in range(n):
            for j in range(n):
                distance = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                field[i, j] += max_height * np.exp(- (distance ** 2) / (2 * sigma ** 2))
    
    field = field - np.min(field)
    field = field / np.max(field)
    
    return field

def generate_biome_map(n, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
    """ Génère une carte des biomes en utilisant le bruit de Perlin """
    biome_map = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            biome_map[i, j] = snoise2(i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
    
    biome_map = (biome_map - np.min(biome_map)) / (np.max(biome_map) - np.min(biome_map))
    
    return biome_map

def random_forest(p, n, biome_map, slope_map):
    """ Génère une forêt avec arbres et bâtiments """
    units = [(line, col) for col in range(n) for line in range(n)]
    nitems = int(n ** 2 * p)
    items = sample(units, nitems)
    
    # Définir les types de végétation en fonction des biomes
    biome_types = {
        'Chêne': (0.6, 1.0),
        'Pin': (0.3, 0.6),
        'Épicéa': (0.0, 0.3),
        'Bouleau': (0.4, 0.7),
    }
    
    # Assignation des hauteurs, tailles, et types d'éléments
    states = [['empty'] * n for _ in range(n)]
    heights = [[randint(0, 100) for _ in range(n)] for _ in range(n)]
    soil_types = [choices(['dry', 'wet', 'rocky'], k=n) for _ in range(n)]
    
    # Ajouter des bâtiments aux endroits aléatoires
    buildings = [(i, j) for i, j in sample(units, int(nitems * 0.1))]
    
    for (i, j) in items:
        biome_value = biome_map[i, j]
        item_type = None
        for tree_type, (min_biome, max_biome) in biome_types.items():
            if min_biome <= biome_value <= max_biome:
                item_type = tree_type
                break
        states[i][j] = {
            'type': item_type, 
            'state': 1, 
            'height': heights[i][j], 
            'size': randint(1, 3),
            'slope': slope_map[i, j],
            'soil': soil_types[i][j]
        }
    
    # Ajouter des bâtiments
    for i, j in buildings:
        item_type = choices(['Maison', 'Bureau', 'École', 'Hôpital'])[0]
        states[i][j] = {
            'type': item_type, 
            'state': 1, 
            'height': randint(0, 100), 
            'size': randint(1, 3),
            'slope': slope_map[i, j],
            'soil': choices(['dry', 'wet', 'rocky'])[0]
        }
    
    return states

def voisins(n, i, j):
    return [(a, b) for (a, b) in
            [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j)]
            if a in range(n) and b in range(n)]

def fill_cell(states, line, col, canvas, unit, draw_legend=False):
    A = (unit * col, unit * line)
    B = (unit * (col + 1), unit * (line + 1))
    cell = states[line][col]
    
    if cell == 'empty':
        color = COLORS[0]
    elif 'type' in cell:
        state = cell['state']
        color = PROPERTIES[cell['type']]['color'] if state == 1 else COLORS[state]
    
    canvas.create_rectangle(A, B, fill=color, outline='')
    
    if draw_legend:
        draw_legend_on_canvas(canvas)

def draw_legend_on_canvas(canvas):
    legend_x_start = canvas.winfo_width()
    legend_y_start = 0
    legend_width = 200
    legend_height = 150
    
    canvas.create_rectangle(legend_x_start, legend_y_start, legend_x_start + legend_width, legend_y_start + legend_height, fill='white', outline='black')
    canvas.create_text(legend_x_start + 10, legend_y_start + 10, anchor='nw', text='Légende', font='Arial 12 bold')

    y_position = legend_y_start + 30
    for item_type, properties in PROPERTIES.items():
        color = properties['color']
        canvas.create_rectangle(legend_x_start + 10, y_position, legend_x_start + 30, y_position + 20, fill=color, outline='black')
        canvas.create_text(legend_x_start + 40, y_position + 10, anchor='w', text=item_type, font='Arial 10')
        y_position += 25

def fill(states, canvas):
    n = len(states)
    unit = min(canvas.winfo_width(), canvas.winfo_height()) // n
    for line in range(n):
        for col in range(n):
            fill_cell(states, line, col, canvas, unit)
    draw_legend_on_canvas(canvas)

def update_states(states):
    global destroyed_buildings, total_destruction_value
    
    n = len(states)
    to_fire = []
    destroyed_buildings = []
    
    for line in range(n):
        for col in range(n):
            cell = states[line][col]
            if cell != 'empty' and 'state' in cell and cell['state'] == 2:
                cell['state'] = 3
                for (i, j) in voisins(n, line, col):
                    neighbor = states[i][j]
                    if neighbor != 'empty' and 'state' in neighbor and neighbor['state'] == 1:
                        # Propagation du feu influencée par la pente
                        elevation_diff = abs(cell['slope'] - neighbor['slope'])
                        propagation_chance = max(0, (1 - elevation_diff / 100) * PROPERTIES[cell['type']]['inflammability'])
                        if np.random.rand() < propagation_chance:
                            to_fire.append((i, j))
                    if neighbor != 'empty' and 'state' in neighbor and neighbor['state'] == 3:
                        destroyed_buildings.append(neighbor)
                        total_destruction_value += PROPERTIES[neighbor['type']].get('insurance_value', 0)
    
    for (i, j) in to_fire:
        if states[i][j] != 'empty' and 'state' in states[i][j]:
            states[i][j]['state'] = 2

def init():
    global states, running, cpt, p, n, slope_map, biome_map, destroyed_buildings, total_buildings, total_destruction_value
    
    running = False
    cpt = 0
    p = scale_density.get() / 100
    n = scale_n.get()
    states = [['empty'] * n for _ in range(n)]
    
    # Générer la carte des biomes et la carte de pente
    biome_map = generate_biome_map(n)
    slope_map = generate_slope_field(n)
    
    # Générer la forêt initiale avec des bâtiments
    states = random_forest(p, n, biome_map, slope_map)
    total_buildings = sum(1 for row in states for cell in row if 'type' in cell and cell['type'] in PROPERTIES and 'insurance_value' in PROPERTIES[cell['type']])
    
    destroyed_buildings = []
    total_destruction_value = 0
    canvas.delete("all")
    fill(states, canvas)

def step():
    global cpt
    if running:
        cpt += 1
        update_states(states)
        fill(states, canvas)
        if not any(cell['state'] == 2 for row in states for cell in row if cell != 'empty'):
            stop()

def animation():
    global running
    running = True
    anim()

def anim():
    if running:
        step()
        canvas.after(500, anim)

def stop():
    global running
    running = False

def start_fire():
    line, col = randint(0, scale_n.get() - 1), randint(0, scale_n.get() - 1)
    while states[line][col] == 'empty':
        line, col = randint(0, scale_n.get() - 1), randint(0, scale_n.get() - 1)
    states[line][col]['state'] = 2
    fill(states, canvas)

def show_final_report():
    global destroyed_buildings, total_buildings, total_destruction_value
    report_window = Tk()
    report_window.title("Rapport final")
    
    Label(report_window, text="Rapport de l'incendie", font=("Arial", 16)).pack(pady=10)
    
    total_damaged = len(destroyed_buildings)
    percent_destroyed = (total_damaged / total_buildings) * 100
    
    Label(report_window, text=f"Nombre total de bâtiments : {total_buildings}").pack(pady=5)
    Label(report_window, text=f"Nombre de bâtiments détruits : {total_damaged}").pack(pady=5)
    Label(report_window, text=f"Pourcentage de bâtiments détruits : {percent_destroyed:.2f}%").pack(pady=5)
    Label(report_window, text=f"Valeur totale des destructions : {total_destruction_value}€").pack(pady=5)
    
    Button(report_window, text="Fermer", command=report_window.destroy).pack(pady=20)

def quit():
    global running
    running = False
    root.destroy()

root = Tk()
root.title("Simulation d'incendie en forêt")

canvas = Canvas(root, width=600, height=600, bg="ivory")
canvas.grid(row=0, rowspan=8, column=1)

Label(root, text="Taille de la forêt (n x n):").grid(row=0, column=0, sticky="w")
scale_n = Scale(root, from_=10, to=100, orient="horizontal")
scale_n.set(50)
scale_n.grid(row=1, column=0)

Label(root, text="Densité de végétation (%):").grid(row=2, column=0, sticky="w")
scale_density = Scale(root, from_=10, to=100, orient="horizontal")
scale_density.set(70)
scale_density.grid(row=3, column=0)

Button(root, text="Initialiser la forêt", command=init).grid(row=4, column=0)

Button(root, text="Allumer le feu", command=start_fire).grid(row=5, column=0)

Button(root, text="Lancer la simulation", command=animation).grid(row=6, column=0)
Button(root, text="Arrêter la simulation", command=stop).grid(row=7, column=0)

Button(root, text="Quitter", command=quit).grid(row=8, column=0)
Button(root, text="Voir rapport", command=show_final_report).grid(row=9, column=0)

root.mainloop()
