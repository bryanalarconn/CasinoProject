import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette Game with Spinning Wheel and Marble")

# Colors
GREEN_BG = (53, 101, 77)  # Background color
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Color for 0
GOLD = (255, 215, 0)
BUTTON_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (255, 255, 0)  # Lighter color for hover effect
BUTTON_COLOR = (255, 215, 0)
# Fonts (Comic Sans)
font = pygame.font.SysFont("Comic Sans MS", 24)
large_font = pygame.font.SysFont("Comic Sans MS", 36)
wheel_font = pygame.font.SysFont("Comic Sans MS", 18)  # Smaller font for wheel text


# Roulette Slots and Colors
SLOTS = [str(i) for i in range(37)]
SLOTCOLORS = ["Green"] + ["Red" if i % 2 == 0 else "Black" for i in range(1, 37)]

# Constants for the wheel
CENTER = (WIDTH // 4, HEIGHT // 2 + 50)  # Adjusted center for bigger wheel
RADIUS = 150  # Bigger radius for the wheel
SLICE_ANGLE = 360 / len(SLOTS)

# Betting Buttons
def create_buttons():
    buttons = []
    button_width = WIDTH // 13  # Button width for grid
    button_height = HEIGHT // 12  # Button height for grid
    margin = 5

    # Add the "0" button
    buttons.append({
        "rect": pygame.Rect(margin, 25 + margin, button_width - margin,  button_height * 3 - margin),
        "number": "0",
        "color": GREEN
    })

    # Add buttons for 1 to 36
    for col in range(12):
        for row in range(3):
            number = col * 3 + row + 1
            if number > 36:
                break
            rect = pygame.Rect(
                button_width + col * button_width + margin,  # X position
                25 + margin + row * button_height,  # Y position shifted down by 50
                button_width - margin,  # Width
                button_height - margin  # Height
            )
            buttons.append({
                "rect": rect,
                "number": str(number),
                "color": RED if int(number) % 2 == 0 else BLACK
            })
    return buttons

# Draw betting buttons
def draw_buttons(surface, buttons):
    for button in buttons:
        pygame.draw.rect(surface, button["color"], button["rect"])  # Fill color
        pygame.draw.rect(surface, BLACK, button["rect"], 2)  # Outline
        text = font.render(button["number"], True, WHITE)
        surface.blit(
            text,
            (button["rect"].centerx - text.get_width() // 2, button["rect"].centery - text.get_height() // 2)
        )

def draw_round_rect(surface, rect, color, border_radius=15):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

def draw_wheel(surface, center, radius, angle):
    pygame.draw.circle(surface, GOLD, center, radius + 10)  # Gold border slightly larger than the wheel

    for i, slot in enumerate(SLOTS):
        start_angle = math.radians(i * SLICE_ANGLE + angle)
        end_angle = math.radians((i + 1) * SLICE_ANGLE + angle)
        color = GREEN if slot == "0" else RED if int(slot) % 2 == 0 else BLACK

        # Draw slice
        points = [
            center,
            (center[0] + radius * math.cos(start_angle), center[1] + radius * math.sin(start_angle)),
            (center[0] + radius * math.cos(end_angle), center[1] + radius * math.sin(end_angle)),
        ]
        pygame.draw.polygon(surface, color, points)

        # Draw number with smaller text size
        text_angle = math.radians(i * SLICE_ANGLE + angle + SLICE_ANGLE / 2)
        text_x = center[0] + (radius - 30) * math.cos(text_angle)
        text_y = center[1] + (radius - 30) * math.sin(text_angle)
        text = wheel_font.render(slot, True, WHITE)  # Use smaller wheel font
        surface.blit(text, (text_x - text.get_width() // 2, text_y - text.get_height() // 2))


# Draw the marble
def draw_marble(surface, center, radius, angle):
    marble_x = center[0] + (radius - 15) * math.cos(math.radians(angle))
    marble_y = center[1] + (radius - 15) * math.sin(math.radians(angle))
    pygame.draw.circle(surface, WHITE, (int(marble_x), int(marble_y)), 10)

# Draw spin result
def draw_result(surface, number, color, win):
    result_text = f"Result: {number} ({color})"
    result_color = GREEN if win else RED
    text = large_font.render(result_text, True, result_color)
    surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

# Spin simulation with wheel and marble animation
def spin_wheel():
    wheel_angle = 0
    marble_angle = random.uniform(0, 360)  # Random starting position for marble
    speed = random.uniform(15, 20)  # Random initial speed
    marble_speed = -random.uniform(20, 25)  # Faster counter-spin for marble
    friction = 0.1  # Friction to slow down the wheel and marble

    while speed > 0.1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        wheel_angle += speed
        marble_angle += marble_speed
        speed -= friction
        marble_speed += friction if marble_speed < 0 else -friction

        screen.fill(GREEN_BG)  # Background
        draw_wheel(screen, CENTER, RADIUS, wheel_angle)
        draw_marble(screen, CENTER, RADIUS, marble_angle)
        draw_buttons(screen, buttons)
        pygame.draw.rect(screen, BUTTON_COLOR, spin_button)
        pygame.draw.rect(screen, BLACK, spin_button, 2)
        spin_text = font.render("SPIN", True, WHITE)
        screen.blit(
            spin_text,
            (spin_button.centerx - spin_text.get_width() // 2, spin_button.centery - spin_text.get_height() // 2)
        )

        pygame.display.flip()
        pygame.time.delay(30)

    # Determine result
    final_angle = (marble_angle - wheel_angle) % 360
    landed_index = int(final_angle // SLICE_ANGLE)
    result = SLOTS[landed_index], SLOTCOLORS[landed_index]

    # Show the final frame and pause
    pygame.display.flip()  # Ensure the final frame is shown
    pygame.time.wait(3000)  # Pause for 3 seconds (3000 milliseconds)

    return result

def draw_user_bet(surface, user_guess):
    if user_guess:
        bet_text = f"You bet on: {user_guess[0]} ({user_guess[1]})"
        text = large_font.render(bet_text, True, WHITE)  # Use large_font for bigger text
        surface.blit(text, (3 * WIDTH // 4 - text.get_width() // 2, 300))  # Right side, below the betting table



def draw_result(surface, number, color, win):
    # Display the spin result
    result_text = f"Result: {number} ({color})"
    result_color = WHITE
    text = large_font.render(result_text, True, result_color)
    surface.blit(text, (3 * WIDTH // 4 - text.get_width() // 2, 350))  # Right side, below the user's bet message

    # Display win or loss message
    if win:
        outcome_text = "You WIN!"
        outcome_color = GREEN
    else:
        outcome_text = "You LOSE!"
        outcome_color = RED

    outcome = large_font.render(outcome_text, True, outcome_color)
    surface.blit(outcome, (3 * WIDTH // 4 - outcome.get_width() // 2, 400))  # Below the result message


# Main game loop
def rouletteMain():
    global buttons, spin_button
    running = True
    buttons = create_buttons()
    user_guess = None
    spin_result = None
    win = False

    # Spin button
    spin_button = pygame.Rect(WIDTH // 4 - 150, HEIGHT - 80, 300, 50)

    # Return to Menu button
    menu_button = pygame.Rect(WIDTH // 2 + 150, HEIGHT - 80, 150, 50)

    while running:
        # Get mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check betting buttons
                for button in buttons:
                    if button["rect"].collidepoint(pos):
                        user_guess = (button["number"], SLOTCOLORS[int(button["number"])])
                        spin_result = None  # Reset the spin result when a new bet is placed

                # Check spin button
                if spin_button.collidepoint(pos) and user_guess:
                    marble_num, marble_color = spin_wheel()  # Spin the wheel
                    spin_result = (marble_num, marble_color)
                    win = user_guess == spin_result  # Check if the user wins

                # Check Return to Menu button
                if menu_button.collidepoint(pos):
                    running = False
                    return  # Exit roulette and return to the menu

        # Fill the background
        screen.fill(GREEN_BG)

        # Draw betting buttons
        draw_buttons(screen, buttons)

        # Draw user's bet
        draw_user_bet(screen, user_guess)

        # Draw the wheel
        draw_wheel(screen, CENTER, RADIUS, 0)

        # Draw round Spin button with hover effect
        spin_color = HIGHLIGHT_COLOR if spin_button.collidepoint(mouse_pos) else BUTTON_COLOR
        draw_round_rect(screen, spin_button, spin_color)
        spin_text = font.render("SPIN", True, BLACK)
        screen.blit(
            spin_text,
            (spin_button.centerx - spin_text.get_width() // 2, spin_button.centery - spin_text.get_height() // 2)
        )

        # Draw round Menu button with hover effect
        menu_color = HIGHLIGHT_COLOR if menu_button.collidepoint(mouse_pos) else BUTTON_COLOR
        draw_round_rect(screen, menu_button, menu_color)
        menu_text = font.render("MENU", True, BLACK)
        screen.blit(
            menu_text,
            (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2)
        )

        # Draw result if available
        if spin_result:
            draw_result(screen, spin_result[0], spin_result[1], win)

        # Update display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    rouletteMain()



