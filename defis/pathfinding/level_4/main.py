"""
NIVEAU 4 : Portails
===================
Objectif : Atteindre l'arrivée E en utilisant des portails magiques
Stamina : 61 490
Terrains : Sol (.) = 1, Eau (~) = 200, Boue (X) = 30 000
Portails (P) : Téléportation magique (x,y) → (y,x)
Stratégie : Utiliser Dijkstra avec support des portails
"""

from pathlib import Path
from ressources.gui import test

# Charger le labyrinthe
inputMaze = Path('ressources/assets/maze.txt').read_text().strip('\n')

# Votre solution : séquence optimisée avec portails
mySolution = "VOTRE_SOLUTION_ICI"

# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("NIVEAU 4 : Portails")
    print("=" * 50)
    print("Stamina disponible : 61 490")
    print("Portails : (x,y) → (y,x)\n")
    
    # Test rapide
    result = test(maze=inputMaze, moves=mySolution, level=4, display=False)
    
    if result:
        print("✅ SUCCÈS ! Coût acceptable")
    else:
        print("❌ Échec : vérifiez que coût ≤ 61 490")
    
    # Test avec visualisation (voir portails en action)
    print("\n🎮 Visualisation (observez les téléportations)...")
    test(maze=inputMaze, moves=mySolution, level=4, delay=300, display=True)
