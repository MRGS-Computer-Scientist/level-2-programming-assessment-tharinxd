import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tasks import TasksFrame

class SetReminderWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.title("Set Reminder")
        self.geometry("300x200")

        # Task selection
        tk.Label(self, text="Select Task:").pack()
        self.task_var = tk.StringVar()
        self.task_menu = ttk.Combobox(self, textvariable=self.task_var)
        self.task_menu['values'] = ["Physics ESA Chapter 10", "Maths Stats Mock", "English Novel Questions"]
        self.task_menu.pack()

        # Reminder options
        tk.Label(self, text="Reminder Options:").pack()
        self.daily_var = tk.IntVar()
        tk.Checkbutton(self, text="Daily", variable=self.daily_var).pack()
        self.weekly_var = tk.IntVar()
        tk.Checkbutton(self, text="Weekly", variable=self.weekly_var).pack()
        self.monthly_var = tk.IntVar()
        tk.Checkbutton(self, text="Monthly", variable=self.monthly_var).pack()

        # Set reminder button
        tk.Button(self, text="Set Reminder", command=self.set_reminder).pack()

    def set_reminder(self):
        task = self.task_var.get()
        daily = self.daily_var.get()
        weekly = self.weekly_var.get()
        monthly = self.monthly_var.get()
        print(f"Reminder set for {task}: daily={daily}, weekly={weekly}, monthly={monthly}")
        self.destroy()
        
    def set_reminder_window(self):
        try:
            SetReminderWindow(self.master)
        except Exception as e:
            print(f"Error creating SetReminderWindow: {e}")



class HomeFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        
        image_path = "background.png"  
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

    # Background image
        background_image = Image.open("background.png")
        background_photo = ImageTk.PhotoImage(background_image)

        background_label = tk.Label(self, image=background_photo)
        background_label.image = background_photo  # Keep a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Overlay image
        overlay_image = Image.open("pfpv1.png")  
        overlay_photo = ImageTk.PhotoImage(overlay_image)

        overlay_label = tk.Label(self, image=overlay_photo, bg="white")
        overlay_label.image = overlay_photo  # Keep a reference to the image
        overlay_label.place(x=25, y=70,)  # Adjust the position and size as needed

        # Search entry
        search_entry = tk.Entry(self, font=("Inter", 12), width=50, relief="solid")
        search_entry.insert(0, "Quick Search")
        search_entry.place(x=700, y=20)

        # Upcoming Tasks Table
        self.table_frame = tk.Frame(self, bg="white", relief="solid", bd=1)
        self.table_frame.place(relx=0.5, rely=0.6, anchor="center")

        columns = ["Subject", "Task", "Due Date", "Time"]
        self.table = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=280)
        
        self.table.pack()

        # Increase font size for rows and columns
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Inter", 60))
        style.configure("Treeview", font=("Inter", 45), rowheight=100)
        
        self.update_table()

    def update_table(self):
        self.table.delete(*self.table.get_children())

        # Sample data for table
        data = [
            ("Physics", "ESA Chapter 10", "12/04/24", "8:00 P.M"),
            ("Maths", "Stats Mock", "5/04/24", "11:59 P.M"),
            ("English", "Novel Questions", "15/05/24", "TBD")
        ]

        # Insert data into the table
        for item in data:
            self.table.insert("", tk.END, values=item)

        # Add Task button
        set_reminder_button = tk.Button(self, text="Set a Reminder", font=("Inter", 12), bg="black", fg="white", width=20, relief="flat", command=self.set_reminder_window)
        set_reminder_button.place(relx=0.04, rely=0.8)

        # Edit Task button
        edit_task_button = tk.Button(self, text="Edit Task", font=("Inter", 12, "bold"), bg="white", width=15, relief="solid")
        edit_task_button.place(relx=0.04, rely=0.95)

        # Logout button
        logout_button = tk.Button(self, text="Logout", font=("Inter", 12, "bold"), bg="white", width=10, relief="solid", command=self.logout)
        logout_button.place(relx=0.89, rely=0.95)
        
        heading_label = tk.Label(self, text="Upcoming Tasks:", font=("Inter", 28, "bold italic"), bg=None)
        heading_label.place(relx=0.5, rely=0.4, anchor="center")  
        
        heading_label = tk.Label(self, text="Welcome Back Tharin", font=("Inter",  30, "italic"),  bg=None)
        heading_label.place(x=220, y=40, anchor="center")

    def set_reminder_window(self):
        SetReminderWindow(self.master)

    
    def logout(self):
            self.destroy()
            self.login_window.destroy()