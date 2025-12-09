"""Debug overlay for visualizing game state"""
import pygame
from .. import config


class DebugOverlay:
    """Debug visualization overlay for development"""
    
    def __init__(self):
        """Initialize debug overlay"""
        self.enabled = config.DEBUG_ENABLED_BY_DEFAULT
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
    
    def toggle(self):
        """Toggle debug overlay on/off"""
        self.enabled = not self.enabled
    
    def draw(self, screen, level, player, ghosts, state_machine, fps=60):
        """
        Draw debug overlay.
        
        Args:
            screen: Pygame screen surface
            level: Level instance
            player: Player instance
            ghosts: List of Ghost instances
            state_machine: GameStateMachine instance
            fps: Current FPS
        """
        if not self.enabled:
            return
        
        # Draw tile grid
        if config.DEBUG_SHOW_GRID:
            self.draw_grid(screen, level)
        
        # Draw collision boxes
        if config.DEBUG_SHOW_COLLISION:
            self.draw_collision_boxes(screen, player, ghosts)
        
        # Draw ghost targets and paths
        if config.DEBUG_SHOW_TARGETS:
            self.draw_ghost_targets(screen, ghosts)
        
        # Draw debug info panel
        self.draw_info_panel(screen, player, ghosts, state_machine, fps)
    
    def draw_grid(self, screen, level):
        """Draw tile grid overlay"""
        for row in range(config.GRID_ROWS):
            for col in range(config.GRID_COLS):
                x = col * config.TILE_SIZE
                y = row * config.TILE_SIZE
                
                # Draw grid lines
                pygame.draw.rect(screen, (50, 50, 50), 
                               (x, y, config.TILE_SIZE, config.TILE_SIZE), 1)
                
                # Mark tile centers
                center_x = x + config.TILE_SIZE // 2
                center_y = y + config.TILE_SIZE // 2
                pygame.draw.circle(screen, (70, 70, 70), (center_x, center_y), 1)
    
    def draw_collision_boxes(self, screen, player, ghosts):
        """Draw collision circles around entities"""
        # Player collision box (green)
        pygame.draw.circle(screen, (0, 255, 0), 
                         (int(player.x), int(player.y)), player.radius, 1)
        
        # Ghost collision boxes (red)
        for ghost in ghosts:
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(ghost.x), int(ghost.y)), ghost.radius, 1)
    
    def draw_ghost_targets(self, screen, ghosts):
        """Draw ghost target tiles and behavior"""
        for ghost in ghosts:
            if ghost.target_tile:
                # Draw target tile
                target_x = ghost.target_tile[0] * config.TILE_SIZE
                target_y = ghost.target_tile[1] * config.TILE_SIZE
                
                # Color based on ghost type
                color = ghost.color
                
                # Draw target square
                pygame.draw.rect(screen, color, 
                               (target_x, target_y, config.TILE_SIZE, config.TILE_SIZE), 2)
                
                # Draw line from ghost to target
                ghost_pos = (int(ghost.x), int(ghost.y))
                target_center = (target_x + config.TILE_SIZE // 2, 
                               target_y + config.TILE_SIZE // 2)
                pygame.draw.line(screen, color, ghost_pos, target_center, 1)
                
                # Draw behavior text
                behavior_text = ghost.behavior.name
                text_surface = self.small_font.render(behavior_text, True, color)
                screen.blit(text_surface, (int(ghost.x) - 20, int(ghost.y) - 25))
    
    def draw_info_panel(self, screen, player, ghosts, state_machine, fps):
        """Draw debug information panel"""
        panel_x = 10
        panel_y = 10
        line_height = 18
        
        # Semi-transparent background
        panel_width = 250
        panel_height = 150
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.set_alpha(180)
        panel_surface.fill((0, 0, 0))
        screen.blit(panel_surface, (panel_x - 5, panel_y - 5))
        
        # FPS
        fps_text = f"FPS: {int(fps)}"
        self.draw_text(screen, fps_text, panel_x, panel_y, config.WHITE)
        panel_y += line_height
        
        # Game state
        state_text = f"State: {state_machine.get_state().name}"
        self.draw_text(screen, state_text, panel_x, panel_y, config.YELLOW)
        panel_y += line_height
        
        # Player position
        player_grid_x = int(player.x / config.TILE_SIZE)
        player_grid_y = int(player.y / config.TILE_SIZE)
        player_text = f"Player: ({player_grid_x}, {player_grid_y})"
        self.draw_text(screen, player_text, panel_x, panel_y, config.GREEN)
        panel_y += line_height
        
        # Player direction
        dir_text = f"Direction: {player.direction}"
        self.draw_text(screen, dir_text, panel_x, panel_y, config.GREEN)
        panel_y += line_height
        
        # At tile center
        centered = "Yes" if player.is_at_tile_center() else "No"
        center_text = f"At Center: {centered}"
        self.draw_text(screen, center_text, panel_x, panel_y, config.GREEN)
        panel_y += line_height
        
        # Ghost info
        panel_y += 5
        for i, ghost in enumerate(ghosts):
            ghost_grid_x = int(ghost.x / config.TILE_SIZE)
            ghost_grid_y = int(ghost.y / config.TILE_SIZE)
            ghost_text = f"{ghost.ghost_type[:3]}: ({ghost_grid_x},{ghost_grid_y}) {ghost.behavior.name[:3]}"
            self.draw_text(screen, ghost_text, panel_x, panel_y, ghost.color)
            panel_y += line_height
    
    def draw_text(self, screen, text, x, y, color):
        """Helper to draw text"""
        text_surface = self.small_font.render(text, True, color)
        screen.blit(text_surface, (x, y))
