import pytest
from pacman_game import config
from pacman_game.level import PelletManager
from pacman_game.state_machine import GameStateMachine, GameState

def test_pellet_collection():
    """Test that collecting pellets removes them and reduces count"""
    pm = PelletManager()
    initial_count = pm.pellets_remaining()
    
    # Simple map in default Level might be large, but let's test specific logic
    # Find a dot. In LEVEL_MAP, (1, 1) is a dot (2).
    # See level.py line 7: [1, 2, ...
    
    # Collect at (1, 1) -> x=45, y=45
    x = 1 * config.TILE_SIZE + 5
    y = 1 * config.TILE_SIZE + 5
    
    points = pm.collect_pellet(x, y)
    
    assert points == config.POINTS_PER_PELLET
    assert pm.pellets_remaining() == initial_count - 1
    
    # Collect same again -> should be 0 points
    points = pm.collect_pellet(x, y)
    assert points == 0
    assert pm.pellets_remaining() == initial_count - 1

def test_level_complete_trigger():
    """Test that emptying pellets triggers LEVEL_COMPLETE"""
    pm = PelletManager()
    sm = GameStateMachine()
    
    # Simulate collecting ALL pellets
    # We can hack the grid to empty it quickly
    for row in range(len(pm.pellet_grid)):
        for col in range(len(pm.pellet_grid[0])):
            pm.pellet_grid[row][col] = 0
    
    pm.collected_count = pm.total_pellets
    
    # Check trigger
    triggered = sm.check_level_complete(pm.pellets_remaining())
    
    assert triggered is True
    assert sm.get_state() == GameState.LEVEL_COMPLETE

def test_level_progression():
    """Test leveling up increments level number"""
    sm = GameStateMachine()
    sm.current_state = GameState.LEVEL_COMPLETE
    sm.transition_timer = 119 # 1 frame before trigger
    
    # Update to trigger
    action = sm.update_transition()
    
    assert action == 'reload_level'
    assert sm.level_number == 2
    assert sm.get_state() == GameState.PLAYING

def test_reset_pellets():
    """Test resizing restores pellets"""
    pm = PelletManager()
    total = pm.total_pellets
    
    # Collect one
    pm.collect_pellet(45, 45) # (1,1)
    assert pm.pellets_remaining() == total - 1
    
    # Reset
    pm.reset()
    assert pm.pellets_remaining() == total
