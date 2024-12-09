import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GREEN = (53, 101, 77)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 255, 0) 
YELLOW = (255, 215, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load Dice Images
dice_images = [pygame.image.load(f"images/dice_{i}.png") for i in range(1, 7)]
dice_images = [pygame.transform.scale(img, (100, 100)) for img in dice_images]

# Load fonts
title_font = pygame.font.SysFont("Comic Sans MS", 60) 
font = pygame.font.SysFont("Comic Sans MS", 36)      

# Function to roll dice
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

# Dice rolling animation
def roll_dice_animation():
    clock = pygame.time.Clock()
    rolling_time = 1.5  # Roll for 1.5 seconds
    start_time = time.time()

    dice1_value, dice2_value, dice3_value = 1, 1, 1  # Initial dice values

    while time.time() - start_time < rolling_time:
        # Generate random dice faces for animation
        dice1_value = random.randint(1, 6)
        dice2_value = random.randint(1, 6)
        dice3_value = random.randint(1, 6)

        # Clear screen with background color
        screen.fill(GREEN)

        # Display dice in triangular layout
        screen.blit(dice_images[dice1_value - 1], (WIDTH // 2 - 125, 200))  # Top-left dice
        screen.blit(dice_images[dice2_value - 1], (WIDTH // 2 + 25, 200))   # Top-right dice
        screen.blit(dice_images[dice3_value - 1], (WIDTH // 2 - 50, 350))   # Bottom-center dice

        # Update display
        pygame.display.flip()
        clock.tick(15)  

    # Final dice results
    return [dice1_value, dice2_value, dice3_value]


# Function to display text
def display_text(text, x, y, font, color=WHITE):
    render_text = font.render(text, True, color)
    text_rect = render_text.get_rect(center=(x, y))  
    screen.blit(render_text, text_rect)


# Function to check dice roll
def check_roll(dice):
    dice_counts = {i: dice.count(i) for i in dice}
    pairs = [num for num, count in dice_counts.items() if count == 2]

    if len(pairs) == 1:
        return [num for num in dice if num != pairs[0]][0]
    elif sorted(dice) == [4, 5, 6]:
        return "auto_win"
    elif sorted(dice) == [1, 2, 3]:
        return "auto_loss"
    return None


# Display results
def display_dice_results(player_dice, dealer_dice):
    # Clear screen with background color
    screen.fill(GREEN)

    # Define the layout constants
    section_width = WIDTH // 2 
    top_dice_spacing = 75  
    bottom_dice_y = 350  
    dice_size = dice_images[0].get_width()  

    # Player Side
    player_x_center = section_width // 2
    display_text("Player", player_x_center, 100, font)
    # Dice positions
    screen.blit(dice_images[player_dice[0] - 1], (player_x_center - dice_size - (top_dice_spacing // 2), 200))
    screen.blit(dice_images[player_dice[1] - 1], (player_x_center + (top_dice_spacing // 2), 200))
    screen.blit(dice_images[player_dice[2] - 1], (player_x_center - dice_size // 2, bottom_dice_y))

    # Dealer Side
    dealer_x_center = 3 * section_width // 2
    display_text("Dealer", dealer_x_center, 100, font)
    # Dice positions
    screen.blit(dice_images[dealer_dice[0] - 1], (dealer_x_center - dice_size - (top_dice_spacing // 2), 200))
    screen.blit(dice_images[dealer_dice[1] - 1], (dealer_x_center + (top_dice_spacing // 2), 200))
    screen.blit(dice_images[dealer_dice[2] - 1], (dealer_x_center - dice_size // 2, bottom_dice_y))


def dealer_ai():
    while True:
        dealer_dice = roll_dice()  # Roll three dice
        result = check_roll(dealer_dice)
        if result is not None:  # Only return valid results
            return dealer_dice, result


def diceMain():
    running = True
    game_started = False
    winner_shown = False
    player_result = None
    dealer_result = None

    def roll_dice_action():
        nonlocal game_started, player_result, dealer_result, winner_shown
        game_started = True

        # Player rolls dice
        player_dice = roll_dice_animation()
        player_result = check_roll(player_dice)

        # Dealer AI rolls dice
        dealer_dice, dealer_result = dealer_ai()

        # Display the results
        display_dice_results(player_dice, dealer_dice)

        # Determine winner and display results
        if player_result == "auto_win" or dealer_result == "auto_loss":
            display_text("Player Wins!", WIDTH // 2, 500, font)
        elif dealer_result == "auto_win" or player_result == "auto_loss":
            display_text("Dealer Wins!", WIDTH // 2, 500, font)
        elif isinstance(player_result, int) and isinstance(dealer_result, int):
            if player_result > dealer_result:
                display_text("Player Wins!", WIDTH // 2, 500, font)
            elif dealer_result > player_result:
                display_text("Dealer Wins!", WIDTH // 2, 500, font)
            else:
                display_text("It's a draw!", WIDTH // 2, 500, font)

        winner_shown = True
        pygame.display.update()
        time.sleep(3)

    def return_to_menu():
        nonlocal running
        running = False

    while running:
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for SPACE bar press to roll dice
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game_started or winner_shown:
                    roll_dice_action()

        if not game_started:
            # Display title
            display_text("Dice Game", WIDTH // 2, 50, title_font)
            display_text("Press SPACE to Roll Dice", WIDTH // 2, 150, font)

            # Display dice layout
            for i, img in enumerate(dice_images[:3]):
                if i < 2:
                    screen.blit(img, (WIDTH // 2 - 125 + i * 150, 200))  # Top row
                else:
                    screen.blit(img, (WIDTH // 2 - 50, 350))  # Bottom row
        elif winner_shown:
            display_text("Press SPACE to Play Again", WIDTH // 2, 150, font)

        # Add MENU button
        menu_button = pygame.Rect(WIDTH // 2 - 75, 500, 150, 75)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = menu_button.collidepoint(mouse_x, mouse_y)
        current_color = GOLD if is_hovered else YELLOW
        pygame.draw.rect(screen, current_color, menu_button, border_radius=15)
        menu_text = font.render("Menu", True, BLACK)
        screen.blit(
            menu_text,
            (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2)
        )

        if pygame.mouse.get_pressed()[0] and is_hovered:
            return_to_menu()

        pygame.display.flip()


if __name__ == "__main__":
    diceMain()
