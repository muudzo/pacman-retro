"""Ghost entities with AI"""
import pygame
import random
from .entities.base import Entity
from . import config


class Ghost(Entity):
    """Ghost enemy with random movement AI"""
    
    def __init__(self, x, y, color, ghost_type="BLINKY"):
        """
        Initialize ghost.
        
        Args:
            x: Starting X position (tile coordinate)
            y: Starting Y position (tile coordinate)
            color: RGB color tuple
            ghost_type: Type of ghost (for future AI differentiation)
        """
        # Convert tile position to center pixel position
        center_x = x + config.TILE_SIZE / 2
        center_y = y + config.TILE_SIZE / 2
        radius = config.TILE_SIZE // 2 - config.GHOST_RADIUS_OFFSET
        
        super().__init__(center_x, center_y, config.GHOST_SPEED, radius, color)
        
        self.ghost_type = ghost_type
        self.change_direction_timer = 0
        self.change_direction_interval = config.GHOST_DIRECTION_CHANGE_INTERVAL
    
    def update(self, level):
        """
        Update ghost position and AI.
        
        Args:
            level: Level instance for collision detection
        """
        self.change_direction_timer += 1
        
        # Randomly change direction periodically or when hitting a wall
        if self.change_direction_timer >= self.change_direction_interval:
            self.choose_new_direction(level)
            self.change_direction_timer = 0
        
        # Try to move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # If can move, do it; otherwise choose new direction
        if level.can_move_to(new_x, new_y, self.radius):
            self.x = new_x
            self.y = new_y
        else:
            # Hit a wall, choose new direction immediately
            self.choose_new_direction(level)
    
    def choose_new_direction(self, level):
        """
        Choose a random valid direction.
        
        Args:
            level: Level instance for collision detection
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down
        random.shuffle(directions)
        
        # Try each direction and pick the first valid one
        for direction in directions:
            new_x = self.x + direction[0] * self.speed * 5  # Look ahead a bit
            new_y = self.y + direction[1] * self.speed * 5
            
            if level.can_move_to(new_x, new_y, self.radius):
                self.direction = direction
                return
        
        # If no valid direction found, stop
        self.direction = (0, 0)
    
    def draw(self, screen):
        """Draw the ghost with eyes"""
        # Draw body using parent class
        super().draw(screen)
        
        # Draw eyes
        eye_offset = 5
        eye_radius = 3
        # Left eye
        pygame.draw.circle(screen, config.WHITE, 
                         (int(self.x - eye_offset), int(self.y - 3)), eye_radius)
        pygame.draw.circle(screen, config.BLACK, 
                         (int(self.x - eye_offset), int(self.y - 3)), eye_radius // 2)
        # Right eye
        pygame.draw.circle(screen, config.WHITE, 
                         (int(self.x + eye_offset), int(self.y - 3)), eye_radius)
        pygame.draw.circle(screen, config.BLACK, 
                         (int(self.x + eye_offset), int(self.y - 3)), eye_radius // 2)
