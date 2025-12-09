import pytest
from hypothesis import given, strategies as st
from pacman_game.ai.ghost_behaviors import get_target_tile, GhostBehavior
from pacman_game import config

def test_ghost_targeting_basic():
    """Verify basic targeting for a known state"""
    player_pos = (1, 1)
    player_dir = (1, 0)
    target = get_target_tile("BLINKY", GhostBehavior.CHASE, (0,0), player_pos, player_dir)
    assert target == (1, 1)

def test_ghost_targeting_unknown_type():
    """Edge Case: Unknown ghost type should fallback to player position"""
    player_pos = (5, 5)
    target = get_target_tile("UNKNOWN_GHOST", GhostBehavior.CHASE, (0,0), player_pos, (0,0))
    assert target == player_pos

def test_ghost_frightened_mode():
    """Edge Case: Frightened mode should return current ghost position (placeholder)"""
    ghost_pos = (3, 3)
    target = get_target_tile("BLINKY", GhostBehavior.FRIGHTENED, ghost_pos, (0,0), (0,0))
    assert target == ghost_pos

@given(
    ghost_type=st.sampled_from(["BLINKY", "PINKY", "INKY", "CLYDE"]),
    behavior=st.sampled_from(GhostBehavior),
    gx=st.integers(min_value=0, max_value=20),
    gy=st.integers(min_value=0, max_value=20),
    px=st.integers(min_value=0, max_value=20),
    py=st.integers(min_value=0, max_value=20),
    pdx=st.sampled_from([-1, 0, 1]),
    pdy=st.sampled_from([-1, 0, 1])
)
def test_ghost_targeting_fuzz(ghost_type, behavior, gx, gy, px, py, pdx, pdy):
    """Property Check: get_target_tile must always return a coordinate tuple (int, int)"""
    ghost_pos = (gx, gy)
    player_pos = (px, py)
    player_dir = (pdx, pdy)
    blinky_pos = (0, 0) # Fixed for simplicity or random?
    
    target = get_target_tile(ghost_type, behavior, ghost_pos, player_pos, player_dir, blinky_pos)
    
    # Invariant: Output is a tuple of two integers
    assert isinstance(target, tuple)
    assert len(target) == 2
    assert isinstance(target[0], int)
    assert isinstance(target[1], int)
    
    # Invariant: Coordinates are somewhat bounded (at least finite).
    # Scatter targets might be outside grid? SCATTER_TARGETS in code are valid.
    # Logic clamps Pinky/Inky targets.
    # Blinky targets player.
    # So generally, coordinates should be reasonable (e.g. not billions)
    assert -100 < target[0] < 100
    assert -100 < target[1] < 100
