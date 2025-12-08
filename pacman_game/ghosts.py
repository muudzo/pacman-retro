import pygame
import random
from . import constants

class Ghost:
    def __init__(self, x, y, color):
        # Store position as CENTER of Ghost
        self.x = x + constants.TILE_SIZE / 2
        self.y = y + constants.TILE_SIZE / 2
        self.speed = 1.5  # Slightly slower than Pac-Man
        self.color = color
        self.direction = (0, 0)
        self.radius = constants.TILE_SIZE // 2 - 4
        self.change_direction_timer = 0
        self.change_direction_interval = 60  # Change direction every 60 frames

    def update(self, maze):
        """Update ghost position and AI."""
        self.change_direction_timer += 1
        
        # Randomly change direction periodically or when hitting a wall
        if self.change_direction_timer >= self.change_direction_interval:
            self.choose_new_direction(maze)
            self.change_direction_timer = 0
        
        # Try to move in current direction
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # If can move, do it; otherwise choose new direction
        if maze.can_move_to(new_x, new_y, self.radius):
            self.x = new_x
            self.y = new_y
        else:
            # Hit a wall, choose new direction immediately
            self.choose_new_direction(maze)

    def choose_new_direction(self, maze):
        """Choose a random valid direction."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # left, right, up, down
        random.shuffle(directions)
        
        # Try each direction and pick the first valid one
        for direction in directions:
            new_x = self.x + direction[0] * self.speed * 5  # Look ahead a bit
            new_y = self.y + direction[1] * self.speed * 5
            
            if maze.can_move_to(new_x, new_y, self.radius):
                self.direction = direction
                return
        
        # If no valid direction found, stop
        self.direction = (0, 0)

    def collides_with(self, player):
        """Check if ghost collides with player."""
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance < (self.radius + player.radius)

    def draw(self, screen):
        """Draw the ghost as a colored circle."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw eyes
        eye_offset = 5
        eye_radius = 3
        # Left eye
        pygame.draw.circle(screen, constants.WHITE, 
                         (int(self.x - eye_offset), int(self.y - 3)), eye_radius)
        pygame.draw.circle(screen, constants.BLACK, 
                         (int(self.x - eye_offset), int(self.y - 3)), eye_radius // 2)
        # Right eye
        pygame.draw.circle(screen, constants.WHITE, 
                         (int(self.x + eye_offset), int(self.y - 3)), eye_radius)
        pygame.draw.circle(screen, constants.BLACK, 
                         (int(self.x + eye_offset), int(self.y - 3)), eye_radius // 2)
