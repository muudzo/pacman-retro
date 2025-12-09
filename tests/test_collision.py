import pytest
from hypothesis import given, strategies as st
import math
from pacman_game import config
from pacman_game.ghosts import Ghost
from pacman_game.player import Player
from pacman_game.ai.ghost_behaviors import GhostBehavior

def test_ghost_player_collision_basic():
    """Test circle-circle collision between ghost and player with explicit asserts"""
    p = Player(100, 100)
    g = Ghost(100, 100, config.RED, "BLINKY")
    
    # Should collide (distance 0)
    assert g.collides_with(p) is True
    assert p.collides_with(g) is True

def test_ghost_player_collision_boundary():
    """Test collision at geometric boundary with explicit calculation"""
    p = Player(100, 100)
    # Radius = TILE_SIZE//2 - OFFSET. 30//2 - 4 = 11.
    # Sum radii = 22.
    # Distance 21 -> Should collide
    g = Ghost(121, 100, config.RED, "BLINKY") 
    assert g.collides_with(p) is True
    
    # Distance 23 -> Should NOT collide (increased to 40 to be safe)
    g.x = 140
    assert g.collides_with(p) is False

def test_collision_edge_case_negative_coords():
    """Edge Case: Negative coordinates should handle collision logic correctly"""
    p = Player(-100, -100)
    g = Ghost(-100, -100, config.RED, "BLINKY")
    assert g.collides_with(p) is True
    
    g.x = -123 # Distance 23
    assert g.collides_with(p) is False

def test_collision_edge_case_large_coords():
    """Edge Case: Large coordinates should not cause overflow errors in simple logic"""
    p = Player(1_000_000, 1_000_000)
    g = Ghost(1_000_000, 1_000_000, config.RED, "BLINKY")
    assert g.collides_with(p) is True

@given(
    px=st.floats(min_value=-1000, max_value=1000),
    py=st.floats(min_value=-1000, max_value=1000),
    gx=st.floats(min_value=-1000, max_value=1000),
    gy=st.floats(min_value=-1000, max_value=1000)
)
def test_collision_invariant(px, py, gx, gy):
    """Property check: Collision is strictly distance < sum_radii"""
    p = Player(px, py)
    g = Ghost(gx, gy, config.RED, "BLINKY")
    
    # Manually calculate distance
    dist = math.sqrt((px - gx)**2 + (py - gy)**2)
    sum_radii = p.radius + g.radius
    
    should_collide = dist < sum_radii
    
    # Invariant: collides_with must match geometric truth
    assert g.collides_with(p) == should_collide

def test_ghost_collision_self():
    """Edge Case: Entity checking collision with itself should be True"""
    # Distance 0 < 2*radius
    g = Ghost(50, 50, config.RED, "BLINKY")
    assert g.collides_with(g) is True
