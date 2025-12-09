"""Level management - static level data and collision detection"""
import pygame
from . import config

# Level map: 1 = Wall, 2 = Dot, 0 = Empty
LEVEL_MAP = [
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


class Level:
    """Manages static level data and collision detection"""
    
    def __init__(self):
        """Initialize the level with the static map"""
        # Store immutable level grid (walls only)
        self.grid = [[1 if cell == 1 else 0 for cell in row] for row in LEVEL_MAP]
        self.tile_size = config.TILE_SIZE
    
    def is_wall(self, grid_x, grid_y):
        """
        Check if a grid position is a wall.
        
        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate
            
        Returns:
            bool: True if position is a wall or out of bounds
        """
        if grid_y < 0 or grid_y >= len(self.grid):
            return True
        if grid_x < 0 or grid_x >= len(self.grid[0]):
            return True
        return self.grid[grid_y][grid_x] == 1
    
    def can_move_to(self, x, y, radius):
        """
        Check if a circular entity can move to pixel position (x, y).
        
        Args:
            x: Pixel X coordinate (center of entity)
            y: Pixel Y coordinate (center of entity)
            radius: Collision radius of entity
            
        Returns:
            bool: True if position is valid (not colliding with walls)
        """
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
        """Draw the level walls"""
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    # Draw wall
                    pygame.draw.rect(
                        screen,
                        config.BLUE,
                        (col_idx * self.tile_size, row_idx * self.tile_size, 
                         self.tile_size, self.tile_size)
                    )


class PelletManager:
    """Manages pellet state and collection"""
    
    def __init__(self):
        """Initialize pellet grid from level map"""
        # Create a copy of pellets from the level map
        self.pellet_grid = [[1 if cell == 2 else 0 for cell in row] for row in LEVEL_MAP]
        self.tile_size = config.TILE_SIZE
        self.total_pellets = sum(row.count(1) for row in self.pellet_grid)
        self.collected_count = 0
    
    def collect_pellet(self, x, y):
        """
        Collect a pellet at pixel position (x, y).
        
        Args:
            x: Pixel X coordinate
            y: Pixel Y coordinate
            
        Returns:
            int: Points earned (POINTS_PER_PELLET or 0)
        """
        grid_x = int(x / self.tile_size)
        grid_y = int(y / self.tile_size)
        
        if 0 <= grid_y < len(self.pellet_grid) and 0 <= grid_x < len(self.pellet_grid[0]):
            if self.pellet_grid[grid_y][grid_x] == 1:
                self.pellet_grid[grid_y][grid_x] = 0  # Remove the pellet
                self.collected_count += 1
                return config.POINTS_PER_PELLET
        return 0
    
    def pellets_remaining(self):
        """
        Get the number of pellets remaining.
        
        Returns:
            int: Number of uncollected pellets
        """
        return self.total_pellets - self.collected_count
    
    def reset(self):
        """Reset all pellets to initial state"""
        self.pellet_grid = [[1 if cell == 2 else 0 for cell in row] for row in LEVEL_MAP]
        self.collected_count = 0
    
    def draw(self, screen):
        """Draw all uncollected pellets"""
        for row_idx, row in enumerate(self.pellet_grid):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    # Draw pellet
                    center_x = col_idx * self.tile_size + self.tile_size // 2
                    center_y = row_idx * self.tile_size + self.tile_size // 2
                    pygame.draw.circle(screen, config.WHITE, (center_x, center_y), 3)
