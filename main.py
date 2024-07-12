import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
from home import HomeFrame
from tasks import TasksFrame
from help_support import Help_SupportFrame
import re

# List of sections for the sidebar
sections = ["Home", "Tasks", "Subjects", "Account", "Theme", "Report a Problem", "Help And Support", "Feedback"]

# File to store user credentials
credentials_file = "credentials.json"

try:
    # Attempt to load existing user credentials from file
    with open(credentials_file, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    # If file does not exist, initialize an empty user list
    users = []

# Main application class inheriting from tk.Tk
class MainApplication(tk.Tk):
    def __init__(self, username):
        # Initialize tkinter main window
        tk.Tk.__init__(self)
        
        # Set window properties
        self.title("Homework Tracker")
        self.geometry("1024x768")
        self.state('zoomed')
        self._frame = None
        
        # Store the current username
        self.username = username

        # Load and display background image
        image_path = "background.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(self, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create sidebar and main content frames
        self.sidebar = tk.Frame(self, width=320, bg='#E0E0E0')
        self.sidebar.pack(expand=False, fill='y', side='left', anchor='nw')

        self.main_content = tk.Frame(self, bg='#74a9dd')
        self.main_content.pack(expand=True, fill='both', side='right')

        # Title label for the application
        title_label = tk.Label(self.sidebar, text="Homework Tracker™", font=("Inter", 20, "bold"), bg="#E0E0E0")
        title_label.pack(pady=10)

        # Create buttons for each section in the sidebar
        self.buttons = []
        for section in sections:
            button = tk.Button(self.sidebar, text=section, font=("Inter", 14, "bold"), width=30, height=2, bg="#FFFFFF", relief="flat", command=lambda s=section: self.show_frame(s))
            button.pack(pady=5)
            self.buttons.append(button)

        # Dictionary to store frames for each section
        self.frames = {}
        for section in sections:
            frame = ttk.Frame(self.main_content)
            self.frames[section] = frame

        # Create frames for each section
        self.create_frames()

        # Initialize with Home section
        self.current_section = "Home"
        self.update_button_styles()
        self.show_frame("Home")

    # Method to switch to a new frame
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    # Create frames for all sections
    def create_frames(self):
        for section in sections:
            if section == "Home":
                self.frames[section] = HomeFrame(self.main_content, self.username)
            elif section == "Tasks":
                self.frames[section] = TasksFrame(self.main_content, self.username)
            elif section == "Help And Support":
                self.frames[section] = Help_SupportFrame(self.main_content)
            else:
                self.frames[section] = ttk.Frame(self.main_content)
            self.frames[section].pack(fill='both', expand=True)

    # Method to show a specific section/frame
    def show_frame(self, section):
        for sec in sections:
            if sec != section:
                self.frames[sec].pack_forget()  # Hide other frames
        frame = self.frames[section]
        frame.pack(fill='both', expand=True)
        frame.tkraise()  # Bring the frame to the front
        self.current_section = section
        self.update_button_styles()

    # Update the styles of sidebar buttons based on current section
    def update_button_styles(self):
        for button in self.buttons:
            if button['text'] == self.current_section:
                button.config(bg="#A9A9A9")  # Highlight current section button
            else:
                button.config(bg="#FFFFFF")

    # Method to show the login window
    def show_login_window(self):
        self.destroy()  # Close current window
        show_login_window(users)

# Function to handle login with email and password
def login_with_email(email_entry, password_entry, users, login_window):
    email = email_entry.get()
    password = password_entry.get()
    for user in users:
        if user['email'] == email and user['password'] == password:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            app = MainApplication(user['name'])  # Start main application with user's name
            app.run()
            return
    messagebox.showerror("Error", "Invalid email or password!")  # Show error if login fails

# Function to continue as a guest
def login_as_guest(login_window):
    messagebox.showinfo("Guest", "Continuing as guest.")
    login_window.destroy()
    app = MainApplication("guest")  # Start main application as guest
    app.run()

# Function to show the login window
def show_login_window(users):
    login_window = tk.Tk()
    login_window.title("Homework Tracker")
    login_window.geometry("1024x768")
    login_window.state('zoomed')
    login_window.configure(bg="white")

    title_font = ("Inter", 32, "bold")
    bold_label_font = ("Inter", 24, "bold")
    label_font = ("Inter", 15)
    entry_font = ("Inter", 18)
    button_font = ("Inter", 15, "bold")

    # Title label
    title_label = tk.Label(login_window, text="Homework Tracker™", font=title_font, bg="white")
    title_label.place(x=21, y=21)

    # Login label
    login_label = tk.Label(login_window, text="Login", font=bold_label_font, bg="white")
    login_label.place(relx=0.47, rely=0.23, anchor='center')

    # Email instruction label
    email_instruction_label = tk.Label(login_window, text="Enter your email and password to login for this app", font=label_font, bg="white")
    email_instruction_label.place(relx=0.47, rely=0.28, anchor='center')

    # Email entry field
    email_entry = tk.Entry(login_window, font=entry_font, width=35, borderwidth=0.5, relief="solid", fg="#828282")
    email_entry.insert(0, "email@domain.com")
    email_entry.place(relx=0.47, rely=0.34, anchor='center', height=40)

    # Password entry field
    password_entry = tk.Entry(login_window, font=entry_font, width=35, relief="solid", show="*", fg="#828282")
    password_entry.insert(0, "enter password")
    password_entry.place(relx=0.47, rely=0.40, anchor='center', height=40)

    # Login button
    login_button = tk.Button(login_window, text="Login with email", font=button_font, bg="black", fg="white", width=38, command=lambda: login_with_email(email_entry, password_entry, users, login_window))
    login_button.place(relx=0.47, rely=0.46, anchor='center')

    # Separator label
    separator_label = tk.Label(login_window, text="----------------- or continue as a guest ------------------", font=label_font, bg="white", fg="#828282")
    separator_label.place(relx=0.47, rely=0.53, anchor='center')

    # Guest button
    guest_button = tk.Button(login_window, text="Guest", font=button_font, bg="lightgrey", width=38, command=lambda: login_as_guest(login_window))
    guest_button.place(relx=0.47, rely=0.59, anchor='center')

    # Terms of Service and Privacy Policy labels
    tos_label = tk.Label(login_window, text="By continuing, you agree to our ", font=("Inter", 15), bg="white", fg="#828282")
    tos_label.place(relx=0.42, rely=0.65, anchor='center')

    tos_label = tk.Label(login_window, text="Terms of Service", font=("Inter", 15), bg="white")
    tos_label.place(relx=0.56, rely=0.65, anchor='center')

    tos_label = tk.Label(login_window, text="and", font=("Inter", 15), bg="white", fg="#828282")
    tos_label.place(relx=0.423, rely=0.68, anchor='center')

    tos_label = tk.Label(login_window, text="Privacy Policy", font=("Inter", 15), bg="white")
    tos_label.place(relx=0.48, rely=0.68, anchor='center')

    # Signup label and button
    signup_label = tk.Label(login_window, text="Don't Have An Account?", font=button_font, bg="white")
    signup_label.place(relx=0.92, rely=0.90, anchor='center')

    signup_button = tk.Button(login_window, text="Sign Up", font=button_font, bg="black", fg="white", width=15, relief="solid", command=lambda: show_signup_window(users, login_window))
    signup_button.place(relx=0.92, rely=0.95, anchor='center')

    # Function to add an image to the bottom left
    def add_image():
        # Open and display an image using PIL
        image_path = "123.png"
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Create and place a label to display the image
        image_label = tk.Label(login_window, image=photo, bg="white")
        image_label.image = photo  # Retain reference to the image to prevent garbage collection
        image_label.place(relx=0.10, rely=0.85, anchor='center')

    add_image()  # Call the function to add the image

    login_window.mainloop()  # Start the main loop for the login window

# Function to show the signup window
def show_signup_window(users, login_window):
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")
    signup_window.geometry("1024x768")
    signup_window.state('zoomed')
    signup_window.configure(bg="white")

    title_font = ("Inter", 32, "bold")
    label_font = ("Inter", 15)
    entry_font = ("Inter", 18)
    button_font = ("Inter", 15, "bold")

    # Title label
    title_label = tk.Label(signup_window, text="Homework Tracker™", font=title_font, bg="white")
    title_label.place(x=21, y=21)

    # Signup label
    signup_label = tk.Label(signup_window, text="Sign Up", font=("Inter", 24, "bold"), bg="white")
    signup_label.place(relx=0.47, rely=0.23, anchor='center')

    # Email instruction label
    email_instruction_label = tk.Label(signup_window, text="Enter your email to sign up for this app", font=label_font, bg="white")
    email_instruction_label.place(relx=0.47, rely=0.28, anchor='center')

    # Email entry field
    email_entry = tk.Entry(signup_window, font=entry_font, width=35, borderwidth=0.5, relief="solid", fg="#828282")
    email_entry.insert(0, "email@domain.com")
    email_entry.place(relx=0.47, rely=0.34, anchor='center', height=40)

    # Username entry field
    name_entry = tk.Entry(signup_window, font=entry_font, width=35, borderwidth=0.5, relief="solid", fg="#828282")
    name_entry.insert(0, "Username")
    name_entry.place(relx=0.47, rely=0.40, anchor='center', height=40)

    # Password label and entry field
    password_label = tk.Label(signup_window, text="Create Password", font=label_font, bg="white")
    password_label.place(relx=0.47, rely=0.46, anchor='center')

    password_entry = tk.Entry(signup_window, font=entry_font, width=35, relief="solid", show="*", fg="#828282")
    password_entry.insert(0, "enter password")
    password_entry.place(relx=0.47, rely=0.50, anchor='center', height=40)

    # Confirm password label and entry field
    confirm_password_label = tk.Label(signup_window, text="Confirm Password", font=label_font, bg="white")
    confirm_password_label.place(relx=0.47, rely=0.56, anchor='center')

    confirm_password_entry = tk.Entry(signup_window, font=entry_font, width=35, relief="solid", show="*", fg="#828282")
    confirm_password_entry.insert(0, "confirm password")
    confirm_password_entry.place(relx=0.47, rely=0.60, anchor='center', height=40)

    # Signup function to handle registration
    def signup():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Basic validation checks
        if not name.strip() or not email.strip() or not password.strip() or not confirm_password.strip():
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        error_label = tk.Label(signup_window, text="", font=("Inter", 12), fg="red", bg="white")
        error_label.place(relx=0.47, rely=0.72, anchor='center')

        if password != confirm_password:
            error_label.config(text= "Passwords do not match.")
            return

        if len(name) > 20:
            error_label.config(text="Username should be maximum 20 characters.")
            return

        # Password complexity checks
        has_number = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)

        if not has_number or not has_upper:
            error_label.config(text="Password must contain at least one number and one capital letter.")
            return

        if not (5 <= len(password) <= 20):
            error_label.config(text="Password should be between 5 and 20 characters.")
            return
        
        if re.search(r'[\U00010000-\U0010ffff]', name):
            error_label.config(text="Emojis are not allowed in username.")
            return
        
        # Check for symbols in username
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', name):
            error_label.config(text="Symbols are not allowed in username.")
            return

        # Check if email already exists
        for user in users:
            if user['email'] == email:
                error_label.config(text="Account already exists.")
                return

        # If all checks pass, add the user to the list and save to file
        users.append({
            'name': name,
            'email': email,
            'password': password
        })

        with open(credentials_file, 'w') as file:
            json.dump(users, file, indent=4)

        messagebox.showinfo("Success", "Registration successful!")
        signup_window.destroy()

    # Signup button
    signup_button = tk.Button(signup_window, text="Sign Up", font=button_font, bg="black", fg="white", width=38, command=signup)
    signup_button.place(relx=0.47, rely=0.66, anchor='center')

    # Login label and button
    login_label = tk.Label(signup_window, text="Already Have An Account?", font=button_font, bg="white")
    login_label.place(relx=0.92, rely=0.90, anchor='center')

    login_button = tk.Button(signup_window, text="Login", font=button_font, bg="black", fg="white", width=15, relief="solid", command=lambda: show_login_window(users))
    login_button.place(relx=0.92, rely=0.95, anchor='center')

    # Function to add an image to the bottom left
    def add_image():
        image_path = "123.png"
        image = Image.open(image_path)
        image = image.resize((340, 340), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(image)

        image_label = tk.Label(signup_window, image=photo_image, bg="white")
        image_label.image = photo_image  # Retain reference to the image
        image_label.place(relx=0.10, rely=0.85, anchor='center')

    add_image()  # Call the function to add the image

    signup_window.mainloop()  # Start the main loop for the signup window

# Entry point of the application
if __name__ == "__main__":
    show_login_window(users)  # Show the login window when the script is run
