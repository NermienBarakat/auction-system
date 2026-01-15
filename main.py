import pygame
import time


# ============ CONFIGURATION ============
class Config:
    """All settings in one place"""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 650
    AUCTION_DURATION = 600  # 10 minutes (change to 60 for testing)
    CURRENCY = "£"
    
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
    CARD_BG = (60, 60, 90)
    INPUT_BG = (50, 50, 70)
    
    # Grid settings
    COLS = 3
    CARD_WIDTH = 220
    CARD_HEIGHT = 140
    MARGIN_X = 30
    MARGIN_Y = 20
    START_Y = 100


# ============ DATABASE ============
class Database:
    """Simple database to store bids"""
    
    def __init__(self):
        self.bids = []
        self.items = [
            {"id": 1, "name": "Wireless Headphones", "description": "RGB Gaming Edition", "starting_price": 50.00, "max_bid": 150.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 2, "name": "Gaming Controller", "description": "Glow in the dark!", "starting_price": 35.00, "max_bid": 100.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 3, "name": "Phone Ring Light", "description": "Perfect for TikToks!", "starting_price": 15.00, "max_bid": 50.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 4, "name": "LED Backpack", "description": "Changes colors!", "starting_price": 40.00, "max_bid": 120.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 5, "name": "Mini Skateboard", "description": "Fingerboard pro set", "starting_price": 10.00, "max_bid": 40.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 6, "name": "Bubble Tea Kit", "description": "Make your own boba!", "starting_price": 20.00, "max_bid": 60.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 7, "name": "Karaoke Mic", "description": "Bluetooth speaker", "starting_price": 25.00, "max_bid": 80.00, "current_bid": 0, "highest_bidder": ""},
            {"id": 8, "name": "LED Strip Lights", "description": "16 million colors!", "starting_price": 18.00, "max_bid": 55.00, "current_bid": 0, "highest_bidder": ""},
        ]
    
    def save_bid(self, item_id, bidder_name, bid_amount):
        """Save a bid to the database"""
        bid_record = {
            "item_id": item_id,
            "bidder_name": bidder_name,
            "bid_amount": bid_amount,
            "timestamp": time.time()
        }
        self.bids.append(bid_record)
        print(f"Saved to DB: {bid_record}")
    
    def add_item(self, name, description, starting_price, max_bid):
        """Add a new item to the auction"""
        new_item = {
            "id": len(self.items) + 1,
            "name": name,
            "description": description or "No description",
            "starting_price": starting_price,
            "max_bid": max_bid,
            "current_bid": 0,
            "highest_bidder": ""
        }
        self.items.append(new_item)
        return new_item
    
    def print_all_bids(self):
        """Print all bids to terminal"""
        print("\n=== FINAL DATABASE ===")
        for bid in self.bids:
            print(bid)
        print("======================\n")


# ============ UI COMPONENTS ============
class UIComponents:
    """Reusable UI drawing functions"""
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.font = fonts['normal']
        self.small_font = fonts['small']
        self.title_font = fonts['title']
        self.big_font = fonts['big']
    
    def draw_button(self, text, x, y, width, height, color, text_color=None):
        """Draw a button and return its rect"""
        if text_color is None:
            text_color = Config.WHITE
        
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, Config.WHITE, rect, 2, border_radius=8)
        
        text_surface = self.font.render(text, True, text_color)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        return rect
    
    def draw_input_box(self, label, value, x, y, width, is_active):
        """Draw an input box and return its rect"""
        # Label
        label_surface = self.small_font.render(label, True, Config.LIGHT_GRAY)
        self.screen.blit(label_surface, (x, y - 20))
        
        # Box
        rect = pygame.Rect(x, y, width, 35)
        color = Config.PINK if is_active else Config.DARK_GRAY
        pygame.draw.rect(self.screen, Config.INPUT_BG, rect, border_radius=5)
        pygame.draw.rect(self.screen, color, rect, 2, border_radius=5)
        
        # Text
        text_surface = self.font.render(value, True, Config.WHITE)
        self.screen.blit(text_surface, (x + 10, y + 8))
        
        return rect
    
    def draw_timer(self, minutes, seconds, remaining, x, y, use_big=False):
        """Draw the countdown timer"""
        timer_color = Config.RED if remaining < 60 else Config.GREEN
        font_to_use = self.big_font if use_big else self.title_font
        timer_text = font_to_use.render(f"{minutes:02d}:{seconds:02d}", True, timer_color)
        self.screen.blit(timer_text, (x, y))
    
    def draw_title(self, text, y, color=None):
        """Draw centered title"""
        if color is None:
            color = Config.PINK
        title = self.title_font.render(text, True, color)
        self.screen.blit(title, (Config.SCREEN_WIDTH // 2 - title.get_width() // 2, y))


# ============ SCREENS ============
class ItemsScreen:
    """The main screen showing all auction items"""
    
    def __init__(self, screen, ui, db):
        self.screen = screen
        self.ui = ui
        self.db = db
        self.scroll_y = 0
        self.card_rects = []
    
    def get_total_height(self):
        """Calculate total height needed for all items"""
        num_items = len(self.db.items) + 1  # +1 for add button
        rows = (num_items + Config.COLS - 1) // Config.COLS
        return Config.START_Y + rows * (Config.CARD_HEIGHT + Config.MARGIN_Y) + 80
    
    def handle_scroll(self, direction):
        """Handle mouse wheel scrolling"""
        total_height = self.get_total_height()
        max_scroll = max(0, total_height - Config.SCREEN_HEIGHT + 100)
        
        # direction is positive when scrolling up, negative when scrolling down
        self.scroll_y += direction * 40
        # Clamp scroll between -max_scroll (scrolled down) and 0 (at top)
        self.scroll_y = max(-max_scroll, min(0, self.scroll_y))
    
    def draw(self, timer_info):
        """Draw the items screen"""
        minutes, seconds, remaining = timer_info
        
        self.screen.fill(Config.DARK_BG)
        
        # Timer
        self.ui.draw_timer(minutes, seconds, remaining, Config.SCREEN_WIDTH - 150, 20)
        
        # Title
        title = self.ui.title_font.render("Auction Zone", True, Config.PINK)
        self.screen.blit(title, (30, 20))
        
        # Scroll hint
        if len(self.db.items) > 6:
            hint = self.ui.small_font.render("Scroll to see more items", True, Config.LIGHT_GRAY)
            self.screen.blit(hint, (Config.SCREEN_WIDTH // 2 - hint.get_width() // 2, 65))
        
        # Draw items grid
        self.card_rects = []
        for i, item in enumerate(self.db.items):
            row = i // Config.COLS
            col = i % Config.COLS
            
            x = Config.MARGIN_X + col * (Config.CARD_WIDTH + Config.MARGIN_X)
            y = Config.START_Y + row * (Config.CARD_HEIGHT + Config.MARGIN_Y) + self.scroll_y
            
            rect = pygame.Rect(x, y, Config.CARD_WIDTH, Config.CARD_HEIGHT)
            self.card_rects.append(rect)
            
            # Only draw if visible
            if y + Config.CARD_HEIGHT > 80 and y < Config.SCREEN_HEIGHT - 70:
                self._draw_item_card(item, x, y, rect)
        
        # Draw "+" add button as a card
        add_index = len(self.db.items)
        row = add_index // Config.COLS
        col = add_index % Config.COLS
        add_x = Config.MARGIN_X + col * (Config.CARD_WIDTH + Config.MARGIN_X)
        add_y = Config.START_Y + row * (Config.CARD_HEIGHT + Config.MARGIN_Y) + self.scroll_y
        
        add_rect = pygame.Rect(add_x, add_y, Config.CARD_WIDTH, Config.CARD_HEIGHT)
        
        if add_y + Config.CARD_HEIGHT > 80 and add_y < Config.SCREEN_HEIGHT - 70:
            pygame.draw.rect(self.screen, (40, 40, 60), add_rect, border_radius=12)
            pygame.draw.rect(self.screen, Config.PURPLE, add_rect, 2, border_radius=12)
            plus_text = self.ui.title_font.render("+", True, Config.PURPLE)
            self.screen.blit(plus_text, (add_x + Config.CARD_WIDTH // 2 - plus_text.get_width() // 2, 
                                          add_y + Config.CARD_HEIGHT // 2 - plus_text.get_height() // 2))
        
        # End Auction button (fixed at bottom)
        pygame.draw.rect(self.screen, Config.DARK_BG, (0, Config.SCREEN_HEIGHT - 70, Config.SCREEN_WIDTH, 70))
        end_btn = self.ui.draw_button("End Auction", Config.SCREEN_WIDTH // 2 - 70, Config.SCREEN_HEIGHT - 60, 140, 40, Config.RED)
        
        return add_rect, end_btn
    
    def _draw_item_card(self, item, x, y, rect):
        """Draw a single item card"""
        # Card background
        pygame.draw.rect(self.screen, Config.CARD_BG, rect, border_radius=12)
        pygame.draw.rect(self.screen, Config.PURPLE, rect, 2, border_radius=12)
        
        # Item name
        name_text = self.ui.font.render(item["name"][:18], True, Config.WHITE)
        self.screen.blit(name_text, (x + 10, y + 15))
        
        # Description
        desc_text = self.ui.small_font.render(item["description"][:25], True, Config.LIGHT_GRAY)
        self.screen.blit(desc_text, (x + 10, y + 42))
        
        # Current bid info
        if item["current_bid"] > 0:
            bid_label = self.ui.small_font.render("Current Bid:", True, Config.GREEN)
            self.screen.blit(bid_label, (x + 10, y + 70))
            bid_text = self.ui.font.render(f"{Config.CURRENCY}{item['current_bid']:.2f}", True, Config.GREEN)
            self.screen.blit(bid_text, (x + 10, y + 88))
            bidder_text = self.ui.small_font.render(f"by {item['highest_bidder'][:12]}", True, Config.LIGHT_GRAY)
            self.screen.blit(bidder_text, (x + 10, y + 115))
        else:
            price_label = self.ui.small_font.render("Starting:", True, Config.LIGHT_GRAY)
            self.screen.blit(price_label, (x + 10, y + 80))
            price_text = self.ui.font.render(f"{Config.CURRENCY}{item['starting_price']:.2f}", True, Config.PINK)
            self.screen.blit(price_text, (x + 10, y + 100))
    
    def get_clicked_item(self, mouse_pos):
        """Check if an item was clicked and return it"""
        for i, rect in enumerate(self.card_rects):
            if rect.collidepoint(mouse_pos):
                return self.db.items[i]
        return None


class DetailScreen:
    """Screen showing item details and bid form"""
    
    def __init__(self, screen, ui, db):
        self.screen = screen
        self.ui = ui
        self.db = db
        self.item = None
        self.name_input = ""
        self.bid_input = ""
        self.active_input = None
        self.message = ""
    
    def set_item(self, item):
        """Set the item to display"""
        self.item = item
        self.name_input = ""
        self.bid_input = ""
        self.active_input = None
        self.message = ""
    
    def draw(self, timer_info):
        """Draw the detail screen"""
        minutes, seconds, remaining = timer_info
        
        self.screen.fill(Config.DARK_BG)
        
        # Back button
        back_btn = self.ui.draw_button("< Back", 20, 20, 80, 35, Config.DARK_GRAY)
        
        # Timer
        self.ui.draw_timer(minutes, seconds, remaining, Config.SCREEN_WIDTH - 120, 25, use_big=True)
        
        # Title
        self.ui.draw_title("Item Information", 80)
        
        # Item details box
        self._draw_item_details()
        
        # Input form box
        name_rect, bid_rect = self._draw_input_form()
        
        # BID button
        bid_btn = self.ui.draw_button("BID", 250, 380, 300, 50, Config.GREEN, Config.BLACK)
        
        # Message
        if self.message:
            msg_color = Config.GREEN if "Success" in self.message else Config.RED
            msg_surface = self.ui.font.render(self.message, True, msg_color)
            self.screen.blit(msg_surface, (Config.SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, 450))
        
        return back_btn, name_rect, bid_rect, bid_btn
    
    def _draw_item_details(self):
        """Draw the item details box"""
        detail_box = pygame.Rect(50, 140, 350, 200)
        pygame.draw.rect(self.screen, Config.INPUT_BG, detail_box, border_radius=10)
        pygame.draw.rect(self.screen, Config.PURPLE, detail_box, 2, border_radius=10)
        
        info_x = 70
        info_y = 160
        
        # Item name
        name_label = self.ui.font.render(f"Item: {self.item['name']}", True, Config.WHITE)
        self.screen.blit(name_label, (info_x, info_y))
        
        # Current price
        current_price = self.item['current_bid'] if self.item['current_bid'] > 0 else self.item['starting_price']
        current_label = self.ui.font.render(f"Current Price: {Config.CURRENCY}{current_price:.2f}", True, Config.GREEN)
        self.screen.blit(current_label, (info_x, info_y + 40))
        
        # Original price
        original_label = self.ui.font.render(f"Original Price: {Config.CURRENCY}{self.item['starting_price']:.2f}", True, Config.LIGHT_GRAY)
        self.screen.blit(original_label, (info_x, info_y + 80))
        
        # Bid limit
        limit_label = self.ui.font.render(f"Bid Limit: {Config.CURRENCY}{self.item['max_bid']:.2f}", True, Config.RED)
        self.screen.blit(limit_label, (info_x, info_y + 120))
        
        # Highest bidder
        if self.item['highest_bidder']:
            bidder_label = self.ui.small_font.render(f"Highest Bidder: {self.item['highest_bidder']}", True, Config.GREEN)
            self.screen.blit(bidder_label, (info_x, info_y + 155))
    
    def _draw_input_form(self):
        """Draw the input form box"""
        input_box = pygame.Rect(430, 140, 320, 200)
        pygame.draw.rect(self.screen, Config.INPUT_BG, input_box, border_radius=10)
        pygame.draw.rect(self.screen, Config.PURPLE, input_box, 2, border_radius=10)
        
        details_title = self.ui.font.render("Enter Your Details", True, Config.WHITE)
        self.screen.blit(details_title, (480, 155))
        
        name_rect = self.ui.draw_input_box("Name:", self.name_input, 450, 210, 280, self.active_input == "name")
        bid_rect = self.ui.draw_input_box(f"Bid Price: {Config.CURRENCY}", self.bid_input, 450, 280, 280, self.active_input == "bid")
        
        return name_rect, bid_rect
    
    def process_bid(self):
        """Process the bid submission"""
        if self.name_input.strip() == "":
            self.message = "Please enter your name!"
            return False
        
        if self.bid_input.strip() == "":
            self.message = "Please enter a bid amount!"
            return False
        
        try:
            bid_amount = float(self.bid_input)
            min_bid = self.item["current_bid"] if self.item["current_bid"] > 0 else self.item["starting_price"]
            
            if bid_amount <= min_bid:
                self.message = f"Bid must be higher than {Config.CURRENCY}{min_bid:.2f}!"
                return False
            
            if bid_amount > self.item["max_bid"]:
                self.message = f"Bid cannot exceed {Config.CURRENCY}{self.item['max_bid']:.2f}!"
                return False
            
            # Valid bid!
            self.item["current_bid"] = bid_amount
            self.item["highest_bidder"] = self.name_input
            self.db.save_bid(self.item["id"], self.name_input, bid_amount)
            self.message = "Success! Your bid has been placed!"
            self.name_input = ""
            self.bid_input = ""
            return True
            
        except ValueError:
            self.message = "Please enter a valid number!"
            return False
    
    def handle_key(self, event):
        """Handle keyboard input"""
        if event.key == pygame.K_BACKSPACE:
            if self.active_input == "name":
                self.name_input = self.name_input[:-1]
            elif self.active_input == "bid":
                self.bid_input = self.bid_input[:-1]
        elif event.key == pygame.K_TAB:
            self.active_input = "bid" if self.active_input == "name" else "name"
        else:
            char = event.unicode
            if self.active_input == "name" and len(self.name_input) < 20:
                self.name_input += char
            elif self.active_input == "bid" and len(self.bid_input) < 10:
                if char.isdigit() or char == ".":
                    self.bid_input += char


class AddItemScreen:
    """Screen for adding a new auction item"""
    
    def __init__(self, screen, ui, db):
        self.screen = screen
        self.ui = ui
        self.db = db
        self.name_input = ""
        self.desc_input = ""
        self.price_input = ""
        self.max_input = ""
        self.active_input = None
        self.message = ""
    
    def reset(self):
        """Reset all inputs"""
        self.name_input = ""
        self.desc_input = ""
        self.price_input = ""
        self.max_input = ""
        self.active_input = None
        self.message = ""
    
    def draw(self):
        """Draw the add item screen"""
        self.screen.fill(Config.DARK_BG)
        
        # Back button
        back_btn = self.ui.draw_button("< Back", 20, 20, 80, 35, Config.DARK_GRAY)
        
        # Title
        self.ui.draw_title("Add New Item", 80)
        
        # Input fields
        name_rect = self.ui.draw_input_box("Item Name:", self.name_input, 200, 180, 400, self.active_input == "name")
        desc_rect = self.ui.draw_input_box("Description:", self.desc_input, 200, 260, 400, self.active_input == "desc")
        price_rect = self.ui.draw_input_box(f"Starting Price: {Config.CURRENCY}", self.price_input, 200, 340, 180, self.active_input == "price")
        max_rect = self.ui.draw_input_box(f"Max Bid: {Config.CURRENCY}", self.max_input, 420, 340, 180, self.active_input == "max")
        
        # Add button
        add_btn = self.ui.draw_button("Add Item", 300, 420, 200, 50, Config.GREEN, Config.BLACK)
        
        # Message
        if self.message:
            msg_color = Config.RED
            msg_surface = self.ui.font.render(self.message, True, msg_color)
            self.screen.blit(msg_surface, (Config.SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, 490))
        
        return back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn
    
    def add_item(self):
        """Try to add the new item"""
        if not self.name_input.strip():
            self.message = "Please enter an item name!"
            return False
        
        if not self.price_input.strip() or not self.max_input.strip():
            self.message = "Please enter prices!"
            return False
        
        try:
            starting_price = float(self.price_input)
            max_bid = float(self.max_input)
            
            if max_bid <= starting_price:
                self.message = "Max bid must be higher than starting price!"
                return False
            
            self.db.add_item(self.name_input, self.desc_input, starting_price, max_bid)
            return True
            
        except ValueError:
            self.message = "Please enter valid numbers for prices!"
            return False
    
    def handle_key(self, event):
        """Handle keyboard input"""
        if event.key == pygame.K_BACKSPACE:
            if self.active_input == "name":
                self.name_input = self.name_input[:-1]
            elif self.active_input == "desc":
                self.desc_input = self.desc_input[:-1]
            elif self.active_input == "price":
                self.price_input = self.price_input[:-1]
            elif self.active_input == "max":
                self.max_input = self.max_input[:-1]
        elif event.key == pygame.K_TAB:
            order = ["name", "desc", "price", "max"]
            if self.active_input in order:
                idx = order.index(self.active_input)
                self.active_input = order[(idx + 1) % len(order)]
        else:
            char = event.unicode
            if self.active_input == "name" and len(self.name_input) < 25:
                self.name_input += char
            elif self.active_input == "desc" and len(self.desc_input) < 30:
                self.desc_input += char
            elif self.active_input in ["price", "max"]:
                if char.isdigit() or char == ".":
                    if self.active_input == "price" and len(self.price_input) < 8:
                        self.price_input += char
                    elif self.active_input == "max" and len(self.max_input) < 8:
                        self.max_input += char


class ResultsScreen:
    """Screen showing auction results"""
    
    def __init__(self, screen, ui, db):
        self.screen = screen
        self.ui = ui
        self.db = db
        self.scroll_y = 0
        self.printed = False
    
    def handle_scroll(self, direction):
        """Handle mouse wheel scrolling"""
        total_height = 100 + len(self.db.items) * 60 + 80
        max_scroll = max(0, total_height - Config.SCREEN_HEIGHT + 80)
        
        self.scroll_y += direction * 30
        self.scroll_y = max(-max_scroll, min(0, self.scroll_y))
    
    def draw(self):
        """Draw the results screen"""
        self.screen.fill(Config.DARK_BG)
        
        # Title
        self.ui.draw_title("Auction Results!", 30)
        
        # Show results with scrolling
        y = 100 + self.scroll_y
        for item in self.db.items:
            if y + 50 > 70 and y < Config.SCREEN_HEIGHT - 80:
                box = pygame.Rect(50, y, Config.SCREEN_WIDTH - 100, 50)
                pygame.draw.rect(self.screen, Config.INPUT_BG, box, border_radius=8)
                pygame.draw.rect(self.screen, Config.PURPLE, box, 2, border_radius=8)
                
                # Item name
                name_text = self.ui.font.render(item["name"][:20], True, Config.WHITE)
                self.screen.blit(name_text, (70, y + 15))
                
                # Winner
                if item["current_bid"] > 0:
                    winner_text = self.ui.font.render(f"Winner: {item['highest_bidder']} - {Config.CURRENCY}{item['current_bid']:.2f}", True, Config.GREEN)
                else:
                    winner_text = self.ui.font.render("No bids", True, Config.DARK_GRAY)
                self.screen.blit(winner_text, (350, y + 15))
            
            y += 60
        
        # Print database once
        if not self.printed:
            self.db.print_all_bids()
            self.printed = True
        
        # Close button (fixed at bottom)
        pygame.draw.rect(self.screen, Config.DARK_BG, (0, Config.SCREEN_HEIGHT - 80, Config.SCREEN_WIDTH, 80))
        close_btn = self.ui.draw_button("Close", Config.SCREEN_WIDTH // 2 - 60, Config.SCREEN_HEIGHT - 70, 120, 45, Config.RED)
        
        return close_btn


# ============ MAIN GAME CLASS ============
class AuctionGame:
    """Main game controller"""
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Group 2 - Auction Zone")
        
        # Fonts
        self.fonts = {
            'normal': pygame.font.Font(None, 26),
            'small': pygame.font.Font(None, 20),
            'title': pygame.font.Font(None, 48),
            'big': pygame.font.Font(None, 36)
        }
        
        # Database
        self.db = Database()
        
        # UI Components
        self.ui = UIComponents(self.screen, self.fonts)
        
        # Screens
        self.items_screen = ItemsScreen(self.screen, self.ui, self.db)
        self.detail_screen = DetailScreen(self.screen, self.ui, self.db)
        self.add_item_screen = AddItemScreen(self.screen, self.ui, self.db)
        self.results_screen = ResultsScreen(self.screen, self.ui, self.db)
        
        # State
        self.current_screen = "items"
        self.start_time = time.time()
        self.running = True
        self.clock = pygame.time.Clock()
    
    def get_time_remaining(self):
        """Calculate remaining auction time"""
        elapsed = time.time() - self.start_time
        remaining = Config.AUCTION_DURATION - elapsed
        if remaining < 0:
            remaining = 0
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return minutes, seconds, remaining
    
    def run(self):
        """Main game loop"""
        while self.running:
            timer_info = self.get_time_remaining()
            _, _, remaining = timer_info
            
            # Auto-end when time is up
            if remaining <= 0 and self.current_screen != "results":
                self.current_screen = "results"
            
            self._handle_events(timer_info)
            self._draw(timer_info)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
    def _handle_events(self, timer_info):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEWHEEL:
                if self.current_screen == "items":
                    self.items_screen.handle_scroll(event.y)
                elif self.current_screen == "results":
                    self.results_screen.handle_scroll(event.y)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Only respond to left mouse button click (button 1)
                if event.button == 1:
                    self._handle_click(pygame.mouse.get_pos(), timer_info)
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event)
    
    def _handle_click(self, mouse_pos, timer_info):
        """Handle mouse clicks"""
        if self.current_screen == "items":
            add_rect, end_btn = self.items_screen.draw(timer_info)
            
            # Check item clicks
            clicked_item = self.items_screen.get_clicked_item(mouse_pos)
            if clicked_item:
                self.detail_screen.set_item(clicked_item)
                self.current_screen = "detail"
            
            # Check add button
            elif add_rect.collidepoint(mouse_pos):
                self.add_item_screen.reset()
                self.current_screen = "add_item"
            
            # Check end button
            elif end_btn.collidepoint(mouse_pos):
                self.current_screen = "results"
        
        elif self.current_screen == "detail":
            back_btn, name_rect, bid_rect, bid_btn = self.detail_screen.draw(timer_info)
            
            if back_btn.collidepoint(mouse_pos):
                self.current_screen = "items"
            elif name_rect.collidepoint(mouse_pos):
                self.detail_screen.active_input = "name"
            elif bid_rect.collidepoint(mouse_pos):
                self.detail_screen.active_input = "bid"
            elif bid_btn.collidepoint(mouse_pos):
                self.detail_screen.process_bid()
        
        elif self.current_screen == "add_item":
            back_btn, name_rect, desc_rect, price_rect, max_rect, add_btn = self.add_item_screen.draw()
            
            if back_btn.collidepoint(mouse_pos):
                self.current_screen = "items"
            elif name_rect.collidepoint(mouse_pos):
                self.add_item_screen.active_input = "name"
            elif desc_rect.collidepoint(mouse_pos):
                self.add_item_screen.active_input = "desc"
            elif price_rect.collidepoint(mouse_pos):
                self.add_item_screen.active_input = "price"
            elif max_rect.collidepoint(mouse_pos):
                self.add_item_screen.active_input = "max"
            elif add_btn.collidepoint(mouse_pos):
                if self.add_item_screen.add_item():
                    self.current_screen = "items"
        
        elif self.current_screen == "results":
            close_btn = self.results_screen.draw()
            if close_btn.collidepoint(mouse_pos):
                self.running = False
    
    def _handle_key(self, event):
        """Handle keyboard input"""
        if self.current_screen == "detail":
            self.detail_screen.handle_key(event)
        elif self.current_screen == "add_item":
            self.add_item_screen.handle_key(event)
    
    def _draw(self, timer_info):
        """Draw the current screen"""
        if self.current_screen == "items":
            self.items_screen.draw(timer_info)
        elif self.current_screen == "detail":
            self.detail_screen.draw(timer_info)
        elif self.current_screen == "add_item":
            self.add_item_screen.draw()
        elif self.current_screen == "results":
            self.results_screen.draw()


# ============ RUN THE GAME ============
if __name__ == "__main__":
    game = AuctionGame()
    game.run()
