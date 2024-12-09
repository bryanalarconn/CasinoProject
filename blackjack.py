import pygame as pygame
import sys
import time
import random

SUITS = ['c', 's', 'h', 'd']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 144, 192
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (53, 101, 77)
GREY = (128, 128, 128)
GOLD = (255, 255, 0)
YELLOW = (255, 215, 0)

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for value in RANKS:
            for suit in SUITS:
                self.cards.append((value, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.card_img = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calc_hand(self):

        self.value = 0  # Reset hand value
        first_card_index = [a_card[0] for a_card in self.cards]
        non_aces = [c for c in first_card_index if c != 'A']
        aces = [c for c in first_card_index if c == 'A']

        # Add non-ace values
        for card in non_aces:
            if card in 'JQK':
                self.value += 10
            else:
                self.value += int(card)

        # Add ace values (1 or 11)
        for card in aces:
            if self.value <= 10:
                self.value += 11
            else:
                self.value += 1

    def display_cards(self):
        for card in self.cards:
            cards = "".join((card[0], card[1]))
            if cards not in self.card_img:
                self.card_img.append(cards)

class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.buttons_enabled = False  # Buttons initially disabled

        
    def reveal_dealer_cards(self):
        firstDealerCard = pygame.image.load('images/' + self.dealer.card_img[0] + '.png').convert()
        firstDealerCard = pygame.transform.scale(firstDealerCard, (CARD_WIDTH, CARD_HEIGHT))
        secondDealerCard = pygame.image.load('images/' + self.dealer.card_img[1] + '.png').convert()
        secondDealerCard = pygame.transform.scale(secondDealerCard, (CARD_WIDTH, CARD_HEIGHT))

        # Display both dealer cards
        gameDisplay.blit(firstDealerCard, (292, 50))
        gameDisplay.blit(secondDealerCard, (364, 50))
        pygame.display.update()

        
    def blackjack(self):
        self.dealer.calc_hand()
        self.player.calc_hand()

        if self.player.value == 21 and self.dealer.value == 21:
            # Reveal both dealer cards
            self.reveal_dealer_cards()
            game_texts("PUSH!")
            time.sleep(1)
            self.play_or_exit()
        elif self.player.value == 21:
            game_texts("WINNER! WINNER! CHICKEN DINNER!")
            time.sleep(1)
            self.play_or_exit()
        elif self.dealer.value == 21:
            # Reveal both dealer cards
            self.reveal_dealer_cards()
            game_texts("DEALER BLACKJACK!")
            time.sleep(1)
            self.play_or_exit()


    def deal(self):
        self.buttons_enabled = True  # Enable buttons after dealing

        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())
        self.dealer.display_cards()
        self.player.display_cards()
        self.firstPlayerCard = 1

        firstDealerCard = pygame.image.load('images/' + self.dealer.card_img[0] + '.png').convert()
        firstDealerCard = pygame.transform.scale(firstDealerCard, (CARD_WIDTH, CARD_HEIGHT))
        hiddenDealerCard = pygame.image.load('images/back.png').convert()
        hiddenDealerCard = pygame.transform.scale(hiddenDealerCard, (CARD_WIDTH, CARD_HEIGHT))

        firstPlayerCard = pygame.image.load('images/' + self.player.card_img[0] + '.png').convert()
        firstPlayerCard = pygame.transform.scale(firstPlayerCard, (CARD_WIDTH, CARD_HEIGHT))
        secondPlayerCard = pygame.image.load('images/' + self.player.card_img[1] + '.png').convert()
        secondPlayerCard = pygame.transform.scale(secondPlayerCard, (CARD_WIDTH, CARD_HEIGHT))

        # Display the dealer's first card and a hidden card
        gameDisplay.blit(firstDealerCard, (292, 50))
        gameDisplay.blit(hiddenDealerCard, (364, 50))

        # Display the player's cards
        gameDisplay.blit(firstPlayerCard, (292, 300))
        gameDisplay.blit(secondPlayerCard, (364, 300))

        # Check for blackjack conditions
        self.blackjack()

            
    def hit(self):
        if not self.buttons_enabled:
            return
        self.player.add_card(self.deck.deal())
        self.blackjack()
        self.player.calc_hand()
        self.player.display_cards()

        # Clear the player area
        pygame.draw.rect(gameDisplay, GREEN, pygame.Rect(200, 300, 400, 192))

        # Calculate centered positions for the player's cards with overlap
        total_cards = len(self.player.card_img)
        card_overlap = CARD_WIDTH // 2
        total_width = CARD_WIDTH + (total_cards - 1) * card_overlap
        start_x = (WIDTH - total_width) // 2

        for index, card_img in enumerate(self.player.card_img):
            card_image = pygame.image.load(f'images/{card_img}.png').convert()
            card_image = pygame.transform.scale(card_image, (CARD_WIDTH, 192))
            gameDisplay.blit(card_image, (start_x + index * card_overlap, 300))


        if self.player.value > 21:
            show_firstDealerCard = pygame.image.load(f'images/{self.dealer.card_img[1]}.png').convert()
            show_firstDealerCard = pygame.transform.scale(show_firstDealerCard, (144, 192))
            game_texts("You Busted!")
            time.sleep(1)
            self.play_or_exit()

        pygame.display.update()

        pass


            
    def stand(self):
        if not self.buttons_enabled:
            return
        # Reveal the dealer's second card
        show_firstDealerCard = pygame.image.load('images/' + self.dealer.card_img[1] + '.png').convert()
        show_firstDealerCard = pygame.transform.scale(show_firstDealerCard, (CARD_WIDTH, CARD_HEIGHT))
        gameDisplay.blit(show_firstDealerCard, (364, 50))
        pygame.display.update()
        time.sleep(1)

        # Dealer keeps hitting until their hand value is at least 17
        self.dealer.calc_hand()
        while self.dealer.value < 17:
            self.dealer.add_card(self.deck.deal())
            self.dealer.calc_hand()
            self.dealer.display_cards()

            # Clear the dealer area
            pygame.draw.rect(gameDisplay, GREEN, pygame.Rect(200, 50, 400, CARD_HEIGHT))

            # Calculate centered positions for the dealer's cards with overlap
            total_cards = len(self.dealer.card_img)
            card_overlap = CARD_WIDTH // 2 
            total_width = CARD_WIDTH + (total_cards - 1) * card_overlap
            start_x = (WIDTH - total_width) // 2

            for index, card_img in enumerate(self.dealer.card_img):
                card_image = pygame.image.load(f'images/{card_img}.png').convert()
                card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
                gameDisplay.blit(card_image, (start_x + index * card_overlap, 50))

            pygame.display.update()
            time.sleep(1)
            
        # Calculate final hand values
        self.player.calc_hand()

        print(f"dealer has {self.dealer.value}")
        print(f"player has {self.player.value}")

        # Determine the outcome of the game
        if self.dealer.value > 21:
            game_texts("DEALER BUSTED! YOU WIN!")
        elif self.player.value > self.dealer.value:
            game_texts("YOU WIN!")
        elif self.player.value < self.dealer.value:
            game_texts("DEALER WINS!")
        else:
            game_texts("PUSH!")
        
        time.sleep(1)
        self.play_or_exit()

        pass
    
    def exit(self):
        sys.exit()
    
    def play_or_exit(self):
        time.sleep(1)
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Hand()
        self.dealer = Hand()
        self.buttons_enabled = False
        gameDisplay.fill(GREEN)
        pygame.display.update()

pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 35)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gameDisplay.fill(GREEN)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()
def game_texts(text, x=None, y=None):
    TextSurf, TextRect = text_objects(text, font)
    if x is None:
        x = WIDTH // 2
    if y is None:
        dealer_y = 50  
        player_y = 300  
        y = (dealer_y + player_y + CARD_HEIGHT) // 2
        
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
def button(text, x, y, w, h, ic, ac, action=None, border_radius=15, enabled=True):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    current_color = ac if enabled and x + w > mouse[0] > x and y + h > mouse[1] > y else ic
    if not enabled: 
        current_color = GREY

    pygame.draw.rect(gameDisplay, current_color, (x, y, w, h), border_radius=border_radius)

    if enabled and x + w > mouse[0] > x and y + h > mouse[1] > y and click[0] == 1:
        pygame.time.wait(150)
        if action is not None:
            action()
            
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = (x + w / 2, y + h / 2)
    gameDisplay.blit(TextSurf, TextRect)
def blackjackMain():
    play_blackjack = Play()

    running = True
    show_text = True
    hand_in_progress = False  # Flag to track if a hand is in progress

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Trigger deal on spacebar
                    if not hand_in_progress:  # Only deal if no hand is in progress
                        play_blackjack.deal()
                        show_text = False
                        hand_in_progress = True  # Mark hand as in progress
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if MENU button is clicked
                if menu_button.collidepoint(pos):
                    running = False
                    return  # Exit blackjack and return to menu

        # Render buttons, passing the enabled state
        button("Hit", 50, 475, 150, 75, YELLOW, GOLD, play_blackjack.hit, enabled=play_blackjack.buttons_enabled)
        button("Stand", 600, 475, 150, 75, YELLOW, GOLD, play_blackjack.stand, enabled=play_blackjack.buttons_enabled)
        menu_button = pygame.Rect(600, 50, 150, 75) 

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Draw the MENU button
        is_hovered = menu_button.collidepoint(mouse_x, mouse_y)
        current_color = GOLD if is_hovered else YELLOW
        pygame.draw.rect(gameDisplay, current_color, menu_button, border_radius=15)  # Rounded rectangle
        menu_text = font.render("Menu", True, BLACK)
        gameDisplay.blit(
            menu_text,
            (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2)
        )

        # Render "Press SPACE to deal" if cards haven't been dealt
        if show_text:
            text_surface, text_rect = text_objects("Press SPACE to deal", font)
            text_rect.center = (WIDTH // 2, HEIGHT - 50)
            gameDisplay.blit(text_surface, text_rect)

        # Reset the hand_in_progress flag when the hand ends
        if not play_blackjack.buttons_enabled and not show_text:
            hand_in_progress = False  # Allow dealing a new hand

        pygame.display.flip()  # Update the display

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    blackjackMain()
