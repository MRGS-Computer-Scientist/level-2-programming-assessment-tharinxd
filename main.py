import tkinter as tk
from tkinter import messagebox,simpledialog


# Function to handle login with email
def login_with_email():
    email = email_entry.get()
    password = password_entry.get()
    if email and password:
        
        messagebox.showinfo("Login", "Logged in with email")
    else:
        messagebox.showwarning("Input error", "Please enter both email and password")

# Function to handle guest login
def login_as_guest():
    messagebox.showinfo("Guest", "Continuing as Guest")

# Set up the login window
login_window = tk.Tk()
login_window.title("Homework Tracker")
login_window.geometry("400x400")
login_window.configure(bg="white")

# Set up fonts and styles
title_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")

# Title
title_label = tk.Label(login_window, text="Homework Tracker™", font=title_font, bg="white")
title_label.pack(pady=(50, 20))

# Email and Password Labels and Entries
email_label = tk.Label(login_window, text="Enter your email and password to login for this app", font=label_font, bg="white")
email_label.pack(pady=(0, 10))

email_entry = tk.Entry(login_window, font=entry_font, width=30, borderwidth=2, relief="solid")
email_entry.insert(0, "email@domain.com")
email_entry.pack(pady=(0, 10))

password_entry = tk.Entry(login_window, font=entry_font, width=30, borderwidth=2, relief="solid", show="*")
password_entry.insert(0, "enter password")
password_entry.pack(pady=(0, 20))

# Login Button
login_button = tk.Button(login_window, text="Login with email", font=button_font, bg="black", fg="white", command=login_with_email)
login_button.pack(pady=(0, 20))

# Separator
separator_label = tk.Label(login_window, text="or continue as a guest", font=label_font, bg="white")
separator_label.pack(pady=(0, 10))

# Guest Button
guest_button = tk.Button(login_window, text="Guest", font=button_font, bg="lightgrey", command=login_as_guest)
guest_button.pack(pady=(0, 20))

# Terms of Service and Privacy Policy
tos_label = tk.Label(login_window, text="By continuing, you agree to our Terms of Service and Privacy Policy", font=("Helvetica", 10), bg="white")
tos_label.pack(side="bottom", pady=(20, 10))

#add image to bottom right
def add_image():
    # Create a PhotoImage object from an image file
    image = tk.PhotoImage(file="wompwomp.png")  

    # Create a label to display the image
    image_label = tk.Label(login_window, image=image, bg="white")
    image_label.image = image  

    # Position the image at the bottom right
    image_label.place(relx=0.0, rely=1.0, anchor='sw', x=0, y=0)

add_image()

# Run the Tkinter event loop
login_window.mainloop()
