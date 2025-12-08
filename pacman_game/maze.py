import pygame
from . import constants

# 0 = Empty, 1 = Wall, 2 = Dot (later)
# Simple 20x20 grid (assuming 30x30 tiles for 600x600 screen, or similar math)
# Let's use 20 columns * 30px = 600 width
# 20 rows * 30px = 600 height (plus some buffer for score? let's stick to 600x600 for map now)

TILE_SIZE = 30
COLS = 20
ROWS = 20

# 1 = Wall, 0 = Empty path
level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Maze:
    def __init__(self):
        self.grid = level_map
        self.tile_size = TILE_SIZE

    def is_wall(self, grid_x, grid_y):
        """Check if a grid position is a wall."""
        if grid_y < 0 or grid_y >= len(self.grid):
            return True
        if grid_x < 0 or grid_x >= len(self.grid[0]):
            return True
        return self.grid[grid_y][grid_x] == 1

    def can_move_to(self, x, y, radius):
        """Check if a circular entity can move to pixel position (x, y)."""
        # Check the four corners of the bounding box
        left = x - radius
        right = x + radius
        top = y - radius
        bottom = y + radius
        
        # Convert to grid coordinates
        grid_left = int(left / self.tile_size)
        grid_right = int(right / self.tile_size)
        grid_top = int(top / self.tile_size)
        grid_bottom = int(bottom / self.tile_size)
        
        # Check all four corners
        if self.is_wall(grid_left, grid_top):
            return False
        if self.is_wall(grid_right, grid_top):
            return False
        if self.is_wall(grid_left, grid_bottom):
            return False
        if self.is_wall(grid_right, grid_bottom):
            return False
        
        return True

    def draw(self, screen):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(
                        screen,
                        constants.BLUE,
                        (col_idx * self.tile_size, row_idx * self.tile_size, self.tile_size, self.tile_size)
                    )

