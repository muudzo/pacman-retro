import pygame
from . import constants

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.radius = constants.TILE_SIZE // 2 - 2

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.next_direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.next_direction = (1, 0)
        elif keys[pygame.K_UP]:
            self.next_direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.next_direction = (0, 1)

    def update(self):
        # Apply the next direction if possible (collision detection will come later)
        # For now, just change direction immediately
        if self.next_direction != (0, 0):
            self.direction = self.next_direction
        
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Screen wrapping (classic Pac-Man feature)
        if self.x > constants.SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = constants.SCREEN_WIDTH
        
        # Simple bounds checking (vertical) - keep in screen
        if self.y > constants.SCREEN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = constants.SCREEN_HEIGHT

    def draw(self, screen):
        # Draw Pac-Man as a yellow circle
        # Offset by radius because x,y are usually top-left in grids, 
        # but let's treat x,y as center for the circle drawing or adjust accordingly.
        # Let's assume x,y is the top-left of the tile for now to match maze grid.
        center_x = int(self.x + constants.TILE_SIZE / 2)
        center_y = int(self.y + constants.TILE_SIZE / 2)
        
        pygame.draw.circle(screen, constants.YELLOW, (center_x, center_y), self.radius)
