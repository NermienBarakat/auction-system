import pygame

# List of bidders 
bidders = []

# List of auction items (9 items for 3x3 grid)
auction_items = [
    {"id": 1, "name": "Wireless Headphones", "description": "RGB Gaming Edition", "starting_price": 50.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 2, "name": "Gaming Controller", "description": "Glow in the dark!", "starting_price": 35.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 3, "name": "Phone Ring Light", "description": "Perfect for TikToks!", "starting_price": 15.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 4, "name": "LED Backpack", "description": "Changes colors!", "starting_price": 40.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 5, "name": "Mini Skateboard", "description": "Fingerboard pro set", "starting_price": 10.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 6, "name": "Bubble Tea Kit", "description": "Make your own boba!", "starting_price": 20.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 7, "name": "Karaoke Mic", "description": "Bluetooth speaker", "starting_price": 25.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 8, "name": "LED Strip Lights", "description": "16 million colors!", "starting_price": 18.00, "current_bid": 0, "highest_bidder_id": None},
    {"id": 9, "name": "Portable Projector", "description": "Movie nights!", "starting_price": 60.00, "current_bid": 0, "highest_bidder_id": None},
]

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Group 2 - Auction Zone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
PURPLE = (138, 43, 226)
PINK = (255, 105, 180)
DARK_BG = (30, 30, 50)

# Font
font = pygame.font.Font(None, 26)
small_font = pygame.font.Font(None, 20)
title_font = pygame.font.Font(None, 48)

# Grid settings
COLS = 3
ROWS = 3
CARD_WIDTH = 220
CARD_HEIGHT = 140
MARGIN_X = 25
MARGIN_Y = 20
START_Y = 100

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(DARK_BG)

    # Draw title
    title = title_font.render("Group 2 - Auction Zone", True, PINK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 25))

    # Draw 3x3 grid of items
    for i, item in enumerate(auction_items):
        if i >= 9:  # Only show 9 items
            break
        
        row = i // COLS
        col = i % COLS
        
        x = MARGIN_X + col * (CARD_WIDTH + MARGIN_X)
        y = START_Y + row * (CARD_HEIGHT + MARGIN_Y)
        
        # Card background
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        card_color = (60, 60, 90)
        pygame.draw.rect(screen, card_color, card_rect, border_radius=12)
        pygame.draw.rect(screen, PURPLE, card_rect, 2, border_radius=12)
        
        # Item name
        name_text = font.render(item["name"], True, WHITE)
        screen.blit(name_text, (x + 10, y + 15))
        
        # Item description
        desc_text = small_font.render(item["description"], True, LIGHT_GRAY)
        screen.blit(desc_text, (x + 10, y + 45))
        
        # Starting price label
        price_label = small_font.render("Starting Price:", True, LIGHT_GRAY)
        screen.blit(price_label, (x + 10, y + 80))
        
        # Price value
        price_text = font.render(f"${item['starting_price']:.2f}", True, PINK)
        screen.blit(price_text, (x + 10, y + 100))

    pygame.display.flip()

pygame.quit()
