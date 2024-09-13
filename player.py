# player.py

import pygame

class Player:
    def __init__(self, grid):
        self.grid = grid
        # Start position is a walkable tile
        self.position = [0, 0]  # Starting at (0, 0)
        self.speed = 5
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 165, 0))  # Orange color for the player


    def update(self, keys, delta_time):
        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -self.speed * delta_time
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = self.speed * delta_time
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -self.speed * delta_time
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = self.speed * delta_time

        # Calculate new position
        new_x = self.position[0] + move_x
        new_y = self.position[1] + move_y

        # Check boundaries
        new_x = max(0, min(new_x, self.grid.width - 1))
        new_y = max(0, min(new_y, self.grid.height - 1))

        # Check if the new position is walkable
        if self.grid.is_walkable(int(new_x + 0.5), int(new_y + 0.5)):
            self.position[0] = new_x
            self.position[1] = new_y
        else:
            # If not walkable, don't move
            pass

    def interact(self, racks):
        for rack in racks:
            if self.grid.is_in_proximity(self.position, (rack.grid_x, rack.grid_y), proximity=1.0):
                rack.interact()

    def draw(self, screen):
        iso_x, iso_y = self.grid.to_isometric(self.position[0], self.position[1])
        points = [
            (iso_x, iso_y - 10),  # Top point
            (iso_x - 10, iso_y + 10),  # Bottom left
            (iso_x + 10, iso_y + 10)  # Bottom right
        ]
        pygame.draw.polygon(screen, (255, 165, 0), points)