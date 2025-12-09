"""Game state machine for managing game states and transitions"""
from enum import Enum, auto


class GameState(Enum):
    """Enumeration of all possible game states"""
    MENU = auto()
    PLAYING = auto()
    LEVEL_COMPLETE = auto()
    LIFE_LOST = auto()
    GAME_OVER = auto()


class GameStateMachine:
    """Manages game state transitions and state-specific logic"""
    
    def __init__(self):
        """Initialize state machine"""
        self.current_state = GameState.PLAYING
        self.lives = 3
        self.level_number = 1
        self.transition_timer = 0
    
    def get_state(self):
        """Get current game state"""
        return self.current_state
    
    def is_playing(self):
        """Check if game is in playing state"""
        return self.current_state == GameState.PLAYING
    
    def is_game_over(self):
        """Check if game is over"""
        return self.current_state == GameState.GAME_OVER
    
    def check_level_complete(self, pellets_remaining):
        """
        Check if level is complete and transition if needed.
        
        Args:
            pellets_remaining: Number of pellets left
            
        Returns:
            bool: True if level was just completed
        """
        if self.current_state == GameState.PLAYING and pellets_remaining == 0:
            self.current_state = GameState.LEVEL_COMPLETE
            self.transition_timer = 0
            return True
        return False
    
    def check_life_lost(self, collision_occurred):
        """
        Check if player lost a life and transition if needed.
        
        Args:
            collision_occurred: True if player hit a ghost
            
        Returns:
            bool: True if life was just lost
        """
        if self.current_state == GameState.PLAYING and collision_occurred:
            self.lives -= 1
            if self.lives <= 0:
                self.current_state = GameState.GAME_OVER
            else:
                self.current_state = GameState.LIFE_LOST
            self.transition_timer = 0
            return True
        return False
    
    def update_transition(self):
        """
        Update transition timer and handle automatic state transitions.
        
        Returns:
            str: Action to take ('reload_level', 'respawn', or None)
        """
        if self.current_state in [GameState.LEVEL_COMPLETE, GameState.LIFE_LOST]:
            self.transition_timer += 1
            
            # Auto-transition after 2 seconds (120 frames at 60 FPS)
            if self.transition_timer >= 120:
                if self.current_state == GameState.LEVEL_COMPLETE:
                    self.level_number += 1
                    self.current_state = GameState.PLAYING
                    return 'reload_level'
                elif self.current_state == GameState.LIFE_LOST:
                    self.current_state = GameState.PLAYING
                    return 'respawn'
        
        return None
    
    def reset(self):
        """Reset state machine to initial state"""
        self.current_state = GameState.PLAYING
        self.lives = 3
        self.level_number = 1
        self.transition_timer = 0
