"""Input handling with buffering support"""
import pygame


class InputHandler:
    """Centralizes input handling and provides input buffering"""
    
    def __init__(self):
        """Initialize input handler"""
        self.quit_requested = False
        self.restart_requested = False
        self.debug_toggle_requested = False
        self.current_direction_input = (0, 0)
    
    def process_events(self, game_over=False):
        """
        Process pygame events.
        
        Args:
            game_over: Whether the game is in game over state
            
        Returns:
            dict: Dictionary with event flags
        """
        self.quit_requested = False
        self.restart_requested = False
        self.debug_toggle_requested = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    self.restart_requested = True
                elif event.key == pygame.K_F3:
                    self.debug_toggle_requested = True
        
        return {
            'quit': self.quit_requested,
            'restart': self.restart_requested,
            'debug_toggle': self.debug_toggle_requested
        }
    
    def get_direction_input(self):
        """
        Get current directional input from keyboard.
        
        Returns:
            tuple: Direction as (dx, dy) or (0, 0) if no input
        """
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            return (-1, 0)
        elif keys[pygame.K_RIGHT]:
            return (1, 0)
        elif keys[pygame.K_UP]:
            return (0, -1)
        elif keys[pygame.K_DOWN]:
            return (0, 1)
        
        return (0, 0)
