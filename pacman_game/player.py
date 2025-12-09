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
        self.desired_direction = (0, 0)
    
    def set_next_direction(self, direction):
        """
        Set the next desired direction from input.
        
        Args:
            direction: Tuple (dx, dy) representing direction
        """
        if direction != (0, 0):
            self.desired_direction = direction
    
    def is_at_tile_center(self):
        """
        Check if player is approximately at a tile center.
        
        Returns:
            bool: True if at or near tile center
        """
        # Calculate position within tile
        tile_x = self.x % config.TILE_SIZE
        tile_y = self.y % config.TILE_SIZE
        center = config.TILE_SIZE / 2
        
        # Check if within tolerance of center
        x_centered = abs(tile_x - center) <= config.TILE_CENTER_TOLERANCE
        y_centered = abs(tile_y - center) <= config.TILE_CENTER_TOLERANCE
        
        return x_centered and y_centered
    
    def update(self, level, input_handler=None):
        """
        Update player position.
        
        Args:
            level: Level instance for collision detection
            input_handler: InputHandler instance for buffered input
        """
        # Get buffered input if available
        if input_handler:
            buffered = input_handler.get_buffered_direction()
            if buffered != (0, 0):
                self.desired_direction = buffered
        
        # Check for immediate reverse (allowed anywhere)
        if self.desired_direction != (0, 0) and self.direction != (0, 0):
            # Check if opposite
            if (self.desired_direction[0] == -self.direction[0] and 
                self.desired_direction[1] == -self.direction[1]):
                self.direction = self.desired_direction
                if input_handler:
                    input_handler.clear_buffer()
        
        # Try to change direction:
        # 1. Check if at tile center (Standard turn)
        if self.desired_direction != (0, 0) and self.is_at_tile_center():
            # Try the desired direction
            new_x = self.x + self.desired_direction[0] * self.speed
            new_y = self.y + self.desired_direction[1] * self.speed
            
            if level.can_move_to(new_x, new_y, self.radius):
                self.direction = self.desired_direction
                # Clear buffer after successful turn
                if input_handler:
                    input_handler.clear_buffer()

        # 2. If NOT at center but Blocked (Wall Turn / Cornering)
        elif self.desired_direction != (0, 0):
            # Check if current direction is blocked
            next_x = self.x + self.direction[0] * self.speed
            next_y = self.y + self.direction[1] * self.speed
            
            if not level.can_move_to(next_x, next_y, self.radius):
                # Stuck! Try to snap-turn.
                # Determine snap target based on Desired Direction axis
                snap_x = self.x
                snap_y = self.y
                
                # Formula: round((val - offset) / tile_size) * tile_size + offset
                offset = config.TILE_SIZE / 2
                
                if self.desired_direction[0] != 0: # Horizontal turn -> Snap Y
                    grid_y_idx = round((self.y - offset) / config.TILE_SIZE)
                    snap_y = grid_y_idx * config.TILE_SIZE + offset
                    
                elif self.desired_direction[1] != 0: # Vertical turn -> Snap X
                    grid_x_idx = round((self.x - offset) / config.TILE_SIZE)
                    snap_x = grid_x_idx * config.TILE_SIZE + offset
                
                # Check if turn is valid from SNAP position
                check_x = snap_x + self.desired_direction[0] * self.speed
                check_y = snap_y + self.desired_direction[1] * self.speed
                
                if level.can_move_to(check_x, check_y, self.radius):
                    # Valid turn! Snap and turn.
                    self.x = snap_x
                    self.y = snap_y
                    self.direction = self.desired_direction
                    if input_handler:
                        input_handler.clear_buffer()
        
        # Try to move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Only move if the new position is valid
        if level.can_move_to(new_x, new_y, self.radius):
            self.x = new_x
            self.y = new_y
        elif config.WALL_SLIDE_ENABLED and self.is_at_tile_center():
            # If hitting a wall at tile center, try to align perfectly
            grid_x = int(self.x / config.TILE_SIZE)
            grid_y = int(self.y / config.TILE_SIZE)
            self.x = grid_x * config.TILE_SIZE + config.TILE_SIZE / 2
            self.y = grid_y * config.TILE_SIZE + config.TILE_SIZE / 2

