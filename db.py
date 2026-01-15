
# Database module - handles all database operations using SQLite
import sqlite3
import time

DATABASE_FILE = "auction.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            starting_price REAL NOT NULL,
            max_bid REAL NOT NULL,
            current_bid REAL DEFAULT 0,
            highest_bidder TEXT DEFAULT ''
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            bidder_name TEXT NOT NULL,
            bid_amount REAL NOT NULL,
            timestamp REAL,
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    """)
    conn.commit()
    conn.close()

def add_default_items():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    if count == 0:
        default_items = [
            ("Wireless Headphones", "RGB Gaming Edition", 50.00, 150.00),
            ("Gaming Controller", "Glow in the dark!", 35.00, 100.00),
            ("Phone Ring Light", "Perfect for TikToks!", 15.00, 50.00),
            ("LED Backpack", "Changes colors!", 40.00, 120.00),
            ("Mini Skateboard", "Fingerboard pro set", 10.00, 40.00),
            ("Bubble Tea Kit", "Make your own boba!", 20.00, 60.00),
            ("Karaoke Mic", "Bluetooth speaker", 25.00, 80.00),
            ("LED Strip Lights", "16 million colors!", 18.00, 55.00),
        ]
        cursor.executemany("""
            INSERT INTO items (name, description, starting_price, max_bid)
            VALUES (?, ?, ?, ?)
        """, default_items)
        conn.commit()
        print("Added default items to database!")
    conn.close()

def get_all_items():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, starting_price, max_bid, current_bid, highest_bidder
        FROM items
    """)
    rows = cursor.fetchall()
    conn.close()
    items = []
    for row in rows:
        items.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "starting_price": row[3],
            "max_bid": row[4],
            "current_bid": row[5],
            "highest_bidder": row[6]
        })
    return items

def get_item(item_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "starting_price": row[3],
            "max_bid": row[4],
            "current_bid": row[5],
            "highest_bidder": row[6]
        }
    return None

def add_item(name, description, starting_price, max_bid):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO items (name, description, starting_price, max_bid)
        VALUES (?, ?, ?, ?)
    """, (name, description, starting_price, max_bid))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"Added item: {name} (ID: {new_id})")
    return new_id

def update_bid(item_id, bid_amount, bidder_name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE items 
        SET current_bid = ?, highest_bidder = ?
        WHERE id = ?
    """, (bid_amount, bidder_name, item_id))
    cursor.execute("""
        INSERT INTO bids (item_id, bidder_name, bid_amount, timestamp)
        VALUES (?, ?, ?, ?)
    """, (item_id, bidder_name, bid_amount, time.time()))
    conn.commit()
    conn.close()
    print(f"Bid saved: {bidder_name} bid £{bid_amount:.2f} on item {item_id}")

def get_all_bids():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, b.item_id, i.name, b.bidder_name, b.bid_amount, b.timestamp
        FROM bids b
        JOIN items i ON b.item_id = i.id
        ORDER BY b.timestamp
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def reset_auction():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET current_bid = 0, highest_bidder = ''")
    cursor.execute("DELETE FROM bids")
    conn.commit()
    conn.close()
    print("Auction reset!")

def print_results():
    print("\n" + "=" * 50)
    print("AUCTION RESULTS")
    print("=" * 50)
    items = get_all_items()
    for item in items:
        if item["current_bid"] > 0:
            print(f"✓ {item['name']}: {item['highest_bidder']} won with £{item['current_bid']:.2f}")
        else:
            print(f"✗ {item['name']}: No bids")
    print("\n" + "-" * 50)
    print("ALL BIDS:")
    print("-" * 50)
    bids = get_all_bids()
    for bid in bids:
        print(f"  {bid[3]} bid £{bid[4]:.2f} on {bid[2]}")
    print("=" * 50 + "\n")

def reset_to_default_items():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bids")
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()
    add_default_items()
    print("Database reset to original 8 items!")

def init():
    create_tables()
    add_default_items()

# Run init when module loads
init()
"""
Database module - handles all database operations using SQLite
SQLite is a simple file-based database built into Python!
"""
import sqlite3
import time

# Database file name
DATABASE_FILE = "auction.db"


def create_tables():
    """Create the database tables if they don't exist"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            starting_price REAL NOT NULL,
            max_bid REAL NOT NULL,
            current_bid REAL DEFAULT 0,
            highest_bidder TEXT DEFAULT ''
        )
    """)
    
    # Create bids table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            bidder_name TEXT NOT NULL,
            bid_amount REAL NOT NULL,
            timestamp REAL,
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    """)
    
    conn.commit()
    conn.close()


def add_default_items():
    """Add default items if the database is empty"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if items exist
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    
    if count == 0:
        default_items = [
            ("Wireless Headphones", "RGB Gaming Edition", 50.00, 150.00),
            ("Gaming Controller", "Glow in the dark!", 35.00, 100.00),
            ("Phone Ring Light", "Perfect for TikToks!", 15.00, 50.00),
            ("LED Backpack", "Changes colors!", 40.00, 120.00),
            ("Mini Skateboard", "Fingerboard pro set", 10.00, 40.00),
            ("Bubble Tea Kit", "Make your own boba!", 20.00, 60.00),
            ("Karaoke Mic", "Bluetooth speaker", 25.00, 80.00),
            ("LED Strip Lights", "16 million colors!", 18.00, 55.00),
        ]
        
        cursor.executemany("""
            INSERT INTO items (name, description, starting_price, max_bid)
            VALUES (?, ?, ?, ?)
        """, default_items)
        
        conn.commit()
        print("Added default items to database!")
    
    conn.close()


def get_all_items():
    """Get all items from the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, description, starting_price, max_bid, current_bid, highest_bidder
        FROM items
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries (easier to use)
    items = []
    for row in rows:
        items.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "starting_price": row[3],
            "max_bid": row[4],
            "current_bid": row[5],
            "highest_bidder": row[6]
        })
    
    return items


def get_item(item_id):
    """Get a single item by ID"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "starting_price": row[3],
            "max_bid": row[4],
            "current_bid": row[5],
            "highest_bidder": row[6]
        }
    return None


def add_item(name, description, starting_price, max_bid):
    """Add a new item to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO items (name, description, starting_price, max_bid)
        VALUES (?, ?, ?, ?)
    """, (name, description, starting_price, max_bid))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"Added item: {name} (ID: {new_id})")
    return new_id


def update_bid(item_id, bid_amount, bidder_name):
    """Update the current bid on an item"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Update the item
    cursor.execute("""
        UPDATE items 
        SET current_bid = ?, highest_bidder = ?
        WHERE id = ?
    """, (bid_amount, bidder_name, item_id))
    
    # Save to bids history
    cursor.execute("""
        INSERT INTO bids (item_id, bidder_name, bid_amount, timestamp)
        VALUES (?, ?, ?, ?)
    """, (item_id, bidder_name, bid_amount, time.time()))
    
    conn.commit()
    conn.close()
    
    print(f"Bid saved: {bidder_name} bid £{bid_amount:.2f} on item {item_id}")


def get_all_bids():
    """Get all bids from the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.id, b.item_id, i.name, b.bidder_name, b.bid_amount, b.timestamp
        FROM bids b
        JOIN items i ON b.item_id = i.id
        ORDER BY b.timestamp
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return rows


def reset_auction():
    """Reset all bids (for a new auction)"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE items SET current_bid = 0, highest_bidder = ''")
    cursor.execute("DELETE FROM bids")
    
    conn.commit()
    conn.close()
    
    print("Auction reset!")


def print_results():
    """Print all results to terminal"""
    print("\n" + "=" * 50)
    print("AUCTION RESULTS")
    print("=" * 50)
    
    items = get_all_items()
    for item in items:
        if item["current_bid"] > 0:
            print(f"✓ {item['name']}: {item['highest_bidder']} won with £{item['current_bid']:.2f}")
        else:
            print(f"✗ {item['name']}: No bids")
    
    print("\n" + "-" * 50)
    print("ALL BIDS:")
    print("-" * 50)
    
    bids = get_all_bids()
    for bid in bids:
        print(f"  {bid[3]} bid £{bid[4]:.2f} on {bid[2]}")
    
    print("=" * 50 + "\n")
    
def reset_to_default_items():
    """Delete all items and bids, then re-add the 8 default items."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bids")
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()
    add_default_items()
    print("Database reset to original 8 items!")


# Initialize database when this module is imported
def init():
    """Initialize the database"""
    create_tables()
    add_default_items()


# Run init when module loads
init()
