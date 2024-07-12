import tkinter as tk
from tkinter import ttk, messagebox  # Importing tkinter modules for GUI components and messagebox
from PIL import Image, ImageTk  # Importing Image and ImageTk from PIL for image handling
from tkcalendar import Calendar  # Importing Calendar widget from tkcalendar
from ttkwidgets.autocomplete import AutocompleteCombobox  # Importing AutocompleteCombobox from ttkwidgets
import datetime  # Importing datetime module for date and time handling
import json  # Importing json module for reading and writing JSON data

# Define the User class to hold user information and tasks
class User:
    def __init__(self, username):
        """
        Initialize a User instance.

        """
        self.username = username
        self.tasks = []  # Initialize an empty list to store tasks for the user


# Define the Task class to represent individual tasks
class Task:
    def __init__(self, subject, task, due_date, time):
        """
        Initialize a Task instance.

        """
        self.subject = subject
        self.task = task
        self.due_date = due_date
        self.time = time


# Initialize an empty list to store User objects
users = []
USERS_FILE = "users.json"  # File to store user data in JSON format


def load_users():
    """
    Load users' data from a JSON file into the 'users' list.
    """
    global users
    try:
        with open(USERS_FILE, "r") as file:
            users_data = json.load(file)
            users = []
            for user_data in users_data:
                username = user_data["username"]
                user_tasks = user_data["tasks"]
                new_user = User(username)
                for task_data in user_tasks:
                    subject = task_data["subject"]
                    task = task_data["task"]
                    due_date = task_data["due_date"]
                    time = task_data["time"]
                    new_task = Task(subject, task, due_date, time)
                    new_user.tasks.append(new_task)
                users.append(new_user)
            print("Users loaded:", users)
    except FileNotFoundError:
        users = []  # Handle case where the file doesn't exist


def save_users():
    """
    Save users' data from the 'users' list into a JSON file.
    """
    users_data = [{"username": user.username, "tasks": [task.__dict__ for task in user.tasks]} for user in users]
    with open(USERS_FILE, "w") as file:
        json.dump(users_data, file, indent=4)
    print("Users saved.")


def add_user(username):
    """
    Create a new User instance and add it to the 'users' list.

    Returns:
        User: The newly created User object.
    """
    new_user = User(username)
    users.append(new_user)
    save_users()
    return new_user


def get_user(username):
    """
    Retrieve a User object from the 'users' list based on the username.


    Returns:
        User or None: The User object if found, None if not found.
    """
    for user in users:
        if user.username == username:
            return user
    return None


def add_task(user, subject, task, due_date, time):
    """
    Create a new Task instance and add it to the tasks list of a User object.

    """
    new_task = Task(subject, task, due_date, time)
    user.tasks.append(new_task)
    print("Task added for user", user.username, ":", new_task)
    save_users()


def remove_task(user, task_index):
    """
    Remove a task from the tasks list of a User object based on its index.


    Returns:
        bool: True if the task was successfully removed, False otherwise.
    """
    if task_index < len(user.tasks):
        user.tasks.pop(task_index)
        save_users()
        return True
    return False


# Load existing users on startup
load_users()


# Define the TasksFrame class to create and manage the main GUI window
class TasksFrame(tk.Frame):
    def __init__(self, master, username):
        """
        Initialize the TasksFrame.

        Args:
            master (tk.Tk or tk.Toplevel): The parent window.
            username (str): The username of the current user.
        """
        tk.Frame.__init__(self, master)
        self.master = master
        self.username = username
        self.user = get_user(username) or add_user(username)  # Retrieve or create a User object
        self.style = ttk.Style(self)
        self.configure_styles()  # Configure the visual style of the GUI
        self.create_widgets()  # Create GUI widgets
        self.update_tasks_table()  # Update the tasks table with user's tasks

    def configure_styles(self):
        """
        Configure the visual style of the GUI using ttk.Style.
        """
        self.master.tk_setPalette(background="#f0f0f0")  # Set the background color of the window
        self.style.theme_use("clam")  # Use the 'clam' theme for ttk widgets
        
        # Configure styles for various widgets
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", font=("Arial", 12), foreground="#333333")
        self.style.configure('TButton', background="#EEEEEE", foreground="black", font=("Arial", 10, "bold"))
        self.style.map('TButton', background=[('active', '#45a049')])
        
        self.style.configure('Calendar', background="#ffffff", fieldbackground="#ffffff", foreground="#333333", font=("Arial", 10))
        self.style.configure('TEntry', foreground="#333333", font=("Arial", 10))
        self.style.configure('Treeview', background="#ffffff", fieldbackground="#ffffff", foreground="#333333", font=("Arial", 10))
        self.style.configure('Treeview.Heading', font=("Arial", 10, "bold"))

    def create_widgets(self):
        """
        Create GUI widgets and place them within the frame.
        """
        image_path = "background.png"  # Path to the background image
        image = Image.open(image_path)  # Open the image file
        photo = ImageTk.PhotoImage(image)  # Create a PhotoImage object from the image

        # Background image label
        background_label = tk.Label(self, image=photo)
        background_label.image = photo  # Keep a reference to the image to prevent garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Places the label in the frame

        # Buttons
        self.add_task_button = ttk.Button(self, text="Add Task", command=self.submit_task, style='TButton')
        self.add_task_button.grid(row=1, column=0, padx=5)

        self.remove_task_button = ttk.Button(self, text="Remove Task", command=self.remove_task, style='TButton')
        self.remove_task_button.grid(row=1, column=1, padx=5)

        # Calendar widget
        self.calendar = Calendar(self, selectmode='day', year=2024, month=7, day=12, date_pattern='yyyy-mm-dd', showweeknumbers=False)
        self.calendar.place(relx=0.02, rely=0.3, relwidth=0.4, relheight=0.4)

        # Entry widgets for subject, task, and time
        self.subject_entry = tk.Entry(self, font=("Inter", 12), width=70)
        self.subject_entry.place(relx=0.43, rely=0.37)
        self.add_placeholder(self.subject_entry, "Enter Subject")

        self.task_entry = tk.Entry(self, font=("Inter", 12), width=42)
        self.task_entry.place(relx=0.645, rely=0.32)
        self.add_placeholder(self.task_entry, "Enter Task")

        self.time_entry = AutocompleteCombobox(self, completevalues=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)])
        self.time_entry.place(relx=0.43, rely=0.32)
        self.add_placeholder(self.time_entry, "Select A Time")

        # Submit button
        self.submit_button = tk.Button(self, text="Submit", font=("Inter", 12), bg="black", fg="white", width=30, relief="flat", command=self.submit_task)
        self.submit_button.place(relx=0.43, rely=0.66)

        # Frame for the tasks table
        self.table_frame = tk.Frame(self, background="#f0f0f0")
        self.table_frame.place(relx=0.43, rely=0.45, relwidth=0.56, relheight=0.2)
        self.create_tasks_table()  # Create the tasks table within the table frame

        # Logout button
        logout_button = tk.Button(self, text="Logout", font=("Inter", 12, "bold"), bg="white", width=10, relief="solid", command=self.logout)
        logout_button.place(relx=0.89, rely=0.95)

    def add_placeholder(self, widget, placeholder_text):
        """
        Add placeholder text to an Entry or Combobox widget.

        """
        def on_focus_in(event):
            if widget.get() == placeholder_text:
                widget.delete(0, tk.END)

        def on_focus_out(event):
            if widget.get() == "":
                widget.insert(0, placeholder_text)

        widget.insert(0, placeholder_text)  # Insert placeholder text initially
        widget.bind("<FocusIn>", on_focus_in)  # Bind focus in event to remove placeholder on focus
        widget.bind("<FocusOut>", on_focus_out)  # Bind focus out event to restore placeholder if empty

    def create_tasks_table(self):
        """
        Create the tasks table using Treeview widget to display user's tasks.
        """
        self.table = ttk.Treeview(self.table_frame, columns=("Subject", "Task", "Due Date", "Time"), show="headings", style='Treeview')
        self.table.heading("Subject", text="Subject")
        self.table.heading("Task", text="Task")
        self.table.heading("Due Date", text="Due Date")
        self.table.heading("Time", text="Time")
        
        # Set column widths proportionally based on the table frame width
        total_width = self.table_frame.winfo_width()
        column_widths = [int(total_width * 0.25)] * 4

        for idx, col in enumerate(["Subject", "Task", "Due Date", "Time"]):
            self.table.column(col, width=column_widths[idx], anchor="center")

        self.table.pack(fill="both", expand=True)  # Pack the table widget to fill the available space
        self.update_tasks_table()  # Update the table with user's tasks

    def submit_task(self):
        """
        Validate user input and add a new task to the user's task list.
        """
        subject = self.subject_entry.get()
        task = self.task_entry.get()
        due_date_str = self.calendar.get_date()
        time_str = self.time_entry.get()

        # Validate input fields
        if not subject or subject == "Enter Subject" or not task or task == "Enter Task" or not due_date_str or not time_str or time_str == "Select A Time":
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Converts due date to datetime.date object
            time = datetime.datetime.strptime(time_str, "%H:%M").time()  # Converts time to datetime.time object
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Use YYYY-MM-DD and HH:MM.")
            return

        add_task(self.user, subject, task, due_date_str, time_str)  # Adds the task to user's task list
        self.update_tasks_table()  # Updates the tasks table to reflect the changes
        self.clear_entries()  # Clears input fields after submission

    def clear_entries(self):
        """
        Clear all input fields and reset placeholders.
        """
        self.subject_entry.delete(0, tk.END)
        self.task_entry.delete(0, tk.END)
        self.time_entry.set('')
        self.add_placeholder(self.subject_entry, "Enter Subject")
        self.add_placeholder(self.task_entry, "Enter Task")
        self.add_placeholder(self.time_entry, "Select A Time")

    def remove_task(self):
        """
        Remove a selected task from the user's tasks list and update the tasks table.
        """
        selected_item = self.table.selection()  # Gets the selected item from the tasks table
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to remove.")
            return

        for item in selected_item:
            task_index = self.table.index(item)  # Gets the index of the selected task
            remove_task(self.user, task_index)  # Removes the task from user's task list
            self.table.delete(item)  # Deletes the task from the tasks table

    def update_tasks_table(self):
        """
        Update the tasks table with the tasks from the user's task list.
        """
        for i in self.table.get_children():
            self.table.delete(i)  # Clears existing table rows

        for task in self.user.tasks:
            self.table.insert("", "end", values=(task.subject, task.task, task.due_date, task.time))  # Insert each task into the table

    def logout(self):
        """
        Logout the current user and return to the login window.
        """
        self.master.master.show_login_window()  # Calls the show_login_window method of the parent window

    def back(self):
        """
        Return to the main application frame.
        """
        self.master.master.show_main_frame()  # Calls the show_main_frame method of the parent window


if __name__ == "__main__":
    # Main program execution starts here
    root = tk.Tk()  # Creates the main application window
    root.title("Homework Tracker")  # Sets the title of the window
    root.geometry("800x600")  # Sets the initial size of the window
    TasksFrame(root, "testuser").pack(fill="both", expand=True)  # Creates an instance of TasksFrame and pack it into the window
    root.mainloop()  # Starts the tkinter event loop
