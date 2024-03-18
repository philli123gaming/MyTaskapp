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
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task.name} - {task.description} - {'Completed' if task.completed else 'Not Completed'}")

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




mytodolist = Todolist()

task1 = Task("wash dishes", "self explanatory really")
mytodolist.add_task(task1)
mytodolist.view_tasks()

mytodolist.mark_completed(1)

mytodolist.view_tasks()

mytodolist.remove_task(1)
mytodolist.view_tasks()



