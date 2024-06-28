import tkinter as tk
from tkinter import ttk, messagebox
import json

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
            self.frames[section] = ttk.Frame(self.main_content)

        self.current_section = "Home"
        self.update_button_styles()
        self.show_frame("Home")

    def show_frame(self, section):
        for sec in sections:
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

    

    login_window.mainloop()

if __name__ == "__main__":
    show_login_window(users)
