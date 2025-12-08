import pygame
import sys
from . import constants

from .maze import Maze
from .player import Player
from .ghosts import Ghost

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Retro")
        self.clock = pygame.time.Clock()
        self.running = True
        self.maze = Maze()
        # Start at tile (1, 1) -> (30, 30)
        self.player = Player(constants.TILE_SIZE, constants.TILE_SIZE)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        
        # Create ghosts at different starting positions
        self.ghosts = [
            Ghost(constants.TILE_SIZE * 9, constants.TILE_SIZE * 9, constants.RED),
            Ghost(constants.TILE_SIZE * 10, constants.TILE_SIZE * 9, constants.PINK),
            Ghost(constants.TILE_SIZE * 9, constants.TILE_SIZE * 10, constants.CYAN),
            Ghost(constants.TILE_SIZE * 10, constants.TILE_SIZE * 10, constants.ORANGE),
        ]

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(constants.FPS)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    # Restart game
                    self.__init__()
        
        if not self.game_over:
            self.player.handle_keys()

    def update(self):
        """Update game state."""
        if self.game_over:
            return
        
        self.player.update(self.maze)
        
        # Collect dots
        points = self.maze.collect_dot(self.player.x, self.player.y)
        self.score += points
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze)
            
            # Check collision with player
            if ghost.collides_with(self.player):
                self.game_over = True

    def draw(self):
        """Render to the screen."""
        self.screen.fill(constants.BLACK)
        self.maze.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        self.player.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, constants.WHITE)
        self.screen.blit(score_text, (10, constants.SCREEN_HEIGHT - 40))
        
        # Draw dots remaining
        dots_remaining = self.maze.total_dots - self.maze.dots_collected
        dots_text = self.font.render(f"Dots: {dots_remaining}", True, constants.WHITE)
        self.screen.blit(dots_text, (10, constants.SCREEN_HEIGHT - 80))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, constants.RED)
            restart_text = self.font.render("Press R to Restart", True, constants.WHITE)
            text_rect = game_over_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
