# Game Configuration
# Single source of truth for all game parameters

# Display Settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Tile/Grid Settings
TILE_SIZE = 30
GRID_COLS = 20
GRID_ROWS = 20

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Entity Parameters
PLAYER_SPEED = 2
PLAYER_RADIUS_OFFSET = 4  # Subtracted from TILE_SIZE // 2

GHOST_SPEED = 1.5
GHOST_RADIUS_OFFSET = 4

# Gameplay Settings
POINTS_PER_PELLET = 10
STARTING_LIVES = 3

# AI Parameters (for future use)
GHOST_DIRECTION_CHANGE_INTERVAL = 60  # frames
SCATTER_DURATION = 7 * FPS  # 7 seconds in frames
CHASE_DURATION = 20 * FPS  # 20 seconds in frames
PATHFINDING_UPDATE_INTERVAL = 10  # frames

# Movement Parameters (for future use)
INPUT_BUFFER_DURATION = 200  # milliseconds
TILE_CENTER_TOLERANCE = 2  # pixels
WALL_SLIDE_ENABLED = True

# Debug Settings
DEBUG_ENABLED_BY_DEFAULT = False
DEBUG_SHOW_GRID = True
DEBUG_SHOW_TARGETS = True
DEBUG_SHOW_COLLISION = True
DEBUG_SHOW_PATHS = True

# Level Complete Settings
LEVEL_COMPLETE_DELAY = 2 * FPS  # 2 seconds in frames
