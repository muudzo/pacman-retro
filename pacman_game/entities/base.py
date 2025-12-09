"""Base entity class for all game entities"""
import pygame


class Entity:
    """Base class for all moving entities in the game (Player, Ghosts)"""
    
    def __init__(self, x, y, speed, radius, color):
        """
        Initialize an entity.
        
        Args:
            x: X position (will be converted to center)
            y: Y position (will be converted to center)
            speed: Movement speed in pixels per frame
            radius: Collision radius
            color: RGB color tuple
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.color = color
        self.direction = (0, 0)
    
    def draw(self, screen):
        """Draw the entity as a circle"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def collides_with(self, other):
        """
        Check collision with another entity using circle collision.
        
        Args:
            other: Another Entity instance
            
        Returns:
            bool: True if entities are colliding
        """
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return distance < (self.radius + other.radius)
