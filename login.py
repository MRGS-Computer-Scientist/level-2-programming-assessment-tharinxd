import tkinter as tk
from tkinter import messagebox
import json
from main import MainApplication

def show_login_window(users):
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    # Create login form
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username] == password:
            login_window.destroy()
            # Start the main application
            main_app = MainApplication(None)
            main_app.run()
        else:
            messagebox.showerror("Invalid Credentials", "Username or password is incorrect")

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack()

    def login_as_guest():
        login_window.destroy()
        # Start the main application as a guest
        main_app = MainApplication(None)
        main_app.run()

    guest_button = tk.Button(login_window, text="Login as Guest", command=login_as_guest)
    guest_button.pack()

    def show_signup_window():
        login_window.destroy()
        # Show the signup window
        signup_window = tk.Tk()
        signup_window.title("Sign up")
        signup_window.geometry("300x200")

        # Create signup form
        username_label = tk.Label(signup_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(signup_window)
        username_entry.pack()

        password_label = tk.Label(signup_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(signup_window, show="*")
        password_entry.pack()

        def signup():
            username = username_entry.get()
            password = password_entry.get()
            if username not in users:
                users[username] = password
                with open("credentials.json", 'w') as file:
                    json.dump(users, file)
                signup_window.destroy()
                show_login_window(users)
            else:
                messagebox.showerror("Username Taken", "Username is already taken")

        signup_button = tk.Button(signup_window, text="Sign up", command=signup)
        signup_button.pack()

    signup_button = tk.Button(login_window, text="Sign up", command=show_signup_window)
    signup_button.pack()

    login_window.mainloop()

def login_with_email():
    # Implement email login functionality
    pass