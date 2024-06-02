import tkinter as tk
from tkinter import messagebox,simpledialog


# Function to handle login with email
def login_with_email(): 
    email = email_entry.get()
    password = password_entry.get()
    if email and password:
        messagebox.showinfo("Login", "Logged in with email")
        login_window.destroy()  # Destroy the login window
        home_page()  # Call the home page function
    else:
        messagebox.showwarning("Input error", "Please enter both email and password")

# Function to handle guest login
def login_as_guest():
    messagebox.showinfo("Guest", "Continuing as Guest")
    login_window.destroy()  # Destroy the login window
    home_page()  # Call the home page function

# Function to create the home page
def home_page():
    root = tk.Tk()
    root.title("Homework Tracker")
    root.geometry("1920x1800")
    root.configure(bg="white")


    root.mainloop


# Set up the login window
login_window = tk.Tk()
login_window.title("Homework Tracker")
login_window.geometry("1920x1080")
login_window.state('zoomed') 
login_window.configure(bg="white")

# Set up fonts and styles
title_font = ("Inter", 30, "bold")
bold_label_font = ("Inter", 20, "bold")
label_font = ("Inter", 12)
entry_font = ("Inter", 12)
button_font = ("Inter", 12, "bold")

# Title
title_label = tk.Label(login_window, text="Homework Tracker™", font=title_font, bg="white")
title_label.place(x=0, y=0, anchor='nw')

email_label = tk.Label(login_window, text="Login", font=bold_label_font, bg="white")
email_label.place(relx=0.5, rely=0.25, anchor='center')

# Email and Password Labels and Entries
email_label = tk.Label(login_window, text="Enter your email and password to login for this app", font=label_font, bg="white")
email_label.place(relx=0.5, rely=0.3, anchor='center')

email_entry = tk.Entry(login_window, font=entry_font, width=40, borderwidth=0.5, relief="solid" )
email_entry.insert(0, "email@domain.com")
email_entry.place(relx=0.5, rely=0.35, anchor='center')

password_entry = tk.Entry(login_window, font=entry_font, width=40, borderwidth=0.5, relief="solid", show="*" )
password_entry.insert(0, "enter password")
password_entry.place(relx=0.5, rely=0.4, anchor='center')

# Login Button
login_button = tk.Button(login_window, text="Login with email", font=button_font, bg="black", fg="white", width=35, command=login_with_email)
login_button.place(relx=0.5, rely=0.45, anchor='center')

# Separator
separator_label = tk.Label(login_window, text="or continue as a guest", font=label_font, bg="white")
separator_label.place(relx=0.5, rely=0.5, anchor='center')

# Guest Button
guest_button = tk.Button(login_window, text="Guest", font=button_font, bg="lightgrey", width=35, command=login_as_guest)
guest_button.place(relx=0.5, rely=0.55, anchor='center')

# Terms of Service and Privacy Policy
tos_label = tk.Label(login_window, text="By continuing, you agree to our Terms of Service and Privacy Policy", font=("Helvetica", 10), bg="white")
tos_label.pack(side="bottom", pady=(20, 10))

#add image to bottom right
def add_image():
    # Create a PhotoImage object from an image file
    image = tk.PhotoImage(file="123.png")  

    

    # Create a label to display the image
    image_label = tk.Label(login_window, image=image, bg="white")
    image_label.image = image  

    # Position the image at the bottom right
    image_label.place(relx=0.0, rely=1.0, anchor='sw', x=0, y=0)

add_image()

# Run the Tkinter event loop
login_window.mainloop()
