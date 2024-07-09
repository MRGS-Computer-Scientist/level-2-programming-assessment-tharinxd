import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class ProgressTrackerWindow(tk.Toplevel):
    def __init__(self, parent, task, home_frame, task_data):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.home_frame = home_frame
        self.task = task
        self.task_data = task_data
        self.steps = []
        self.step_vars = []
        self.create_widgets()

    def create_widgets(self):
        self.title(f"Progress Tracker - {self.task}")
        self.geometry("1920x1080")
        
        image_path = "background.png"  
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        background_label = tk.Label(self, image=photo)
        background_label.image = photo  # Keep a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Top frame
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(pady=20)


        # Steps frame
        self.steps_frame = tk.Frame(self, bg="white")
        self.steps_frame.pack(pady=20)

        # Add step entry
        self.step_entry = tk.Entry(self.steps_frame, font=("Inter", 12), width=40)
        self.step_entry.pack(pady=10, side="left", padx=20)

        # Add step button
        add_step_button = tk.Button(self.steps_frame, text="Add Step", command=self.add_step)
        add_step_button.pack(pady=10, side="left", padx=20)

        # Display task table
        self.create_task_table()

        # Complete task button
        self.complete_task_button = tk.Button(self, text="Complete Task", command=self.complete_task, state="disabled")
        self.complete_task_button.pack(pady=20)

        # Back button
        back_button = tk.Button(self, text="Back", command=self.close_window)
        back_button.pack(pady=20)

    def add_step(self):
        step = self.step_entry.get()
        if step:
            self.steps.append(step)
            self.step_entry.delete(0, tk.END)

            step_frame = tk.Frame(self.steps_frame, relief="solid", bd=1, bg="lightblue")
            step_frame.pack(pady=10, fill="x", expand=True)

            step_var = tk.BooleanVar(value=False)
            self.step_vars.append(step_var)

            step_checkbox = tk.Checkbutton(step_frame, text=f"Step: {step}", variable=step_var, command=self.update_progress, font=("Inter", 14))
            step_checkbox.pack(side="left", padx=10, pady=10)

            progress_bar = ttk.Progressbar(step_frame, orient="horizontal", length=200, mode="determinate", value=0)
            progress_bar.pack(side="left", padx=20, pady=10)

            if len(self.step_vars) == 4:
                self.complete_task_button.config(state="normal")

    def update_progress(self):
        if all(var.get() for var in self.step_vars):
            self.complete_task_button.config(state="normal")
        else:
            self.complete_task_button.config(state="disabled")

    def complete_task(self):
        selected_item = self.home_frame.table.selection()  # Use the HomeFrame instance
        if selected_item:
            self.home_frame.table.delete(selected_item)
            self.destroy()  # Close the ProgressTrackerWindow instance
        else:
            tk.messagebox.showwarning("No Task Selected", "Please select a task from the table.")


    def close_window(self):
        self.destroy()

    def create_task_table(self):
        table_frame = tk.Frame(self, bg="white", relief="solid", bd=1)
        table_frame.pack(pady=20)

        columns = ["Subject", "Task", "Due Date", "Time"]
        task_table = ttk.Treeview(table_frame, columns=columns, show='headings', height=1)
        
        for col in columns:
            task_table.heading(col, text=col)
            task_table.column(col, anchor="center", width=150)
        
        task_table.pack()

        task_table.insert("", tk.END, values=self.task_data)


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
        self.search_entry = tk.Entry(self, font=("Inter", 12), width=50, relief="solid")
        self.search_entry.insert(0, "Quick Search")
        self.search_entry.place(x=700, y=20)

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
        
        # Add Task button
        set_reminder_button = tk.Button(self, text="Set a Reminder", font=("Inter", 12), bg="black", fg="white", width=20, relief="flat", command=self.set_reminder_window)
        set_reminder_button.place(relx=0.04, rely=0.8)
        
        progress_button = tk.Button(self, text="Progress", font=("Inter", 12, "bold"), bg="white", width=15, relief="solid", command=self.progress_window)
        progress_button.place(relx=0.04, rely=0.95)
        


        # Logout button
        logout_button = tk.Button(self, text="Logout", font=("Inter", 12, "bold"), bg="white", width=10, relief="solid", command=self.logout)
        logout_button.place(relx=0.89, rely=0.95)
        
        heading_label = tk.Label(self, text="Upcoming Tasks:", font=("Inter", 28, "bold italic"), bg="#269bf2")
        heading_label.place(relx=0.5, rely=0.4, anchor="center")  
        
        heading_label = tk.Label(self, text="Welcome Back Tharin", font=("Inter",  30, "italic"), bg="#74b3e0")
        heading_label.place(x=220, y=40, anchor="center")
        
    def progress_window(self):
        selected_item = self.table.selection()
        if selected_item:
            task_data = self.table.item(selected_item[0])["values"]
            task = task_data[1]
            ProgressTrackerWindow(self.master, self, task, task_data)  # Pass self as the home_frame argument
        else:
            tk.messagebox.showwarning("No Task Selected", "Please select a task from the table.")

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

    def set_reminder_window(self):
        SetReminderWindow(self.master)

    def logout(self):
        self.master.master.show_login_window()

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("NCEA Study Tracker")
        self.geometry("1280x720")
        self.create_widgets()

    def create_widgets(self):
        self.home_frame = HomeFrame(self)
        self.home_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()