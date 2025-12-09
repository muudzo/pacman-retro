import pytest
from hypothesis import given, strategies as st
from pacman_game import config
from pacman_game.ai.pathfinding import a_star, get_next_direction, get_neighbors
from pacman_game.level import Level

def test_a_star_path_found_basic(simple_grid_level):
    """Test A* finds path in clear grid with explicit path validation"""
    start = (1, 1)
    goal = (3, 1)
    path = a_star(start, goal, simple_grid_level)
    
    assert path is not None
    assert len(path) == 3 # (1,1)->(2,1)->(3,1)
    assert path == [(1,1), (2,1), (3,1)]

def test_a_star_start_is_goal(simple_grid_level):
    """Edge Case: Start equals Goal should return path with single node"""
    start = (1, 1)
    path = a_star(start, start, simple_grid_level)
    assert path == [start]

def test_a_star_no_path_blocked(simple_grid_level):
    """Edge Case: Goal is unreachable"""
    # Enclose (5, 5) with walls
    simple_grid_level.grid[4][5] = 1
    simple_grid_level.grid[6][5] = 1
    simple_grid_level.grid[5][4] = 1
    simple_grid_level.grid[5][6] = 1
    
    start = (1, 1)
    goal = (5, 5)
    path = a_star(start, goal, simple_grid_level)
    assert path is None

def test_pathfinding_out_of_bounds(simple_grid_level):
    """Edge Case: Querying out of bounds should return None gracefully"""
    start = (1, 1)
    goal = (-5, -5)
    path = a_star(start, goal, simple_grid_level)
    assert path is None
    
    # Start OOB
    path = a_star((-1, -1), (1, 1), simple_grid_level)
    assert path is None

@given(
    sx=st.integers(min_value=0, max_value=9),
    sy=st.integers(min_value=0, max_value=9),
    gx=st.integers(min_value=0, max_value=9),
    gy=st.integers(min_value=0, max_value=9),
    # Generate random 10x10 wall grid (0=Empty, 1=Wall)
    grid_rows=st.lists(
        st.lists(st.integers(min_value=0, max_value=1), min_size=10, max_size=10),
        min_size=10, max_size=10
    )
)
def test_pathfinding_fuzz(sx, sy, gx, gy, grid_rows):
    """Property check: A* behaves safely on random grids"""
    # Create mock level
    lvl = Level()
    lvl.grid = grid_rows
    
    start = (sx, sy)
    goal = (gx, gy)
    
    path = a_star(start, goal, lvl)
    
    if path is not None:
        # Invariants if path found:
        assert len(path) > 0
        assert path[0] == start
        assert path[-1] == goal
        
        # Path continuity
        for i in range(len(path)-1):
            curr = path[i]
            nxt = path[i+1]
            dist = abs(curr[0] - nxt[0]) + abs(curr[1] - nxt[1])
            assert dist == 1 # Steps must be adjacent
            # Steps must be walkable
            assert lvl.is_wall(curr[0], curr[1]) is False
            assert lvl.is_wall(nxt[0], nxt[1]) is False

def test_get_neighbors_validity(simple_grid_level):
    """Ensure get_neighbors only returns valid, walkable, in-bounds cells"""
    neighbors = get_neighbors((1, 1), simple_grid_level)
    for n in neighbors:
        assert simple_grid_level.is_wall(n[0], n[1]) is False
        # Manhatten dist is 1
        assert abs(n[0] - 1) + abs(n[1] - 1) == 1
