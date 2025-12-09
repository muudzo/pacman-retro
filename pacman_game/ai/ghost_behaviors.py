"""Ghost behavior states and targeting logic"""
from enum import Enum, auto
from typing import Tuple
from .. import config


class GhostBehavior(Enum):
    """Ghost behavior states"""
    SCATTER = auto()
    CHASE = auto()
    FRIGHTENED = auto()


# Scatter target corners for each ghost type
SCATTER_TARGETS = {
    "BLINKY": (config.GRID_COLS - 2, 1),  # Top-right corner
    "PINKY": (1, 1),  # Top-left corner
    "INKY": (config.GRID_COLS - 2, config.GRID_ROWS - 2),  # Bottom-right corner
    "CLYDE": (1, config.GRID_ROWS - 2),  # Bottom-left corner
}


def get_target_tile(ghost_type: str, behavior: GhostBehavior, ghost_pos: Tuple[int, int], 
                    player_pos: Tuple[int, int], player_direction: Tuple[int, int],
                    blinky_pos: Tuple[int, int] = None) -> Tuple[int, int]:
    """
    Get the target tile for a ghost based on its type and behavior.
    
    Args:
        ghost_type: Type of ghost ("BLINKY", "PINKY", "INKY", "CLYDE")
        behavior: Current behavior state
        ghost_pos: Ghost's current position (grid_x, grid_y)
        player_pos: Player's current position (grid_x, grid_y)
        player_direction: Player's current direction (dx, dy)
        blinky_pos: Blinky's position (needed for Inky's targeting)
        
    Returns:
        Target tile position (grid_x, grid_y)
    """
    if behavior == GhostBehavior.SCATTER:
        # In scatter mode, each ghost targets its assigned corner
        return SCATTER_TARGETS.get(ghost_type, (1, 1))
    
    elif behavior == GhostBehavior.CHASE:
        # In chase mode, each ghost has unique targeting
        if ghost_type == "BLINKY":
            # Blinky targets player's current position directly
            return player_pos
        
        elif ghost_type == "PINKY":
            # Pinky targets 4 tiles ahead of player
            target_x = player_pos[0] + player_direction[0] * 4
            target_y = player_pos[1] + player_direction[1] * 4
            # Clamp to grid bounds
            target_x = max(0, min(config.GRID_COLS - 1, target_x))
            target_y = max(0, min(config.GRID_ROWS - 1, target_y))
            return (target_x, target_y)
        
        elif ghost_type == "INKY":
            # Inky uses complex targeting: 2 tiles ahead of player, then double the vector from Blinky
            if blinky_pos:
                # Get point 2 tiles ahead of player
                pivot_x = player_pos[0] + player_direction[0] * 2
                pivot_y = player_pos[1] + player_direction[1] * 2
                
                # Calculate vector from Blinky to pivot
                vec_x = pivot_x - blinky_pos[0]
                vec_y = pivot_y - blinky_pos[1]
                
                # Double the vector
                target_x = blinky_pos[0] + vec_x * 2
                target_y = blinky_pos[1] + vec_y * 2
                
                # Clamp to grid bounds
                target_x = max(0, min(config.GRID_COLS - 1, target_x))
                target_y = max(0, min(config.GRID_ROWS - 1, target_y))
                return (target_x, target_y)
            else:
                # Fallback to player position if Blinky position not available
                return player_pos
        
        elif ghost_type == "CLYDE":
            # Clyde is "shy" - chases when far, scatters when close
            distance = abs(ghost_pos[0] - player_pos[0]) + abs(ghost_pos[1] - player_pos[1])
            
            if distance > 8:
                # Far from player - chase directly
                return player_pos
            else:
                # Close to player - retreat to scatter corner
                return SCATTER_TARGETS["CLYDE"]
    
    elif behavior == GhostBehavior.FRIGHTENED:
        # In frightened mode, move randomly (handled elsewhere)
        # Return current position as placeholder
        return ghost_pos
    
    # Default fallback
    return player_pos
