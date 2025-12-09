"""Main game orchestration"""
import pygame
import sys
from . import config

from .level import Level, PelletManager
from .player import Player
from .ghosts import Ghost
from .utils import HighScoreManager
from .state_machine import GameStateMachine, GameState
from .input_handler import InputHandler


class Game:
    """Main game class - orchestrates game loop and components"""
    
    def __init__(self):
        """Initialize game and all components"""
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Retro")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
        # Initialize components
        self.level = Level()
        self.pellet_manager = PelletManager()
        self.state_machine = GameStateMachine()
        self.input_handler = InputHandler()
        self.high_score_manager = HighScoreManager()
        
        # Initialize entities
        self.player = Player(config.TILE_SIZE, config.TILE_SIZE)
        self.ghosts = [
            Ghost(config.TILE_SIZE * 9, config.TILE_SIZE * 9, config.RED, "BLINKY"),
            Ghost(config.TILE_SIZE * 10, config.TILE_SIZE * 9, config.PINK, "PINKY"),
            Ghost(config.TILE_SIZE * 9, config.TILE_SIZE * 10, config.CYAN, "INKY"),
            Ghost(config.TILE_SIZE * 10, config.TILE_SIZE * 10, config.ORANGE, "CLYDE"),
        ]
        
        self.score = 0
        self.new_high_score = False

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Process input events"""
        events = self.input_handler.process_events(
            game_over=self.state_machine.is_game_over()
        )
        
        if events['quit']:
            self.running = False
        elif events['restart'] and self.state_machine.is_game_over():
            self.reset()
        
        # Get directional input and pass to player
        if self.state_machine.is_playing():
            direction = self.input_handler.get_direction_input()
            self.player.set_next_direction(direction)

    def update(self):
        """Update game state"""
        # Check for state transitions
        action = self.state_machine.update_transition()
        if action == 'reload_level':
            self.reload_level()
        elif action == 'respawn':
            self.respawn_entities()
        
        # Only update entities during active gameplay
        if not self.state_machine.is_playing():
            return
        
        # Update player
        self.player.update(self.level)
        
        # Collect pellets
        points = self.pellet_manager.collect_pellet(self.player.x, self.player.y)
        self.score += points
        
        # Check level completion
        self.state_machine.check_level_complete(self.pellet_manager.pellets_remaining())
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.level)
            
            # Check collision with player
            if ghost.collides_with(self.player):
                if self.state_machine.check_life_lost(True):
                    # Update high score if game over
                    if self.state_machine.is_game_over():
                        self.new_high_score = self.high_score_manager.update_high_score(self.score)

    def draw(self):
        """Render to the screen"""
        self.screen.fill(config.BLACK)
        
        # Draw level and pellets
        self.level.draw(self.screen)
        self.pellet_manager.draw(self.screen)
        
        # Draw entities
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        self.player.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw UI elements (score, lives, messages)"""
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        self.screen.blit(score_text, (10, config.SCREEN_HEIGHT - 40))
        
        # Draw high score
        high_score = self.high_score_manager.get_high_score()
        high_score_text = self.font.render(f"High Score: {high_score}", True, config.YELLOW)
        self.screen.blit(high_score_text, (config.SCREEN_WIDTH - 250, config.SCREEN_HEIGHT - 40))
        
        # Draw pellets remaining
        pellets_remaining = self.pellet_manager.pellets_remaining()
        pellets_text = self.font.render(f"Pellets: {pellets_remaining}", True, config.WHITE)
        self.screen.blit(pellets_text, (10, config.SCREEN_HEIGHT - 80))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.state_machine.lives}", True, config.WHITE)
        self.screen.blit(lives_text, (10, config.SCREEN_HEIGHT - 120))
        
        # Draw level number
        level_text = self.font.render(f"Level: {self.state_machine.level_number}", True, config.WHITE)
        self.screen.blit(level_text, (config.SCREEN_WIDTH - 150, config.SCREEN_HEIGHT - 80))
        
        # Draw state-specific messages
        current_state = self.state_machine.get_state()
        
        if current_state == GameState.GAME_OVER:
            game_over_text = self.font.render("GAME OVER!", True, config.RED)
            text_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            if self.new_high_score:
                new_high_text = self.font.render("NEW HIGH SCORE!", True, config.YELLOW)
                new_high_rect = new_high_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
                self.screen.blit(new_high_text, new_high_rect)
            
            restart_text = self.font.render("Press R to Restart", True, config.WHITE)
            restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        elif current_state == GameState.LEVEL_COMPLETE:
            complete_text = self.font.render("LEVEL COMPLETE!", True, config.YELLOW)
            text_rect = complete_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(complete_text, text_rect)
        
        elif current_state == GameState.LIFE_LOST:
            life_lost_text = self.font.render("LIFE LOST!", True, config.RED)
            text_rect = life_lost_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(life_lost_text, text_rect)
    
    def reload_level(self):
        """Reload level (reset pellets and entities)"""
        self.pellet_manager.reset()
        self.respawn_entities()
    
    def respawn_entities(self):
        """Respawn player and ghosts at starting positions"""
        self.player = Player(config.TILE_SIZE, config.TILE_SIZE)
        self.ghosts = [
            Ghost(config.TILE_SIZE * 9, config.TILE_SIZE * 9, config.RED, "BLINKY"),
            Ghost(config.TILE_SIZE * 10, config.TILE_SIZE * 9, config.PINK, "PINKY"),
            Ghost(config.TILE_SIZE * 9, config.TILE_SIZE * 10, config.CYAN, "INKY"),
            Ghost(config.TILE_SIZE * 10, config.TILE_SIZE * 10, config.ORANGE, "CLYDE"),
        ]
    
    def reset(self):
        """Reset game to initial state"""
        self.state_machine.reset()
        self.pellet_manager.reset()
        self.respawn_entities()
        self.score = 0
        self.new_high_score = False
