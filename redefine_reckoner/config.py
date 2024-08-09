import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
DB_FILE = os.path.join(PROJECT_ROOT, 'database', 'ready_reckoner.db')

# Data files
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
CHECKOUT_TYPES_FILE = os.path.join(DATA_DIR, 'checkout_types.json')
VERTICAL_NAMES_FILE = os.path.join(DATA_DIR, 'vertical_names.json')
METHODS_FILE = os.path.join(DATA_DIR, 'methods.json')