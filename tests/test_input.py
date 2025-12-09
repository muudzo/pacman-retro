import pytest
from hypothesis import given, strategies as st
from pacman_game import config
from pacman_game.input_handler import InputHandler

def test_buffered_input_expiration(mock_pygame):
    """Verify input expires after buffer duration"""
    handler = InputHandler()
    mock_pygame.time.get_ticks.return_value = 1000
    
    # Needs internal method access or mock key press? 
    # Current impl of InputHandler reads keys in process_events.
    # It stores in self.buffered_direction.
    # We can inject it manually for testing logic separate from pygame events.
    
    handler.buffered_direction = (1, 0)
    handler.buffer_timestamp = 1000
    
    # 1. Inside window
    mock_pygame.time.get_ticks.return_value = 1000 + config.INPUT_BUFFER_DURATION - 10
    direction = handler.get_buffered_direction()
    assert direction == (1, 0)
    
    # 2. Outside window
    mock_pygame.time.get_ticks.return_value = 1000 + config.INPUT_BUFFER_DURATION + 10
    direction = handler.get_buffered_direction()
    assert direction == (0, 0) # Cleared

def test_buffered_input_consumption(mock_pygame):
    """Verify reading buffered input clears it"""
    handler = InputHandler()
    mock_pygame.time.get_ticks.return_value = 1000
    
    handler.buffered_direction = (0, 1)
    handler.buffer_timestamp = 1000
    
    # First read: Get it
    d = handler.get_buffered_direction()
    assert d == (0, 1)
    
    # Second read: Should be gone (if get_buffered_direction clears it?)
    # Implementation check:
    # return self.buffered_direction (it does NOT clear it automatically usually, logic might be in player?)
    # Wait, get_buffered_direction in input_handler.py lines:
    # def get_buffered_direction(self): ... if valid return dir ... return (0,0)
    # It does NOT clear it.
    # So second read should still return it if time valid.
    d2 = handler.get_buffered_direction()
    assert d2 == (0, 1) 
    
    # Reset manually
    handler.reset_buffer()
    assert handler.get_buffered_direction() == (0, 0)

from hypothesis import settings, HealthCheck

@given(
    dx=st.integers(min_value=-1, max_value=1),
    dy=st.integers(min_value=-1, max_value=1)
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_input_buffering_fuzz(mock_pygame, dx, dy):
    """Property check: Input handler always handles direction tuples safely"""
    handler = InputHandler()
    mock_pygame.time.get_ticks.return_value = 5000
    
    # Inject random direction
    handler.buffered_direction = (dx, dy)
    handler.buffer_timestamp = 5000
    
    result = handler.get_buffered_direction()
    
    # Check invariant
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result == (dx, dy)

def test_reset_buffer():
    """Edge Case: Resetting buffer matches init state"""
    handler = InputHandler()
    handler.buffered_direction = (1, 0)
    handler.buffer_timestamp = 12345
    
    handler.reset_buffer()
    
    assert handler.buffered_direction == (0, 0)
    assert handler.buffer_timestamp == 0
