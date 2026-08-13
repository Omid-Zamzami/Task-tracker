from datetime import datetime

tasks_list = []
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
    print("5. Observe tasks (all, todo, in-progress, done)\n")

def add_task():
    task = {}
    global id
    task_id = id
    id += 1
    task_description = input("Enter your task's description: ")
    task_status = input("Enter your task's status (todo, in-progress, or done): ").lower()
    while task_status not in ["todo", "in-progress", "done"]:
        print("Wrong input! Try again.")
        task_status = input("Enter your task's status (todo, in-progress, or done): ")
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

def update_task():
    task_id = 0
    number_of_tasks = len(tasks_list)
    while task_id < 1 or task_id > number_of_tasks:
        try:
            task_id = int(input(f"Enter the ID of the task you want to update (1-{number_of_tasks}): "))
        except ValueError:
            print(f"wrong input! Try a number in the correct range (1-{number_of_tasks}): ")

    for task in tasks_list:
        if task["id"] == task_id:
            print(f"The task's previous description: {task["description"]}")
            new_description = input("Update the description: ")
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["description"] = new_description
            task["updated_at"] = updated_at

            print("Task description updated")
            print(f"New task description: {task["description"]}")
            print(f"Task updated at: {task["updated_at"]}")
            break

def delete_task():
    global id
    task_id = 0
    number_of_tasks = len(tasks_list)
    while task_id < 1 or task_id > number_of_tasks:
        try:
            task_id = int(input(f"Enter the ID of the task you want to delete (1-{number_of_tasks}): "))
        except ValueError:
            print(f"wrong input! Try a number in the correct range (1-{number_of_tasks}).")

    for task in tasks_list:
        if task["id"] == task_id:
            choice = input(f"Are you sure you want to delete {task["description"]} (yes/no, y/n)? ").lower()
            while choice not in ["y", "yes", "n", "no"]:
                choice = input("Wrong input! Try again (yes/no)? ").lower()
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


welcome()
while True:
    main_menu()
    user_input = 0
    while user_input not in [1, 2, 3, 4, 5]:
        try:
            user_input = int(input("Enter your number of choice (1-5): "))
        except ValueError:
            print("Oops, Wrong input!")
    match user_input:
        case 1:
            add_task()
        case 2:
            update_task()
        case 3:
            delete_task()
        case 4:
            pass
            #Mark_task()
        case 5:
            pass
            #Observe_task()