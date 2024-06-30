import tkinter as tk
from tkinter import ttk

class SubjectsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for the subjects section
        self.label = ttk.Label(self, text="Welcome to the Subjects section!")
        self.label.pack()
