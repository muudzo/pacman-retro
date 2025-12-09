"""A* pathfinding algorithm for ghost navigation"""
import heapq
from typing import Tuple, List, Optional


def heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance heuristic.
    
    Args:
        pos1: First position (grid_x, grid_y)
        pos2: Second position (grid_x, grid_y)
        
    Returns:
        Manhattan distance between positions
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_neighbors(pos: Tuple[int, int], level) -> List[Tuple[int, int]]:
    """
    Get valid neighboring tiles.
    
    Args:
        pos: Current position (grid_x, grid_y)
        level: Level instance for collision detection
        
    Returns:
        List of valid neighbor positions
    """
    x, y = pos
    neighbors = []
    
    # Check all four directions
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if not level.is_wall(new_x, new_y):
            neighbors.append((new_x, new_y))
    
    return neighbors


def a_star(start: Tuple[int, int], goal: Tuple[int, int], level) -> Optional[List[Tuple[int, int]]]:
    """
    A* pathfinding algorithm.
    
    Args:
        start: Starting position (grid_x, grid_y)
        goal: Goal position (grid_x, grid_y)
        level: Level instance for collision detection
        
    Returns:
        List of positions from start to goal, or None if no path exists
    """
    # If start or goal is a wall, return None
    if level.is_wall(start[0], start[1]) or level.is_wall(goal[0], goal[1]):
        return None
    
    # Priority queue: (f_score, counter, position, path)
    counter = 0
    open_set = [(0, counter, start, [start])]
    closed_set = set()
    
    while open_set:
        f_score, _, current, path = heapq.heappop(open_set)
        
        # Goal reached
        if current == goal:
            return path
        
        # Skip if already visited
        if current in closed_set:
            continue
        
        closed_set.add(current)
        
        # Explore neighbors
        for neighbor in get_neighbors(current, level):
            if neighbor in closed_set:
                continue
            
            new_path = path + [neighbor]
            g_score = len(new_path) - 1  # Cost from start
            h_score = heuristic(neighbor, goal)  # Estimated cost to goal
            f_score = g_score + h_score
            
            counter += 1
            heapq.heappush(open_set, (f_score, counter, neighbor, new_path))
    
    # No path found
    return None


def get_next_direction(current_pos: Tuple[int, int], target_pos: Tuple[int, int], level) -> Tuple[int, int]:
    """
    Get the next direction to move towards target using A*.
    
    Args:
        current_pos: Current position (grid_x, grid_y)
        target_pos: Target position (grid_x, grid_y)
        level: Level instance for collision detection
        
    Returns:
        Direction tuple (dx, dy) or (0, 0) if no path
    """
    path = a_star(current_pos, target_pos, level)
    
    if path and len(path) > 1:
        # Get next position in path
        next_pos = path[1]
        dx = next_pos[0] - current_pos[0]
        dy = next_pos[1] - current_pos[1]
        return (dx, dy)
    
    return (0, 0)
