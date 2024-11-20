# dice_rolling.py

import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BACKGROUND_COLOR = (50, 150, 200)
DICE_SIZE = 100
FPS = 30

# Load Dice Images
dice_images = [pygame.image.load(f"dice_sides/dice_{i}.png") for i in range(1, 7)]

# Resize Dice Images
dice_images = [pygame.transform.scale(img, (DICE_SIZE, DICE_SIZE)) for img in dice_images]

# Create Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rolling Dice Animation")

# Dice Rolling Function
def roll_dice():
    clock = pygame.time.Clock()
    rolling_time = 1.5  # Animation duration in seconds
    start_time = time.time()
    
    dice1_value, dice2_value = 1, 1  # Initial values
    
    while time.time() - start_time < rolling_time:
        # Random dice faces
        dice1_value = random.randint(1, 6)
        dice2_value = random.randint(1, 6)
        dice3_value = random.randint(1, 6)

        
        # Draw Background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw Dice
        screen.blit(dice_images[dice1_value - 1], (WIDTH // 4 - DICE_SIZE // 2, HEIGHT // 2 - DICE_SIZE // 2))
        screen.blit(dice_images[dice2_value - 1], (3 * WIDTH // 4 - DICE_SIZE // 2, HEIGHT // 2 - DICE_SIZE // 2))
        screen.blit(dice_images[dice3_value - 1], ( 1.5 * WIDTH // 4 - DICE_SIZE // 2, HEIGHT - DICE_SIZE // 2))

        
        # Update Display
        pygame.display.flip()
        
        # Control Frame Rate
        clock.tick(FPS)
    
    # Final Result
    return dice1_value, dice2_value, dice3_value

# Main Game Loop
def main():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to roll dice
                    dice1, dice2, dice3 = roll_dice()
                    print(f"Dice Results: {dice1}, {dice2}, {dice3}")
        
        # Draw Instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to roll the dice. Press ESC to exit.", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))
        
        # Update Display
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
