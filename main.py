from app_settings import load_credentials
from app import create_login_window

# Load stored credentials
load_credentials()
print("Loaded users:", users)  # Print loaded users for debugging

# Start the application
create_login_window()
