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


class Todolist:
    def __init__(self, name=None):
        self.name = name
        self.tasks = []

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
            if filter:
                return [(task.name, task.description, task.completed, task.priority, task.categories) for task in
                        self.tasks if filter in task.categories]
            else:
                return [(task.name, task.description, task.completed, task.priority, task.categories) for task in
                        self.tasks]
            # for i, task in enumerate(self.tasks, 1):
            # print(f"{i}. {task.name} - {task.description} - {'Completed' if task.completed else 'Not Completed'}")

    # Mark Task as Completed: Users can mark tasks as completed.
    def mark_completed(self, task_index):
        # marks the task as complete by subtracting the given number by one to get the index
        if task_index >= 1 and task_index <= len(self.tasks):
            if self.tasks[task_index - 1].completed:
                self.tasks[task_index - 1].completed = False
                print("Task marked as incomplete.")
            else:
                self.tasks[task_index - 1].completed = True
                print("Task marked as completed.")
        else:
            print("Invalid task index.")

    # Remove Task: Users can remove tasks from their to-do list.
    def remove_task(self, task_index):
        self.tasks.pop(task_index - 1)

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

    def edit_task(self, choice1, choice2):
        if choice2 == "1":
            property = "Name"
        elif choice2 == "2":
            property = "Description"
        elif choice2 == "3":
            property = "completed"
        elif choice2 == "4":
            property = "Priority"
        elif choice2 == "5":
            property = "Categories"
        else:
            print("not a changeable property")

        if property == "Name":
            self.tasks[choice1 - 1].name = input(f"please input what you want to change the {property} to")
        elif property == "Description":
            self.tasks[choice1 - 1].description = input(f"please input what you want to change the {property}")
        elif property == "Priority":
            response = int(input(
                f"please input what you want to change the {property} to: \nHigh - 1\nMedium - 2\nLow - 3\n"))
            if response in range(1, 4):
                self.tasks[choice1 - 1].priority = response
        elif property == "Categories":
            if self.tasks[choice1 - 1].categories:
                print(self.tasks[choice1 - 1].categories)
                print("These are the categories you can edit")
        print("Record edited")

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


def view_tasks(tasks):
    for i, task in enumerate(tasks, 1):
        name, description, completed, priority, categories = task
        if priority == 1:
            priority = "High"
        elif priority == 2:
            priority = "Medium"
        elif priority == 3:
            priority = "Low"
        print(
            f"{i}. {name} - {description} - Status: {'Completed' if completed else 'Not Completed'} - Priority: {priority} - categories: {categories}")


def write_tasks_to_file(tasks, todolistname):
    with open(todolistname, 'w') as file:
        for task in tasks:
            file.write(f"{task.name},{task.description},{task.completed},{task.priority},{task.categories}\n")


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
    filepath = filedialog.askopenfilename(initialdir="C:\Documents", title="Open a Text File")
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

            dirwindow.mainloop()

            todo_list = Todolist()
            todo_list.tasks = tasks
            todo_list.name = todo_list_name

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
                if response.lower() == "yes":
                    while True:
                        categories.append(input("Write your category now"))
                        response = input("Do you want to add another one: ")
                        if response.lower() == "yes":
                            continue
                        else:
                            break

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

                task = Task(name, description, priority=int(priority), categories=categories)

                todo_list.add_task(task)
                print("Task added.")

            elif choice == "2":
                response = input("is there a filter you would like to add")
                if response.lower() == "yes":
                    filter = (input("Write your filter now"))
                    tasks = todo_list.view_tasks(filter)
                else:
                    tasks = todo_list.view_tasks()

                if not tasks:
                    print("No tasks.")
                else:
                    view_tasks(tasks)

            elif choice == "3":
                tasks = todo_list.view_tasks()
                if not tasks:
                    print("No tasks to edit.")
                else:
                    view_tasks(tasks)
                    choice1 = int(input("\nwhich task would you like to edit "))
                    if choice1 not in range(len(tasks) + 1):
                        print("Can't find a task for that number view tasks")
                    else:
                        print(tasks[int(choice1) - 1])
                        choice2 = input("What would you like to change"
                                        "\nName = 1"
                                        "\nDescription = 2"
                                        "\nIs it completed = 3"
                                        "\nPriority = 4"
                                        "\nCategories = 5")
                        todo_list.edit_task(choice1, choice2)

            elif choice == "4":
                tasks = todo_list.view_tasks()
                if not tasks:
                    print("No tasks to mark.")
                else:
                    view_tasks(tasks)
                    task_index = int(input("Enter the index of the task to mark as completed: "))
                    todo_list.mark_completed(task_index)

            elif choice == "5":
                tasks = todo_list.view_tasks()
                if not tasks:
                    print("No tasks to remove.")
                else:
                    view_tasks(tasks)
                    task_index = int(input("Enter the index of the task to remove: "))
                    todo_list.remove_task(task_index)
                    history = [{"action": "Remove task"}, tasks[task_index - 1], (int(task_index) - 1)]

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

                response = input("Are you sure you want to save"
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
