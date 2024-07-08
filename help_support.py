import tkinter as tk
from tkinter import ttk

class Help_SupportFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for the subjects section
        self.label = ttk.Label(self, text="Homework Tracker™", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        self.contact_label = ttk.Label(self, text="Contact Us", font=("Arial", 18))
        self.contact_label.pack()

        # Create input fields
        self.first_name_label = ttk.Label(self, text="First name")
        self.first_name_label.pack()
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.pack()

        self.last_name_label = ttk.Label(self, text="Last name")
        self.last_name_label.pack()
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.pack()

        self.email_label = ttk.Label(self, text="Email address")
        self.email_label.pack()
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()

        self.message_label = ttk.Label(self, text="Your message")
        self.message_label.pack()
        self.message_entry = tk.Text(self, height=5)  # Use Text for multiline input
        self.message_entry.pack()

        # Create submit button
        self.submit_button = ttk.Button(self, text="Submit")
        self.submit_button.pack(pady=10)


root = tk.Tk()
root.title("Help and Support")

help_support_frame = Help_SupportFrame(root)
help_support_frame.pack(pady=20)

root.mainloop()