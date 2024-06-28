import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
from home import HomeFrame
from tasks import TasksFrame

sections = ["Home", "Tasks", "Subjects", "Account", "Connected Apps", "Theme", "Report a Problem", "Help And Support", "Feedback"]
credentials_file = "credentials.json"

try:
    with open(credentials_file, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = []

class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Homework Tracker")
        self.geometry("1280x720")
        self.config(bg="#74a9dd")

        self.sidebar = tk.Frame(self, width=320, bg='#E0E0E0')
        self.sidebar.pack(expand=False, fill='y', side='left', anchor='nw')

        self.main_content = tk.Frame(self, bg='#74a9dd')
        self.main_content.pack(expand=True, fill='both', side='right')

        title_label = tk.Label(self.sidebar, text="Homework Tracker™", font=("Inter", 20, "bold"), bg="#E0E0E0")
        title_label.pack(pady=10)

        self.buttons = []
        for section in sections:
            button = tk.Button(self.sidebar, text=section, font=("Inter", 14), width=30, height=2, bg="#FFFFFF", relief="flat", command=lambda s=section: self.show_frame(s))
            button.pack(pady=5)
            self.buttons.append(button)

        self.frames = {}
        for section in sections:
            frame = ttk.Frame(self.main_content)
            self.frames[section] = frame

        self.create_frames()

        self.current_section = "Home"
        self.update_button_styles()
        self.show_frame("Home")

    def show_frame_and_update_tasks(self, section):
        self.show_frame(section)
        if section == "Tasks":
            self.frames[section].update_tasks_table()

    def create_frames(self):
        for section in sections:
            if section == "Home":
                self.frames[section] = HomeFrame(self.main_content)
            elif section == "Tasks":
                self.frames[section] = TasksFrame(self.main_content)
            else:
                self.frames[section] = ttk.Frame(self.main_content)
            self.frames[section].pack(fill='both', expand=True)  # Pack the frame here

        # Add the other frames here

    def show_frame(self, section):
        for sec in sections:
            if sec != section:
                self.frames[sec].pack_forget()
        frame = self.frames[section]
        frame.pack(fill='both', expand=True)
        frame.tkraise()  # Bring the frame to the front
        self.current_section = section
        self.update_button_styles()

    def update_button_styles(self):
        for button in self.buttons:
            if button['text'] == self.current_section:
                button.config(bg="#A9A9A9")
            else:
                button.config(bg="#FFFFFF")

    def run(self):
        self.mainloop()

def login_with_email(email_entry, password_entry, users, login_window):
    email = email_entry.get()
    password = password_entry.get()
    for user in users:
        if user['email'] == email and user['password'] == password:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            app = MainApplication()
            app.run()
            return
    messagebox.showerror("Error", "Invalid email or password!")

def login_as_guest(login_window):
    messagebox.showinfo("Guest", "Continuing as guest.")
    login_window.destroy()
    app = MainApplication()
    app.run()

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

    title_label = tk.Label(login_window, text="Homework Tracker™", font=title_font, bg="white")
    title_label.place(x=21, y=21)

    login_label = tk.Label(login_window, text="Login", font=bold_label_font, bg="white")
    login_label.place(relx=0.47, rely=0.23, anchor='center')

    email_instruction_label = tk.Label(login_window, text="Enter your email and password to login for this app", font=label_font, bg="white")
    email_instruction_label.place(relx=0.47, rely=0.28, anchor='center')

    email_entry = tk.Entry(login_window, font=entry_font, width=35, borderwidth=0.5, relief="solid", fg="#828282")
    email_entry.insert(0, "email@domain.com")
    email_entry.place(relx=0.47, rely=0.34, anchor='center', height=40)

    password_entry = tk.Entry(login_window, font=entry_font, width=35, relief="solid", show="*", fg="#828282")
    password_entry.insert(0, "enter password")
    password_entry.place(relx=0.47, rely=0.40, anchor='center', height=40)

    login_button = tk.Button(login_window, text="Login with email", font=button_font, bg="black", fg="white", width=38, command=lambda: login_with_email(email_entry, password_entry, users, login_window))
    login_button.place(relx=0.47, rely=0.46, anchor='center')

    separator_label = tk.Label(login_window, text="----------------- or continue as a guest ------------------", font=label_font, bg="white", fg="#828282")
    separator_label.place(relx=0.47, rely=0.53, anchor='center')

    guest_button = tk.Button(login_window, text="Guest", font=button_font, bg="lightgrey", width=38, command=lambda: login_as_guest(login_window))
    guest_button.place(relx=0.47, rely=0.59, anchor='center')

    # Terms of Service and Privacy Policy
    tos_label = tk.Label(login_window, text="By continuing, you agree to our ", font=("Inter", 15), bg="white", fg="#828282")
    tos_label.place(relx=0.42, rely=0.65, anchor='center')

    tos_label = tk.Label(login_window, text="Terms of Service", font=("Inter", 15), bg="white")
    tos_label.place(relx=0.56, rely=0.65, anchor='center')

    tos_label = tk.Label(login_window, text="and", font=("Inter", 15), bg="white", fg="#828282")
    tos_label.place(relx=0.423, rely=0.68, anchor='center')

    tos_label = tk.Label(login_window, text="Privacy Policy", font=("Inter", 15), bg="white")
    tos_label.place(relx=0.48, rely=0.68, anchor='center')

    signup_label = tk.Label(login_window, text="Dont Have An Account?", font=button_font, bg="white")
    signup_label.place(relx=0.92, rely=0.90, anchor='center')

    signup_button = tk.Button(login_window, text="Sign Up", font=button_font, bg="black", fg="white", width=15, relief="solid", command=lambda: show_signup_window(users, login_window))
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

    login_window.mainloop()

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

    signup_title_label = tk.Label(signup_window, text="Sign Up", font=title_font, bg="white")
    signup_title_label.place(relx=0.5, rely=0.1, anchor='center')

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

    def signup():
        email = signup_email_entry.get()
        password = signup_password_entry.get()
        confirm_password = signup_confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        for user in users:
            if user['email'] == email:
                messagebox.showerror("Error", "Email already exists!")
                return

        users.append({'email': email, 'password': password})
        with open(credentials_file, 'w') as file:
            json.dump(users, file)

        messagebox.showinfo("Success", "Account created successfully!")
        signup_window.destroy()
        login_window.destroy()
        app = MainApplication()
        app.run()

    signup_button = tk.Button(signup_window, text="Sign Up", font=button_font, bg="black", fg="white", width=36, command=signup)
    signup_button.place(relx=0.5, rely=0.55, anchor='center')

    signup_window.mainloop()

show_login_window(users)