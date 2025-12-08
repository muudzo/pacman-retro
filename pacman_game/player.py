import pygame
from . import constants

class Player:
    def __init__(self, x, y):
        # Store position as CENTER of Pac-Man, not top-left
        self.x = x + constants.TILE_SIZE / 2
        self.y = y + constants.TILE_SIZE / 2
        self.speed = 2
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.radius = constants.TILE_SIZE // 2 - 4  # Slightly smaller for better collision feel

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

    def update(self, maze):
        # Try to change direction if a new direction is requested
        if self.next_direction != (0, 0):
            # Try the new direction
            new_x = self.x + self.next_direction[0] * self.speed
            new_y = self.y + self.next_direction[1] * self.speed
            
            if maze.can_move_to(new_x, new_y, self.radius):
                self.direction = self.next_direction
        
        # Try to move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Only move if the new position is valid
        if maze.can_move_to(new_x, new_y, self.radius):
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        # Draw Pac-Man as a yellow circle (x, y are already center coordinates)
        pygame.draw.circle(screen, constants.YELLOW, (int(self.x), int(self.y)), self.radius)
