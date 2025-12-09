import pytest
from hypothesis import given, strategies as st
from pacman_game import config
from pacman_game.level import PelletManager
from pacman_game.state_machine import GameStateMachine, GameState

def test_pellet_collection(level):
    """Test pellet collection reduces count and returns points"""
    pm = PelletManager()
    initial = pm.pellets_remaining()
    
    # Collect at known pellet location (1,1) -> 45,45
    x, y = 45, 45
    points = pm.collect_pellet(x, y)
    
    assert points == config.POINTS_PER_PELLET
    assert pm.pellets_remaining() == initial - 1

def test_pellet_double_collection():
    """Edge Case: Double collection should yield 0 points"""
    pm = PelletManager()
    x, y = 45, 45
    pm.collect_pellet(x, y)
    points = pm.collect_pellet(x, y)
    assert points == 0

def test_pellet_collection_out_of_bounds():
    """Edge Case: Collecting outside grid shouldn't crash"""
    pm = PelletManager()
    initial = pm.pellets_remaining()
    
    points = pm.collect_pellet(-100, -100)
    assert points == 0
    assert pm.pellets_remaining() == initial
    
    points = pm.collect_pellet(10000, 10000)
    assert points == 0

@given(
    x=st.integers(min_value=-1000, max_value=2000),
    y=st.integers(min_value=-1000, max_value=2000)
)
def test_pellet_collection_fuzz(x, y):
    """Property test: Collection attempts never crash game"""
    pm = PelletManager()
    try:
        points = pm.collect_pellet(x, y)
    except Exception as e:
        pytest.fail(f"collect_pellet crashed with {e}")
    
    assert points in [0, config.POINTS_PER_PELLET]
    
def test_pellet_manager_reset():
    """Verify reset restores all pellets"""
    pm = PelletManager()
    total = pm.pellets_remaining()
    
    # Collect one
    pm.collect_pellet(45, 45)
    assert pm.pellets_remaining() == total - 1
    
    pm.reset()
    assert pm.pellets_remaining() == total

def test_level_progression():
    """Verify state machine progression logic"""
    sm = GameStateMachine()
    
    # Set to end of level complete state
    sm.current_state = GameState.LEVEL_COMPLETE
    sm.level_number = 1
    sm.transition_timer = config.LEVEL_COMPLETE_DELAY - 1
    
    # Update should act
    action = sm.update_transition()
    assert action == 'reload_level'
    assert sm.level_number == 2
