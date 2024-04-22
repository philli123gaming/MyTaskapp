import sys
import tkinter as tk

from tkinter import *
from tkinter import filedialog

import classes
from functions import *



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

            todo_list = classes.Todolist()
            todo_list.tasks = tasks
            try:
                todo_list.name = todo_list_name
            except NameError:
                todo_list.name = None


        elif choice == "2":
            todo_list = classes.Todolist()

        elif choice == "0":
            sys.exit()

        else:
            print("Invalid Choice")
            continue

        window = tk.Tk()
        window.geometry("600x800")

        list_menu = Frame(window)
        list_menu.grid(row=0, column=0, sticky="nsew")


        label = Label(list_menu, text="list menu")
        label.pack(pady=20)

        while True:
            list_menu.tkraise()
            choice = StringVar(value=None)

            def choice_maker(value):
                if value == "1":
                    choice.set("1")

            print("\n1. Add Task")
            add_button = Button(list_menu, text= "1. Add Task", command=lambda : choice_maker("1"))
            add_button.pack()
            print("2. View Tasks")
            view_button = Button(list_menu, text= "1. View Tasks")
            view_button.pack()
            print("3. Edit tasks")
            edit_button = Button(list_menu, text= "1. Edit Tasks")
            edit_button.pack()
            print("4. Mark Task as Completed / Incomplete")
            mark_button = Button(list_menu, text= "4. Mark Task as Completed / Incomplete")
            mark_button.pack()
            print("5. Remove Task")
            remove_button = Button(list_menu, text="5. Remove Task")
            remove_button.pack()
            print("6. Remove completed Tasks")
            remove_c_button = Button(list_menu, text="6. Remove completed Tasks")
            remove_c_button.pack()
            print("7. Undo Action")
            undo_button = Button(list_menu, text="7. Undo Action")
            undo_button.pack()
            print("8. Save List")
            save_button = Button(list_menu, text="8. Save List")
            save_button.pack()
            print("9. Back to Main Menu")
            back_button = Button(list_menu, text="9. Back to Main Menu")
            back_button.pack()
            print("0. Exit")
            exit_button = Button(list_menu, text="X")
            exit_button.pack()

            if not choice.get():
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

                    task = classes.Task(name, description, priority=int(priority), categories=categories)

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
                        choice1 = (int(input("\nwhich task would you like to edit?: ")) - 1)
                        if choice1 not in range(len(todo_list.tasks)):
                            print("Can't find a task for that number view tasks")
                        else:
                            print(todo_list.tasks[choice1])
                            choice2 = input("\nWhat property would you like to change?: "
                                            "\nName = 1"
                                            "\nDescription = 2"
                                            "\nStatus = 3"
                                            "\nPriority = 4"
                                            "\nCategories = 5")
                            todo_list.edit_task(choice1, choice2)

                elif choice == "4":
                    if not todo_list.tasks:
                        print("No tasks to mark.")
                    else:
                        todo_list.view_tasks()
                        choice = (int(input("Enter the number of the task to mark as completed: ")) - 1)
                        todo_list.mark_completed(choice)

                elif choice == "5":
                    if not todo_list.tasks:
                        print("No tasks to remove.")
                    else:
                        todo_list.view_tasks()
                        choice = (int(input("Enter the index of the task to remove: ")) - 1)

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

    window.mainloop()
if __name__ == "__main__":
    main()
