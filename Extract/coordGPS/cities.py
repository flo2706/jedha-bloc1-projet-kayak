import json
import os

# Always resolve paths relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_cities_to_json(cities, file_name="cities.json"):
    """
    Save a list of French cities into a JSON file next to this script.
    """
    file_path = os.path.join(BASE_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cities, f, indent=4, ensure_ascii=False)
    print(f"City list saved to {file_path}")

if __name__ == "__main__":
    cities = [
        "Le Mont-Saint-Michel, France", "Saint-Malo, France", "Bayeux, France",
        "Le Havre, France", "Rouen, France", "Paris, France", "Amiens, France",
        "Lille, France", "Strasbourg, France", "Château du Haut-Koenigsbourg, France",
        "Colmar, France", "Eguisheim, France", "Besançon, France", "Dijon, France",
        "Annecy, France", "Grenoble, France", "Lyon, France", "Gorges du Verdon, France",
        "Bormes-les-Mimosas, France", "Cassis, France", "Marseille, France",
        "Aix-en-Provence, France", "Avignon, France", "Uzes, France", "Nimes, France",
        "Aigues-Mortes, France", "Les Saintes-Maries-de-la-Mer, France",
        "Collioure, France", "Carcassonne, France", "Ariège, France", "Toulouse, France",
        "Montauban, France", "Biarritz, France", "Bayonne, France", "La Rochelle, France"
    ]
    save_cities_to_json(cities)
