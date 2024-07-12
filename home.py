import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tasks import get_user, add_task, remove_task, save_users, load_users


class ProgressTrackerWindow(tk.Toplevel):
    def __init__(self, parent, home_frame, task, task_data):
        """
        Initialize the Progress Tracker Window.

        """
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.home_frame = home_frame
        self.task = task
        self.task_data = task_data
        self.steps = []
        self.step_vars = []
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets for the Progress Tracker Window.
        """
        self.title(f"Progress Tracker - {self.task}")
        self.geometry("1920x1080")
        
        # Load background image
        image_path = "background.png"
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        # Set background image
        background_label = tk.Label(self, image=photo)
        background_label.image = photo  # Keep a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame for steps
        self.steps_frame = tk.Frame(self, bg="white")
        self.steps_frame.pack(pady=20)

        # Entry for adding steps
        self.step_entry = tk.Entry(self, font=("Inter", 12), width=40)
        self.step_entry.pack(pady=10)

        # Button to add steps
        add_step_button = tk.Button(self, text="Add Step", command=self.add_step)
        add_step_button.pack(pady=10)

        # Frame for displaying steps
        self.steps_grid = tk.Frame(self, bg="white")
        self.steps_grid.pack(pady=20, fill="x")

        # Create table for task details
        self.create_task_table()

        # Button to complete task
        self.complete_task_button = tk.Button(self, text="Complete Task", command=self.complete_task, state="disabled")
        self.complete_task_button.pack(pady=20)

        # Button to go back
        back_button = tk.Button(self, text="Back", command=self.close_window)
        back_button.pack(pady=20)

    def add_step(self):
        """
        Add a step to the task.
        """
        if len(self.steps) < 8:
            step_detail = self.step_entry.get()
            if step_detail:
                step_number = len(self.steps) + 1
                step_label = f"Step {step_number}: {step_detail}"
                self.steps.append(step_label)
                self.step_entry.delete(0, tk.END)

                self.create_step_frame(step_label)

    def create_step_frame(self, step_label):
        """
        Create a frame for displaying a step.

        """
        step_frame = tk.Frame(self.steps_grid, relief="solid", bd=1, bg="lightblue")
        row, col = divmod(len(self.steps) - 1, 2)
        step_frame.grid(row=row, column=col, padx=20, pady=10, sticky="w")

        step_var = tk.BooleanVar(value=False)
        self.step_vars.append(step_var)

        step_checkbox = tk.Checkbutton(step_frame, text=step_label, variable=step_var, command=self.update_progress, font=("Inter", 14), bg="lightblue", selectcolor="lightblue")
        step_checkbox.pack(side="left", padx=10, pady=10)

        edit_button = tk.Button(step_frame, text="Edit", command=lambda: self.edit_step(step_label, step_frame))
        edit_button.pack(side="left", padx=10)

        delete_button = tk.Button(step_frame, text="Delete", command=lambda: self.delete_step(step_label, step_frame))
        delete_button.pack(side="left", padx=10)

    def edit_step(self, step_label, step_frame):
        """
        Edit a step.

        """
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Step")
        edit_window.geometry("300x150")

        step_detail = step_label.split(": ", 1)[1]
        entry = tk.Entry(edit_window, font=("Inter", 12), width=40)
        entry.insert(0, step_detail)
        entry.pack(pady=20)

        def save_edit():
            new_step_detail = entry.get()
            if new_step_detail:
                step_number = self.steps.index(step_label) + 1
                new_step_label = f"Step {step_number}: {new_step_detail}"
                self.steps[self.steps.index(step_label)] = new_step_label
                for child in step_frame.winfo_children():
                    if isinstance(child, tk.Checkbutton):
                        child.config(text=new_step_label)
                edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_edit)
        save_button.pack(pady=10)

    def delete_step(self, step_label, step_frame):
        """
        Delete a step.

        """
        index = self.steps.index(step_label)
        del self.steps[index]
        del self.step_vars[index]
        step_frame.destroy()
        self.reorder_steps()
        self.update_progress()

    def reorder_steps(self):
        """
        Reorder steps after deleting a step.
        """
        for i, step_label in enumerate(self.steps):
            step_number = i + 1
            new_step_label = f"Step {step_number}: {step_label.split(': ', 1)[1]}"
            self.steps[i] = new_step_label

            step_frame = self.steps_grid.grid_slaves(row=i//2, column=i%2)[0]
            for child in step_frame.winfo_children():
                if isinstance(child, tk.Checkbutton):
                    child.config(text=new_step_label)

    def update_progress(self):
        """
        Update the progress button state based on step completion.
        """
        all_checked = all(var.get() for var in self.step_vars)
        self.complete_task_button.config(state="normal" if all_checked and len(self.steps) == 8 else "disabled")

    def complete_task(self):
        """
        Complete the task and close the window.
        """
        selected_item = self.home_frame.table.selection()
        if selected_item:
            self.home_frame.table.delete(selected_item)
            self.destroy()
        else:
            tk.messagebox.showwarning("No Task Selected", "Please select a task from the table.")

    def close_window(self):
        """
        Close the window.
        """
        self.destroy()

    def create_task_table(self):
        """
        Create the task table.
        """
        table_frame = tk.Frame(self, bg="white", relief="solid", bd=1)
        table_frame.pack(pady=100, side="bottom", fill="x")

        columns = ["Subject", "Task", "Due Date", "Time"]
        task_table = ttk.Treeview(table_frame, columns=columns, show='headings', height=1)
        
        for col in columns:
            task_table.heading(col, text=col)
            task_table.column(col, anchor="center", width=150)
        
        task_table.pack(expand=True, fill="x")

        task_table.insert("", tk.END, values=self.task_data)


class SetReminderWindow(tk.Toplevel):
    def __init__(self, parent):
        """
        Initialize the Set Reminder Window.

        """
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets for the Set Reminder Window.
        """
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
        """
        Set the reminder based on user input.
        """
        task = self.task_var.get()
        daily = self.daily_var.get()
        weekly = self.weekly_var.get()
        monthly = self.monthly_var.get()
        print(f"Reminder set for {task}: daily={daily}, weekly={weekly}, monthly={monthly}")
        self.destroy()


class HomeFrame(tk.Frame):
    def __init__(self, parent, username):
        """
        Initialize the Home Frame.

        """
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.username = username
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        """
        Create widgets for the Home Frame.
        """
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
        
        self.welcome_label = tk.Label(self, text=f"Welcome Back {self.username}", font=("Inter", 30, "italic"), bg="#74b3e0")
        self.welcome_label.place(x=1, y=28, anchor="w")  # Positioning to the right of the sidebar

        # Make the welcome label wrap text to fit within the window width
        max_width = self.winfo_width() - 340  # Adjust based on the window width and padding
        self.welcome_label.config(wraplength=max_width)

    def progress_window(self):
        """
        Open the Progress Tracker Window for the selected task.
        """
        selected_item = self.table.selection()
        if selected_item:
            task_data = self.table.item(selected_item[0])["values"]
            task = task_data[1]
            ProgressTrackerWindow(self.master, self, task, task_data)  # Pass self as the home_frame argument
        else:
            tk.messagebox.showwarning("No Task Selected", "Please select a task from the table.")

    def update_table(self):
        """
        Update the table with user's tasks.
        """
        self.table.delete(*self.table.get_children())
        user = get_user(self.username)
        if user:
            tasks = user.tasks
            for task in tasks:
                self.table.insert("", tk.END, values=(task.subject, task.task, task.due_date, task.time))

    def set_reminder_window(self):
        """
        Open the Set Reminder Window.
        """
        SetReminderWindow(self.master)

    def logout(self):
        """
        Logout the user and show the login window.
        """
        self.master.master.show_login_window()


class MainApp(tk.Tk):
    def __init__(self):
        """
        Initialize the main application window.
        """
        tk.Tk.__init__(self)
        self.title("NCEA Study Tracker")
        self.geometry("1280x720")
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets for the main application window.
        """
        self.home_frame = HomeFrame(self, username="your_username_here")  # Pass the username
        self.home_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
