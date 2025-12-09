"""Input handling with buffering support"""
import pygame
from . import config


class InputHandler:
    """Centralizes input handling and provides input buffering"""
    
    def __init__(self):
        """Initialize input handler"""
        self.quit_requested = False
        self.restart_requested = False
        self.debug_toggle_requested = False
        self.current_direction_input = (0, 0)
        
        # Input buffering
        self.buffered_direction = (0, 0)
        self.buffer_timestamp = 0
    
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
        Get current directional input from keyboard with buffering.
        
        Returns:
            tuple: Direction as (dx, dy) or (0, 0) if no input
        """
        keys = pygame.key.get_pressed()
        new_direction = (0, 0)
        
        if keys[pygame.K_LEFT]:
            new_direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            new_direction = (1, 0)
        elif keys[pygame.K_UP]:
            new_direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            new_direction = (0, 1)
        
        # If a new direction is pressed, buffer it
        if new_direction != (0, 0):
            self.buffered_direction = new_direction
            self.buffer_timestamp = pygame.time.get_ticks()
        
        return new_direction
    
    def get_buffered_direction(self):
        """
        Get buffered direction if still valid.
        
        Returns:
            tuple: Buffered direction or (0, 0) if expired
        """
        current_time = pygame.time.get_ticks()
        
        # Check if buffer is still valid (within INPUT_BUFFER_DURATION ms)
        if current_time - self.buffer_timestamp <= config.INPUT_BUFFER_DURATION:
            return self.buffered_direction
        
        return (0, 0)
    
    def clear_buffer(self):
        """Clear the input buffer"""
        self.buffered_direction = (0, 0)
        self.buffer_timestamp = 0

