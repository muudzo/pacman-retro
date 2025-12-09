"""AI module for ghost behaviors and pathfinding"""
from .pathfinding import a_star, get_next_direction
from .ghost_behaviors import GhostBehavior, get_target_tile

__all__ = ['a_star', 'get_next_direction', 'GhostBehavior', 'get_target_tile']
