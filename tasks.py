import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import Calendar
from ttkwidgets.autocomplete import AutocompleteCombobox
import datetime

class Task:
    def __init__(self, subject, task, due_date, time):
        self.subject = subject
        self.task = task
        self.due_date = due_date
        self.time = time

tasks = []  # Initialize an empty list to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    global tasks
    try:
        with open(TASKS_FILE, "r") as file:
            tasks_data = json.load(file)
            tasks = [Task(**task_data) for task_data in tasks_data]
            print("Tasks loaded:", tasks)
    except FileNotFoundError:
        tasks = []

def save_tasks():
    tasks_data = [{"subject": task.subject, "task": task.task, "due_date": task.due_date,
                   "time": task.time} for task in tasks]
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks_data, file, indent=4)
    print("Tasks saved.")

def add_task(subject, task, due_date, time):
    new_task = Task(subject, task, due_date, time)
    tasks.append(new_task)
    print("Task added:", new_task)
    save_tasks()

def get_tasks():
    return tasks

class TasksFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        load_tasks()
        self.tasks = get_tasks()
        self.style = ttk.Style(self)
        self.configure_styles()
        self.create_widgets()
        self.update_tasks_table()

    def configure_styles(self):
        self.master.tk_setPalette(background="#f0f0f0")
        self.style.theme_use("clam")
        
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", font=("Arial", 12), foreground="#333333")
        self.style.configure('TButton', background="#4CAF50", foreground="white", font=("Arial", 10, "bold"))
        self.style.map('TButton', background=[('active', '#45a049')])
        
        self.style.configure('Calendar', background="#ffffff", fieldbackground="#ffffff", foreground="#333333", font=("Arial", 10))
        self.style.configure('TEntry', foreground="#333333", font=("Arial", 10))
        self.style.configure('Treeview', background="#ffffff", fieldbackground="#ffffff", foreground="#333333", font=("Arial", 10))
        self.style.configure('Treeview.Heading', font=("Arial", 10, "bold"))

    def create_widgets(self):
        
        image_path = "background.png"  
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        # Background image
        background_label = tk.Label(self, image=photo)
        background_label.image = photo  # Keep a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Button frame
        self.button_frame = tk.Frame(self, background="#f0f0f0")
        self.button_frame.pack(pady=5)  

        self.remove_task_button = ttk.Button(self.button_frame, text="Remove Task", command=self.remove_task, style='TButton')
        self.remove_task_button.grid(row=0, column=1, padx=5)

        # Calendar Frame
        self.calendar_frame = tk.Frame(self, background="#f0f0f0")
        self.calendar_frame.pack(pady=10)

        self.calendar = Calendar(self.calendar_frame, date_pattern='yyyy-mm-dd', showweeknumbers=False)
        self.calendar.pack()

        # Entry Frame
        self.entry_frame = tk.Frame(self, background="#f0f0f0")
        self.entry_frame.pack(pady=10)

        self.subject_label = ttk.Label(self.entry_frame, text="Subject:")
        self.subject_label.grid(row=0, column=0, padx=5, pady=5)

        self.subject_entry = ttk.Entry(self.entry_frame)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        self.task_label = ttk.Label(self.entry_frame, text="Task:")
        self.task_label.grid(row=1, column=0, padx=5, pady=5)

        self.task_entry = ttk.Entry(self.entry_frame)
        self.task_entry.grid(row=1, column=1, padx=5, pady=5)

        self.time_label = ttk.Label(self.entry_frame, text="Time:")
        self.time_label.grid(row=2, column=0, padx=5, pady=5)

        self.time_entry = AutocompleteCombobox(self.entry_frame, completevalues=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 5)])
        self.time_entry.grid(row=2, column=1, padx=5, pady=5)

        # Task Table Frame
        self.table_frame = tk.Frame(self, background="#f0f0f0")
        self.table_frame.pack(pady=10)
        self.create_tasks_table()

        # Submit Button
        self.submit_button = ttk.Button(self, text="Add Task", command=self.submit_task, style='TButton')
        self.submit_button.pack(pady=10)

        # Logout Button
        self.logout_button = ttk.Button(self, text="Logout", command=self.logout, style='TButton')
        self.logout_button.pack(pady=10)

        # Back Button
        self.back_button = ttk.Button(self, text="Back", command=self.back, style='TButton')
        self.back_button.pack(anchor=tk.E, padx=10, pady=5)

    def create_tasks_table(self):
        self.table = ttk.Treeview(self.table_frame, columns=("Subject", "Task", "Due Date", "Time"), show="headings", style='Treeview')
        self.table.heading("Subject", text="Subject")
        self.table.heading("Task", text="Task")
        self.table.heading("Due Date", text="Due Date")
        self.table.heading("Time", text="Time")
        self.table.pack(fill="both", expand=True)
        self.update_tasks_table()

    def submit_task(self):
        subject = self.subject_entry.get()
        task = self.task_entry.get()
        due_date_str = self.calendar.get_date()
        time_str = self.time_entry.get()

        if not subject or not task or not due_date_str or not time_str:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            time = datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Use YYYY-MM-DD and HH:MM.")
            return

        add_task(subject, task, due_date_str, time_str)  # Pass the parsed datetime objects
        self.update_tasks_table()
        self.clear_entries()
        save_tasks()

    def clear_entries(self):
        self.subject_entry.delete(0, tk.END)
        self.task_entry.delete(0, tk.END)
        self.time_entry.set('')

    def remove_task(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to remove.")
            return

        for item in selected_item:
            task_index = self.table.index(item)
            self.tasks.pop(task_index)
            self.table.delete(item)
        save_tasks()

    def update_tasks_table(self):
        for i in self.table.get_children():
            self.table.delete(i)

        for task in self.tasks:
            self.table.insert("", "end", values=(task.subject, task.task, task.due_date, task.time))

    def logout(self):
        self.master.master.show_login_window()

    def back(self):
        self.master.master.show_main_frame()

# Assuming you have a root window and login/main frame switching mechanism set up.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Homework Tracker")
    root.geometry("800x600")
    TasksFrame(root).pack(fill="both", expand=True)
    root.mainloop()
