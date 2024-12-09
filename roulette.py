import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
GREEN_BG = (53, 101, 77)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)

# Fonts (Comic Sans)
font = pygame.font.SysFont("Comic Sans MS", 24)
large_font = pygame.font.SysFont("Comic Sans MS", 36)
wheel_font = pygame.font.SysFont("Comic Sans MS", 18)

# Roulette Slots and Colors
SLOTS = [str(i) for i in range(37)]
SLOTCOLORS = ["Green"] + ["Red" if i % 2 == 0 else "Black" for i in range(1, 37)]

# Constants for the wheel
CENTER = (WIDTH // 4, HEIGHT // 2 + 50) 
RADIUS = 150  
SLICE_ANGLE = 360 / len(SLOTS)

# Betting Buttons
def create_buttons():
    buttons = []
    button_width = WIDTH // 13  
    button_height = HEIGHT // 12  
    margin = 5

    # Add 0 button
    buttons.append({
        "rect": pygame.Rect(margin, 25 + margin, button_width - margin, button_height * 3 - margin),
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
                button_width + col * button_width + margin,
                25 + margin + row * button_height, 
                button_width - margin,  
                button_height - margin  
            )
            buttons.append({
                "rect": rect,
                "number": str(number),
                "color": RED if int(number) % 2 == 0 else BLACK
            })
    return buttons

# Draw betting buttons with selected marker
def draw_buttons(surface, buttons, selected_button):
    for button in buttons:
        pygame.draw.rect(surface, button["color"], button["rect"], border_radius = 15)  # Rounded corners

        # Draw the number text
        text = font.render(button["number"], True, WHITE)
        surface.blit(
            text,
            (button["rect"].centerx - text.get_width() // 2, button["rect"].centery - text.get_height() // 2)
        )

        # Draw a marker if this button is selected
        if selected_button == button["number"]:
            marker_rect = button["rect"].inflate(-10, -10) 
            pygame.draw.rect(surface, GOLD, marker_rect, 3, border_radius=10)  




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
        text = wheel_font.render(slot, True, WHITE)  
        surface.blit(text, (text_x - text.get_width() // 2, text_y - text.get_height() // 2))

# Draw the marble
def draw_marble(surface, center, radius, angle):
    marble_x = center[0] + (radius - 15) * math.cos(math.radians(angle))
    marble_y = center[1] + (radius - 15) * math.sin(math.radians(angle))
    pygame.draw.circle(surface, WHITE, (int(marble_x), int(marble_y)), 10)

# Spin simulation with wheel and marble animation
def spin_wheel():
    wheel_angle = 0
    marble_angle = random.uniform(0, 360)  # Random starting position for marble
    speed = random.uniform(15, 20)  # Random initial speed
    marble_speed = -random.uniform(20, 25)  # Faster counterspin for marble
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
        draw_buttons(screen, buttons, selected_button)

        # Draw spin button
        spin_color = GOLD if spin_button.collidepoint(pygame.mouse.get_pos()) else YELLOW
        pygame.draw.rect(screen, spin_color, spin_button, border_radius=15) 
        spin_text = font.render("SPIN", True, BLACK)
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
    pygame.display.flip() 
    pygame.time.wait(3000)  # Pause for 3 seconds

    return result
 

# Main game loop
def rouletteMain():
    global buttons, spin_button, selected_button
    running = True
    buttons = create_buttons()
    selected_button = None
    spin_result = None
    win = False

    # Define buttons
    spin_button = pygame.Rect(WIDTH // 4 - 150, HEIGHT - 80, 300, 50)
    menu_button = pygame.Rect(WIDTH // 2 + 150, HEIGHT - 80, 150, 50)

    while running:
        # Update mouse position every frame
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
                        selected_button = button["number"]  # Mark the selected button
                        spin_result = None  # Reset the spin result when a new bet is placed

                # Check spin button
                if spin_button.collidepoint(pos) and selected_button:
                    marble_num, marble_color = spin_wheel() 
                    spin_result = (marble_num, marble_color)
                    win = selected_button == marble_num  # Check if the user wins

                # Check menu button
                if menu_button.collidepoint(pos):
                    running = False
                    return  # Exit roulette and return to the menu

        # Fill the background
        screen.fill(GREEN_BG)

        # Draw betting buttons
        draw_buttons(screen, buttons, selected_button)

        # Draw the wheel
        draw_wheel(screen, CENTER, RADIUS, 0)

        # Draw SPIN button
        spin_color = GOLD if spin_button.collidepoint(mouse_pos) else YELLOW
        pygame.draw.rect(screen, spin_color, spin_button, border_radius=15) 
        spin_text = font.render("SPIN", True, BLACK)
        screen.blit(
            spin_text,
            (spin_button.centerx - spin_text.get_width() // 2, spin_button.centery - spin_text.get_height() // 2)
        )

        # Draw MENU button
        menu_color = GOLD if menu_button.collidepoint(mouse_pos) else YELLOW
        pygame.draw.rect(screen, menu_color, menu_button, border_radius=15)  
        menu_text = font.render("MENU", True, BLACK)
        screen.blit(
            menu_text,
            (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2)
        )

        # Draw result
        if spin_result:
            result_text = f"Result: {spin_result[0]} ({spin_result[1]})"
            result_color = GREEN if win else RED
            result_render = large_font.render(result_text, True, result_color)
            screen.blit(
                result_render,
                (CENTER[0] + RADIUS + 50, CENTER[1] - result_render.get_height() // 2 - 30)
            )

            # Add win/loss message below the result
            outcome_text = "You WIN!" if win else "You LOSE!"
            outcome_color = GREEN if win else RED
            outcome_render = large_font.render(outcome_text, True, outcome_color)
            screen.blit(
                outcome_render,
                (CENTER[0] + RADIUS + 50, CENTER[1] + 30)
            )

        # Update display every frame
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    rouletteMain()
