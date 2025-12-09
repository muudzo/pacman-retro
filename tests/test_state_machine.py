import pytest
from pacman_game.state_machine import GameStateMachine, GameState

def test_initial_state():
    """Test initial state is PLAYING"""
    sm = GameStateMachine()
    # As per implementation, starts at PLAYING for this simple engine
    assert sm.current_state == GameState.PLAYING
    assert sm.lives == 3
    assert sm.level_number == 1

def test_life_lost_transition():
    """Test transition to LIFE_LOST"""
    sm = GameStateMachine()
    
    # Trigger collision with lives > 1
    transitioned = sm.check_life_lost(True)
    
    assert transitioned is True
    assert sm.current_state == GameState.LIFE_LOST
    assert sm.lives == 2
    assert sm.transition_timer == 0

def test_game_over_transition():
    """Test transition to GAME_OVER when lives run out"""
    sm = GameStateMachine()
    sm.lives = 1
    
    transitioned = sm.check_life_lost(True)
    
    assert transitioned is True
    assert sm.current_state == GameState.GAME_OVER
    assert sm.lives == 0

def test_level_complete_transition():
    """Test transition to LEVEL_COMPLETE"""
    sm = GameStateMachine()
    
    transitioned = sm.check_level_complete(0) # 0 pellets left
    
    assert transitioned is True
    assert sm.current_state == GameState.LEVEL_COMPLETE
    assert sm.transition_timer == 0

def test_auto_transition_from_life_lost():
    """Test auto-resume from LIFE_LOST"""
    sm = GameStateMachine()
    sm.current_state = GameState.LIFE_LOST
    sm.transition_timer = 119
    
    action = sm.update_transition()
    
    assert action == 'respawn'
    assert sm.current_state == GameState.PLAYING

def test_auto_transition_from_level_complete():
    """Test auto-advance from LEVEL_COMPLETE"""
    sm = GameStateMachine()
    sm.current_state = GameState.LEVEL_COMPLETE
    sm.level_number = 1
    sm.transition_timer = 119
    
    action = sm.update_transition()
    
    assert action == 'reload_level'
    assert sm.level_number == 2
    assert sm.current_state == GameState.PLAYING

def test_game_over_is_terminal():
    """Test GAME_OVER does not auto-transition"""
    sm = GameStateMachine()
    sm.current_state = GameState.GAME_OVER
    
    action = sm.update_transition()
    assert action is None
    assert sm.current_state == GameState.GAME_OVER

def test_reset():
    """Test reset restores initial state"""
    sm = GameStateMachine()
    sm.lives = 0
    sm.current_state = GameState.GAME_OVER
    sm.level_number = 5
    
    sm.reset()
    
    assert sm.lives == 3
    assert sm.level_number == 1
    assert sm.current_state == GameState.PLAYING
