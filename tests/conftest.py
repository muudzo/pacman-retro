import pytest
from unittest.mock import MagicMock
import sys
import os

# Mock pygame before importing game modules that might use it
sys.modules['pygame'] = MagicMock()

# Now import game modules
from pacman_game.level import Level
from pacman_game.player import Player
from pacman_game.ghosts import Ghost
from pacman_game.state_machine import GameStateMachine
from pacman_game import config

@pytest.fixture
def mock_pygame():
    """Ensure pygame is mocked"""
    return sys.modules['pygame']

@pytest.fixture
def level():
    """Provide a standard level instance"""
    return Level()

@pytest.fixture
def player():
    """Provide a player instance at a standard position"""
    # Position at (1, 1) to be safe from walls
    return Player(config.TILE_SIZE * 1, config.TILE_SIZE * 1)

@pytest.fixture
def ghosts():
    """Provide a list of one ghost of each type"""
    return [
        Ghost(config.TILE_SIZE * 9, config.TILE_SIZE * 9, (255, 0, 0), "BLINKY"),
        Ghost(config.TILE_SIZE * 10, config.TILE_SIZE * 9, (255, 182, 255), "PINKY"),
        Ghost(config.TILE_SIZE * 9, config.TILE_SIZE * 10, (0, 255, 255), "INKY"),
        Ghost(config.TILE_SIZE * 10, config.TILE_SIZE * 10, (255, 182, 85), "CLYDE")
    ]

@pytest.fixture
def state_machine():
    """Provide a clean state machine"""
    return GameStateMachine()

@pytest.fixture
def simple_grid_level():
    """Provide a simplified 10x10 level for predictable pathfinding tests"""
    # Mocking the internal grid to be simple empty room surrounded by walls
    lvl = Level()
    # 10x10 grid: Boundary walls, empty inside
    # 1 = Wall, 0 = Empty
    grid = [[1] * 10 for _ in range(10)]
    for r in range(1, 9):
        for c in range(1, 9):
            grid[r][c] = 0
    
    lvl.grid = grid
    return lvl
