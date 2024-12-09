import pygame
import subprocess
from blackjack import blackjackMain
from roulette import rouletteMain
from dice import diceMain

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cal State Casino")

# Define green background color
GREEN_BG = (53, 101, 77)

# Set up fonts
title_font = pygame.font.SysFont('comicsansms', 80)
font = pygame.font.SysFont('comicsansms', 50)      

# Define button properties
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
button_width, button_height = 400, 75 
border_radius = 20                   

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

# Function to draw buttons
def draw_button(text, x, y, width, height, hovered, border_radius):
    color = GOLD if hovered else YELLOW
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=border_radius)
    draw_text(text, font, BLACK, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2)

# Main game loop
def main_menu():
    running = True
    while running:
        # Fill the background with green
        screen.fill(GREEN_BG)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Button positions and sizes (center the buttons horizontally)
        button_positions = [
            ((WIDTH - button_width) // 2, 200, "Play Roulette"),
            ((WIDTH - button_width) // 2, 300, "Play Blackjack"),
            ((WIDTH - button_width) // 2, 400, "Play Dice"),
            ((WIDTH - button_width) // 2, 500, "Exit")
        ]

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button is clicked
                for (x, y, text) in button_positions:
                    if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                        if text == "Play Roulette":
                            rouletteMain()
                        elif text == "Play Blackjack":
                            blackjackMain()
                        elif text == "Play Dice":
                            diceMain()
                        elif text == "Exit":
                            running = False
                            pygame.quit()
                            return

        # Draw title at the top of the screen
        draw_text("Cal State Casino", title_font, (255, 255, 255), (WIDTH - title_font.size("Cal State Casino")[0]) // 2, 50)

        # Draw buttons with rounded corners
        for (x, y, text) in button_positions:
            hovered = x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height
            draw_button(text, x, y, button_width, button_height, hovered, border_radius)

        # Update display
        pygame.display.flip()

# Main function to start the menu
if __name__ == "__main__":
    main_menu()
