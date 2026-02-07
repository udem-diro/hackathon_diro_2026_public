

# Move directions
MOVES = {
    'U': (0, -1),  # up (row - 1)
    'D': (0, 1),   # down (row + 1)
    'L': (-1, 0),  # left (col - 1)
    'R': (1, 0)    # right (col + 1)
    
}

# Given stamina for each level
LEVEL_START_STAMINA = {
    1: float("inf"),  # Level 1: just find any path
    2: 77,            # Level 2: basic pathfinding with stamina
    3: 93513,         # Level 3: terrain costs (water, mud)
    4: 61490,         # Level 4: portals
    5: float("inf"),  # Level 5: checkpoints (no stamina limit)
}

# Optional per-level cost limits (used by test() to enforce optimality)
maxCostPerLevel = {
    5: 122919,  # Level 5: optimal path through checkpoints
}

import cv2
from functools import cache
import pygame
import numpy as np

def blackToGray(image):
    """Replace black pixels with gray"""
    # Create a mask for black pixels (all channels close to 0)
    black_mask = np.all(image < 30, axis=2)
    # Replace black with gray (128, 128, 128)
    image[black_mask] = [128, 128, 128]
    return image

def npToPygame(image, w=16, h=16, alpha=False):
    """Converts a numpy array image to a pygame surface.
    
    Args:
        image (np.ndarray): Numpy array containing image data.
        w (int): Width of the image in pixels.
        h (int): Height of the image in pixels.
        alpha (bool): If True, creates RGBA surface; otherwise RGB.
    
    Returns:
        pygame.Surface: Pygame surface object ready for blitting.
    """
    if alpha:
        return pygame.image.frombuffer(image.tobytes(), (w, h), "RGBA")
    return pygame.image.frombuffer(image.tobytes(), (w, h), "RGB")
    

class Robot:
    """Represents a robot that navigates through a maze.
    
    The robot tracks its position, stamina, and alive status. It can move in
    four directions and handles crashes when encountering obstacles.
    
    Attributes:
        stamina (float): Remaining stamina (decreases with moves in level 4).
        x (int): Current x-coordinate (column) in the maze.
        y (int): Current y-coordinate (row) in the maze.
        _alive (bool): Whether the robot is still operational.
    """
    def __init__(self, stamina=float("inf"), x=0, y=0):
        self._alive = True
        self.stamina = stamina
        self.x, self.y = x, y
        self.bitmap = {
            d: None for d in MOVES
        }
        
    def crashes(self):
        self._alive = False
        
    def isAlive(self):
        return self._alive
    
    def move(self, direction):
        if direction not in MOVES:
            return False
        dx, dy = MOVES[direction]
        self.x += dx
        self.y += dy
        return True
    
    @staticmethod
    @cache
    def image(colorRGB=(255, 255, 255), direction="U"):
        robotMapWhiteUp = cv2.imread("ressources/assets/robotUp.png")
        robotMap = cv2.cvtColor(robotMapWhiteUp, cv2.COLOR_BGR2RGB)
        
        robotMap = robotMap.astype(float)/255.0
        for i, intensity in enumerate(colorRGB):
            robotMap[:, :, i] *= intensity
        robotMap = robotMap.astype(np.uint8)
        if direction == "U": 
            res = robotMap
        else:
            rotation = {
                "D": cv2.ROTATE_180,
                "L": cv2.ROTATE_90_COUNTERCLOCKWISE,
                "R": cv2.ROTATE_90_CLOCKWISE
            }
            res = cv2.rotate(robotMap, rotation[direction])
        res = cv2.resize(res, (16, 16))
        
        # Add alpha channel and make black pixels transparent
        r, g, b = res[:, :, 0], res[:, :, 1], res[:, :, 2]
        alpha = np.ones((16, 16), dtype=np.uint8) * 255
        # Make black pixels (all channels < 30) transparent
        black_mask = (r < 30) & (g < 30) & (b < 30)
        alpha[black_mask] = 0
        res = np.dstack((r, g, b, alpha))
        
        return npToPygame(res, alpha=True)
    
waterMap = cv2.imread("ressources/assets/water.png")
waterMap = cv2.cvtColor(waterMap, cv2.COLOR_BGR2RGB)
waterMap = cv2.resize(waterMap, (16, 16))
waterMap = blackToGray(waterMap)
WATER_IMG = npToPygame(waterMap)

mudMap = cv2.imread("ressources/assets/mud.png")
mudMap = cv2.cvtColor(mudMap, cv2.COLOR_BGR2RGB)
mudMap = cv2.resize(mudMap, (16, 16))
mudMap = blackToGray(mudMap)
MUD_IMG = npToPygame(mudMap)

portalMap = cv2.imread("ressources/assets/portal.png")
portalMap = cv2.cvtColor(portalMap, cv2.COLOR_BGR2RGB)
portalMap = cv2.resize(portalMap, (16, 16))
portalMap = blackToGray(portalMap)
PORTAL_IMG = npToPygame(portalMap)

groundMap = np.ones((16, 16, 3), np.uint8)*255
GROUND_IMG = npToPygame(groundMap)

refuelMap = cv2.imread("ressources/assets/refuel.png")
refuelMap = cv2.cvtColor(refuelMap, cv2.COLOR_BGR2RGB)
refuelMap = cv2.resize(refuelMap, (16, 16))
refuelMap = blackToGray(refuelMap)
REFUEL_IMG = npToPygame(refuelMap)

checkpointMap = cv2.imread("ressources/assets/checkpoint.png")
checkpointMap = cv2.cvtColor(checkpointMap, cv2.COLOR_BGR2RGB)
checkpointMap = cv2.resize(checkpointMap, (16, 16))
checkpointMap = blackToGray(checkpointMap)
CHECKPOINT_IMG = npToPygame(checkpointMap)

startMap = cv2.imread("ressources/assets/start.png")
startMap = cv2.cvtColor(startMap, cv2.COLOR_BGR2RGB)
startMap = cv2.resize(startMap, (16, 16))
startMap = blackToGray(startMap)
START_IMG = npToPygame(startMap)

endMap = cv2.imread("ressources/assets/end.png")
endMap = cv2.cvtColor(endMap, cv2.COLOR_BGR2RGB)
endMap = cv2.resize(endMap, (16, 16))
endMap = blackToGray(endMap)
END_IMG = npToPygame(endMap)

wallMap = np.ones((16, 16, 3), np.uint8) * 128  # gray color
WALL_IMG = npToPygame(wallMap)

# Create a small green dot for visited cells (16x16)
dotMap = np.ones((8, 8, 3), np.uint8) * 200  # light gray background
cv2.circle(dotMap, (4, 4), 3, (0, 200, 0), -1)  # green dot in the center
DOT_IMG = npToPygame(dotMap, 8, 8)