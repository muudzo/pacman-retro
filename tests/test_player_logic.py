import pytest
from unittest.mock import MagicMock
from pacman_game.player import Player
from pacman_game import config

@pytest.fixture
def mock_level():
    level = MagicMock()
    # Default to allowing movement
    level.can_move_to.return_value = True
    return level

@pytest.fixture
def mock_input_handler():
    handler = MagicMock()
    handler.get_buffered_direction.return_value = (0, 0)
    return handler

def test_player_init_position():
    """Verify player initializes at center of tile"""
    p = Player(1 * config.TILE_SIZE, 1 * config.TILE_SIZE) # Tile (1, 1) pixels
    # Center = 30 + 15 = 45
    assert p.x == 45
    assert p.y == 45
    assert p.direction == (0, 0)

def test_is_at_tile_center():
    """Verify center tolerance check"""
    p = Player(30, 30)
    p.x = 45
    p.y = 45
    assert p.is_at_tile_center() is True
    
    # Edge tolerance
    p.x = 45 + config.TILE_CENTER_TOLERANCE
    assert p.is_at_tile_center() is True
    
    # Out of tolerance
    p.x = 45 + config.TILE_CENTER_TOLERANCE + 1
    assert p.is_at_tile_center() is False

def test_update_consumes_input(mock_level, mock_input_handler):
    """Verify update reads from input handler"""
    p = Player(30, 30)
    mock_input_handler.get_buffered_direction.return_value = (1, 0)
    
    p.update(mock_level, mock_input_handler)
    
    assert p.desired_direction == (1, 0)
    mock_input_handler.get_buffered_direction.assert_called_once()

def test_update_turns_at_center(mock_level, mock_input_handler):
    """Verify turning logic executes when at center and path validity check passes"""
    p = Player(30, 30)
    p.desired_direction = (0, 1) # Want to go DOWN
    p.direction = (1, 0) # Currently going RIGHT
    
    # Ensure at center
    p.x = 45
    p.y = 45
    
    # Mock level allows move
    mock_level.can_move_to.return_value = True
    
    p.update(mock_level, mock_input_handler)
    
    # Should have turned
    assert p.direction == (0, 1)
    # Should have cleared buffer
    mock_input_handler.clear_buffer.assert_called_once()
    
    # verify movement happened in new direction
    # speed is usually 2 or 3.
    target = 45 + p.speed
    # Floating point comparison safety generally good for exact int addition but let's be safe
    assert p.y == target

def test_update_blocks_turn_if_wall(mock_level, mock_input_handler):
    """Verify turn blocked if level says no"""
    p = Player(30, 30)
    p.desired_direction = (0, 1)
    p.direction = (1, 0)
    
    mock_level.can_move_to.side_effect = [False, True] 
    # First call is for turning (new_x/y with desired). Return False (Wall).
    # Second call is for continuing current direction. Return True (Continue).
    
    p.update(mock_level, mock_input_handler)
    
    assert p.direction == (1, 0) # No turn
    mock_input_handler.clear_buffer.assert_not_called()
    assert p.x == 45 + p.speed # Continued right

def test_wall_slide_alignment(mock_level, mock_input_handler):
    """Verify wall slide aligns to grid if stuck"""
    config.WALL_SLIDE_ENABLED = True
    p = Player(30, 30)
    p.direction = (1, 0)
    
    # At center
    p.x = 45
    p.y = 45
    
    # Wall ahead
    mock_level.can_move_to.return_value = False
    
    # Update
    p.update(mock_level, mock_input_handler)
    
    # Should stay at 45 (or be realigned to 45 if slight drift, but here initialized at 45)
    assert p.x == 45
    assert p.y == 45
    
    # If off center but within tolerance
    p.x = 46 # Off by 1
    p.update(mock_level, mock_input_handler)
    
    # Should act to snap/slide? 
    # impl: if not can_move_to and at_center -> grid_x*size + size/2
    # 46 is at center (tolerance 2).
    # grid_x for 46 (tile 1) is 1. 1*30+15 = 45.
    assert p.x == 45 # Re-aligned logic check

def test_reverse_direction_anywhere(mock_level, mock_input_handler):
    """Verify player can reverse direction even if not at center"""
    p = Player(30, 30)
    p.direction = (1, 0) # Moving RIGHT
    p.speed = 2
    
    # Position player NOT at center
    # Center is 45. Let's say 50.
    p.x = 50 
    p.y = 45
    assert p.is_at_tile_center() is False
    
    # Input: LEFT (Reverse)
    mock_input_handler.get_buffered_direction.return_value = (-1, 0)
    
    # Update
    p.update(mock_level, mock_input_handler)
    
    # Should have turned LEFT immediately
    assert p.desired_direction == (-1, 0)
    assert p.direction == (-1, 0)
    # Should move left
    assert p.x == 50 - 2

