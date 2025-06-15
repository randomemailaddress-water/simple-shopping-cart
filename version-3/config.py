# Configuration settings for the shopping cart program

# Importing os module for file path handling
import os

# Database settings
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shop.db')

# Variable limits
MAX_USERNAME_LENGTH = 20
MAX_ITEM_NAME_LENGTH = 50
MAX_PRICE = 10000.0
MAX_QUANTITY = 100 # I wouldn't think anyone would want to add more than 100 of a specific item to their cart.

# Security stuff
MIN_PASSWORD_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 3

# Discount settings
DISCOUNT_THRESHOLD = 100  # Orders over $100 get discount
DISCOUNT_PERCENTAGE = 10  # 10% discount