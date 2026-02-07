"""
NIVEAU 5 : Points de Contrôle (TSP)
===================================
Objectif : Atteindre l'arrivée E en passant par TOUS les points de contrôle C
Stamina : Illimité (mais coût optimal ≤ 122 919 pour bonus)
Terrains : Sol (.) = 1, Eau (~) = 200, Boue (X) = 30 000
Portails (P) : Téléportation (x,y) → (y,x)
Points de Contrôle (C) : OBLIGATOIRES
Stratégie : Résoudre le Traveling Salesman Problem (TSP)
"""

from pathlib import Path
from ressources.gui import test

# Charger le labyrinthe
inputMaze = Path('ressources/assets/maze.txt').read_text().strip('\n')

# Votre solution : séquence qui passe par tous les checkpoints
mySolution = "VOTRE_SOLUTION_ICI"

# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("NIVEAU 5 : Points de Contrôle (TSP)")
    print("=" * 50)
    print("Objectif de coût optimal : ≤ 122 919\n")
    
    # Test rapide
    result = test(maze=inputMaze, moves=mySolution, level=5, display=False)
    
    if result:
        print("✅ SUCCÈS ! Tous les checkpoints visités")
    else:
        print("❌ Échec : vérifiez que vous visitez TOUS les checkpoints (C)")
    
    # Test avec visualisation (voir checkpoints)
    print("\n🎮 Visualisation (points bleus = checkpoints)...")
    test(maze=inputMaze, moves=mySolution, level=5, delay=200, display=True)
