import pytest
from pacman_game.ai.pathfinding import a_star, get_next_direction, get_neighbors
from pacman_game import config

def test_a_star_path_found(simple_grid_level):
    """Test A* finds path in clear grid"""
    # Start (1,1), Goal (3,1). Should adhere to grid.
    start = (1, 1)
    goal = (3, 1)
    
    path = a_star(start, goal, simple_grid_level)
    
    assert path is not None
    assert len(path) > 1
    assert path[0] == start
    assert path[-1] == goal
    
    # Path should be contiguous
    for i in range(len(path)-1):
        curr = path[i]
        next_n = path[i+1]
        dist = abs(curr[0] - next_n[0]) + abs(curr[1] - next_n[1])
        assert dist == 1

def test_a_star_no_path_to_wall(simple_grid_level):
    """Test pathfinding to a wall returns None"""
    start = (1, 1)
    # (0, 0) is a wall in simple grid
    goal = (0, 0)
    
    path = a_star(start, goal, simple_grid_level)
    assert path is None

def test_a_star_from_wall_start(simple_grid_level):
    """Test pathfinding from a wall returns None"""
    start = (0, 0)
    goal = (1, 1)
    
    path = a_star(start, goal, simple_grid_level)
    assert path is None

def test_a_star_blocked_path(simple_grid_level):
    """Test blocked path returns correct route or None"""
    # Block path
    # Wall at (2, 1)
    simple_grid_level.grid[1][2] = 1
    
    start = (1, 1)
    goal = (3, 1)
    
    # Needs to go around: (1,1) -> (1,2) -> (2,2) -> (3,2) -> (3,1) or similar
    path = a_star(start, goal, simple_grid_level)
    assert path is not None
    assert (2, 1) not in path

def test_get_next_direction(simple_grid_level):
    """Test getting next move direction from path"""
    start = (1, 1)
    goal = (3, 1)
    
    # Next step should be (2, 1) -> direction (1, 0)
    dx_dy = get_next_direction(start, goal, simple_grid_level)
    assert dx_dy == (1, 0)

def test_get_next_direction_no_path(simple_grid_level):
    """Test direction is (0,0) if no path"""
    start = (1, 1)
    goal = (0, 0) # Wall
    
    dx_dy = get_next_direction(start, goal, simple_grid_level)
    assert dx_dy == (0, 0)

def test_get_neighbors(simple_grid_level):
    """Test neighbor validity"""
    # (1, 1) in simple grid -> Neighbors: (1,2), (2,1). Walls at (0,1) and (1,0).
    neighbors = get_neighbors((1, 1), simple_grid_level)
    assert (1, 2) in neighbors
    assert (2, 1) in neighbors
    assert len(neighbors) == 2
