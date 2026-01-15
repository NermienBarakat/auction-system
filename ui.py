"""
UI module - simple helper functions for drawing UI elements
"""
import pygame

# ============ SETTINGS ============
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
CURRENCY = "£"

# Colors (easy to change!)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
PURPLE = (138, 43, 226)
PINK = (255, 105, 180)
DARK_BG = (30, 30, 50)
GREEN = (50, 205, 50)
RED = (255, 80, 80)
CARD_BG = (60, 60, 90)
INPUT_BG = (50, 50, 70)

# Grid settings
COLS = 3
CARD_WIDTH = 220
CARD_HEIGHT = 140
MARGIN_X = 30
MARGIN_Y = 20
START_Y = 100


def init_fonts():
    """Initialize and return fonts dictionary"""
    return {
        'normal': pygame.font.Font(None, 26),
        'small': pygame.font.Font(None, 20),
        'title': pygame.font.Font(None, 48),
        'big': pygame.font.Font(None, 36)
    }


def draw_button(screen, fonts, text, x, y, width, height, color, text_color=WHITE):
    """Draw a button and return its rectangle for click detection"""
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    
    text_surface = fonts['normal'].render(text, True, text_color)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))
    
    return rect


def draw_input_box(screen, fonts, label, value, x, y, width, is_active):
    """Draw an input box and return its rectangle"""
    # Label above the box
    label_surface = fonts['small'].render(label, True, LIGHT_GRAY)
    screen.blit(label_surface, (x, y - 20))
    
    # The input box
    rect = pygame.Rect(x, y, width, 35)
    border_color = PINK if is_active else DARK_GRAY
    pygame.draw.rect(screen, INPUT_BG, rect, border_radius=5)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=5)
    
    # Text inside the box
    text_surface = fonts['normal'].render(value, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 8))
    
    return rect


def draw_timer(screen, fonts, minutes, seconds, remaining, x, y):
    """Draw the countdown timer"""
    color = RED if remaining < 60 else GREEN
    timer_text = fonts['title'].render(f"{minutes:02d}:{seconds:02d}", True, color)
    screen.blit(timer_text, (x, y))


def draw_title(screen, fonts, text, y, color=PINK):
    """Draw a centered title"""
    title = fonts['title'].render(text, True, color)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, y))


def draw_item_card(screen, fonts, item, x, y):
    """Draw a single item card"""
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    
    # Card background
    pygame.draw.rect(screen, CARD_BG, rect, border_radius=12)
    pygame.draw.rect(screen, PURPLE, rect, 2, border_radius=12)
    
    # Item name
    name_text = fonts['normal'].render(item["name"][:18], True, WHITE)
    screen.blit(name_text, (x + 10, y + 15))
    
    # Description
    desc_text = fonts['small'].render(item["description"][:25], True, LIGHT_GRAY)
    screen.blit(desc_text, (x + 10, y + 42))
    
    # Current bid or starting price
    if item["current_bid"] > 0:
        bid_label = fonts['small'].render("Current Bid:", True, GREEN)
        screen.blit(bid_label, (x + 10, y + 70))
        bid_text = fonts['normal'].render(f"{CURRENCY}{item['current_bid']:.2f}", True, GREEN)
        screen.blit(bid_text, (x + 10, y + 88))
        bidder_text = fonts['small'].render(f"by {item['highest_bidder'][:12]}", True, LIGHT_GRAY)
        screen.blit(bidder_text, (x + 10, y + 115))
    else:
        price_label = fonts['small'].render("Starting:", True, LIGHT_GRAY)
        screen.blit(price_label, (x + 10, y + 80))
        price_text = fonts['normal'].render(f"{CURRENCY}{item['starting_price']:.2f}", True, PINK)
        screen.blit(price_text, (x + 10, y + 100))
    
    return rect


def draw_add_card(screen, fonts, x, y):
    """Draw the + button card for adding items"""
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    
    pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
    pygame.draw.rect(screen, PURPLE, rect, 2, border_radius=12)
    
    plus_text = fonts['title'].render("+", True, PURPLE)
    screen.blit(plus_text, (x + CARD_WIDTH // 2 - plus_text.get_width() // 2,
                            y + CARD_HEIGHT // 2 - plus_text.get_height() // 2))
    
    return rect


def get_card_position(index, scroll_y=0):
    """Calculate x, y position for a card at given index"""
    row = index // COLS
    col = index % COLS
    x = MARGIN_X + col * (CARD_WIDTH + MARGIN_X)
    y = START_Y + row * (CARD_HEIGHT + MARGIN_Y) + scroll_y
    return x, y


def is_visible(y):
    """Check if a card at y position is visible on screen"""
    return y + CARD_HEIGHT > 80 and y < SCREEN_HEIGHT - 70
