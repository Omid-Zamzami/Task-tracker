def welcome():
    print("***** Welcome to Task Tracker *****")
    print("You can Add, Update, and Delete tasks.")
    print("Also you will be able to observe the status on your tasks and mark them as todo, in-progress, or done.\n")

def main_menu():
    print("***** Main menu *****")
    print("1. Observe tasks (all, todo, in-progress, done)")
    print("2. Mark task")
    print("3. Add task")
    print("4. Update task")
    print("5. Delete task\n")


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
            pass
            #Observe_task()
        case 2:
            pass
            #Mark_task()
        case 3:
            pass
            #Add_task()
        case 4:
            pass
            #Update_task()
        case 5:
            pass
            #Delete_task()
    break