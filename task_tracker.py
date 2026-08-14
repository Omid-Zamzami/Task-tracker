from datetime import datetime
import json
import sys

tasks_list = []
tasks_dict = {"tasks": tasks_list}
id = 1

def welcome():
    print("***** Welcome to Task Tracker *****")
    print("You can Add, Update, and Delete tasks.")
    print("Also you will be able to observe the status on your tasks and mark them as todo, in-progress, or done.\n")


def main_menu():
    print("***** Main menu *****")
    print("1. Add task")
    print("2. Update task")
    print("3. Delete task")
    print("4. Mark task")
    print("5. Observe tasks (all tasks, todo, in-progress, done)")
    print("6. Quit Task Tracker\n")


def add_task():
    task = {}
    global id
    task_id = id
    id += 1

    task_description = input("Enter your task's description: ")
    task_status = input("Enter your task's status (todo, in-progress, or done): ").lower()
    while task_status not in ["todo", "in-progress", "done"]:
        print("Wrong input! Try again.")
        task_status = input("Enter your task's status (todo, in-progress, or done): ").lower()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    task["id"] = task_id
    task["description"] = task_description
    task["status"] = task_status
    task["created_at"] = created_at
    tasks_list.append(task)
    
    print(f"Task '{task_description}' created")
    print(f"Task id: {task_id}")
    print(f"Status: {task_status}")
    print(f"Created at: {created_at}")

    with open("tasks.json", "w") as file:
        json.dump(tasks_dict, file, indent=2)


def update_task():
    with open("tasks.json", "r") as file:
        data = json.load(file)
    data_list = data["tasks"]

    task_id = 0
    number_of_tasks = len(data_list)
    while task_id < 1 or task_id > number_of_tasks:
        try:
            task_id = int(input(f"Enter the task's id that you want to update (1-{number_of_tasks}): "))
        except ValueError:
            print(f"wrong input! Try a number in the correct range (1-{number_of_tasks}). ")

    for task in tasks_list:
        if task["id"] == task_id:
            print(f"The task's previous description: {task["description"]}")
            new_description = input("Update the description: ")
            updated_description_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["description"] = new_description
            task["updated_description_at"] = updated_description_at

            print("Task description updated")
            print(f"New task description: {task["description"]}")
            print(f"Task updated at: {task["updated_description_at"]}")
            break

    with open("tasks.json", "w") as file:
        json.dump(tasks_dict, file, indent=2)


def delete_task():
    with open("tasks.json", "r") as file:
        data = json.load(file)
    data_list = data["tasks"]

    global id
    task_id = 0
    number_of_tasks = len(data_list)
    while task_id < 1 or task_id > number_of_tasks:
        try:
            task_id = int(input(f"Enter the task's id that you want to delete (1-{number_of_tasks}): "))
        except ValueError:
            print(f"wrong input! Try a number in the correct range (1-{number_of_tasks}).")

    for task in tasks_list:
        if task["id"] == task_id:
            choice = input(f"Are you sure you want to delete {task["description"]} (yes/no, y/n)? ").lower()
            while choice not in ["y", "yes", "n", "no"]:
                choice = input("Wrong input! Try again (yes/no, y/n): ").lower()
            if choice in ["n", "no"]:
                print(f"Task {task["description"]} was not deleted.")
                break
            else:
                deleted_id = task["id"]
                print(f"task {task["description"]} deleted successfully")
                tasks_list.remove(task)
                for other_task in tasks_list:
                    if other_task["id"] > deleted_id:
                        other_task["id"] -= 1
                id -= 1

    with open("tasks.json", "w") as file:
        json.dump(tasks_dict, file, indent=2)


def mark_task():
    with open("tasks.json", "r") as file:
        data = json.load(file)
    data_list = data["tasks"]
    
    task_id = 0
    number_of_tasks = len(data_list)
    while task_id < 1 or task_id > number_of_tasks:
        try:
            task_id = int(input(f"Enter the task's id that you want to change its status (1-{number_of_tasks}): "))
        except ValueError:
            print(f"wrong input! Try a number in the correct range (1-{number_of_tasks}).")

    for task in tasks_list:
        if task["id"] == task_id:
            new_status = input(f"Enter the new status for {task["description"]} (todo, in-progress, or done): ").lower()
            while new_status not in ["todo", "in-progress", "done"]:
                new_status = input("Wrong input! Try again: ")
            updated_status_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            task["status"] = new_status
            task["updated_status_at"] = updated_status_at

            print("Task status updated")
            print(f"New task status: {task["status"]}")
            print(f"Task updated at: {task["updated_status_at"]}")
            break

    with open("tasks.json", "w") as file:
        json.dump(tasks_dict, file, indent=2)


def observe_task():
    with open("tasks.json", "r") as file:
        data = json.load(file)
    data_list = data["tasks"]

    user_status = input("Enter status to see the task(s) with the same status (all tasks, todo, in-progress, done): ").lower()
    while user_status not in ["all tasks", "todo", "in-progress", "done"]:
        user_status = input("Wrong input! Try again (all tasks, todo, in-progress, done): ").lower()

    print()

    if user_status == "all tasks":
        for task in data_list:
            for key, value in task.items():
                print(f"{key}: {value}")
            print()

    else:
        for task in data_list:
            if task["status"] == user_status:
                for key, value in task.items():
                    print(f"{key}: {value}")
                print()


def quit_task_tracker():
    choice = input("Are you sure you want to quit Task Tracker (yes/no, y/n)? ").lower()
    while choice not in ["y", "yes", "n", "no"]:
        choice = input("Wrong input! Try again (yes/no, y/n): ").lower()
    if choice in ["y", "yes"]:
        print("Thank you for using Task Tracker! Goodbye!")
        sys.exit()
    else:
        pass


welcome()

with open("tasks.json", "w") as file:
    json.dump(tasks_dict, file, indent=2)

while True:
    main_menu()
    user_input = 0
    while user_input not in [1, 2, 3, 4, 5, 6]:
        try:
            user_input = int(input("Enter your number of choice (1-6): "))
        except ValueError:
            print("Oops, Wrong input!")

    if (not tasks_list) and (user_input in [2, 3, 4, 5]):
        print("There is no tasks!\n")
        continue
    
    match user_input:
        case 1:
            add_task()
        case 2:
            update_task()
        case 3:
            delete_task()
        case 4:
            mark_task()
        case 5:
            observe_task()
        case 6:
            quit_task_tracker()