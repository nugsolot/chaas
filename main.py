# main.py

import pygame
from player import Player
from rack import Rack
from chaas import CHaaS
from grid import Grid

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Data Center Defense')

# Clock to control the game's frame rate
clock = pygame.time.Clock()

# Create game objects
grid = Grid(7, 7, 40, SCREEN_WIDTH, SCREEN_HEIGHT)  # Grid size is 7x7
racks = grid.create_racks()
player = Player(grid)
chaas = CHaaS(grid)

# Initialize fonts
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
hud_font = pygame.font.SysFont('Arial', 18)

# Game state variables
running = True
win_timer = None  # Timer for win condition
WIN_DURATION = 60  # Time in seconds to hold all racks configured

# Message variables
message = ""
message_timer = 0

def display_in_game_message(text, duration=2):
    global message, message_timer
    message = text
    message_timer = duration  # Duration in seconds

def display_end_message(text):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing

# Main game loop
while running:
    delta_time = clock.tick(60) / 1000.0  # Time since last frame in seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player interaction
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.interact(racks)

        # Mouse interaction
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                clicked_rack = None
                for rack in racks:
                    if rack.rect and rack.rect.collidepoint(mouse_pos):
                        clicked_rack = rack
                        break
                if clicked_rack:
                    # Check if player is close enough to interact
                    if grid.is_in_proximity(player.position, (clicked_rack.grid_x, clicked_rack.grid_y), proximity=1.0):
                        clicked_rack.interact()
                    else:
                        display_in_game_message("You are too far from the rack to interact.", duration=2)

    # Update game state
    keys = pygame.key.get_pressed()
    player.update(keys, delta_time)
    chaas.update(delta_time, racks)

    # Update racks
    for rack in racks:
        rack.update(delta_time)

    # Calculate rack status counts
    total_racks = len(racks)
    level_0_racks = sum(1 for rack in racks if rack.level == 0 and not rack.contaminated)
    level_1_racks = sum(1 for rack in racks if rack.level == 1 and not rack.contaminated)
    level_2_racks = sum(1 for rack in racks if rack.level == 2 and not rack.contaminated)
    contaminated_racks = sum(1 for rack in racks if rack.contaminated)
    protected_racks = sum(1 for rack in racks if rack.protected_time > 0 and not rack.contaminated)

    # Check win condition
    if all(rack.level == 2 and not rack.contaminated for rack in racks):
        if win_timer is None:
            win_timer = WIN_DURATION  # Start the win timer
        else:
            win_timer -= delta_time
            if win_timer <= 0:
                display_end_message("You have successfully configured all racks! You win!")
                running = False
    else:
        win_timer = None  # Reset win timer if any rack is not fully configured

    # Check loss condition
    if all(rack.contaminated for rack in racks):
        display_end_message("All racks have been contaminated! You lose.")
        running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw everything
    grid.draw(screen)
    for rack in racks:
        rack.draw(screen)
    player.draw(screen)
    chaas.draw(screen)

    # Draw HUD background
    hud_background = pygame.Surface((250, 160))  # Adjust size as needed
    hud_background.set_alpha(128)  # Set transparency
    hud_background.fill((0, 0, 0))  # Black background
    screen.blit(hud_background, (5, 5))

    # Define colors for each rack status
    colors = {
        'level_0': (100, 100, 100),         # Gray for Empty
        'level_1': (0, 0, 255),             # Blue for ToR Installed
        'level_2': (0, 255, 0),             # Green for Configured
        'contaminated': (255, 0, 0),        # Red for Contaminated
        'protected': (255, 255, 0),         # Yellow for Protected (matching the outline color)
    }

    # Adjusted HUD lines
    hud_lines = [
        ('Total Racks: {}'.format(total_racks), None),
        ('Level 0 (Empty): {}'.format(level_0_racks), colors['level_0']),
        ('Level 1 (ToR Installed): {}'.format(level_1_racks), colors['level_1']),
        ('Level 2 (Configured): {}'.format(level_2_racks), colors['level_2']),
        ('Contaminated Racks: {}'.format(contaminated_racks), colors['contaminated']),
        ('Protected Racks: {}'.format(protected_racks), colors['protected']),
    ]

    # Draw the HUD
    for i, (line, color) in enumerate(hud_lines):
        y_position = 10 + i * 20
        if color:
            # Draw color swatch
            pygame.draw.rect(screen, color, (10, y_position, 15, 15))
            # Render text
            text_surface = hud_font.render(line, True, (255, 255, 255))  # White text
            screen.blit(text_surface, (30, y_position))
        else:
            # No color swatch for 'Total Racks'
            text_surface = hud_font.render(line, True, (255, 255, 255))  # White text
            screen.blit(text_surface, (10, y_position))

    # Display win timer if active
    if win_timer is not None:
        win_timer_text = f"Time to Win: {int(win_timer)}s"
        text_surface = hud_font.render(win_timer_text, True, (255, 255, 0))
        screen.blit(text_surface, (10, 10 + len(hud_lines) * 20))

    # Display in-game message if active
    if message_timer > 0:
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(text_surface, text_rect)
        message_timer -= delta_time
        if message_timer <= 0:
            message = ""

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()