import pytest
from hypothesis import given, strategies as st
from pacman_game.state_machine import GameStateMachine, GameState

def test_state_machine_init():
    """Verify initial state correctness"""
    sm = GameStateMachine()
    assert sm.current_state == GameState.PLAYING
    assert sm.lives == 3
    assert sm.level_number == 1
    assert sm.transition_timer == 0

def test_life_lost_decrement():
    """Verify decrement logic"""
    sm = GameStateMachine()
    initial_lives = sm.lives
    
    triggered = sm.check_life_lost(True)
    assert triggered is True
    assert sm.lives == initial_lives - 1
    assert sm.current_state == GameState.LIFE_LOST

def test_game_over_trigger():
    """Verify game over logic"""
    sm = GameStateMachine()
    sm.lives = 1
    triggered = sm.check_life_lost(True)
    assert triggered is True
    assert sm.lives == 0
    assert sm.current_state == GameState.GAME_OVER

def test_level_complete_trigger_logic():
    """Verify level complete trigger only at 0 pellets"""
    sm = GameStateMachine()
    # 1 pellet left -> No trigger
    assert sm.check_level_complete(1) is False
    assert sm.current_state == GameState.PLAYING
    
    # 0 pellets -> Trigger
    assert sm.check_level_complete(0) is True
    assert sm.current_state == GameState.LEVEL_COMPLETE

def test_invalid_state_transition():
    """Edge Case: Calling update_transition in PLAYING should do nothing"""
    sm = GameStateMachine()
    sm.current_state = GameState.PLAYING
    action = sm.update_transition()
    assert action is None

@given(st.sampled_from(GameState))
def test_reset_from_any_state(state):
    """Property: Reset must always restore PLAYING state, 3 lives, level 1"""
    sm = GameStateMachine()
    sm.current_state = state
    sm.lives = 0
    sm.level_number = 999
    
    sm.reset()
    
    assert sm.current_state == GameState.PLAYING
    assert sm.lives == 3
    assert sm.level_number == 1
    assert sm.transition_timer == 0

@given(st.integers(min_value=-100, max_value=200)) # Fuzz transition timer
def test_transition_timer_robustness(timer_val):
    """Property: Timer logic should be stable regardless of value"""
    sm = GameStateMachine()
    sm.current_state = GameState.LEVEL_COMPLETE
    sm.transition_timer = timer_val
    
    # Calling update
    action = sm.update_transition()
    
    if timer_val >= 119: # 120 is threshold, code checks +=1 first? 
    # Code: timer += 1. if timer >= 120.
    # So if input is 119, 119+1=120 -> Trigger.
        assert action == 'reload_level'
    else:
        assert action is None
