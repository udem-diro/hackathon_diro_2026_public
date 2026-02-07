"""
NIVEAU 2 : Navigation de Base
==============================
Objectif : Atteindre l'arrivée E avec un stamina limité (77)
Stamina : 77 (chaque mouvement coûte 1)
Stratégie : Trouver le chemin le plus court
"""

from pathlib import Path
from ressources.gui import test

# Charger le labyrinthe
inputMaze = Path('ressources/assets/maze.txt').read_text().strip('\n')

# Votre solution : séquence optimisée (max 77 mouvements)
mySolution = "VOTRE_SOLUTION_ICI"

# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("NIVEAU 2 : Navigation de Base")
    print("=" * 50)
    print("Stamina disponible : 77\n")
    
    # Test rapide
    result = test(maze=inputMaze, moves=mySolution, level=2, display=False)
    
    if result:
        print("✅ SUCCÈS ! Stamina suffisant")
    else:
        print("❌ Échec : vérifiez que vous n'utilisez pas plus de 77 mouvements")
    
    # Test avec visualisation (voir la stamina en temps réel)
    print("\n🎮 Visualisation (HUD affiche stamina)...")
    test(maze=inputMaze, moves=mySolution, level=2, delay=200, display=True)
