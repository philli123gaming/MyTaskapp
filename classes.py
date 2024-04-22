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
                    print(
                        f"{i}. {task.name} - {task.description} - Status: {'Completed' if task.completed else 'Not Completed'} - Priority: {task.priority_num_to_word(task.priority)} - categories: {task.categories}")

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