import sys

from tkinter import *
from tkinter import filedialog


class Task:
    def __init__(self, name, description, priority=2, completed=False, categories=[]):
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
            "completed" if self.completed else "Not completed ") + f' - Priority: {self.priority} ({p_word}) - Categories: {self.categories})'

    def priority_num_to_word(self, priority):
        if priority == 1:
            priority = "High"
        elif priority == 2:
            priority = "Medium"
        elif priority == 3:
            priority = "Low"
        return priority


class Todolist:
    def __init__(self, name=None):

        self.tasks = []
        self.name = name

    # Add Task: Users can add tasks to their to-do list.
    def add_task(self, task, index=0):
        if index:
            self.tasks.insert(index, task)
        else:
            self.tasks.append(task)
        self.tasks = sorted(self.tasks, key=lambda x: x.priority)

    # View Tasks: Users can view all tasks currently on their to-do list.
    def view_tasks(self, filter=None):
        if len(self.tasks) < 1:
            print("There are no tasks to view")
        else:
            filtered_tasks = []
            if filter:
                filtered_tasks = [task for task in self.tasks if filter in task.categories]
                for i, task in enumerate(filtered_tasks, 1):
                    print(f"{i}. {task.name} - {task.description} - Status: {'Completed' if task.completed else 'Not Completed'} - Priority: {task.priority_num_to_word(task.priority)} - categories: {task.categories}")

            else:
                for i, task in enumerate(self.tasks, 1):
                    print(
                        f"{i}. {task.name} - {task.description} - Status: {'Completed' if task.completed else 'Not Completed'} - Priority: {task.priority_num_to_word(task.priority)} - categories: {task.categories}")





            # for i, task in enumerate(self.tasks, 1):
            # print(f"{i}. {task.name} - {task.description} - {'Completed' if task.completed else 'Not Completed'}")

    # Mark Task as Completed: Users can mark tasks as completed.
    def mark_completed(self, index):
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
    def remove_task(self, index):
        task = self.tasks[index]
        self.tasks.pop(index)
        return task


    def remove_completed_tasks(self):
        updated_tasks = []
        removed_tasks = []
        if not self.tasks:
            print("No tasks.")
        else:
            # self.tasks = [task for task in enumerate(self.tasks, 1) if not task.completed]
            for task in self.tasks:
                if task.completed:
                    removed_tasks.append(task)
                else:
                    updated_tasks.append(task)
            self.tasks = updated_tasks
            return removed_tasks

    def edit_task(self, index, choice2):
        if choice2 == "1":
            property = "Name"
            self.tasks[index].name = input(f"please input what you want to change the {property} to")
        elif choice2 == "2":
            property = "Description"
            self.tasks[index].description = input(f"please input what you want to change the {property}")
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
                    response = input("Your options are to ADD DELETE or EDIT a category What would you like to do? (You can also type exit to abort editing): ")
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
                                cat_number = (int(input(f"Enter the number of the task to " + ("delete" if response.lower() == "delete" else "edit") + ": "))-1)
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


    def undo_action(self, last_action):
        if last_action[0]['action'] == "Remove task":
            task = Task(name=last_action[1].name, description=last_action[1].description,
                        priority=last_action[1].priority,
                        completed=last_action[1].completed, categories=last_action[1].categories)
            self.add_task(task, last_action[2])
            print("Time rewinded")
        elif last_action[0]['action'] == "Remove tasks":
            for task in last_action[1]:
                task = Task(task.name, task.description, priority=task.priority,
                            completed=task.completed, categories=task.categories)
                self.add_task(task)
                print("Time rewinded")
        else:
            print("Time not rewinded")

def write_tasks_to_file(tasks, todolistname):
    default_file_name = "tasks"  # Default file name
    file_path = filedialog.asksaveasfilename(initialdir="default_note_save", defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    print("File path selected:", file_path)
    if file_path:
        # Extract the file name from the file path
        file_name = file_path.split("/")[-1]  # Assuming '/' is the path separator
        print("File name:", file_name)
        with open(file_path, 'w') as file:
            for task in tasks:
                file.write(f"{task.task_name},{task.priority},{task.completed}\n")
        print("Tasks saved to:", file_path)

tasks = []

def read_tasks_from_file(file_path):
    new_tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            task_data = line.strip().split(',')
            task_name, description, completed, priority, categories = task_data

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
    filepath = filedialog.asksaveasfilename(initialdir="default_note_save", defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    todo_list_name = filepath.split("/")[-1]
    tasks = read_tasks_from_file(filepath)
    dirwindow.destroy()


def main():
    global tasks, dirwindow, todo_list_name
    while True:
        print("Main Menu")
        print("1. Load to do list")
        print("2. Start from scratch")
        print("0. Close app")

        choice = input("Enter your choice: ")

        history = []
        if choice == "1":
            # Creating an instance of window
            dirwindow = Tk(screenName="here")

            # Set the geometry of the window
            dirwindow.geometry("700x300")

            # Create a label
            Label(dirwindow, text="Click the button to select your task file (it should be a csv file)",
                  font='Arial 16 bold').pack(pady=15)

            # change back to just C:/ for late

            # Create a button to trigger the dialog
            button = Button(dirwindow, text="Open", command=open_folder)
            button.pack()

            dirwindow.focus_force()
            dirwindow.lift()
            dirwindow.mainloop()

            todo_list = Todolist()
            todo_list.tasks = tasks
            try:
                todo_list.name = todo_list_name
            except NameError:
                todo_list.name = None


        elif choice == "2":
            todo_list = Todolist()

        elif choice == "0":
            sys.exit()

        else:
            print("Invalid Choice")
            continue

        while True:
            print("\n1. Add Task")
            print("2. View Tasks")
            print("3. Edit tasks")
            print("4. Mark Task as Completed / Incomplete")
            print("5. Remove Task")
            print("6. Remove completed Tasks")
            print("7. Undo Action")
            print("8. Save List")
            print("9. Back to Main Menu")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter task name: ")
                if name == "":  name = "untitled"
                description = input("Enter task description: ")
                priority = input("What priority is it "
                                 "\nHigh = 1"
                                 "\nMedium = 2"
                                 "\nLow = 3\n")
                categories = []
                response = input("are there any categories you would like to add\n")

                if not priority == "":
                    try:
                        if int(priority) not in range(1, 4):
                            print("not applicable priority number setting at default")
                            priority = 2
                    except ValueError:
                        print("not applicable priority number setting at default")
                        priority = 2
                else:
                    print("not applicable priority number setting at default")
                    priority = 2

                if response.lower() == "yes":
                    while True:
                        categories.append(input("Write your category now"))
                        response = input("Do you want to add another one: ")
                        if response.lower() == "yes":
                            continue
                        else:
                            break

                task = Task(name, description, priority=int(priority), categories=categories)

                todo_list.add_task(task)
                print("Task added.")

            elif choice == "2":
                if not todo_list.tasks:
                    print("No tasks to see.")
                else:
                    response = input("is there a filter you would like to add? ")
                    if response.lower() == "yes":
                        filter = (input("Write your filter now"))
                        todo_list.view_tasks(filter)
                    else:
                        todo_list.view_tasks()


            elif choice == "3":
                if not todo_list.tasks:
                    print("No tasks to edit.")
                else:
                    todo_list.view_tasks()
                    choice1 = (int(input("\nwhich task would you like to edit?: "))-1)
                    if choice1 not in range(len(todo_list.tasks)):
                        print("Can't find a task for that number view tasks")
                    else:
                        print(todo_list.tasks[choice1])
                        choice2 = input("\nName = 1"
                                        "\nDescription = 2"
                                        "\nStatus = 3"
                                        "\nPriority = 4"
                                        "\nCategories = 5"
                                        "\nWhat property would you like to change?: ")
                        todo_list.edit_task(choice1, choice2)

            elif choice == "4":
                if not todo_list.tasks:
                    print("No tasks to mark.")
                else:
                    todo_list.view_tasks()
                    choice = (int(input("Enter the number of the task to mark as completed: "))-1)
                    todo_list.mark_completed(choice)

            elif choice == "5":
                if not todo_list.tasks:
                    print("No tasks to remove.")
                else:
                    todo_list.view_tasks()
                    choice = (int(input("Enter the index of the task to remove: "))-1)

                    history = [{"action": "Remove task"}, todo_list.remove_task(choice), choice]

            elif choice == "6":
                history = [{"action": "Remove tasks"}, todo_list.remove_completed_tasks()]
                print("Completed tasks have been removed")

            elif choice == "7":
                if not history:
                    print("No recent tasks to Undo")
                else:
                    todo_list.undo_action(history)
                    history = []

            # if there aren't any say it
            # grabs the last action done

            # use the last action done only to reverse changes
            # some other functions need to be able to record history

            elif choice == "8":

                if not todo_list.name:
                    name = input("What would you like to name your list?\n")
                else:
                    response = input(
                        f"I see this list is already named {todo_list.name} would you like to to override? ")
                    if response.lower().strip() == "yes":
                        todo_list.name = input("please write what you would like the new list name to be")
                    elif response.lower().strip() == "no":
                        print(f"{todo_list_name} it is")

                response = input("Are you sure you want to save (type exit to abort saving\n)"
                                 "yes no or exit\n")
                if response.lower().strip() == "yes":
                    write_tasks_to_file(todo_list.tasks, name)
                elif response.lower().strip() == "exit":
                    break
                else:
                    continue

            elif choice == "9":
                print("Back to the Main menu")
                break

            elif choice == "0":
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
