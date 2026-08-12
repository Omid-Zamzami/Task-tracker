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


welcome()
while True:
    main_menu()
    user_input = None
    while user_input not in [1, 2, 3, 4, 5]:
        try:
            user_input = int(input("Enter your number of choice (1-5): "))
        except ValueError:
            print("Oops, Wrong input!")
    match user_input:
        case 1:
            add_task()
        case 2:
            pass
            #Update_task()
        case 3:
            pass
            #Delete_task()
        case 4:
            pass
            #Mark_task()
        case 5:
            pass
            #Observe_task()