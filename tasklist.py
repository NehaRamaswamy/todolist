import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class ToDoApp:
    PRIORITY_CHOICES = ["low", "medium", "high"]

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.pack(pady=20)

        self.entry_task = tk.Entry(self.root, width=50)
        self.entry_task.pack()

        self.priority_var = tk.StringVar(self.root)
        self.priority_var.set(self.PRIORITY_CHOICES[1])

        self.priority_label = tk.Label(self.root, text="Priority:")
        self.priority_label.pack()

        self.priority_menu = tk.OptionMenu(self.root, self.priority_var, *self.PRIORITY_CHOICES)
        self.priority_menu.pack(pady=5)

        self.due_date_label = tk.Label(self.root, text="Due Date (YYYY-MM-DD):")
        self.due_date_label.pack()

        self.due_date_entry = tk.Entry(self.root, width=10)
        self.due_date_entry.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self.root, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.mark_button = tk.Button(self.root, text="Mark Completed", command=self.mark_completed)
        self.mark_button.pack(pady=5)

        self.list_tasks()

    def add_task(self):
        task = self.entry_task.get()
        priority = self.priority_var.get()
        due_date_str = self.due_date_entry.get()

        if not task or not due_date_str:
            messagebox.showerror("Error", "Task and Due Date are required.")
            return

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid Due Date format. Please use YYYY-MM-DD.")
            return

        self.tasks.append({"task": task, "priority": priority, "due_date": due_date})
        self.task_listbox.insert(tk.END, f"{task} ({priority} - {due_date.date()})")
        self.entry_task.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.save_tasks()


    def remove_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.remove_task_by_index(selected_task_index)
        except IndexError:
            messagebox.showerror("Error", "No task selected to remove.")

    def mark_completed(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.mark_completed_by_index(selected_task_index)
        except IndexError:
            messagebox.showerror("Error", "No task selected to mark as completed.")

    def remove_task_by_index(self, index):
        del self.tasks[index]
        self.task_listbox.delete(index)
        self.save_tasks()

    def mark_completed_by_index(self, index):
        task = self.tasks[index]
        messagebox.showinfo("Task Completed", f"Task '{task}' marked as completed.")
        self.remove_task_by_index(index)

    def list_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.tasks):
            self.task_listbox.insert(tk.END, task)

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

if __name__ == "__main__":
    root = tk.Tk()
    todo_app = ToDoApp(root)
    root.mainloop()