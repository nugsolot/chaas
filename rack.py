# rack.py

import pygame

class Rack:
    def __init__(self, grid_x, grid_y, grid):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid = grid
        self.level = 0  # 0: Empty, 1: ToR installed, 2: Configured
        self.contaminated = False
        self.wait_time = 0  # Time to wait for next setup level
        self.protected_time = 0  # Time during which the rack is protected from contamination
        self.image = pygame.Surface((20, 20))
        self.rect = None  # Will be set during draw

    def interact(self):
        if self.contaminated:
            # Decontaminate the rack
            self.contaminated = False
            self.level = 0  # Reset the rack to the initial state
            self.wait_time = 2  # Optional: Wait before it can be upgraded again
            self.protected_time = 5  # Rack is protected for 5 seconds
        elif self.level < 2 and self.wait_time <= 0:
            # Proceed with the setup process
            self.level += 1
            self.wait_time = 2  # Wait 2 seconds before next level

    def update(self, delta_time):
        if self.wait_time > 0:
            self.wait_time -= delta_time
            if self.wait_time < 0:
                self.wait_time = 0
        if self.protected_time > 0:
            self.protected_time -= delta_time
            if self.protected_time < 0:
                self.protected_time = 0

    def draw(self, screen):
        # Choose color based on state
        if self.contaminated:
            color = (255, 0, 0)  # Red for contaminated
        else:
            if self.level == 0:
                color = (100, 100, 100)  # Gray for empty
            elif self.level == 1:
                color = (0, 0, 255)      # Blue for ToR installed
            elif self.level == 2:
                color = (0, 255, 0)      # Green for configured

        # Base rectangle (the rack)
        self.image.fill(color)
        iso_x, iso_y = self.grid.to_isometric(self.grid_x, self.grid_y)
        self.rect = pygame.Rect(iso_x - 10, iso_y - 10, 20, 20)
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Draw outline if the rack is protected
        if self.protected_time > 0:
            outline_rect = self.rect.inflate(4, 4)  # Slightly larger rectangle
            pygame.draw.rect(screen, (255, 255, 0), outline_rect, 2)  # Yellow outline with width 2