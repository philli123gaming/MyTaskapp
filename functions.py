from tkinter import filedialog
from classes import *


def write_tasks_to_file(tasks, todolistname = "tasks"):
    # Default file name
    file_path = filedialog.asksaveasfilename(initialdir="default_note_save",initialfile=todolistname, defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    print("File path selected:", file_path)
    if file_path:
        # Extract the file name from the file path
        file_name = file_path.split("/")[-1]  # Assuming '/' is the path separator
        with open(file_path, 'w') as file:
            for task in tasks:
                file.write(f"{task.name},{task.description},{task.completed},{task.priority},{task.categories}\n")
        print("Tasks saved to:", file_name)


tasks = []

def read_tasks_from_file(file_path):
    new_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            task_data = line.strip().split(',')
            task_name, description, completed, priority, categories = task_data

            if not task_name:
                print("a task has no name will name untitled")
                task_name = "untitled"

            if completed == "True":
                completed = True
            elif completed == "False":
                completed = False
            else:
                print("Status is not a true or false string so setting to false")
                completed = False

            try:
                int(priority)
            except ValueError:
                priority = 2
                print("priority value has unreadable value. Setting to 2 ")


            # Remove the square brackets and split the string by commas
            if categories == "[]":
                categories = []
            else:
                categories = categories[1:-1].split(',')

            # Strip whitespace from each item and create the list
            categories = [category.strip() for category in categories]


            task = Task(task_name, description, completed=completed, priority=int(priority), categories=categories)
            new_tasks.append(task)

        return new_tasks


def open_folder():
    global tasks, dirwindow
    filepath = filedialog.askopenfilename(initialdir="default_note_save", defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    todo_list_name = filepath.split("/")[-1]
    tasks = read_tasks_from_file(filepath)
    dirwindow.destroy()
