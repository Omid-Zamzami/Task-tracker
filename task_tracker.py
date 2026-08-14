from datetime import datetime
import json
import sys

FILENAME = "tasks.json"

initial_dict = {"tasks": []}

try:
    with open(FILENAME, "r") as file:
        initial_dict = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    with open(FILENAME, "w") as file:
        json.dump(initial_dict, file, indent=2)

tasks_list = initial_dict.get("tasks", [])
tasks_dict = {"tasks": tasks_list}

if not tasks_list:
    next_id = 1
else:
    next_id = max(task["id"] for task in tasks_list) + 1


def save_tasks():
    with open(FILENAME, "w") as file:
        json.dump(tasks_dict, file, indent=2)


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def welcome():
    print("***** Welcome to Task Tracker *****")
    print("You can Add, Update, and Delete tasks.")
    print("Also you will be able to observe the status of your tasks and mark them as todo, in-progress, or done.\n")


def main_menu():
    print("***** Main Menu *****")
    print("1. Add task")
    print("2. Update task")
    print("3. Delete task")
    print("4. Mark task")
    print("5. Observe tasks (all tasks/all, todo, in-progress, done)")
    print("6. Quit Task Tracker\n")


def add_task():
    global next_id

    task_description = input("Enter your task's description: ").strip()
    while not task_description:
        print("Description cannot be empty! Try again.")
        task_description = input("Enter your task's description: ").strip()

    task_status = input("Enter your task's status (todo, in-progress, or done): ").strip().lower()
    while task_status not in ["todo", "in-progress", "done"]:
        print("Wrong input! Try again.")
        task_status = input("Enter your task's status (todo, in-progress, or done): ").strip().lower()

    created_at = get_current_time()

    task = {
        "id": next_id,
        "description": task_description,
        "status": task_status,
        "created_at": created_at,
    }

    tasks_list.append(task)
    next_id += 1
    save_tasks()

    print(f"\nTask '{task_description}' created successfully!")
    print(f"Task ID: {task['id']}")
    print(f"Status: {task_status}")
    print(f"Created at: {created_at}\n")


def update_task():
    valid_ids = [t["id"] for t in tasks_list]
    task_id = 0

    while task_id not in valid_ids:
        try:
            task_id = int(input(f"Enter the task's ID that you want to update ({min(valid_ids)}-{max(valid_ids)}): "))
            if task_id not in valid_ids:
                print("Task ID not found! Try again.")
        except ValueError:
            print("Wrong input! Please enter a valid number.")

    for task in tasks_list:
        if task["id"] == task_id:
            print(f"The task's previous description: {task['description']}")
            new_description = input("Update the description: ").strip()
            while not new_description:
                print("Description cannot be empty! Try again.")
                new_description = input("Update the description: ").strip()

            task["description"] = new_description
            task["updated_description_at"] = get_current_time()

            print("\nTask description updated!")
            print(f"New task description: {task['description']}")
            print(f"Task updated at: {task['updated_description_at']}\n")
            break

    save_tasks()


def delete_task():
    global next_id
    valid_ids = [t["id"] for t in tasks_list]
    task_id = 0

    while task_id not in valid_ids:
        try:
            task_id = int(input(f"Enter the task's ID that you want to delete ({min(valid_ids)}-{max(valid_ids)}): "))
            if task_id not in valid_ids:
                print("Task ID not found! Try again.")
        except ValueError:
            print("Wrong input! Please enter a valid number.")

    for task in tasks_list:
        if task["id"] == task_id:
            choice = input(f"Are you sure you want to delete '{task['description']}' (yes/no, y/n)? ").strip().lower()
            while choice not in ["y", "yes", "n", "no"]:
                choice = input("Wrong input! Try again (yes/no, y/n): ").strip().lower()

            if choice in ["n", "no"]:
                print(f"Task '{task['description']}' was not deleted.\n")
                return

            deleted_id = task["id"]
            tasks_list.remove(task)

            for other_task in tasks_list:
                if other_task["id"] > deleted_id:
                    other_task["id"] -= 1

            next_id -= 1
            save_tasks()
            print(f"Task '{task['description']}' deleted successfully!\n")
            break


def mark_task():
    valid_ids = [t["id"] for t in tasks_list]
    task_id = 0

    while task_id not in valid_ids:
        try:
            task_id = int(input(f"Enter the task's ID that you want to change its status ({min(valid_ids)}-{max(valid_ids)}): "))
            if task_id not in valid_ids:
                print("Task ID not found! Try again.")
        except ValueError:
            print("Wrong input! Please enter a valid number.")

    for task in tasks_list:
        if task["id"] == task_id:
            new_status = input(f"Enter the new status for '{task['description']}' (todo, in-progress, or done): ").strip().lower()
            while new_status not in ["todo", "in-progress", "done"]:
                new_status = input("Wrong input! Try again (todo, in-progress, done): ").strip().lower()

            task["status"] = new_status
            task["updated_status_at"] = get_current_time()

            save_tasks()
            print("\nTask status updated!")
            print(f"New task status: {task['status']}")
            print(f"Task updated at: {task['updated_status_at']}\n")
            break


def observe_task():
    user_status = input("Enter status to see tasks (all tasks/all, todo, in-progress, done): ").strip().lower()
    while user_status not in [
        "all tasks",
        "all",
        "todo",
        "in-progress",
        "done",
    ]:
        user_status = input("Wrong input! Try again (all tasks/all, todo, in-progress, done): ").strip().lower()

    print()
    filtered_tasks = (
        tasks_list
        if user_status in ["all tasks", "all"]
        else [t for t in tasks_list if t["status"] == user_status])

    if not filtered_tasks:
        print("No tasks found for this status.\n")
        return

    for task in filtered_tasks:
        for key, value in task.items():
            print(f"{key}: {value}")
        print()
    print()


def quit_task_tracker():
    choice = input("Are you sure you want to quit Task Tracker (yes/no, y/n)? ").strip().lower()
    while choice not in ["y", "yes", "n", "no"]:
        choice = input("Wrong input! Try again (yes/no, y/n): ").strip().lower()

    if choice in ["y", "yes"]:
        print("Thank you for using Task Tracker! Goodbye!")
        sys.exit()


welcome()
while True:
    main_menu()
    user_input = 0

    try:
        user_input = int(input("Enter your number of choice (1-6): "))
    except ValueError:
        print("Oops, Wrong input! Please enter a number between 1 and 6.\n")
        continue

    if user_input not in [1, 2, 3, 4, 5, 6]:
        print("Invalid choice! Please select between 1 and 6.\n")
        continue

    if not tasks_list and user_input in [2, 3, 4, 5]:
        print("No task available!\n")
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