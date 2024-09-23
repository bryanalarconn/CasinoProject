import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Street Dice Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load font
font = pygame.font.Font(None, 36)

# Function to roll dice
def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

# Function to display text
def display_text(text, x, y):
    render_text = font.render(text, True, BLACK)
    screen.blit(render_text, (x, y))
    pygame.display.update()

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
    
# Main game loop
def game_loop():
    running = True
    game_started = False
    player_result = None
    dealer_result = None
    winner_shown = False
    game_reset = False
    welcome_screen_shown = False 

    while running:
        # Fill the background with white
        screen.fill(WHITE)

        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game_started and not game_reset:
                    # Start the game
                    player_result = None
                    dealer_result = None
                    winner_shown = False
                    game_started = True
                    welcome_screen_shown = False
                    
                    # Player rolls first
                    player_dice = roll_dice()
                    player_result = check_roll(player_dice)
                    display_roll("Player", player_dice, player_result, 100, 150)  # Display full dice roll and result
                    pygame.display.update()
                    time.sleep(2)  # Wait for 2 seconds before showing dealer's roll
                    
                   # Dealer rolls
                    dealer_dice = roll_dice()
                    dealer_result = check_roll(dealer_dice)
                    display_roll("Dealer", dealer_dice, dealer_result, 100, 200)  # Display full dice roll and result
                    pygame.display.update()
                    time.sleep(1)  # Wait for 1 second before showing the result

                    # If both player and dealer roll None, prompt for a new game
                    if player_result is None and dealer_result is None:
                        display_text("No valid rolls.", 100, 250)
                        time.sleep(2)
                        
                    # Case: Player rolls valid result but dealer rolls None
                    elif player_result is not None and dealer_result is None:
                        display_text("Roll again. Dealer got no valid roll.", 100, 250)
                        time.sleep(2)

                    # Case: Dealer rolls valid result but player rolls None
                    elif dealer_result is not None and player_result is None:
                        display_text("Roll again. You got no valid roll.", 100, 250)
                        time.sleep(2)

                    else:
                        # Determine the winner
                        if player_result == "auto_win" or dealer_result == "auto_loss":
                            display_text("Player Wins!", 100, 250)
                            time.sleep(2)
                        elif dealer_result == "auto_win" or player_result == "auto_loss":
                            display_text("Dealer Wins!", 100, 250)
                            time.sleep(2)
                        elif isinstance(player_result, int) and isinstance(dealer_result, int):
                            # Only compare if both results are valid numbers
                            if player_result > dealer_result:
                                display_text("Player Wins!", 100, 250)
                                time.sleep(2)
                            elif dealer_result > player_result:
                                display_text("Dealer Wins!", 100, 250)
                                time.sleep(2)
                            else:
                                display_text("It's a draw!", 100, 250)
                                time.sleep(2)
                    pygame.display.update()
                    winner_shown = True
                    game_reset = True
                    
                # Reset the game when the player presses space after the result is shown
                elif game_reset:
                    game_reset = False
                    game_started = False

        # Show the welcome message or reset prompt if the game hasn't started or has ended
        if not game_started and not game_reset and not welcome_screen_shown:
            display_text("Welcome to the Street Dice Game!", 100, 50)
            display_text("Press Space to Roll Dice", 100, 280)
            # Display game rules
            display_text("Rules:", 100, 110)
            display_text("- Roll 3 dice. Odd die out is your score.", 100, 140)
            display_text("- [4, 5, 6] = automatic win.", 100, 170)
            display_text("- [1, 2, 3] = automatic loss.", 100, 200)
            display_text("- Highest score wins!", 100, 230)
            pygame.display.update()  # Update the display only once
            welcome_screen_shown = True  # Ensure the welcome screen is only displayed once
        elif winner_shown:
            display_text("Press Space to roll again.", 100, 200)
            pygame.display.update()  # Update the display after showing the reset prompt

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()
