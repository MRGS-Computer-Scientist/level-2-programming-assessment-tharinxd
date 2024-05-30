from tkinter import *
from app_settings import load_credentials, save_credentials, users

# Function to sign in
def sign_in():
    username = username_entry.get()
    password = password_entry.get()
    if username in users and users[username] == password:
        message_label.config(text="Sign-in successful!")
    else:
        message_label.config(text="Username or Password is invalid. Please try again.")

# Function to exit the application
def exit_app():
    root.destroy()

# Main function to create the login window
def create_login_window():
    global root, username_entry, password_entry, message_label

    root = Tk()
    root.title("Login Page")
    root.geometry("800x550")
    root.config(bg="#F2EEE3")

    # Username label and entry
    username_frame = Frame(root, bg="#F2EEE3")
    username_frame.pack(pady=(20, 5))
    username_label = Label(username_frame, text="Username:", bg="#F2EEE3", font=("Arial", 14))
    username_label.pack(side=LEFT)
    username_entry = Entry(username_frame, font=("Arial", 14))
    username_entry.pack(side=LEFT, fill=X, expand=True)

    # Password label and entry
    password_frame = Frame(root, bg="#F2EEE3")
    password_frame.pack(pady=10)
    password_label = Label(password_frame, text="Password:", bg="#F2EEE3", font=("Arial", 14))
    password_label.pack(side=LEFT)
    password_entry = Entry(password_frame, show="*", font=("Arial", 14))
    password_entry.pack(side=LEFT, fill=X, expand=True)

    # Sign in button
    sign_in_button = Button(root, text="SIGN IN", bg="#BCA0A0", font=("Arial", 14), command=sign_in)
    sign_in_button.pack(pady=10)

    # Message label
    message_label = Label(root, text="", bg="#F2EEE3", fg="red", font=("Arial", 14))
    message_label.pack(pady=10)

    # Exit button
    exit_button = Button(root, text="Exit", bg="#BCA0A0", command=exit_app)
    exit_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    root.mainloop()
