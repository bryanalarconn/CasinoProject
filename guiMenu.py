import pygame
import subprocess

# Initialize Pygame
pygame.init()

# Load the casino background image
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cal State Casino")

# Load and scale the background image
background_image = pygame.image.load('casino_background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set up fonts
title_font = pygame.font.SysFont('comicsansms', 80)  # Larger font for the title
font = pygame.font.SysFont('comicsansms', 50)        # Smaller font for buttons

# Define button properties
button_color = (255, 215, 0)  # Gold-like button color
hover_color = (255, 255, 0)   # Lighter gold when hovering
text_color = (0, 0, 0)        # Black text
button_width, button_height = 400, 75    # Button dimensions
border_radius = 20                      # Round corners for buttons

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

# Function to draw buttons with rounded corners
def draw_button(text, x, y, width, height, hovered, border_radius):
    color = hover_color if hovered else button_color
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=border_radius)
    draw_text(text, font, text_color, x + (width - font.size(text)[0]) // 2, y + (height - font.size(text)[1]) // 2)

# Function to run external game files
def run_game(file_name):
    try:
        subprocess.run(['python', file_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_name}: {e}")

# Main game loop
def main_menu():
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw background

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
                            run_game('roulette.py')
                        elif text == "Play Blackjack":
                            run_game('BJGUI.py')
                        elif text == "Play Dice":
                            run_game('dice.py')
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
