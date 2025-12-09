"""Player entity"""
from .entities.base import Entity
from . import config


class Player(Entity):
    """Player-controlled Pac-Man character"""
    
    def __init__(self, x, y):
        """
        Initialize player.
        
        Args:
            x: Starting X position (tile coordinate)
            y: Starting Y position (tile coordinate)
        """
        # Convert tile position to center pixel position
        center_x = x + config.TILE_SIZE / 2
        center_y = y + config.TILE_SIZE / 2
        radius = config.TILE_SIZE // 2 - config.PLAYER_RADIUS_OFFSET
        
        super().__init__(center_x, center_y, config.PLAYER_SPEED, radius, config.YELLOW)
        
        self.next_direction = (0, 0)
    
    def set_next_direction(self, direction):
        """
        Set the next desired direction from input.
        
        Args:
            direction: Tuple (dx, dy) representing direction
        """
        self.next_direction = direction
    
    def update(self, level):
        """
        Update player position.
        
        Args:
            level: Level instance for collision detection
        """
        # Try to change direction if a new direction is requested
        if self.next_direction != (0, 0):
            # Try the new direction
            new_x = self.x + self.next_direction[0] * self.speed
            new_y = self.y + self.next_direction[1] * self.speed
            
            if level.can_move_to(new_x, new_y, self.radius):
                self.direction = self.next_direction
        
        # Try to move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Only move if the new position is valid
        if level.can_move_to(new_x, new_y, self.radius):
            self.x = new_x
            self.y = new_y
