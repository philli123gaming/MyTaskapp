import sys
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
#import ttkbootstrap as ttk


def write_tasks_to_file(tasks):
    # Default file name
    file_path = open_dialog("save")
    print("File path selected:", file_path)
    if file_path:
        # Extract the file name from the file path
        file_name = file_path.split("/")[-1]  # Assuming '/' is the path separator
        with open(file_path, 'w') as file:
            for task in tasks:
                file.write(f"{task.name},{task.description},{task.completed},{task.priority},{task.categories}\n")
        print("Tasks saved to:", file_name)

def read_tasks_from_file():
    new_tasks = []
    file_path = open_dialog("open")
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

def open_dialog(operation):
    if operation == "open":
        file_path = filedialog.askopenfilename(initialdir="default_note_save", defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    elif operation == "save":
        file_path = filedialog.asksaveasfilename(initialdir="default_note_save", initialfile="Untitled",
                                                 defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return file_path

    todo_list_name = filepath.split("/")[-1]
    todolist.tasks = read_tasks_from_file(filepath)
    list_menu.tkraise()


class Task:
    def __init__(self, name="Untitled", description="", priority: int=2, completed=False, categories=[]):
        self.name = name
        self.description = description
        self.completed = completed
        self.priority = priority
        self.categories = categories


    def __repr__(self):
        if self.priority == 1:
            p_word = "High"
        elif self.priority == 2:
            p_word = "Medium"
        elif self.priority == 3:
            p_word = "Low"
        return f"Task (Name: {self.name} - Description: {self.description} - Status: " + (
            "completed" if self.completed else "Not completed ") + f' - Priority: {self.priority} ({p_word}) - ' \
                                                                   f'Categories: {self.categories}) '

    def priority_num_to_word(self, priority):
        if priority == 1:
            priority = "High"
        elif priority == 2:
            priority = "Medium"
        elif priority == 3:
            priority = "Low"
        return priority

    def to_frame(self, master):
        self.master = master
        self.task_frame = Frame(master)
        self.task_frame.pack()

        self.completed_var = BooleanVar(master)
        self.completed_var.set(self.completed)
        self.completed_check = Checkbutton(self.task_frame, variable=self.completed_var, command=lambda: self.update_completed_status())
        self.completed_check.grid(row=0, column=0)

        # Create a button to display task description
        self.name_button = tk.Button(self.task_frame, text=self.name,
                                borderwidth=0, command=self.display_task_details)
        self.name_button.grid(row=0, column=1)

        # Create a label to display task priority
        self.priority_label = tk.Label(self.task_frame, text=self.priority_num_to_word(self.priority))
        self.priority_label.grid(row=0, column=2)

        # Create a label before the buttons
        self.description_label = tk.Label(master, text=self.description)

        self.description_label.pack(in_=master)
        self.description_label.pack_forget()
        pass

    def display_task_details(self):
        # Display more details about the current task (you can implement this as needed)
        if not self.description_label.winfo_ismapped():
            self.description_label.pack(in_=self.master, after=self.task_frame)
        else:
            self.description_label.pack_forget()
        pass

    def update_completed_status(self):
        # Update the completion status of the current task
        self.completed = self.completed_var.get()
        print(self.completed_var.get())



class Todolist:
    def __init__(self, name=None):
        self.tasks = [Task("TASK 1", "task 1 desc", 2, False, [])]
        self.name = name

    def stop_widgets(self):
        for task in self.tasks:
            task.task_frame.destroy()

    # Add Task: Users can add tasks to their to-do list.
    def add_task(self, task=None, index=None):
        if not task:
            add_window = tk.Tk()
            name = StringVar(add_window)
            description = StringVar(add_window)
            categories = StringVar(add_window)

            priority = IntVar(add_window, value=2)
            task_entry = Entry(add_window, textvariable=name)
            task_entry.pack()
            desc_entry = Entry(add_window, textvariable=description)
            desc_entry.pack()
            priority_combo = ttk.Combobox(add_window, values=[1, 2, 3], textvariable=priority)
            priority_combo.pack()
            category_entry = Entry(add_window, textvariable=categories)
            category_entry.pack()
            add_submit = Button(add_window, text="Create Task", command=lambda: [self.tasks.append(
                Task(name.get() if name.get() else "Untitled",
                     description.get(),
                     int(priority_combo.get()),
                     categories=categories.get().split(",") if categories.get() else [])),add_window.destroy()])
            add_submit.pack()
            add_window.mainloop()

        if index:
            self.tasks.insert(index, task)
        else:
            self.tasks.append(task)
        self.tasks = sorted(self.tasks, key=lambda x: x.priority)
        print("Task added.")

    # View Tasks: Users can view all tasks currently on their to-do list.
    def view_tasks(self):
        def view_tasks_fr(filter=None, None_label = Label(view_button, text="There are no tasks to vie")):
            selected_tasks = []
            self.stop_widgets()
            if self.tasks:
                if filter:
                    selected_tasks = [task for task in self.tasks if filter in task.categories]
                    if not selected_tasks:
                        None_label.pack_forget()
                        None_label.pack()


                for i, task in enumerate((selected_tasks if selected_tasks else self.tasks), 1):
                    print(task)
                    task.to_frame(view_window)

            def display_task_details(self):
                # Display more details about the current task (you can implement this as needed)
                if not self.description_label.winfo_ismapped():
                    self.description_label.pack(in_=self.master, before=self.prev_button)
                else:
                    self.description_label.pack_forget()
                pass
        view_window = tk.Tk()
        back_button = Button(view_window,text="Back",command=view_window.destroy)
        back_button.pack()
        if len(self.tasks) < 1:
            print("There are no tasks to view")
            None_label = Label(view_window,text="There are no tasks to view")
            None_label.pack()
        else:
            filter = StringVar(view_window)
            filter_text = Label(view_window,text="Filter: ")
            filter_text.pack()
            filter_entry = Entry(view_window,textvariable=filter)
            filter_entry.pack()
            #filter_entry.bind("<Key>", lambda event: print("text typed"))
            filter_entry.bind("<Key>", lambda event: view_tasks_fr(filter))
            view_tasks_fr()
            view_window.mainloop()





    # Mark Task as Completed: Users can mark tasks as completed.
    def mark_completed(self):

        if not self.tasks:
            print("No tasks to mark.")
        else:
            self.view_tasks()
            index = (int(input("Enter the number of the task to mark as completed: ")) - 1)

        # marks the task as complete by subtracting the given number by one to get the index
        if len(self.tasks) > 0:
            if self.tasks[index].completed:
                self.tasks[index].completed = False
                print("Task marked as incomplete.")
            else:
                self.tasks[index].completed = True
                print("Task marked as completed.")
        else:
            print("can't find a task for that number.")

    # Remove Task: Users can remove tasks from their to-do list.
    def remove_task(self):
        print("here")
        global history
        if not self.tasks:
            print("No tasks to remove.")
        else:
            self.view_tasks()
            index = (int(input("Enter the index of the task to remove: ")) - 1)
            task = self.tasks[index]
            self.tasks.pop(index)
            history = [{"action": "Remove task"}, task, index]
            print("Task Removed")

    def remove_completed_tasks(self):
        global history
        updated_tasks = []
        removed_tasks = []
        if not self.tasks:
            print("No tasks to remove.")
        else:
            # self.tasks = [task for task in enumerate(self.tasks, 1) if not task.completed]
            for task in self.tasks:
                if task.completed:
                    removed_tasks.append(task)
                else:
                    updated_tasks.append(task)
            self.tasks = updated_tasks
            history = [{"action": "Remove tasks"}, removed_tasks]
        print("Completed tasks have been removed")

    def edit_task(self):

        if not self.tasks:
            print("No tasks to edit.")
        else:
            self.view_tasks()
            index = (int(input("\nwhich task would you like to edit?: ")) - 1)
            if index in range(len(self.tasks)):
                print(self.tasks[index])
                choice2 = input("\nWhat property would you like to change?: "
                                "\nName = 1"
                                "\nDescription = 2"
                                "\nStatus = 3"
                                "\nPriority = 4"
                                "\nCategories = 5")
            else:
                print("Can't find a task for that number view tasks")

        if choice2 == "1":
            property = "Name"
            self.tasks[index].name = input(f"please input what you want to change the {property} to ")
        elif choice2 == "2":
            property = "Description"
            self.tasks[index].description = input(f"please input what you want to change the {property} to ")
        elif choice2 == "3":
            property = "completed"
            self.mark_completed(index)
        elif choice2 == "4":
            property = "Priority"
            response = int(input(
                f"please input what you want to change the {property} to: \nHigh - 1\nMedium - 2\nLow - 3\n"))
            if response in range(1, 4):
                self.tasks[index].priority = response
            else:
                print("Invalid choice back to the start")
        elif choice2 == "5":
            property = "Categories"
            if self.tasks[index].categories:
                while True:
                    print(self.tasks[index].categories)
                    print("These are the categories you can edit")
                    response = input(
                        "Your options are to ADD DELETE or EDIT a category What would you like to do? (You can also type exit to abort editing): ")
                    if response.lower().strip() == "add":
                        while True:
                            self.tasks[index].categories.append(input("Write your category now"))
                            response = input("Do you want to add another one: ")
                            if response.lower().strip() == "yes":
                                continue
                            else:
                                break
                    elif response.lower() == "edit" or response.lower() == "delete":
                        while True:
                            for i, category in enumerate(self.tasks[index].categories):
                                print(f"{i}. ,{category}")
                            try:
                                cat_number = (int(input(f"Enter the number of the task to " + (
                                    "delete" if response.lower() == "delete" else "edit") + ": ")) - 1)
                                if response.lower() == "edit":
                                    print(self.tasks[index].categories[cat_number])
                                    response = input("please type what you would like to edit it too")
                                    self.tasks[index].categories[cat_number] = response
                                else:
                                    self.tasks[index].categories.pop(cat_number)
                            except ValueError:
                                print("not a choosable number")
                                response = input("want to try again?")
                                if response.lower().strip() == "yes":
                                    continue
                                else:
                                    break
                    else:
                        print("nothing changed huh")
                        break
            else:
                response = input(
                    "Your options are to ADD a category What would you like to do? (You can also type exit to abort editing): ")
                if response.lower().strip() == "add":
                    while True:
                        self.tasks[index].categories.append(input("Write your category now"))
                        response = input("Do you want to add another one: ")
                        if response.lower().strip() == "yes":
                            continue
                        else:
                            break
        else:
            print("not a changeable property")

    def undo_action(self):
        global history
        if not history:
            print("No recent tasks to Undo")
        else:
            last_action = history
            if last_action[0]['action'] == "Remove task":
                task = Task(name=last_action[1].name, description=last_action[1].description,
                            priority=last_action[1].priority,
                            completed=last_action[1].completed, categories=last_action[1].categories)
                self.add_task(task=task, index=last_action[2])
                print("Time rewinded")
            elif last_action[0]['action'] == "Remove tasks":
                for task in last_action[1]:
                    task = Task(task.name, task.description, priority=task.priority,
                                completed=task.completed, categories=task.categories)
                    self.add_task(task)
                    print("Time rewinded")
            else:
                print("Time not rewinded")
            last_action = None
            history = []

    def save_list(self):
        if not self.name:
            name = input("What would you like to name your list?\n")
        else:
            response = input(
                f"I see this list is already named {self.name} would you like to to override? ")
            if response.lower().strip() == "yes":
                self.name = input("please write what you would like the new list name to be")
            elif response.lower().strip() == "no":
                print(f"{self.name} it is")

        response = input("Are you sure you want to save (type exit to abort saving\n)"
                         "yes no or exit\n")
        if response.lower().strip() == "yes":
            write_tasks_to_file(self.tasks, name)

class App:
    def __init__(self,todolist = Todolist()):
        pass

    def view_tasks(self):
        self.master = tk.Tk()
        self.master.title(f"To-Do List name: {(todolist.name if todolist.name else 'untitled')}")
        # Initialize current task index
        self.current_task_index = 0

        # Create a frame to hold task information
        self.task_frame = tk.Frame(self.master)
        self.task_frame.pack()

        # Create a Checkbutton for task completion status
        self.completed_var = tk.BooleanVar()
        self.completed_var.set(todolist.tasks[self.current_task_index].completed)
        self.completed_check = tk.Checkbutton(self.task_frame, variable=self.completed_var,
                                              command=self.update_completed_status)
        self.completed_check.grid(row=0, column=0)

        # Create a button to display task description
        self.name_button = tk.Button(self.task_frame, text=todolist.tasks[self.current_task_index].name, borderwidth=0,
                                     command=self.display_task_details)
        self.name_button.grid(row=0, column=1)

        # Create a label to display task priority
        self.priority_label = tk.Label(self.task_frame, text="")
        self.priority_label.grid(row=0, column=2)

        # Create a label before the buttons
        self.description_label = tk.Label(self.master, text=todolist.tasks[self.current_task_index].description)

        # Create navigation buttons
        self.prev_button = tk.Button(self.master, text="Previous Task", command=self.prev_task)
        self.prev_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.master, text="Next Task", command=self.next_task)
        self.next_button.pack(side=tk.RIGHT)

        self.description_label.pack(in_=self.master, before=self.prev_button)
        self.description_label.pack_forget()
        # Display initial task
        self.display_task()
        self.master.mainloop()
    def display_task(self):
        # Get the current task
        current_task = todolist.tasks[self.current_task_index]

        # Update Checkbutton status
        self.completed_var.set(current_task.completed)

        # Update button text with task description
        self.name_button.config(text=current_task.name)

        # Update label with task priority
        self.priority_label.config(text=f"Priority: {current_task.priority}")

        self.description_label.config(text=current_task.description)

    def update_completed_status(self):
        # Update the completion status of the current task
        todolist.tasks[self.current_task_index].completed = self.completed_var.get()

    def prev_task(self):
        # Move to the previous task
        if self.current_task_index > 0:
            self.current_task_index -= 1
            self.display_task()
            self.description_label.pack_forget()

    def next_task(self):
        # Move to the next task
        if self.current_task_index < len(self.tasks) - 1:
            self.current_task_index += 1
            self.display_task()
            self.description_label.pack_forget()

    def display_task_details(self):
        # Display more details about the current task (you can implement this as needed)
        if not self.description_label.winfo_ismapped():
            self.description_label.pack(in_=self.master,before=self.prev_button)
        else:
            self.description_label.pack_forget()
        pass

# Create and run the Tkinter application




todolist = Todolist()
history = []
app = App(todolist)

def create_new_list():
    global todolist, history
    todolist = Todolist()
    history = []

def exit():
    sys.exit()

window = tk.Tk()
window.geometry("600x800")
window.title("ToDoListApp")

Main_menu = Frame(window)
Main_menu.grid(row=0, column=0, sticky="nsew")
Page_Title = Label(Main_menu, text="Main Menu", font=24)
Page_Title.pack()
Load_list_button = Button(Main_menu, text="1. Load to do list",
                          command=lambda: [read_tasks_from_file(), list_menu.tkraise()])
Load_list_button.pack()
Make_list_button = Button(Main_menu, text="2. Start from scratch",
                          command=lambda: [list_menu.tkraise(), create_new_list()])
Make_list_button.pack()
exit_button = Button(Main_menu, text="0. Close app", command=exit)
exit_button.pack()

list_menu = Frame(window)
list_menu.grid(row=0, column=0, sticky="nsew")

label = Label(list_menu, text="list menu")
label.pack(pady=20)

print("\n1. Add Task")
add_button = Button(list_menu, text="1. Add Task", command=todolist.add_task)
add_button.pack()
print("2. View Tasks")
view_button = Button(list_menu, text="1. View Tasks", command=todolist.view_tasks)
view_button.pack()
print("3. Edit tasks")
edit_button = Button(list_menu, text="1. Edit Tasks", command=todolist.edit_task)
edit_button.pack()
print("4. Mark Task as Completed / Incomplete")
mark_button = Button(list_menu, text="4. Mark Task as Completed / Incomplete", command=todolist.mark_completed)
mark_button.pack()
print("5. Remove Task")
remove_button = Button(list_menu, text="5. Remove Task", command=todolist.remove_task)
remove_button.pack()
print("6. Remove completed Tasks")
remove_c_button = Button(list_menu, text="6. Remove completed Tasks", command=todolist.remove_completed_tasks)
remove_c_button.pack()
print("7. Undo Action")
undo_button = Button(list_menu, text="7. Undo Action", command=todolist.undo_action)
undo_button.pack()
print("8. Save List")
save_button = Button(list_menu, text="8. Save List", command=todolist.save_list)
save_button.pack()
print("9. Back to Main Menu")
back_button = Button(list_menu, text="9. Back to Main Menu", command=lambda: Main_menu.tkraise())
back_button.pack()
print("0. Exit")
exit_button = Button(list_menu, text="X", command=exit)
exit_button.pack()

Main_menu.tkraise()


window.mainloop()
