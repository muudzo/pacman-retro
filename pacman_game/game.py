import pygame
import sys
from . import constants

from .maze import Maze

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Retro")
        self.clock = pygame.time.Clock()
        self.running = True
        self.maze = Maze()

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

    def update(self):
        """Update game state."""
        pass

    def draw(self):
        """Render to the screen."""
        self.screen.fill(constants.BLACK)
        self.maze.draw(self.screen)
        pygame.display.flip()
