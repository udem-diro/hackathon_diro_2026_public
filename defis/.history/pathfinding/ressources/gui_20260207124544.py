from ressources.translate import getDisplayChar, getFieldCost, getName
from ressources.sounds import teleportSound, winSound, loseSound, checkpointSound, waterSound, mudSound
from ressources.utils import (
    Robot,
    GROUND_IMG,
    MUD_IMG,
    PORTAL_IMG,
    WATER_IMG,
    CHECKPOINT_IMG,
    START_IMG,
    END_IMG,
    WALL_IMG,
    DOT_IMG,
    LEVEL_START_STAMINA,
    maxCostPerLevel,
)
from collections import defaultdict
import pygame
import time

# Image dictionary mapping characters to their images
IMG = {
    '.': GROUND_IMG,
    '~': WATER_IMG,
    'X': MUD_IMG,
    'P': PORTAL_IMG,
    'C': CHECKPOINT_IMG,
    'S': START_IMG,
    'E': END_IMG,
    '#': WALL_IMG,  # walls are gray
}


TEST_MAZE = """######################
#S.......~####X......#
#.####.#.~#....X###.##
#....#.#..#.##.......#
##.#...#P.....####.#.#
#..##.##.###..#...#.#
#.~~~~...#....#.####.#
#.#X##.#.##P####.....#
#.#....#.........###E#
#.##.###.#.#.####.....#
#X...#.~...#....####.#
######################"""


def test(maze=TEST_MAZE, moves: str = "", level: int = 1, delay: int = 500, display: bool = True):
    """Run moves through a maze. Headless when display=False, pygame when True. Returns True if success."""
    raw_rows = maze.strip().split('\n')
    width = max(len(r) for r in raw_rows)
    maze = [row.ljust(width, '#') for row in raw_rows]  # pad ragged rows with walls for safety
    
    # Find start position
    startRow, startCol = None, None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                startRow, startCol = i, j
                break
        if startRow is not None:
            break
    
    # Initialize robot
    initialStamina = LEVEL_START_STAMINA.get(level, float("inf"))
    robot = Robot(stamina=initialStamina, x=startCol, y=startRow)

    # Track mandatory checkpoints for level 5
    checkpoints = {(i, j) for i, row in enumerate(maze) for j, cell in enumerate(row) if cell == 'C'}
    visitedCheckpoints = set()
    totalCost = 0

    # Headless fast path
    if not display:
        costLimit = maxCostPerLevel.get(level)
        for mv in moves:
            if not robot.move(mv):
                return False
            if robot.y < 0 or robot.y >= len(maze) or robot.x < 0 or robot.x >= width:
                return False
            cell = maze[robot.y][robot.x]
            if getName(cell) == 'wall':
                return False
            if getName(cell) == 'portal' and level >= 4:
                robot.x, robot.y = robot.y, robot.x
                if robot.y < 0 or robot.y >= len(maze) or robot.x < 0 or robot.x >= width:
                    return False
                cell = maze[robot.y][robot.x]
                if getName(cell) == 'wall':
                    return False
            stepCost = getFieldCost(cell, level)
            totalCost += stepCost
            if robot.stamina != float("inf"):
                robot.stamina -= stepCost
            if level == 5 and getName(cell) == 'checkpoint':
                visitedCheckpoints.add((robot.y, robot.x))
            if robot.stamina != float("inf") and robot.stamina < 0 and cell != 'E':
                return False
        at_end = maze[robot.y][robot.x] == 'E'
        checkpoints_ok = (level < 5) or (len(visitedCheckpoints) == len(checkpoints))
        cost_ok = True
        if level == 5 and costLimit is not None and totalCost > costLimit:
            cost_ok = False
        return at_end and checkpoints_ok and cost_ok

    pygame.init()
    WIDTH, HEIGHT = width*16, len(maze)*16
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    icon = pygame.image.load("ressources/assets/maze.png")
    pygame.display.set_icon(icon)
    
    visited = defaultdict(bool)
    visited[(startRow, startCol)] = True
    
    moveIdx = 0
    currentDirection = 'U'
    running = True
    won = False
    costFailed = False
    soundPlayed = False
    # Cooldowns for terrain sounds
    lastWaterSound = 0.0
    lastMudSound = 0.0
    
    # History to track states for undo functionality
    stateHistory = [{
        'x': robot.x,
        'y': robot.y,
        'stamina': robot.stamina,
        'alive': robot.isAlive(),
        'totalCost': totalCost,
        'visited': dict(visited),
        'direction': currentDirection,
        'visitedCheckpoints': set(visitedCheckpoints)
    }]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moves += "U"
                elif event.key == pygame.K_DOWN:
                    moves += "D"
                elif event.key == pygame.K_LEFT:
                    moves += "L"
                elif event.key == pygame.K_RIGHT:
                    moves += "R"
                elif event.key == pygame.K_b:
                    # Undo last move
                    if moveIdx > 0 and len(stateHistory) > 1:
                        # Remove last move from moves string
                        moves = moves[:moveIdx-1] + moves[moveIdx:]
                        moveIdx -= 1
                        # Restore previous state
                        prevState = stateHistory[moveIdx]
                        robot.x = prevState['x']
                        robot.y = prevState['y']
                        robot.stamina = prevState['stamina']
                        robot._alive = prevState['alive']
                        totalCost = prevState['totalCost']
                        visited.clear()
                        visited.update(prevState['visited'])
                        currentDirection = prevState['direction']
                        visitedCheckpoints = set(prevState.get('visitedCheckpoints', set()))
                        # Remove states after current position
                        stateHistory = stateHistory[:moveIdx+1]
                        won = False
                        soundPlayed = False
        
        # Clear screen
        screen.fill("black")
        
        # Draw maze
        for i, row in enumerate(maze):
            for j, cell in enumerate(row.strip()):
                x = j * 32
                y = i * 32
                displayCell = getDisplayChar(cell, level)
                screen.blit(IMG[displayCell], (x, y))
                
                # Draw green dot if visited
                if visited[(i, j)]:
                    screen.blit(DOT_IMG, (x + 8, y + 8))
        
        # Draw robot (red if dead, green if won, dark gray at start)
        robotX = robot.x * 32
        robotY = robot.y * 32
        if not robot.isAlive():
            robotColor = (255, 0, 0)  # Red when dead
        elif won:
            robotColor = (0, 255, 0)  # Green when won
        else:
            robotColor = (50, 50, 50)  # Dark gray normally
        robotImg = Robot.image(colorRGB=robotColor, direction=currentDirection)
        screen.blit(robotImg, (robotX, robotY))
        
        # Update caption
        # Display stamina (infinite shows as ∞)
        staminaStr = "∞" if robot.stamina == float("inf") else f"{int(robot.stamina)}"
        status = "FAILED!" if (not robot.isAlive() or costFailed) else ("WON!" if won else "Running")
        checkpointStr = ""
        if level == 5:
            checkpointStr = f" | Checkpoints: {len(visitedCheckpoints)}/{len(checkpoints)}"
        pygame.display.set_caption(f"Level {level}{checkpointStr} | Stamina: {staminaStr} | Robot at: {robot.x, robot.y} | {status}")
        
        pygame.display.update()
        
        # Play sounds after visual updates (cell and color changes) - only once
        if not soundPlayed:
            if (not robot.isAlive() or costFailed) and moveIdx > 0:
                loseSound()
                soundPlayed = True
            elif won:
                winSound()
                soundPlayed = True
        
        # Execute next move
        if moveIdx < len(moves) and robot.isAlive() and not won:
            pygame.time.delay(delay)
            
            direction = moves[moveIdx]
            currentDirection = direction
            
            # Try to move robot
            if not robot.move(direction):
                robot.crashes()
                moveIdx += 1
                continue
            
            # Check bounds
            if robot.y < 0 or robot.y >= len(maze) or robot.x < 0 or robot.x >= width:
                robot.crashes()
                moveIdx += 1
                continue
            
            cell = maze[robot.y][robot.x]
            
            # Check wall collision
            if getName(cell) == 'wall':
                robot.crashes()
                moveIdx += 1
                continue
            
            # Handle portal teleportation
            if getName(cell) == 'portal' and level >= 4:
                teleportSound()
                robot.x, robot.y = robot.y, robot.x  # Swap coordinates
                if robot.y < 0 or robot.y >= len(maze) or robot.x < 0 or robot.x >= width:
                    robot.crashes()
                    moveIdx += 1
                    continue
                cell = maze[robot.y][robot.x]
                if getName(cell) == 'wall':
                    robot.crashes()
                    moveIdx += 1
                    continue
            
            # Terrain sounds with cooldowns (display-only feedback)
            n = getName(cell)
            if n == 'water':
                now = time.time()
                if (now - lastWaterSound) > 0.25:
                    waterSound()
                    lastWaterSound = now
            elif n == 'mud':
                now = time.time()
                if (now - lastMudSound) > 0.5:
                    mudSound()
                    lastMudSound = now

            # Update cost
            stepCost = getFieldCost(cell, level)
            totalCost += stepCost
            if robot.stamina != float("inf"):
                robot.stamina -= stepCost
            
            # Level 5: track checkpoints instead of stamina
            if level == 5 and getName(cell) == 'checkpoint':
                visitedCheckpoints.add((robot.y, robot.x))
                checkpointSound()
            
            # Mark as visited
            visited[(robot.y, robot.x)] = True
            
            # Check stamina depletion (lose if out before end)
            if robot.stamina != float("inf") and robot.stamina < 0 and cell != 'E':
                robot.crashes()
                moveIdx += 1
                continue

            # Check if reached end
            if cell == 'E' and (level < 5 or len(visitedCheckpoints) == len(checkpoints)):
                limit = maxCostPerLevel.get(level)
                if level == 5 and limit is not None and totalCost > limit:
                    costFailed = True
                    robot.crashes()
                else:
                    won = True
            
            moveIdx += 1
            
            # Save current state to history
            stateHistory.append({
                'x': robot.x,
                'y': robot.y,
                'stamina': robot.stamina,
                'alive': robot.isAlive(),
                'totalCost': totalCost,
                'visited': dict(visited),
                'direction': currentDirection,
                'visitedCheckpoints': set(visitedCheckpoints)
            })

    pygame.quit()
    return won and not costFailed