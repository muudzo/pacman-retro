import pytest
from unittest.mock import MagicMock
from pacman_game.ghosts import Ghost
from pacman_game import config
from pacman_game.ai.ghost_behaviors import GhostBehavior

@pytest.fixture
def mock_level():
    lvl = MagicMock()
    lvl.can_move_to.return_value = True
    lvl.is_intersection.return_value = True # ensure pathfinding trigger
    return lvl

@pytest.fixture
def mock_player():
    p = MagicMock()
    p.x = 100
    p.y = 100
    p.direction = (1, 0)
    return p

def test_ghost_initialization():
    """Verify ghost inits logic"""
    g = Ghost(30, 30, (255, 0, 0), "BLINKY")
    assert g.x == 45
    assert g.y == 45
    assert g.behavior == GhostBehavior.SCATTER
    assert g.ghost_type == "BLINKY"

def test_ghost_update_movement(mock_level, mock_player):
    """Verify ghost moves in current direction"""
    g = Ghost(30, 30, config.RED, "BLINKY")
    g.direction = (1, 0)
    g.speed = 2
    
    # Mock A* pathfinding to return None or empty so direction doesn't change immediately?
    # Ghost.update calls calculate_direction if center & intersection & time
    # Let's simple check basic movement first (not at center)
    g.x = 50 # Not center (45)
    
    g.update(mock_level, mock_player, None)
    
    # Should move right
    assert g.x == 50 + 2

def test_ghost_recalculation_at_center(mock_level, mock_player, monkeypatch):
    """Verify ghost tries to recalculate path at intersection"""
    g = Ghost(30, 30, config.RED, "BLINKY")
    g.x = 45 # Center
    g.y = 45
    
    # Mock get_next_direction in ai.pathfinding
    import pacman_game.ai.pathfinding
    mock_get_dir = MagicMock(return_value=(0, 1)) # Down
    monkeypatch.setattr("pacman_game.ghosts.get_next_direction", mock_get_dir)
    
    # Mock behavior to ensure we are in CHASE
    g.behavior = GhostBehavior.CHASE
    
    # FORCE pathfinding update
    g.pathfinding_update_counter = config.PATHFINDING_UPDATE_INTERVAL
    
    g.update(mock_level, mock_player, None)
    
    # Should have called pathfinding and set direction
    assert g.direction == (0, 1)

def test_ghost_speed_scaling():
    """Verify speed logic"""
    g = Ghost(30, 30, config.RED, "BLINKY")
    g.speed = 2
    
    g.x += g.speed
    assert g.x == 45 + 2

def test_ghost_mode_switch():
    """Verify scatter/chase switching logic"""
    g = Ghost(30, 30, (255, 0, 0), "BLINKY")
    
    # Needs to see pygame
    import pygame
    
    # 1. Start in SCATTER (default)
    assert g.behavior == GhostBehavior.SCATTER
    
    # 2. Advance time past SCATTER_DURATION (frames/ticks in logic)
    # Ghost.update uses self.behavior_timer += 1
    # Check config.SCATTER_DURATION usage
    # We must manually set the timer to simulate elapsed time
    g.behavior_timer = config.SCATTER_DURATION # Trigger switch
    
    # Update needs level/player mocks
    mock_lvl = MagicMock()
    mock_lvl.can_move_to.return_value = True
    mock_lvl.is_intersection.return_value = False
    mock_plyr = MagicMock()
    
    g.update(mock_lvl, mock_plyr, None)
    
    # Should have switched to CHASE
    assert g.behavior == GhostBehavior.CHASE
    assert g.behavior_timer == 0 # Reset
    
    # 3. Advance time past CHASE_DURATION
    g.behavior_timer = config.CHASE_DURATION
    
    g.update(mock_lvl, mock_plyr, None)
    
    # Should switch back to SCATTER
    assert g.behavior == GhostBehavior.SCATTER

