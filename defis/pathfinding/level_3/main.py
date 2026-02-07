"""
NIVEAU 3 : Coûts de Terrain
===========================
Objectif : Atteindre l'arrivée E en gérant les terrains avec des coûts différents
Stamina : 93 513
Terrains :
  - Sol (.) = 1 stamina
  - Eau (~) = 200 stamina
  - Boue (X) = 30 000 stamina
Stratégie : Utiliser Dijkstra pour trouver le chemin de coût minimum
"""

from pathlib import Path
from ressources.gui import test

# Charger le labyrinthe
inputMaze = Path('ressources/assets/maze.txt').read_text().strip('\n')

# Votre solution : séquence optimisée pour coût minimum
mySolution = "VOTRE_SOLUTION_ICI"

# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("NIVEAU 3 : Coûts de Terrain")
    print("=" * 50)
    print("Stamina disponible : 93 513")
    print("Coûts : Sol=1, Eau=200, Boue=30000\n")
    
    # Test rapide
    result = test(maze=inputMaze, moves=mySolution, level=3, display=False)
    
    if result:
        print("✅ SUCCÈS ! Coût acceptable")
    else:
        print("❌ Échec : vérifiez que coût ≤ 93 513")
    
    # Test avec visualisation (voir stamina en temps réel)
    print("\n🎮 Visualisation (observez la stamina)...")
    test(maze=inputMaze, moves=mySolution, level=3, delay=200, display=True)
