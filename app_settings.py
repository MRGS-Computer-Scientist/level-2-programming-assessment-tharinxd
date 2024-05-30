import csv

# Define users dictionary to store credentials
users = {}

# Function to load stored credentials
def load_credentials():
    try:
        with open('credentials.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                username, password = row
                users[username] = password
        print("Credentials loaded successfully.")
        print("Loaded users:", users)  # Print loaded users for debugging
    except FileNotFoundError:
        print("Credentials file not found.")
        # Create an empty file if it doesn't exist
        with open('credentials.csv', mode='w', newline=''):
            pass
    except Exception as e:
        print("Error loading credentials:", e)

# Function to save new credentials
def save_credentials(username, password):
    try:
        with open('credentials.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
        print("Credentials saved successfully.")
    except Exception as e:
        print("Error saving credentials:", e)
