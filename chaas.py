# chaas.py

import pygame
import random

class CHaaS:
    def __init__(self, grid):
        self.grid = grid
        # Start position is a random walkable tile
        while True:
            self.position = [random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)]
            if grid.is_walkable(int(self.position[0]), int(self.position[1])):
                break
        self.move_timer = 0  # Time until next move
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Yellow color for CHaaS

    def update(self, delta_time, racks):
        self.move_timer -= delta_time
        if self.move_timer <= 0:
            # Attempt to move to a random adjacent walkable tile
            for _ in range(10):  # Try up to 10 times
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                new_x = self.position[0] + dx
                new_y = self.position[1] + dy
                # Check boundaries
                if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
                    # Check if walkable
                    if self.grid.is_walkable(int(new_x), int(new_y)):
                        self.position[0] = new_x
                        self.position[1] = new_y
                        break  # Exit the loop if moved
            self.move_timer = random.uniform(1, 3)  # Next move in 1-3 seconds
            # Contaminate nearby racks
            for rack in racks:
                if self.grid.is_in_proximity(self.position, (rack.grid_x, rack.grid_y), proximity=1):
                    if rack.protected_time <= 0:
                        rack.contaminated = True

    def draw(self, screen):
        iso_x, iso_y = self.grid.to_isometric(self.position[0], self.position[1])
        screen.blit(self.image, (iso_x - 10, iso_y - 10))