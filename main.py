import sys


class Task:
    def __init__(self, name, description, priority=2, completed=False, catergories=[]):
        self.name = name
        self.description = description
        self.completed = completed
        self.priority = priority
        self.catergories = catergories


class Todolist:
    def __init__(self):
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
                return [(task.name, task.description, task.completed, task.priority, task.catergories) for task in self.tasks if filter in task.catergories]
            else:
                return [(task.name, task.description, task.completed, task.priority, task.catergories) for task in
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
        #respone = input("Are you sure"
        #                "\n1. Yes"
         #               "\n2. No")
        #if respone == "1":
            if not self.tasks:
                print("No tasks.")
            else:
                # self.tasks = [task for task in enumerate(self.tasks, 1) if not task.completed]
                updated_tasks = []
                removed_tasks = []
                for task in self.tasks:
                    if not task.completed:
                        updated_tasks.append(task)
                    else:
                        removed_tasks.append([task.name, task.description, task.completed, task.priority])
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
            property = "Catergories"
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
        elif property == "Catergories":
            if self.tasks[choice1 - 1].catergories:
                print(self.tasks[choice1 - 1].catergories)
                print("These are the catergories you can edit")
        print("Reocrd edited")

    def undo_action(self, last_action):
        if last_action[0]['action'] == "Remove task":
            task = Task(last_action[1][0], last_action[1][1], priority=last_action[1][3],
                        completed=last_action[1][2])
            self.add_task(task, last_action[2])
            print("Time rewinded")
        elif last_action[0]['action'] == "Remove tasks":
            for task in last_action[1]:
                task = Task(task[0], task[1], priority=task[3],
                            completed=task[2])
                self.add_task(task)
                print("Time rewinded")

        else:
            print("Time not rewinded")


def view_tasks(tasks):
    for i, task in enumerate(tasks, 1):
        name, description, completed, priority, catergories = task
        if priority == 1:
            priority = "High"
        elif priority == 2:
            priority = "Medium"
        elif priority == 3:
            priority = "Low"
        print(f"{i}. {name} - {description} - Status: {'Completed' if completed else 'Not Completed'} - Priority: {priority} - catergories: {catergories}")


def main():
    todo_list = Todolist()
    history = []

    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed / Incomplete")
        print("4. Remove Task")
        print("6. Remove completed Task")
        print("5. Exit")
        print("7. Edit tasks")
        print("8. Undo Action")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter task name: ")
            description = input("Enter task description: ")
            priority = input("What priority is it "
                             "\nHigh = 1"
                             "\nMedium = 2"
                             "\nLow = 3\n")
            catergories = []
            response = input("are there any categories you would like to add")
            if response.lower() == "yes":
                while True:
                    catergories.append(input("Write your catergory now"))
                    response = input("Do you want to add another one")
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

            task = Task(name, description, priority=int(priority), catergories=catergories)
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
                print("No tasks to mark.")
            else:
                view_tasks(tasks)
                task_index = int(input("Enter the index of the task to mark as completed: "))
                todo_list.mark_completed(task_index)

        elif choice == "4":
            tasks = todo_list.view_tasks()
            if not tasks:
                print("No tasks to remove.")
            else:
                view_tasks(tasks)
                task_index = int(input("Enter the index of the task to remove: "))
                todo_list.remove_task(task_index)
                history = [{"action": "Remove task"}, tasks[task_index - 1], (int(task_index) - 1)]


        elif choice == "5":
            print("Exiting...")
            sys.exit()

        elif choice == "6":
            history = [{"action": "Remove tasks"}, todo_list.remove_completed_tasks()]
            print("Completed tasks have been removed")

            # history.append(                [{"action": "Remove tasks"}, tasks[task_index - 1], (int(task_index) - 1)]            )

        elif choice == "7":
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
                                    " \nName = 1"
                                    "\nDescription = 2"
                                    "\nIs it completed = 3"
                                    "\nPriority = 4"
                                    "\nCatergories = 5")
                    todo_list.edit_task(choice1, choice2)

        elif choice == "8":
            if not history:
                print("No recent tasks to Undo")
            else:
                todo_list.undo_action(history)
                history = []

        # if there aren't any say it
        # grab the last acction done

        # use the last action done only to reverse changes
        # some other functions need to be able to record history
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
