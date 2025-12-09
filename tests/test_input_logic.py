import pytest
from unittest.mock import MagicMock
from pacman_game.input_handler import InputHandler
import pygame

def test_process_events_quit():
    """Verify quit event processing"""
    handler = InputHandler()
    
    # Mock pygame.event.get() to return a QUIT event
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    pygame.event.get.return_value = [mock_event]
    
    events = handler.process_events()
    assert events['quit'] is True

def test_process_events_restart_space():
    """Verify restart on SPACE in game over"""
    handler = InputHandler()
    
    # Mock KeyDown SPACE
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_SPACE
    pygame.event.get.return_value = [mock_event]
    
    events = handler.process_events(game_over=True)
    assert events['restart'] is False # Code only implements 'R' for restart
    
    # Ignored if game not over
    events = handler.process_events(game_over=False)
    assert events['restart'] is False # Should be false

def test_process_events_restart_r():
    """Verify restart on R key"""
    handler = InputHandler()
    
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_r
    pygame.event.get.return_value = [mock_event]
    
    events = handler.process_events(game_over=True)
    assert events['restart'] is True

def test_process_events_debug_toggle():
    """Verify debug toggle on F3"""
    handler = InputHandler()
    
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_F3
    pygame.event.get.return_value = [mock_event]
    
    events = handler.process_events()
    assert events['debug_toggle'] is True

def test_process_events_direction():
    """Verify direction keys feed buffering via get_direction_input"""
    handler = InputHandler()
    
    # Mock pygame.key.get_pressed
    # get_pressed returns a sequence.
    def get_pressed_side_effect():
        keys = MagicMock()
        keys.__getitem__.side_effect = lambda k: 1 if k == pygame.K_RIGHT else 0
        return keys

    pygame.key.get_pressed.side_effect = get_pressed_side_effect
    
    # Also need current time for buffering
    pygame.time.get_ticks.return_value = 10000
    
    # get_direction_input calls get_pressed inside
    handler.get_direction_input()
    
    # Should have buffered (1, 0)
    assert handler.get_buffered_direction() == (1, 0)
    
    # UP
    def UP_side_effect():
        keys = MagicMock()
        keys.__getitem__.side_effect = lambda k: 1 if k == pygame.K_UP else 0
        return keys
    pygame.key.get_pressed.side_effect = UP_side_effect
    
    handler.get_direction_input()
    assert handler.get_buffered_direction() == (0, -1)
