import tkinter as tk
from tkinter import ttk
from tasks import tasks


class HomeFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="#74a9dd")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Create the title label
        title_label = tk.Label(self, text="Homework Tracker™", font=("Inter", 20, "bold"), bg="#74a9dd")
        title_label.pack(pady=10)

        # Search entry
        search_entry = tk.Entry(self, font=("Inter", 12), width=50, relief="solid")
        search_entry.insert(0, "Quick Search")
        search_entry.pack(pady=10)
        


        # Upcoming Tasks Table
        self.table_frame = tk.Frame(self, bg="white", relief="solid", bd=1)
        self.table_frame.pack(pady=20, fill=tk.X, expand=True)

        columns = ["Subject", "Task", "Due Date", "Time"]
        self.table = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=150)
        
        self.table.pack(fill=tk.BOTH, expand=True)

        # Increase font size for rows and columns
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Inter", 14))
        style.configure("Treeview", font=("Inter", 12), rowheight=50)
        
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
        add_task_button = tk.Button(self, text="Add Task", font=("Inter", 12), bg="black", fg="white", width=20, relief="flat", command=self.add_task_window)
        add_task_button.place(relx=0.0, rely=0.7)

        # Edit Task button
        edit_task_button = tk.Button(self, text="Edit Task", font=("Inter", 12), bg="white", width=10, relief="solid")
        edit_task_button.place(relx=0.26, rely=0.95)

        # Logout button
        logout_button = tk.Button(self, text="Logout", font=("Inter", 12), bg="white", relief="solid", command=self.logout)
        logout_button.place(x=1000, y=800)

    def add_task_window(self):
        self.parent.show_tasks_frame()

    def logout(self):
        self.parent.destroy()
