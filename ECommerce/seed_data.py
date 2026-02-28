import random
import models
from database import sessionLocal

# Dummy data generators
first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emma", "James", "Olivia", "Robert", "William", 
               "Sophia", "Daniel", "Matthew", "Andrew", "Jessica", "Joseph", "Ashley", "Christopher", "Amanda", "Kevin"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

product_names = ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch", "Camera", "Keyboard", "Mouse", 
                 "Monitor", "Printer", "Speaker", "Microphone", "Webcam", "Charger", "Cable", "SSD", "RAM",
                 "GPU", "CPU", "Motherboard", "Case", "Power Supply", "Router", "Pen Drive", "External HDD",
                 "Monitor Stand", "Desk Lamp", "Office Chair", "Desk Pad", "Cable Organizer", "Phone Case",
                 "Screen Protector", "Power Bank", "Wireless Charger", "Bluetooth Adapter", "HDMI Cable", "USB Hub"]

product_adjectives = ["Pro", "Plus", "Ultra", "Max", "Lite", "Air", "Mini", "Premium", "Standard", "Basic",
                      "Advanced", "Elite", "Super", "Mega", "Hyper", "Smart", "Wireless", "Portable", "Compact", "Digital"]

order_statuses = ["pending", "completed"]

def generate_users(db, count=40):
    """Generate dummy users"""
    users = []
    for i in range(count):
        first = random.choice(first_names)
        last = random.choice(last_names)
        username = f"{first.lower()}{last.lower()}{i+1}"
        email = f"{first.lower()}.{last.lower()}{i+1}@example.com"
        
        user = models.User(username=username, email=email)
        users.append(user)
        db.add(user)
    
    db.commit()
    return users

def generate_products(db, count=40):
    """Generate dummy products"""
    products = []
    for i in range(count):
        name = f"{random.choice(product_adjectives)} {random.choice(product_names)}"
        price = round(random.uniform(10.0, 2000.0), 2)
        stock = random.randint(0, 100)
        
        product = models.Product(name=name, price=price, stock=stock)
        products.append(product)
        db.add(product)
    
    db.commit()
    return products

def generate_orders(db, users, count=40):
    """Generate dummy orders"""
    orders = []
    for i in range(count):
        user = random.choice(users)
        total_amount = round(random.uniform(10.0, 5000.0), 2)
        status = random.choice(order_statuses)
        
        order = models.Order(total_amount=total_amount, status=status, user_id=user.id)
        orders.append(order)
        db.add(order)
    
    db.commit()
    return orders

def generate_order_items(db, orders, products, count=40):
    """Generate dummy order items"""
    for i in range(count):
        order = random.choice(orders)
        product = random.choice(products)
        quantity = random.randint(1, 10)
        
        order_item = models.OrderItem(order_id=order.id, product_id=product.id, quantity=quantity)
        db.add(order_item)
    
    db.commit()

def seed_database():
    """Seed the database with dummy data (adds to existing data)"""
    db = sessionLocal()
    try:
        # Get existing users to use for orders (if any exist)
        existing_users = db.query(models.User).all()
        
        # Generate dummy data
        print("Creating users...")
        users = generate_users(db, 40)
        print(f"Created {len(users)} users")
        
        # Use both existing and new users for orders
        all_users = existing_users + users if existing_users else users
        
        print("Creating products...")
        products = generate_products(db, 40)
        print(f"Created {len(products)} products")
        
        print("Creating orders...")
        orders = generate_orders(db, all_users, 40)
        print(f"Created {len(orders)} orders")
        
        print("Creating order items...")
        generate_order_items(db, orders, products, 40)
        print("Created 40 order items")
        
        return {
            "message": "Database seeded successfully",
            "users_created": len(users),
            "products_created": len(products),
            "orders_created": len(orders),
            "order_items_created": 40
        }
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    result = seed_database()
    print(result)
