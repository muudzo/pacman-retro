import pytest
from pacman_game import config
from pacman_game.ai.ghost_behaviors import get_target_tile, GhostBehavior

def test_blinky_targeting():
    """Blinky should target player position directly"""
    # Scatter phase (handled by behavior switching, here we test get_target_tile)
    ghost_pos = (5, 5)
    player_pos = (10, 10)
    player_dir = (1, 0)
    
    # 1. Chase Behavior
    target = get_target_tile("BLINKY", GhostBehavior.CHASE, ghost_pos, player_pos, player_dir)
    assert target == player_pos

    # 2. Scatter Behavior (Top Right)
    target = get_target_tile("BLINKY", GhostBehavior.SCATTER, ghost_pos, player_pos, player_dir)
    # BLINKY SCATTER target is (GRID_COLS - 2, 1) -> (18, 1) usually (20x20 grid)
    assert target == (config.GRID_COLS - 2, 1)

def test_pinky_targeting():
    """Pinky should target 4 tiles ahead of player"""
    ghost_pos = (5, 5)
    player_pos = (10, 10)
    
    # Direction RIGHT (1, 0) -> Target (14, 10)
    target = get_target_tile("PINKY", GhostBehavior.CHASE, ghost_pos, player_pos, (1, 0))
    assert target == (14, 10)
    
    # Direction UP (0, -1) -> Target (10, 6)
    target = get_target_tile("PINKY", GhostBehavior.CHASE, ghost_pos, player_pos, (0, -1))
    assert target == (10, 6)
    
    # Scatter (Top Left)
    target = get_target_tile("PINKY", GhostBehavior.SCATTER, ghost_pos, player_pos, (1, 0))
    assert target == (1, 1)

def test_inky_targeting():
    """Inky targets vector from Blinky to 2-ahead-of-Player, doubled"""
    # P = Player, B = Blinky, T = Target
    # P pos: (10, 10), Dir: Right (1, 0)
    # Pivot (2 ahead): (12, 10)
    # Blinky pos: (8, 10)
    # Vector B->Pivot: (4, 0)
    # Target = Blinky + 2*Vector = (8+8, 10+0) = (16, 10)
    
    player_pos = (10, 10)
    player_dir = (1, 0)
    blinky_pos = (8, 10)
    ghost_pos = (5, 5) # Inky's pos doesn't matter for target calc in Chase
    
    target = get_target_tile("INKY", GhostBehavior.CHASE, ghost_pos, player_pos, player_dir, blinky_pos=blinky_pos)
    assert target == (16, 10)
    
    # Scatter (Bottom Right)
    target = get_target_tile("INKY", GhostBehavior.SCATTER, ghost_pos, player_pos, player_dir)
    assert target == (config.GRID_COLS - 2, config.GRID_ROWS - 2)

def test_clyde_targeting():
    """Clyde targets player like Blinky when far, Scatter target when close (< 8 tiles)"""
    player_pos = (10, 10)
    player_dir = (1, 0)
    
    # 1. Far away (> 8 distance)
    # Manhattan dist: abs(0-10) + abs(0-10) = 20 > 8
    clyde_pos = (0, 0)
    target = get_target_tile("CLYDE", GhostBehavior.CHASE, clyde_pos, player_pos, player_dir)
    assert target == player_pos  # Chasing
    
    # 2. Close (< 8 distance)
    # Pos (8, 10). Dist: abs(8-10) + 0 = 2. 2 < 8.
    clyde_pos = (8, 10)
    target = get_target_tile("CLYDE", GhostBehavior.CHASE, clyde_pos, player_pos, player_dir)
    # Retreat to Scatter corner (Bottom Left)
    assert target == (1, config.GRID_ROWS - 2)
    
    # Scatter
    target = get_target_tile("CLYDE", GhostBehavior.SCATTER, clyde_pos, player_pos, player_dir)
    assert target == (1, config.GRID_ROWS - 2)
