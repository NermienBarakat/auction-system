"""
Auction System - Main Game
A simple auction system for teens!

Files:
- main.py (this file) - the main game loop
- db.py - database functions (SQLite)
- ui.py - UI helper functions
"""
import pygame
import time
import db  # Our database module
import ui  # Our UI module


# ============ GAME SETUP ============
pygame.init()
screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
pygame.display.set_caption("Group 2 - Auction Zone")
fonts = ui.init_fonts()
clock = pygame.time.Clock()

# Game state variables
current_screen = "items"  # "items", "detail", "add_item", "results"
selected_item = None
scroll_y = 0
running = True
results_printed = False  # Flag to only print results once

# Timer (10 minutes)
AUCTION_DURATION = 600  # seconds (change to 60 for testing)
start_time = time.time()

# Input fields
inputs = {
    "name": "",
    "bid": "",
    "item_name": "",
    "item_desc": "",
    "item_price": "",
    "item_max": "",
    "active": None  # which input is selected
}
message = ""


# ============ HELPER FUNCTIONS ============
def get_time_remaining():
    """Calculate time left in the auction"""
    elapsed = time.time() - start_time
    remaining = max(0, AUCTION_DURATION - elapsed)
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    return minutes, seconds, remaining


def handle_scroll(direction):
    """Handle scrolling on items screen"""
    global scroll_y
    items = db.get_all_items()
    num_items = len(items) + 1  # +1 for add button
    rows = (num_items + ui.COLS - 1) // ui.COLS
    total_height = ui.START_Y + rows * (ui.CARD_HEIGHT + ui.MARGIN_Y) + 80
    max_scroll = max(0, total_height - ui.SCREEN_HEIGHT + 100)
    
    scroll_y += direction * 40
    scroll_y = max(-max_scroll, min(0, scroll_y))


def clear_inputs():
    """Clear all input fields"""
    inputs["name"] = ""
    inputs["bid"] = ""
    inputs["item_name"] = ""
    inputs["item_desc"] = ""
    inputs["item_price"] = ""
    inputs["item_max"] = ""
    inputs["active"] = None


# ============ SCREEN DRAWING FUNCTIONS ============
def draw_items_screen():
    """Draw the main items grid screen"""
    minutes, seconds, remaining = get_time_remaining()
    
    screen.fill(ui.DARK_BG)
    
    # Header
    title = fonts['title'].render("Auction Zone", True, ui.PINK)
    screen.blit(title, (30, 20))
    ui.draw_timer(screen, fonts, minutes, seconds, remaining, ui.SCREEN_WIDTH - 150, 20)
    
    # Get items from database
    items = db.get_all_items()
    
    # Scroll hint
    if len(items) > 6:
        hint = fonts['small'].render("Scroll to see more items", True, ui.LIGHT_GRAY)
        screen.blit(hint, (ui.SCREEN_WIDTH // 2 - hint.get_width() // 2, 65))
    
    # Draw item cards
    card_rects = []
    for i, item in enumerate(items):
        x, y = ui.get_card_position(i, scroll_y)
        if ui.is_visible(y):
            rect = ui.draw_item_card(screen, fonts, item, x, y)
            card_rects.append((rect, item))
        else:
            card_rects.append((pygame.Rect(x, y, ui.CARD_WIDTH, ui.CARD_HEIGHT), item))
    
    # Draw add button
    add_x, add_y = ui.get_card_position(len(items), scroll_y)
    add_rect = None
    if ui.is_visible(add_y):
        add_rect = ui.draw_add_card(screen, fonts, add_x, add_y)
    else:
        add_rect = pygame.Rect(add_x, add_y, ui.CARD_WIDTH, ui.CARD_HEIGHT)
    
    # Bottom bar with Reset and End Auction buttons
    pygame.draw.rect(screen, ui.DARK_BG, (0, ui.SCREEN_HEIGHT - 70, ui.SCREEN_WIDTH, 70))
    reset_btn = ui.draw_button(screen, fonts, "Reset", 
                                ui.SCREEN_WIDTH // 2 - 160, ui.SCREEN_HEIGHT - 60, 
                                100, 40, ui.PURPLE)
    end_btn = ui.draw_button(screen, fonts, "End Auction", 
                              ui.SCREEN_WIDTH // 2 - 40, ui.SCREEN_HEIGHT - 60, 
                              140, 40, ui.RED)
    
    return card_rects, add_rect, reset_btn, end_btn


def draw_detail_screen():
    """Draw the item detail/bidding screen"""
    global message
    minutes, seconds, remaining = get_time_remaining()
    
    screen.fill(ui.DARK_BG)
    
    # Back button and timer
    back_btn = ui.draw_button(screen, fonts, "< Back", 20, 20, 80, 35, ui.DARK_GRAY)
    ui.draw_timer(screen, fonts, minutes, seconds, remaining, ui.SCREEN_WIDTH - 120, 25)
    
    # Title
    ui.draw_title(screen, fonts, "Item Information", 80)
    
    # Item details box
    detail_box = pygame.Rect(50, 140, 350, 200)
    pygame.draw.rect(screen, ui.INPUT_BG, detail_box, border_radius=10)
    pygame.draw.rect(screen, ui.PURPLE, detail_box, 2, border_radius=10)
    
    # Item info
    current_price = selected_item['current_bid'] if selected_item['current_bid'] > 0 else selected_item['starting_price']
    
    info_lines = [
        (f"Item: {selected_item['name']}", ui.WHITE),
        (f"Current Price: {ui.CURRENCY}{current_price:.2f}", ui.GREEN),
        (f"Original Price: {ui.CURRENCY}{selected_item['starting_price']:.2f}", ui.LIGHT_GRAY),
        (f"Bid Limit: {ui.CURRENCY}{selected_item['max_bid']:.2f}", ui.RED),
    ]
    
    for i, (text, color) in enumerate(info_lines):
        label = fonts['normal'].render(text, True, color)
        screen.blit(label, (70, 160 + i * 40))
    
    if selected_item['highest_bidder']:
        bidder = fonts['small'].render(f"Highest Bidder: {selected_item['highest_bidder']}", True, ui.GREEN)
        screen.blit(bidder, (70, 315))
    
    # Input form box
    input_box = pygame.Rect(430, 140, 320, 200)
    pygame.draw.rect(screen, ui.INPUT_BG, input_box, border_radius=10)
    pygame.draw.rect(screen, ui.PURPLE, input_box, 2, border_radius=10)
    
    title = fonts['normal'].render("Enter Your Details", True, ui.WHITE)
    screen.blit(title, (480, 155))
    
    # Input fields
    name_rect = ui.draw_input_box(screen, fonts, "Name:", inputs["name"], 
                                   450, 210, 280, inputs["active"] == "name")
    bid_rect = ui.draw_input_box(screen, fonts, f"Bid Price: {ui.CURRENCY}", inputs["bid"], 
                                  450, 280, 280, inputs["active"] == "bid")
    
    # BID button
    bid_btn = ui.draw_button(screen, fonts, "BID", 250, 380, 300, 50, ui.GREEN, ui.BLACK)
    
    # Message
    if message:
        color = ui.GREEN if "Success" in message else ui.RED
        msg = fonts['normal'].render(message, True, color)
        screen.blit(msg, (ui.SCREEN_WIDTH // 2 - msg.get_width() // 2, 450))
    
    return back_btn, name_rect, bid_rect, bid_btn


def draw_add_item_screen():
    """Draw the add new item screen"""
    screen.fill(ui.DARK_BG)
    
    # Back button
    back_btn = ui.draw_button(screen, fonts, "< Back", 20, 20, 80, 35, ui.DARK_GRAY)
    
    # Title
    ui.draw_title(screen, fonts, "Add New Item", 80)
    
    # Input fields
    name_rect = ui.draw_input_box(screen, fonts, "Item Name:", inputs["item_name"], 
                                   200, 180, 400, inputs["active"] == "item_name")
    desc_rect = ui.draw_input_box(screen, fonts, "Description:", inputs["item_desc"], 
                                   200, 260, 400, inputs["active"] == "item_desc")
    price_rect = ui.draw_input_box(screen, fonts, f"Starting Price: {ui.CURRENCY}", inputs["item_price"], 
                                    200, 340, 180, inputs["active"] == "item_price")
    max_rect = ui.draw_input_box(screen, fonts, f"Max Bid: {ui.CURRENCY}", inputs["item_max"], 
                                  420, 340, 180, inputs["active"] == "item_max")
    
    # Add button
    add_btn = ui.draw_button(screen, fonts, "Add Item", 300, 420, 200, 50, ui.GREEN, ui.BLACK)
    
    # Message
    if message:
        msg = fonts['normal'].render(message, True, ui.RED)
        screen.blit(msg, (ui.SCREEN_WIDTH // 2 - msg.get_width() // 2, 490))
    
    return back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn


def draw_results_screen():
    """Draw the auction results screen"""
    screen.fill(ui.DARK_BG)
    
    # Title
    ui.draw_title(screen, fonts, "Auction Results!", 30)
    
    # Get final results
    items = db.get_all_items()
    
    # Draw results
    y = 100 + scroll_y
    for item in items:
        if y + 50 > 70 and y < ui.SCREEN_HEIGHT - 80:
            box = pygame.Rect(50, y, ui.SCREEN_WIDTH - 100, 50)
            pygame.draw.rect(screen, ui.INPUT_BG, box, border_radius=8)
            pygame.draw.rect(screen, ui.PURPLE, box, 2, border_radius=8)
            
            name_text = fonts['normal'].render(item["name"][:20], True, ui.WHITE)
            screen.blit(name_text, (70, y + 15))
            
            if item["current_bid"] > 0:
                winner = fonts['normal'].render(
                    f"Winner: {item['highest_bidder']} - {ui.CURRENCY}{item['current_bid']:.2f}", 
                    True, ui.GREEN)
            else:
                winner = fonts['normal'].render("No bids", True, ui.DARK_GRAY)
            screen.blit(winner, (350, y + 15))
        
        y += 60
    
    # Close button
    pygame.draw.rect(screen, ui.DARK_BG, (0, ui.SCREEN_HEIGHT - 80, ui.SCREEN_WIDTH, 80))
    close_btn = ui.draw_button(screen, fonts, "Close", 
                                ui.SCREEN_WIDTH // 2 - 60, ui.SCREEN_HEIGHT - 70, 
                                120, 45, ui.RED)
    
    return close_btn


# ============ EVENT HANDLERS ============
def handle_items_click(mouse_pos, card_rects, add_rect, reset_btn, end_btn):
    """Handle clicks on the items screen"""
    global current_screen, selected_item, message, start_time, results_printed
    
    # Check reset button FIRST
    if reset_btn.collidepoint(mouse_pos):
        db.reset_auction()
        start_time = time.time()  # Reset timer
        results_printed = False   # Allow printing results again
        print("\n🔄 Auction Reset! Timer restarted.\n")
        return
    
    # Check end button
    if end_btn.collidepoint(mouse_pos):
        current_screen = "results"
        if not results_printed:
            db.print_results()
            results_printed = True
        return
    
    # Check item cards
    for rect, item in card_rects:
        if rect.collidepoint(mouse_pos):
            selected_item = item
            current_screen = "detail"
            clear_inputs()
            message = ""
            return
    
    # Check add button (only if visible - not behind bottom bar)
    if add_rect.collidepoint(mouse_pos) and add_rect.y < ui.SCREEN_HEIGHT - 70:
        current_screen = "add_item"
        clear_inputs()
        message = ""
        return


def handle_detail_click(mouse_pos, back_btn, name_rect, bid_rect, bid_btn):
    """Handle clicks on the detail screen"""
    global current_screen, message, selected_item
    
    if back_btn.collidepoint(mouse_pos):
        current_screen = "items"
        return
    
    if name_rect.collidepoint(mouse_pos):
        inputs["active"] = "name"
        return
    
    if bid_rect.collidepoint(mouse_pos):
        inputs["active"] = "bid"
        return
    
    if bid_btn.collidepoint(mouse_pos):
        # Process the bid
        if not inputs["name"].strip():
            message = "Please enter your name!"
            return
        
        if not inputs["bid"].strip():
            message = "Please enter a bid amount!"
            return
        
        try:
            bid_amount = float(inputs["bid"])
            min_bid = selected_item["current_bid"] if selected_item["current_bid"] > 0 else selected_item["starting_price"]
            
            if bid_amount <= min_bid:
                message = f"Bid must be higher than {ui.CURRENCY}{min_bid:.2f}!"
            elif bid_amount > selected_item["max_bid"]:
                message = f"Bid cannot exceed {ui.CURRENCY}{selected_item['max_bid']:.2f}!"
            else:
                # Valid bid - save to database!
                db.update_bid(selected_item["id"], bid_amount, inputs["name"])
                selected_item["current_bid"] = bid_amount
                selected_item["highest_bidder"] = inputs["name"]
                message = "Success! Your bid has been placed!"
                inputs["name"] = ""
                inputs["bid"] = ""
        except ValueError:
            message = "Please enter a valid number!"


def handle_add_item_click(mouse_pos, back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn):
    """Handle clicks on the add item screen"""
    global current_screen, message
    
    if back_btn.collidepoint(mouse_pos):
        current_screen = "items"
        return
    
    if name_rect.collidepoint(mouse_pos):
        inputs["active"] = "item_name"
    elif desc_rect.collidepoint(mouse_pos):
        inputs["active"] = "item_desc"
    elif price_rect.collidepoint(mouse_pos):
        inputs["active"] = "item_price"
    elif max_rect.collidepoint(mouse_pos):
        inputs["active"] = "item_max"
    elif add_btn.collidepoint(mouse_pos):
        # Add the item
        if not inputs["item_name"].strip():
            message = "Please enter an item name!"
            return
        
        if not inputs["item_price"].strip() or not inputs["item_max"].strip():
            message = "Please enter prices!"
            return
        
        try:
            price = float(inputs["item_price"])
            max_bid = float(inputs["item_max"])
            
            if max_bid <= price:
                message = "Max bid must be higher than starting price!"
            else:
                db.add_item(inputs["item_name"], inputs["item_desc"], price, max_bid)
                current_screen = "items"
                message = ""
        except ValueError:
            message = "Please enter valid numbers!"


def handle_key(event):
    """Handle keyboard input"""
    active = inputs["active"]
    
    if active is None:
        return
    
    if event.key == pygame.K_BACKSPACE:
        inputs[active] = inputs[active][:-1]
    elif event.key == pygame.K_TAB:
        # Cycle through inputs
        if current_screen == "detail":
            inputs["active"] = "bid" if active == "name" else "name"
        elif current_screen == "add_item":
            order = ["item_name", "item_desc", "item_price", "item_max"]
            idx = order.index(active) if active in order else -1
            inputs["active"] = order[(idx + 1) % len(order)]
    else:
        char = event.unicode
        # Limit input length
        max_len = 20 if active in ["name", "item_name", "item_desc"] else 10
        
        if len(inputs[active]) < max_len:
            # Only allow numbers for price fields
            if active in ["bid", "item_price", "item_max"]:
                if char.isdigit() or char == ".":
                    inputs[active] += char
            else:
                inputs[active] += char


# ============ MAIN GAME LOOP ============
print("\n🎯 Auction System Started!")
print("📁 Database file: auction.db")
print("⏰ Auction duration: 10 minutes\n")

while running:
    # Check if time is up
    _, _, remaining = get_time_remaining()
    if remaining <= 0 and current_screen != "results":
        current_screen = "results"
        if not results_printed:
            db.print_results()
            results_printed = True
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEWHEEL:
            if current_screen in ["items", "results"]:
                handle_scroll(event.y)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            if current_screen == "items":
                card_rects, add_rect, reset_btn, end_btn = draw_items_screen()
                handle_items_click(mouse_pos, card_rects, add_rect, reset_btn, end_btn)
            
            elif current_screen == "detail":
                back_btn, name_rect, bid_rect, bid_btn = draw_detail_screen()
                handle_detail_click(mouse_pos, back_btn, name_rect, bid_rect, bid_btn)
            
            elif current_screen == "add_item":
                back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn = draw_add_item_screen()
                handle_add_item_click(mouse_pos, back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn)
            
            elif current_screen == "results":
                close_btn = draw_results_screen()
                if close_btn.collidepoint(mouse_pos):
                    running = False
        
        elif event.type == pygame.KEYDOWN:
            handle_key(event)
    
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
print("\n👋 Thanks for using Auction System!")
