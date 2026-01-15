import pygame
import time

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Group 2 - Auction Zone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
PURPLE = (138, 43, 226)
PINK = (255, 105, 180)
DARK_BG = (30, 30, 50)
GREEN = (50, 205, 50)
RED = (255, 80, 80)

# Fonts
font = pygame.font.Font(None, 26)
small_font = pygame.font.Font(None, 20)
title_font = pygame.font.Font(None, 48)
big_font = pygame.font.Font(None, 36)

# ============ DUMMY DATABASE ============
# List of all bids (our simple database)
bids_database = []

# List of auction items (9 items for 3x3 grid)
auction_items = [
    {"id": 1, "name": "Wireless Headphones", "description": "RGB Gaming Edition", "starting_price": 50.00, "max_bid": 150.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 2, "name": "Gaming Controller", "description": "Glow in the dark!", "starting_price": 35.00, "max_bid": 100.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 3, "name": "Phone Ring Light", "description": "Perfect for TikToks!", "starting_price": 15.00, "max_bid": 50.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 4, "name": "LED Backpack", "description": "Changes colors!", "starting_price": 40.00, "max_bid": 120.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 5, "name": "Mini Skateboard", "description": "Fingerboard pro set", "starting_price": 10.00, "max_bid": 40.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 6, "name": "Bubble Tea Kit", "description": "Make your own boba!", "starting_price": 20.00, "max_bid": 60.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 7, "name": "Karaoke Mic", "description": "Bluetooth speaker", "starting_price": 25.00, "max_bid": 80.00, "current_bid": 0, "highest_bidder": ""},
    {"id": 8, "name": "LED Strip Lights", "description": "16 million colors!", "starting_price": 18.00, "max_bid": 55.00, "current_bid": 0, "highest_bidder": ""},
]

# ============ GAME STATE ============
current_screen = "items"  # "items", "detail", "add_item", "results"
selected_item = None
name_input = ""
bid_input = ""
active_input = None  # "name" or "bid"
message = ""
message_timer = 0

# New item inputs
new_item_name = ""
new_item_desc = ""
new_item_price = ""
new_item_max = ""
new_item_active = None

# Timer (10 minutes = 600 seconds, using 60 for testing)
AUCTION_DURATION = 600  # Change to 60 for 1-minute testing
start_time = time.time()

# Grid settings
COLS = 3
ROWS = 3
CARD_WIDTH = 220
CARD_HEIGHT = 140
MARGIN_X = 30
MARGIN_Y = 20
START_Y = 100

# ============ HELPER FUNCTIONS ============
def get_time_remaining():
    elapsed = time.time() - start_time
    remaining = AUCTION_DURATION - elapsed
    if remaining < 0:
        remaining = 0
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    return minutes, seconds, remaining

def draw_button(text, x, y, width, height, color, text_color=WHITE):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    text_surface = font.render(text, True, text_color)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))
    return rect

def draw_input_box(label, value, x, y, width, is_active):
    # Label
    label_surface = small_font.render(label, True, LIGHT_GRAY)
    screen.blit(label_surface, (x, y - 20))
    
    # Box
    rect = pygame.Rect(x, y, width, 35)
    color = PINK if is_active else DARK_GRAY
    pygame.draw.rect(screen, (50, 50, 70), rect, border_radius=5)
    pygame.draw.rect(screen, color, rect, 2, border_radius=5)
    
    # Text
    text_surface = font.render(value, True, WHITE)
    screen.blit(text_surface, (x + 10, y + 8))
    
    return rect

def save_bid_to_database(item_id, bidder_name, bid_amount):
    """Save a bid to our dummy database"""
    bid_record = {
        "item_id": item_id,
        "bidder_name": bidder_name,
        "bid_amount": bid_amount,
        "timestamp": time.time()
    }
    bids_database.append(bid_record)
    print(f"Saved to DB: {bid_record}")  # Shows in terminal

def get_card_rects():
    """Get all card rectangles for click detection"""
    rects = []
    for i in range(len(auction_items)):
        if i >= 9:
            break
        row = i // COLS
        col = i % COLS
        x = MARGIN_X + col * (CARD_WIDTH + MARGIN_X)
        y = START_Y + row * (CARD_HEIGHT + MARGIN_Y)
        rects.append(pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT))
    return rects

# ============ SCREEN DRAWING FUNCTIONS ============
def draw_items_screen():
    global current_screen, selected_item
    
    screen.fill(DARK_BG)
    
    # Timer
    minutes, seconds, remaining = get_time_remaining()
    timer_color = RED if remaining < 60 else GREEN
    timer_text = title_font.render(f"{minutes:02d}:{seconds:02d}", True, timer_color)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))
    
    # Title
    title = title_font.render("Auction Zone", True, PINK)
    screen.blit(title, (30, 20))
    
    # Draw grid of items
    card_rects = get_card_rects()
    for i, item in enumerate(auction_items):
        if i >= 9:
            break
        
        rect = card_rects[i]
        x, y = rect.x, rect.y
        
        # Card background
        card_color = (60, 60, 90)
        pygame.draw.rect(screen, card_color, rect, border_radius=12)
        pygame.draw.rect(screen, PURPLE, rect, 2, border_radius=12)
        
        # Item name
        name_text = font.render(item["name"][:18], True, WHITE)
        screen.blit(name_text, (x + 10, y + 15))
        
        # Description
        desc_text = small_font.render(item["description"][:25], True, LIGHT_GRAY)
        screen.blit(desc_text, (x + 10, y + 42))
        
        # Current bid info
        if item["current_bid"] > 0:
            bid_label = small_font.render("Current Bid:", True, GREEN)
            screen.blit(bid_label, (x + 10, y + 70))
            bid_text = font.render(f"£{item['current_bid']:.2f}", True, GREEN)
            screen.blit(bid_text, (x + 10, y + 88))
            bidder_text = small_font.render(f"by {item['highest_bidder'][:12]}", True, LIGHT_GRAY)
            screen.blit(bidder_text, (x + 10, y + 115))
        else:
            price_label = small_font.render("Starting:", True, LIGHT_GRAY)
            screen.blit(price_label, (x + 10, y + 80))
            price_text = font.render(f"£{item['starting_price']:.2f}", True, PINK)
            screen.blit(price_text, (x + 10, y + 100))
    
    # Add Item button (+ button)
    if len(auction_items) < 9:
        add_btn = draw_button("+", SCREEN_WIDTH - 80, SCREEN_HEIGHT - 60, 50, 40, PURPLE)
    else:
        add_btn = None
    
    # End Auction button
    end_btn = draw_button("End Auction", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT - 60, 140, 40, RED)
    
    return card_rects, add_btn, end_btn

def draw_detail_screen():
    global name_input, bid_input, active_input, message
    
    screen.fill(DARK_BG)
    
    item = selected_item
    
    # Back button
    back_btn = draw_button("< Back", 20, 20, 80, 35, DARK_GRAY)
    
    # Timer
    minutes, seconds, remaining = get_time_remaining()
    timer_color = RED if remaining < 60 else GREEN
    timer_text = big_font.render(f"{minutes:02d}:{seconds:02d}", True, timer_color)
    screen.blit(timer_text, (SCREEN_WIDTH - 120, 25))
    
    # Item Information title
    title = title_font.render("Item Information", True, PINK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    
    # Item details box
    detail_box = pygame.Rect(50, 140, 350, 200)
    pygame.draw.rect(screen, (50, 50, 80), detail_box, border_radius=10)
    pygame.draw.rect(screen, PURPLE, detail_box, 2, border_radius=10)
    
    # Item info
    info_x = 70
    info_y = 160
    
    name_label = font.render(f"Item: {item['name']}", True, WHITE)
    screen.blit(name_label, (info_x, info_y))
    
    current_label = font.render(f"Current Price: £{item['current_bid']:.2f}" if item['current_bid'] > 0 else f"Current Price: £{item['starting_price']:.2f}", True, GREEN)
    screen.blit(current_label, (info_x, info_y + 40))
    
    original_label = font.render(f"Original Price: £{item['starting_price']:.2f}", True, LIGHT_GRAY)
    screen.blit(original_label, (info_x, info_y + 80))
    
    limit_label = font.render(f"Bid Limit: £{item['max_bid']:.2f}", True, RED)
    screen.blit(limit_label, (info_x, info_y + 120))
    
    if item['highest_bidder']:
        bidder_label = small_font.render(f"Highest Bidder: {item['highest_bidder']}", True, GREEN)
        screen.blit(bidder_label, (info_x, info_y + 155))
    
    # Enter your details box
    input_box = pygame.Rect(430, 140, 320, 200)
    pygame.draw.rect(screen, (50, 50, 80), input_box, border_radius=10)
    pygame.draw.rect(screen, PURPLE, input_box, 2, border_radius=10)
    
    details_title = font.render("Enter Your Details", True, WHITE)
    screen.blit(details_title, (480, 155))
    
    # Input fields
    name_rect = draw_input_box("Name:", name_input, 450, 210, 280, active_input == "name")
    bid_rect = draw_input_box("Bid Price: £", bid_input, 450, 280, 280, active_input == "bid")
    
    # BID button
    bid_btn = draw_button("BID", 250, 380, 300, 50, GREEN, BLACK)
    
    # Message
    if message:
        msg_color = GREEN if "Success" in message else RED
        msg_surface = font.render(message, True, msg_color)
        screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, 450))
    
    return back_btn, name_rect, bid_rect, bid_btn

def draw_add_item_screen():
    global new_item_name, new_item_desc, new_item_price, new_item_max, new_item_active
    
    screen.fill(DARK_BG)
    
    # Back button
    back_btn = draw_button("< Back", 20, 20, 80, 35, DARK_GRAY)
    
    # Title
    title = title_font.render("Add New Item", True, PINK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    
    # Input fields
    name_rect = draw_input_box("Item Name:", new_item_name, 200, 180, 400, new_item_active == "name")
    desc_rect = draw_input_box("Description:", new_item_desc, 200, 260, 400, new_item_active == "desc")
    price_rect = draw_input_box("Starting Price: $", new_item_price, 200, 340, 180, new_item_active == "price")
    max_rect = draw_input_box("Max Bid: $", new_item_max, 420, 340, 180, new_item_active == "max")
    
    # Add button
    add_btn = draw_button("Add Item", 300, 420, 200, 50, GREEN, BLACK)
    
    return back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn

def draw_results_screen():
    screen.fill(DARK_BG)
    
    # Title
    title = title_font.render("Auction Results!", True, PINK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
    
    # Show results
    y = 100
    for item in auction_items:
        # Item box
        box = pygame.Rect(50, y, SCREEN_WIDTH - 100, 50)
        pygame.draw.rect(screen, (50, 50, 80), box, border_radius=8)
        pygame.draw.rect(screen, PURPLE, box, 2, border_radius=8)
        
        # Item name
        name_text = font.render(item["name"], True, WHITE)
        screen.blit(name_text, (70, y + 15))
        
        # Winner
        if item["current_bid"] > 0:
            winner_text = font.render(f"Winner: {item['highest_bidder']} - £{item['current_bid']:.2f}", True, GREEN)
        else:
            winner_text = font.render("No bids", True, DARK_GRAY)
        screen.blit(winner_text, (400, y + 15))
        
        y += 60
    
    # Print database
    print("\n=== FINAL DATABASE ===")
    for bid in bids_database:
        print(bid)
    print("======================\n")
    
    # Close button
    close_btn = draw_button("Close", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 70, 120, 45, RED)
    
    return close_btn

# ============ MAIN LOOP ============
running = True
clock = pygame.time.Clock()

while running:
    # Check if time is up
    _, _, remaining = get_time_remaining()
    if remaining <= 0 and current_screen != "results":
        current_screen = "results"
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if current_screen == "items":
                card_rects, add_btn, end_btn = draw_items_screen()
                
                # Check item clicks
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mouse_pos) and i < len(auction_items):
                        selected_item = auction_items[i]
                        current_screen = "detail"
                        name_input = ""
                        bid_input = ""
                        message = ""
                        break
                
                # Check add button
                if add_btn and add_btn.collidepoint(mouse_pos):
                    current_screen = "add_item"
                    new_item_name = ""
                    new_item_desc = ""
                    new_item_price = ""
                    new_item_max = ""
                
                # Check end button
                if end_btn.collidepoint(mouse_pos):
                    current_screen = "results"
            
            elif current_screen == "detail":
                back_btn, name_rect, bid_rect, bid_btn = draw_detail_screen()
                
                if back_btn.collidepoint(mouse_pos):
                    current_screen = "items"
                elif name_rect.collidepoint(mouse_pos):
                    active_input = "name"
                elif bid_rect.collidepoint(mouse_pos):
                    active_input = "bid"
                elif bid_btn.collidepoint(mouse_pos):
                    # Process bid
                    if name_input.strip() == "":
                        message = "Please enter your name!"
                    elif bid_input.strip() == "":
                        message = "Please enter a bid amount!"
                    else:
                        try:
                            bid_amount = float(bid_input)
                            min_bid = selected_item["current_bid"] if selected_item["current_bid"] > 0 else selected_item["starting_price"]
                            
                            if bid_amount <= min_bid:
                                message = f"Bid must be higher than £{min_bid:.2f}!"
                            elif bid_amount > selected_item["max_bid"]:
                                message = f"Bid cannot exceed £{selected_item['max_bid']:.2f}!"
                            else:
                                # Valid bid!
                                selected_item["current_bid"] = bid_amount
                                selected_item["highest_bidder"] = name_input
                                save_bid_to_database(selected_item["id"], name_input, bid_amount)
                                message = "Success! Your bid has been placed!"
                                name_input = ""
                                bid_input = ""
                        except ValueError:
                            message = "Please enter a valid number!"
            
            elif current_screen == "add_item":
                back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn = draw_add_item_screen()
                
                if back_btn.collidepoint(mouse_pos):
                    current_screen = "items"
                elif name_rect.collidepoint(mouse_pos):
                    new_item_active = "name"
                elif desc_rect.collidepoint(mouse_pos):
                    new_item_active = "desc"
                elif price_rect.collidepoint(mouse_pos):
                    new_item_active = "price"
                elif max_rect.collidepoint(mouse_pos):
                    new_item_active = "max"
                elif add_btn.collidepoint(mouse_pos):
                    # Add new item
                    if new_item_name and new_item_price and new_item_max:
                        try:
                            new_item = {
                                "id": len(auction_items) + 1,
                                "name": new_item_name,
                                "description": new_item_desc or "No description",
                                "starting_price": float(new_item_price),
                                "max_bid": float(new_item_max),
                                "current_bid": 0,
                                "highest_bidder": ""
                            }
                            auction_items.append(new_item)
                            current_screen = "items"
                        except ValueError:
                            pass
            
            elif current_screen == "results":
                close_btn = draw_results_screen()
                if close_btn.collidepoint(mouse_pos):
                    running = False
        
        elif event.type == pygame.KEYDOWN:
            if current_screen == "detail":
                if event.key == pygame.K_BACKSPACE:
                    if active_input == "name":
                        name_input = name_input[:-1]
                    elif active_input == "bid":
                        bid_input = bid_input[:-1]
                elif event.key == pygame.K_TAB:
                    active_input = "bid" if active_input == "name" else "name"
                else:
                    char = event.unicode
                    if active_input == "name" and len(name_input) < 20:
                        name_input += char
                    elif active_input == "bid" and len(bid_input) < 10:
                        if char.isdigit() or char == ".":
                            bid_input += char
            
            elif current_screen == "add_item":
                if event.key == pygame.K_BACKSPACE:
                    if new_item_active == "name":
                        new_item_name = new_item_name[:-1]
                    elif new_item_active == "desc":
                        new_item_desc = new_item_desc[:-1]
                    elif new_item_active == "price":
                        new_item_price = new_item_price[:-1]
                    elif new_item_active == "max":
                        new_item_max = new_item_max[:-1]
                else:
                    char = event.unicode
                    if new_item_active == "name" and len(new_item_name) < 25:
                        new_item_name += char
                    elif new_item_active == "desc" and len(new_item_desc) < 30:
                        new_item_desc += char
                    elif new_item_active in ["price", "max"]:
                        if char.isdigit() or char == ".":
                            if new_item_active == "price" and len(new_item_price) < 8:
                                new_item_price += char
                            elif new_item_active == "max" and len(new_item_max) < 8:
                                new_item_max += char
    
    # Draw current screen
    if current_screen == "items":
        draw_items_screen()
    elif current_screen == "detail":
        draw_detail_screen()
    elif current_screen == "add_item":
        draw_add_item_screen()
    elif current_screen == "results":
        draw_results_screen()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
