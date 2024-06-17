from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import os
import json

credentials_file = 'credentials.json'

# Attempt to open and load the JSON data from the specified credentials file.
try:
    with open(credentials_file, 'r') as file:
        users = json.load(file)
# If the file does not exist or the JSON data is malformed, handle the exceptions.
except (FileNotFoundError, json.JSONDecodeError):
    # Initialize an empty list for users if an error occurs.
    users = []
    # Create the credentials file with an empty list to ensure it exists.
    with open(credentials_file, 'w') as file:
        json.dump(users, file)

# Function to handle login with email
def login_with_email(): 
    # Get the email and password from the respective entry fields
    email = email_entry.get()
    password = password_entry.get()
    
    # Check if email and password are entered
    if email and password:
        # Show an info message on successful login
        messagebox.showinfo("Login", "Logged in with email")
        # Close the login window
        login_window.destroy()
        # Open the home page
        home_page()
    else:
        # Show a warning message if email or password is missing
        messagebox.showwarning("Input error", "Please enter both email and password")

# Function to handle guest login
def login_as_guest():
    # Close the login window
    login_window.destroy()
    # Open the home page
    home_page()


# Function to create the home page
def home_page():
  global root, table

  # Create the root window
  root = tk.Tk()
  root.title("Homework Tracker")
  root.geometry("1024x768")

  canvas = tk.Canvas(root, width=1024, height=768)
  canvas.pack(fill="both", expand=True)

  bg_image_path = "images/yeamannn.png"
  if os.path.exists(bg_image_path):
    try:
      bg_image = Image.open(bg_image_path)
      bg_image = bg_image.resize((1920, 1080), Image.BICUBIC)  # Ensure resize matches canvas size
      photo_bg = ImageTk.PhotoImage(bg_image)
      canvas.create_image(0, 0, image=photo_bg, anchor='nw')
      canvas.image = photo_bg  # Keep a reference to the image
    except Exception as e:
      messagebox.showerror("Image Load Error", f"Failed to load background image: {e}")
  else:
    messagebox.showerror("File Not Found", f"Background image not found at {bg_image_path}")

    # Create a frame to hold the widgets and place it on the canvas
    main_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=main_frame, anchor="nw")
    
     # Left Frame for navigation
    left_frame = tk.Frame(root, bg="#FFFFFF", width=210)
    left_frame.pack(fill="y", side="left")

    # Main Frame for content
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)

    # Left Frame content - navigation buttons
    title_label = tk.Label(left_frame, text="Homework Tracker™", font=("Inter", 20, "bold"), bg="#FFFFFF")
    title_label.pack(pady=10)
    sections = ["Home", "Tasks", "Subjects", "Account", "Connected Apps", "Theme", "Report a Problem", "Help And Support", "Feedback"]
    
    for section in sections:
        button = tk.Button(left_frame, text=section, font=("Inter", 12), width=20, height=2, bg="#FFFFFF", relief="flat")
        button.pack(pady=5)

    # Main Frame content - welcome message and search bar
    welcome_label = tk.Label(main_frame, text="Welcome Back Tharin", font=("Inter", 24, "bold"), bg="#FFFFFF")
    welcome_label.place(x=20, y=20)

    search_entry = tk.Entry(main_frame, font=("Inter", 12), width=50, relief="solid")
    search_entry.insert(0, "Quick Search")
    search_entry.place(x=790, y=20)

    # Upcoming Tasks Table
    table_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
    table_frame.place(relx=0.5, rely=0.5, anchor="center")

    columns = ["Subject", "Task", "Due Date", "Time"]
    table = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
    
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=150)
    
    table.pack()

    # Increase font size for rows and columns
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Inter", 14))
    style.configure("Treeview", font=("Inter", 12), rowheight=30)

    # Sample tasks
    tasks = [
        ("Physics", "ESA Chapter 10", "12/04/24", "8:00 P.M"),
        ("Maths", "Stats Mock", "5/04/24", "11:59 P.M"),
        ("English", "Novel Questions", "15/05/24", "TBD")
    ]

    for task in tasks:
        table.insert("", "end", values=task)

    # Add Task button
    add_task_button = tk.Button(main_frame, text="Add Task", font=("Inter", 12), bg="black", fg="white", width=20, relief="flat", command=add_task_window)
    add_task_button.place(relx=0.26, rely=0.7)

    # Edit Task button
    edit_task_button = tk.Button(main_frame, text="Edit Task", font=("Inter", 12), bg="white", width=10, relief="solid")
    edit_task_button.place(relx=0.26, rely=0.95)

    # Logout button
    logout_button = tk.Button(main_frame, text="Logout", font=("Inter", 12), bg="white", relief="solid")
    logout_button.place(relx=0.94, rely=0.95)
    
    root.mainloop ()
    
    # Function to display the window for adding a new task
def add_task_window():
    def submit_task():
        # Get task details from the entry fields
        subject = subject_entry.get()
        task = task_entry.get()
        due_date = due_date_entry.get()
        time = time_entry.get()
        # Check if all fields are filled
        if subject and task and due_date and time:
            # Insert the new task into the table
            table.insert("", "end", values=(subject, task, due_date, time))
            # Close the add task window
            add_window.destroy()

    # Create a new top-level window for adding a task
    add_window = tk.Toplevel(root)
    add_window.title("Add Task")
    add_window.geometry("400x300")

    # Frame for input fields
    input_frame = tk.Frame(add_window, bg="white")
    input_frame.pack(pady=20, padx=20)

    # Labels and entry fields for task details
    subject_label = tk.Label(input_frame, text="Subject", font=("Inter", 12), bg="white")
    subject_label.grid(row=0, column=0, padx=5, pady=5)
    subject_entry = tk.Entry(input_frame, font=("Inter", 12), relief="solid")
    subject_entry.grid(row=0, column=1, padx=5, pady=5)

    task_label = tk.Label(input_frame, text="Task", font=("Inter", 12), bg="white")
    task_label.grid(row=1, column=0, padx=5, pady=5)
    task_entry = tk.Entry(input_frame, font=("Inter", 12), relief="solid")
    task_entry.grid(row=1, column=1, padx=5, pady=5)

    due_date_label = tk.Label(input_frame, text="Due Date", font=("Inter", 12), bg="white")
    due_date_label.grid(row=2, column=0, padx=5, pady=5)
    due_date_entry = tk.Entry(input_frame, font=("Inter", 12), relief="solid")
    due_date_entry.grid(row=2, column=1, padx=5, pady=5)

    time_label = tk.Label(input_frame, text="Time", font=("Inter", 12), bg="white")
    time_label.grid(row=3, column=0, padx=5, pady=5)
    time_entry = tk.Entry(input_frame, font=("Inter", 12), relief="solid")
    time_entry.grid(row=3, column=1, padx=5, pady=5)

    # Submit button to add the task
    submit_button = tk.Button(input_frame, text="Submit", font=("Inter", 12), bg="white", relief="solid", command=submit_task)
    submit_button.grid(row=4, columnspan=2, pady=10)
    

    

# Set up the login window
login_window = tk.Tk()
login_window.title("Homework Tracker")
login_window.geometry("1024x768")
login_window.state('zoomed')
login_window.configure(bg="white")

# Set up fonts and styles
title_font = ("Inter", 32, "bold")
bold_label_font = ("Inter", 24, "bold")
label_font = ("Inter", 15)
entry_font = ("Inter", 18)
button_font = ("Inter", 15, "bold")


# Title
title_label = tk.Label(login_window, text="Homework Tracker™", font=title_font, bg="white")
title_label.place(x=21, y=21)

email_label = tk.Label(login_window, text="Login", font=bold_label_font, bg="white")
email_label.place(relx=0.47, rely=0.23, anchor='center')

email_label = tk.Label(login_window, text="Dont Have An Account?", font=button_font, bg="white")
email_label.place( relx=0.92, rely=0.90, anchor='center')

# Email and Password Labels and Entries
email_label = tk.Label(login_window, text="Enter your email and password to login for this app", font=label_font, bg="white")
email_label.place(relx=0.47, rely=0.28, anchor='center')

email_entry = tk.Entry(login_window, font=entry_font, width=35, borderwidth=0.5, relief="solid", fg="#828282")
email_entry.insert(0, "email@domain.com")
email_entry.place(relx=0.47, rely=0.34, anchor='center', height=40)

password_entry = tk.Entry(login_window, font=entry_font, width=35, relief="solid", show="*", fg="#828282")
password_entry.insert(0, "enter password")
password_entry.place(relx=0.47, rely=0.40, anchor='center',height=40)



# Function to handle email login
def login_with_email():
    email = email_entry.get()
    password = password_entry.get()

    # Validate email and password against stored users
    for user in users:
        if user['email'] == email and user['password'] == password:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()  # Close the login window
            home_page()  # Open the home page
            return

    # Show error if login fails
    messagebox.showerror("Error", "Invalid email or password!")

# Function to handle guest login
def guest_login_action():
    messagebox.showinfo("Guest", "Continuing as guest.")
    login_as_guest()

# Login Button
login_button = tk.Button(login_window, text="Login with email", font=button_font, bg="black", fg="white", width=38, command=login_with_email)
login_button.place(relx=0.47, rely=0.46, anchor='center')

# Separator
separator_label = tk.Label(login_window, text="----------------- or continue as a guest ------------------", font=label_font, bg="white", fg="#828282")
separator_label.place(relx=0.47, rely=0.53, anchor='center')

# Guest Button
guest_button = tk.Button(login_window, text="Guest", font=button_font, bg="lightgrey", width=38, command=guest_login_action)
guest_button.place(relx=0.47, rely=0.59, anchor='center')

# Terms of Service and Privacy Policy
tos_label = tk.Label(login_window, text="By continuing, you agree to our ", font=("Inter", 15), bg="white", fg="#828282")
tos_label.place(relx=0.42, rely=0.65, anchor='center')

tos_label = tk.Label(login_window, text="Terms of Service", font=("Inter", 15), bg="white")
tos_label.place(relx=0.56, rely=0.65, anchor='center')

tos_label = tk.Label(login_window, text="and", font=("Inter", 15), bg="white", fg="#828282")
tos_label.place(relx=0.423, rely=0.68, anchor='center')

tos_label = tk.Label(login_window, text="Privacy Policy", font=("Inter", 15), bg="white",)
tos_label.place(relx=0.48, rely=0.68, anchor='center')



# Function to display the sign-up window
def show_signup_window():
    # Create a new top-level window for sign-up
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")
    signup_window.geometry("1024x768")
    signup_window.state('zoomed')
    signup_window.configure(bg="white")

    # Sign Up Labels and Entries
    signup_title = tk.Label(signup_window, text="Sign Up", font=title_font, bg="white")
    signup_title.place(relx=0.5, rely=0.1, anchor='center')

    signup_email_label = tk.Label(signup_window, text="Email", font=label_font, bg="white")
    signup_email_label.place(relx=0.5, rely=0.2, anchor='center')
    signup_email_entry = tk.Entry(signup_window, font=entry_font, width=40, borderwidth=0.5, relief="solid")
    signup_email_entry.place(relx=0.5, rely=0.25, anchor='center')

    signup_password_label = tk.Label(signup_window, text="Password", font=label_font, bg="white")
    signup_password_label.place(relx=0.5, rely=0.3, anchor='center')
    signup_password_entry = tk.Entry(signup_window, font=entry_font, width=40, borderwidth=0.5, relief="solid", show="*")
    signup_password_entry.place(relx=0.5, rely=0.35, anchor='center')

    signup_confirm_password_label = tk.Label(signup_window, text="Confirm Password", font=label_font, bg="white")
    signup_confirm_password_label.place(relx=0.5, rely=0.4, anchor='center')
    signup_confirm_password_entry = tk.Entry(signup_window, font=entry_font, width=40, borderwidth=0.5, relief="solid", show="*")
    signup_confirm_password_entry.place(relx=0.5, rely=0.45, anchor='center')

    # Function to handle sign-up
    def signup():
        email = signup_email_entry.get()
        password = signup_password_entry.get()
        confirm_password = signup_confirm_password_entry.get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Check if email already exists
        for user in users:
            if user['email'] == email:
                messagebox.showerror("Error", "Email already exists!")
                return

        # Add the new user to the list and save to file
        users.append({'email': email, 'password': password})
        with open(credentials_file, 'w') as file:
            json.dump(users, file)

        # Show success message and close sign-up window
        messagebox.showinfo("Success", "Account created successfully!")
        signup_window.destroy()

    # Sign Up button
    signup_button = tk.Button(signup_window, text="Sign Up", font=button_font, bg="black", fg="white", width=36, command=signup)
    signup_button.place(relx=0.5, rely=0.55, anchor='center')

# Add a Sign Up Button to the Login Window
signup_button = tk.Button(login_window, text="Sign Up", font=button_font, bg="black", fg="white", width=15, command=show_signup_window)
signup_button.place(relx=0.92, rely=0.95, anchor='center')

# Function to add an image to the bottom left
def add_image():
    # Open the image using PIL
    image_path = "123.png"
    image = Image.open(image_path)

    # Resize the image to fit the design (optional, based on your requirements)
    image = image.resize((360, 360), Image.LANCZOS)

    # Create a PhotoImage object from the image
    photo_image = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(login_window, image=photo_image, bg="white")
    image_label.image = photo_image  # Keep a reference to the image

    # Position the image at the bottom left
    image_label.place(relx=0.030, rely=0.97, anchor='sw')


# Add the image to the login window
add_image()

# Run the Tkinter event loop
login_window.mainloop()
