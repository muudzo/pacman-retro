"""Ghost entities with AI"""
import pygame
from .entities.base import Entity
from . import config
from .ai.pathfinding import get_next_direction
from .ai.ghost_behaviors import GhostBehavior, get_target_tile


class Ghost(Entity):
    """Ghost enemy with intelligent AI"""
    
    def __init__(self, x, y, color, ghost_type="BLINKY", speed=None):
        """
        Initialize ghost.
        
        Args:
            x: Starting X position (tile coordinate)
            y: Starting Y position (tile coordinate)
            color: RGB color tuple
            ghost_type: Type of ghost ("BLINKY", "PINKY", "INKY", "CLYDE")
            speed: Movement speed (pixels per frame). If None, uses default.
        """
        # Convert tile position to center pixel position
        center_x = x + config.TILE_SIZE / 2
        center_y = y + config.TILE_SIZE / 2
        radius = config.TILE_SIZE // 2 - config.GHOST_RADIUS_OFFSET
        
        # Use provided speed or default
        move_speed = speed if speed is not None else config.GHOST_SPEED
        
        super().__init__(center_x, center_y, move_speed, radius, color)
        
        self.ghost_type = ghost_type
        self.behavior = GhostBehavior.SCATTER
        self.behavior_timer = 0
        self.target_tile = None
        self.pathfinding_update_counter = 0
    
    def update(self, level, player, blinky=None):
        """
        Update ghost position and AI.
        
        Args:
            level: Level instance for collision detection
            player: Player instance for targeting
            blinky: Blinky ghost instance (needed for Inky's targeting)
        """
        # Update behavior timer and switch between scatter/chase
        if self.behavior == GhostBehavior.IDLE:
            # Ghost is in house, do nothing (or bounce)
            return

        self.behavior_timer += 1
        
        # Behavior pattern: scatter for 7 seconds, chase for 20 seconds, repeat
        if self.behavior == GhostBehavior.SCATTER:
            if self.behavior_timer >= config.SCATTER_DURATION:
                self.behavior = GhostBehavior.CHASE
                self.behavior_timer = 0
        elif self.behavior == GhostBehavior.CHASE:
            if self.behavior_timer >= config.CHASE_DURATION:
                self.behavior = GhostBehavior.SCATTER
                self.behavior_timer = 0
        
        # Update pathfinding periodically (not every frame for performance)
        self.pathfinding_update_counter += 1
        if self.pathfinding_update_counter >= config.PATHFINDING_UPDATE_INTERVAL:
            self.pathfinding_update_counter = 0
            self.update_target(level, player, blinky)
        
        # Move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Only move if the new position is valid
        if level.can_move_to(new_x, new_y, self.radius):
            self.x = new_x
            self.y = new_y
        else:
            # Hit a wall, recalculate path immediately
            self.update_target(level, player, blinky)
    
    def update_target(self, level, player, blinky=None):
        """
        Update target tile and calculate path.
        
        Args:
            level: Level instance for collision detection
            player: Player instance for targeting
            blinky: Blinky ghost instance (for Inky's targeting)
        """
        # Convert positions to grid coordinates
        ghost_grid_pos = (int(self.x / config.TILE_SIZE), int(self.y / config.TILE_SIZE))
        player_grid_pos = (int(player.x / config.TILE_SIZE), int(player.y / config.TILE_SIZE))
        
        # Get player's direction for targeting
        player_direction = player.direction
        
        # Get Blinky's position if available (for Inky)
        blinky_grid_pos = None
        if blinky and self.ghost_type == "INKY":
            blinky_grid_pos = (int(blinky.x / config.TILE_SIZE), int(blinky.y / config.TILE_SIZE))
        
        # Get target tile based on behavior and ghost type
        self.target_tile = get_target_tile(
            self.ghost_type,
            self.behavior,
            ghost_grid_pos,
            player_grid_pos,
            player_direction,
            blinky_grid_pos
        )
        
        # Calculate next direction using A* pathfinding
        next_direction = get_next_direction(ghost_grid_pos, self.target_tile, level)
        
        if next_direction != (0, 0):
            self.direction = next_direction
    
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

