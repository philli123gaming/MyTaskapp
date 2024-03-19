import sys


class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.completed = False


class Todolist:
    def __init__(self):
        self.tasks = []

    # Add Task: Users can add tasks to their to-do list.
    def add_task(self, task):
        self.tasks.append(task)

    # View Tasks: Users can view all tasks currently on their to-do list.
    def view_tasks(self):
        if len(self.tasks) < 1:
            print("There are no tasks to delete")
        else:
            return [(task.name, task.description, task.completed) for task in self.tasks]
            #for i, task in enumerate(self.tasks, 1):
                #print(f"{i}. {task.name} - {task.description} - {'Completed' if task.completed else 'Not Completed'}")

    # Mark Task as Completed: Users can mark tasks as completed.
    def mark_completed(self, task_index):
        #marks the task as complete by subtracting the given number by one to get the index
        if task_index >= 1 and task_index <= len(self.tasks):
            self.tasks[task_index - 1].completed = True
            print("Task marked as completed.")
        else:
            print("Invalid task index.")

    # Remove Task: Users can remove tasks from their to-do list.
    def remove_task(self, task_index):
        self.tasks.pop(task_index - 1)

    def remove_completed_tasks(self):
        respone = input("Are you sure"
                        "\n1. Yes"
                        "\n2. No")
        if respone == "1":
            if not self.tasks:
                print("No tasks.")
            else:
                self.tasks = [task for task in self.tasks if not task.completed]
                print("Completed tasks have been removed")


def main():
    todo_list = Todolist()

    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Remove Task")
        print("6. Remove completed Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter task name: ")
            description = input("Enter task description: ")
            task = Task(name, description)
            todo_list.add_task(task)
            print("Task added.")

        elif choice == "2":
            tasks = todo_list.view_tasks()
            if not tasks:
                print("No tasks.")
            else:
                for i, task in enumerate(tasks, 1):
                    name, description, completed = task
                    print(f"{i}. {name} - {description} - {'Completed' if completed else 'Not Completed'}")

        elif choice == "3":
            tasks = todo_list.view_tasks()
            if not tasks:
                print("No tasks to mark.")
            else:
                for i, task in enumerate(tasks, 1):
                    name, description, completed = task
                    print(f"{i}. {name} - {description} - {'Completed' if completed else 'Not Completed'}")
                task_index = int(input("Enter the index of the task to mark as completed: "))
                todo_list.mark_completed(task_index)

        elif choice == "4":
            tasks = todo_list.view_tasks()
            if not tasks:
                print("No tasks to remove.")
            else:
                for i, task in enumerate(tasks, 1):
                    name, description, completed = task
                    print(f"{i}. {name} - {description} - {'Completed' if completed else 'Not Completed'}")
                task_index = int(input("Enter the index of the task to remove: "))
                todo_list.remove_task(task_index)


        elif choice == "5":
            print("Exiting...")
            sys.exit()

        elif choice == "6":
            todo_list.remove_completed_tasks()

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()





