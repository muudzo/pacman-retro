import pygame
from . import constants

# 0 = Empty (no dot), 1 = Wall, 2 = Dot
TILE_SIZE = 30
COLS = 20
ROWS = 20

# 1 = Wall, 2 = Dot, 0 = Empty (already eaten)
level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1],
    [1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1],
    [1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1],
    [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Maze:
    def __init__(self):
        # Create a copy of the level map so we can modify it
        self.grid = [row[:] for row in level_map]
        self.tile_size = TILE_SIZE
        self.total_dots = sum(row.count(2) for row in self.grid)
        self.dots_collected = 0

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

    def collect_dot(self, x, y):
        """Collect a dot at pixel position (x, y). Returns points earned."""
        grid_x = int(x / self.tile_size)
        grid_y = int(y / self.tile_size)
        
        if 0 <= grid_y < len(self.grid) and 0 <= grid_x < len(self.grid[0]):
            if self.grid[grid_y][grid_x] == 2:
                self.grid[grid_y][grid_x] = 0  # Remove the dot
                self.dots_collected += 1
                return 10  # Points per dot
        return 0

    def draw(self, screen):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    # Draw wall
                    pygame.draw.rect(
                        screen,
                        constants.BLUE,
                        (col_idx * self.tile_size, row_idx * self.tile_size, self.tile_size, self.tile_size)
                    )
                elif tile == 2:
                    # Draw dot
                    center_x = col_idx * self.tile_size + self.tile_size // 2
                    center_y = row_idx * self.tile_size + self.tile_size // 2
                    pygame.draw.circle(screen, constants.WHITE, (center_x, center_y), 3)
