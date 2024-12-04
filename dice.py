import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Load Dice Images
dice_images = [pygame.image.load(f"dice_sides/dice_{i}.png") for i in range(1, 7)]
# Resize Dice Images
dice_images = [pygame.transform.scale(img, (100, 100)) for img in dice_images]

# Initialize Pygame's mixer
pygame.mixer.init()

# Load sound effects
dice_roll_sound = pygame.mixer.Sound("dice_roll.mp3")  # Dice rolling sound
win_sound = pygame.mixer.Sound("win_sound.mp3")        # Winning sound
lose_sound = pygame.mixer.Sound("lose_sound.mp3")      # Losing sound
win_sound.set_volume(1.0)
lose_sound.set_volume(1.0)


# Set up display
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Street Dice Game")

# Load background image
background_image = pygame.image.load('dice_game_background.jpeg')  # Make sure this file exists
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load font
font = pygame.font.Font(None, 36)

# Function to roll dice
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

def roll_dice_animation():
    clock = pygame.time.Clock()
    rolling_time = 1.5  # Animation duration in seconds
    start_time = time.time()
    
    dice_roll_sound.play()

    dice1_value, dice2_value, dice3_value = 1, 1, 1  # Initial values
    
    while time.time() - start_time < rolling_time:
        # Random dice faces
        dice1_value = random.randint(1, 6)
        dice2_value = random.randint(1, 6)
        dice3_value = random.randint(1, 6)
        
        # Draw Background
        screen.blit(background_image, (0, 0))
        
        # Draw Dice Images
        screen.blit(dice_images[dice1_value - 1], (150, 150))  # Player dice 1
        screen.blit(dice_images[dice2_value - 1], (300, 150))  # Player dice 2
        screen.blit(dice_images[dice3_value - 1], (450, 150))  # Player dice 3
        
        # Update Display
        pygame.display.flip()
        
        # Control Frame Rate
        clock.tick(30)
    
     # Final Dice Results (Displayed for 2 seconds)
    screen.blit(background_image, (0, 0))  # Clear background
    screen.blit(dice_images[dice1_value - 1], (150, 150))
    screen.blit(dice_images[dice2_value - 1], (300, 150))
    screen.blit(dice_images[dice3_value - 1], (450, 150))
    pygame.display.flip()  # Update display to show the final dice
    time.sleep(1)  # Pause to show final dice for 2 seconds
    
    # Final Result
    return [dice1_value, dice2_value, dice3_value]

# Function to display text
def display_text(text, x, y):
    render_text = font.render(text, True, BLACK)
    screen.blit(render_text, (x, y))

# Checking dice roll
def check_roll(dice):
    """Check the result of a dice roll."""
    dice_counts = {i: dice.count(i) for i in dice}
    pairs = [num for num, count in dice_counts.items() if count == 2]
    
    if len(pairs) == 1:
        # Return the odd die out as the score
        return [num for num in dice if num != pairs[0]][0]
    elif sorted(dice) == [4, 5, 6]:
        return "auto_win"
    elif sorted(dice) == [1, 2, 3]:
        return "auto_loss"
    else:
        return None

# Function to display roll result
def display_roll(player, dice, result, x, y):
    dice_str = f"{player} rolls = [ {dice[0]} , {dice[1]} , {dice[2]} ] : {result}"
    display_text(dice_str, x, y)

# Function to re-roll until a valid result
def roll_until_valid(player, y_position):
    while True:
        dice = roll_dice_animation()  # Use the animation here
        result = check_roll(dice)
        
        if result is not None:
            # Display final roll
            screen.blit(background_image, (0, 0))
            for i, value in enumerate(dice):
                screen.blit(dice_images[value - 1], (100 + i * 150, y_position))
            pygame.display.flip()
            time.sleep(2)  # Pause before returning
            return dice, result

# Function to create a button
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()  # Get mouse position
    click = pygame.mouse.get_pressed()  # Check for mouse click
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:  # If mouse is over button
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:  # If left mouse button is clicked
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    # Display button text
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width // 4), y + (height // 4)))

# Main game loop
def game_loop():
    running = True
    game_started = False
    first_round = True  # Track if it’s the first round or not
    player_result = None
    dealer_result = None
    winner_shown = False
    game_reset = False
    
    def roll_dice_action():
        nonlocal game_started, player_result, dealer_result, winner_shown, game_reset, first_round
        if not game_started:
            # Start the game
            player_result = None
            dealer_result = None
            winner_shown = False
            game_started = True

            # Player rolls until valid result
            player_dice, player_result = roll_until_valid("Player", 150)
            screen.blit(background_image, (0, 0))  # Redraw the background
            display_roll("Player", player_dice, player_result, 100, 150)  # Display player's roll
            pygame.display.update()
            time.sleep(2)  # Pause before dealer rolls

            # Dealer rolls until valid result
            dealer_dice, dealer_result = roll_until_valid("Dealer", 200)
            screen.blit(background_image, (0, 0))  # Redraw the background
            display_roll("Player", player_dice, player_result, 100, 150)  # Redraw player's roll
            display_roll("Dealer", dealer_dice, dealer_result, 100, 200)  # Display dealer's roll

            # Determine the winner after both rolls
            if player_result == "auto_win" or dealer_result == "auto_loss":
                win_sound.play()
                display_text("Player Wins!", 100, 250)
            elif dealer_result == "auto_win" or player_result == "auto_loss":
                lose_sound.play()
                display_text("Dealer Wins!", 100, 250)
            elif isinstance(player_result, int) and isinstance(dealer_result, int):
                # Only compare if both results are valid numbers
                if player_result > dealer_result:
                    win_sound.play()
                    display_text("Player Wins!", 100, 250)
                elif dealer_result > player_result:
                    lose_sound.play()
                    display_text("Dealer Wins!", 100, 250)
                else:
                    display_text("It's a draw!", 100, 250)
            
            pygame.display.update()
            winner_shown = True
            game_reset = True
            time.sleep(3)
            first_round = False  # Set to False after the first round

    while running:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Show the welcome message and rules if it’s the first round and game hasn't started
        if not game_started:
            screen.blit(background_image, (0, 0))  # Draw the background image
            if first_round:
                # Show welcome message and rules on the first round
                display_text("Welcome to the Street Dice Game!", 100, 50)
                display_text("Click the button to Roll Dice", 100, 280)
                display_text("Rules:", 100, 110)
                display_text("- Roll 3 dice. Odd die out is your score.", 100, 140)
                display_text("- [4, 5, 6] = automatic win.", 100, 170)
                display_text("- [1, 2, 3] = automatic loss.", 100, 200)
                display_text("- Highest score wins!", 100, 230)
            else:
                # Show "Click the button to roll again" after the first round
                display_text("Click the button to roll again", 100, 100)
            # Draw the button for rolling dice
            draw_button("Roll Dice", 250, 320, 200, 50, GREEN, RED, roll_dice_action)
        else:
            screen.blit(background_image, (0, 0))  # Draw the background image

            # After the game has started, handle the dice rolls and results
            if winner_shown and game_reset:
                # Reset the game and allow for a new round
                game_started = False
                game_reset = False

        pygame.display.update()  # Update the display after everything has been drawn

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()
