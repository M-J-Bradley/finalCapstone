# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date


DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if user.count(";") == 1:
        username, password = user.split(';')
        username_password[username] = password
    else:
        continue

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#The following are functions created for the user to use by selecting options from the main menu
#====Function Section====

def reg_user(new_username, new_password, username_password):
    username_error = True        
    ''' Function to register a new user
         giving the user the following data to input
          - unique username
          - password
          - second entry of password to confirm'''    
    # - While loop ensures new users cannot have the same username as another user    
    while username_error == True: 
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Username already exists, please enter a unique username.")
            username_error = True
        else:
            username_error = False                
    password_error = True
    while password_error == True:
        # - Request input of a new password
        new_password = input("New Password: ")
        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")
        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            password_error = False
        else:
            # Loop back to reenter if the passwords do not match
            password_error = True
            print("The passwords do not match, please try again")        

    # The below section updates the user.txt file with the new user        
    with open("user.txt", 'w') as out_file:
        user_data = []
        out_file.seek(0)
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))                              


def add_task(task_username, task_title, task_description, task_due_date, due_date_time, curr_date, new_task, task_list):
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username_error = True
    # While loop to check the username of the assignee exists already in user.txt and username_password
    while task_username_error == True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
                task_username_error = True
                print("User does not exist. Please enter a valid username")
        else:
            task_username_error = False

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    # While loop to ensure a valid date is entered
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
                print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
    Task is created as not yet complete ("completed": False)'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
        }
    task_list.append(new_task)

    
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] == True else "No"
                ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def update_task_file(task_list):
    # Update "tasks.txt" with new task data for changes made through editing and already added to task_list variable

   
    task_file_update_info =[]
    with open("tasks.txt", "w") as task_file_update:                    
        for i in task_list:
            task_file_update_info.append(f"{i['username']};{i['title']};{i['description']};{i['due_date'].strftime(DATETIME_STRING_FORMAT)};{i['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if i['completed'] == True else 'No'}")
        task_file_update.write("\n".join(task_file_update_info))
        print()
        return print("'Task.txt' file updated")

def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
        print(disp_str)
   
    

def view_mine(curr_user, task_list, task_count, task_count_dictionary):
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
    '''
    # Refreshing task after each operation of "view_mine" to ensure data includes latest updates
    operation = update_task_file(task_list)

    # Create the variable for task_count_dictionary to track the task numbers for the list of tasks for the current user
    task_count_dictionary = {}
    print()
    # The code below Loops through tasks by username to match to the current user and retrieve task information
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t\t {t['title']}\n"
            task_count += 1
            task_count_dictionary[str(task_count)] = t['title']
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Task Completed: \t {'Yes' if t['completed'] == True or t['completed'] == 'Yes' else 'No'}\n"

            
            print(f"Task Number: \t\t {task_count}")
            print(disp_str)
            print()

    # Generating an options menu for the current user listing tasks
    print("Options")
    print()
    print("-1: Return to Main Menu")
    for i in task_count_dictionary:
        print(f"{int(i)}: {task_count_dictionary[i]}")
    print()   

    # Asking the user to choose a valid option
    user_selection = 0
    task_option_error = True
    while task_option_error == True:
        while True:
            try:
                # User must choose an integer to enter as an option
                user_selection = int(input("Enter task number for further options:"))
                break
            except ValueError:
                print("Please enter a whole number, numbers with decimals and other signs are not allowed.")


        task_selection = task_count_dictionary[str(user_selection)] if 0 < user_selection <= task_count else "0"
        print(f"Task Selection: {user_selection}. {task_selection}")

        # Finding the index of the chosen task in the original task list, code sourced from https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
        task_index = [i for i,_ in enumerate(task_list) if _['title'] == task_selection and _['username'] == curr_user][0]  if 0 < user_selection < task_count else 0
        print()

        # A -1 selection takes the user back to the main menu
        if user_selection == int(-1):
            task_option_error = False
            print("Back to main menu")

        # An error if the user chooses an integer greater than the list of tasks, or 0, or a negative other than -1:
        elif user_selection > task_count or user_selection == 0 or user_selection < -1:
            task_option_error = True
            print("Invalid selection, please only choose an integer from the given list.")

        # An error if the user selects a task that is completed already, these cannot be edited
        elif task_list[task_index]['completed'] == True:
            task_option_error = True
            print("This task has already been completed and cannot be edited.")

        # Once a valid task number is selected, the user chooses further options to edit the task, mark complete, or cancel the selection
        else:
            task_option_error = False
            print("""Task options: 
            1. Edit Task
            2. Mark Task Complete
            3. Cancel
            """)

            task_option_cancel = False
            while task_option_cancel == False:
                task_option = int(input("Please enter a number for further options:"))
            # User has selected 1 to Edit the task, the code retrieves the task data from 
                if task_option == 1: 
                    task_option_cancel = False
                   
                    # User is asked to select either to edit the username the due date:
                    print("""Edit task options: 
                    1. Edit Username
                    2. Edit Due Date
                    3. Cancel
                    """)

                    edit_task_option = int(input("Please enter a number for the selected option:"))
                    
                    # Creating a variable to ensure closure or continuation of the below while loop
                    edit_task_option_cancel = False

                    # While loop to ensure valid entry of an integer for the options, as well as the option to cancel back to the previous menu
                    while edit_task_option_cancel == False: 
                        # Option 1 gives the user the chance to edit a task's assignee (username)
                        if edit_task_option == 1:              
                            edit_task_option_cancel = False
                            print("Edit assigned user:")
                            print()
                            print(f"Current user is: {curr_user}")
                            task_username_error = True
                            while task_username_error == True:
                                task_username = input("Enter the name of person to be assigned the task: ")
                                if task_username not in username_password.keys():
                                    task_username_error = True
                                    print("User does not exist. Please enter a valid username")
                                else:
                                    task_username_error = False
                            print(curr_user)
                            print(task_username)
                            task_list[task_index]['username'] = task_username

                            # Call operation update_task_file to update "tasks.txt" with new task data                        
                            operation = update_task_file(task_list)

                            # Once complete the user is taken back to the main menu
                            edit_task_option_cancel = True
                            task_option_cancel = True
                    
                        # Option 2 gives the user the chance to edit the due date of a task
                   
                        elif edit_task_option == 2:
                            edit_task_option_cancel = False
                            # While loop to ensure a valid date is entered for the new due date
                            while True:
                                try:
                                    new_task_due_date = input("Due date of task (YYYY-MM-DD): ")
                                    new_due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                                    break

                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified")
                            task_list[task_index]['due_date'] = new_due_date_time

                        
                            # Call operation update_task_file to update "tasks.txt" with new task data                        
                            operation = update_task_file(task_list)

                            # Once complete the user is taken back to the main menu 
                            edit_task_option_cancel = True
                            task_option_cancel = True

                        # Option 3 cancels back to the main menu
                        elif edit_task_option == 3:
                            edit_task_option_cancel = True
                            task_option_cancel = True
                    
                        else:
                            edit_task_option_cancel = False
                            print("Incorrect selection, please enter an integer, 1, 2, or 3.")

                    

                # User has selected 2 to Mark a Task complete              
                elif task_option == 2:
                    task_option_cancel = False
                    task_complete_error = False
                    while task_complete_error == False:
                        print("""Task Completion Options:
                    
                        1. Complete
                        2. Cancel
                        """)
                        task_completion = int(input("Please enter a '1' for complete, or a 'n' for incomplete ():"))

                        # Option 1 lets the user set a task as complete
                        if task_completion == 1:
                            task_list[task_index]['completed'] = "Yes"

                            # Call operation update_task_file to update "tasks.txt" with new task data                        
                            operation = update_task_file(task_list)

                            # Once complete the user is taken back to the main menu 
                            task_complete_error = True
                            edit_task_option_cancel = True
                            task_option_cancel = True

                        # Option 2 lets the user cancel back to the main menu without making a change
                        elif task_completion == 2:
                            task_complete_error = True
                            edit_task_option_cancel = True
                            task_option_cancel = True

                        else:    
                            task_complete_error = False
                            print("Please re-enter your selection")


                # User has selected 3 to cancel the task edit function
                elif task_option == 3:
                    task_option_cancel = True
                    continue
    
                # An incorrect selection has been made
                else:
                    print("Invalid selection.")
                    task_option_cancel = False           

def generate_reports(task_list, total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks, username_password):
    operation = update_task_file(task_list)
    '''The Admin user can use this operation to generate reports in the files task_overview.txt anduser_overview.txt.
    These two files are created in the same folder and contain a summary and a more detailed breakdown of the tasks and their
    related statistics respectively.'''

    # Creating the file task_overview.txt
    # For loop over the information in task list to identify the completed and not completed tasks and count these cumulatively for use in the statistics
    for line in task_list:
        total_tasks += 1
        if line['completed'] == True or line['completed'] == "Yes":
            completed_tasks += 1
        elif line['completed'] == False or line['completed'] == "No":
            uncompleted_tasks += 1   
            if line['due_date'].strftime(DATETIME_STRING_FORMAT) < datetime.today().strftime(DATETIME_STRING_FORMAT):
                overdue_tasks += 1
    completed_task_percentage = ( completed_tasks / total_tasks) * 100
    incomplete_task_percentage = ( uncompleted_tasks / total_tasks ) * 100
    overdue_task_percentage = ( overdue_tasks / total_tasks ) * 100
    
    # Create task_overview.txt if it doesn't exist
    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w") as default_file:
            pass

    # Writing the statistics to task_overview
    with open("task_overview.txt", 'w') as task_overview_file:
        task_overview_file.write("Task Overview:\n")
        task_overview_file.write("\n")
        task_overview_file.write(f"Total Tasks: \t\t\t{total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: \t\t{completed_tasks}\n")
        task_overview_file.write(f"Uncompleted Tasks: \t\t{uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue Tasks Tasks: \t\t{overdue_tasks}\n")
        task_overview_file.write(f"Incomplete '%': \t\t{'{:.2f}'.format(incomplete_task_percentage)}%\n")
        task_overview_file.write(f"Overdue '%': \t\t\t{'{:.2f}'.format(overdue_task_percentage)}%\n")
        task_overview_file.write("\n")
        task_overview_file.write("\n")
        task_overview_file.write("\n")
        task_overview_file.write("Note: Task are assumed overdue if not completed before the due date (i.e. tasks are due at 00:00 am on due date).")


        print()
        print("'task_overview_file.txt' created")

    # Creating the file for user_statistics

    # Creating relevant variables, a dictionary individual_user_statistics, and a list to store these dictionaries, user_statistics
    user_statistics = []
    individual_user_statistics = {'name': "", 
        'tasks': 0, 
        'completed': 0,
        'uncompleted': 0, 
        'overdue_tasks': 0,
        '"%" of Tasks Assigned': 0, 
        '"%" of Tasks Completed': 0, 
        '"%" of Tasks not Completed': 0,
        '"%" of Tasks Overdue': 0}
    
    # For loop over the users in the username_password variable:
    for u in username_password:
        individual_user_statistics = {'name': u,
            'tasks': 0, 
            'completed': 0,
            'uncompleted': 0, 
            'overdue_tasks': 0,
            '"%" of Tasks Assigned': 0, 
            '"%" of Tasks Completed': 0, 
            '"%" of Tasks not Completed': 0,
            '"%" of Tasks Overdue': 0}
        
        # A nested for loop over the information in task_list so that both loops mean that the information is generated by user, and cumulatively by task for each user
        for t in task_list:

            if t['username'] == u:
                individual_user_statistics['tasks'] += 1
                if t['completed'] == True or line['completed'] == "Yes":
                    individual_user_statistics['completed'] += 1
                if t['completed'] == False or line['completed'] == "No":
                    individual_user_statistics['uncompleted'] += 1
                    if t['due_date'].strftime(DATETIME_STRING_FORMAT) < datetime.today().strftime(DATETIME_STRING_FORMAT):
                        individual_user_statistics['overdue_tasks'] += 1
            # To eliminate dividing by zero, if there are no tasks, then the % will also automatically be zero, otherwise the function will calculate percentages.
            if total_tasks == 0:
                individual_user_statistics['"%" of Tasks Assigned'] = 0.00
            else:
                individual_user_statistics['"%" of Tasks Assigned'] = '{:.2f}'.format((individual_user_statistics['tasks'] / total_tasks) * 100)
        
            if individual_user_statistics['tasks'] == 0:
                individual_user_statistics['"%" of Tasks Completed'] = 0.00
                individual_user_statistics['"%" of Tasks not Completed'] = 0.00
                individual_user_statistics['"%" of Tasks Overdue'] = 0.00
            else:
                individual_user_statistics['"%" of Tasks Completed'] = '{:.2f}'.format((individual_user_statistics['completed'] / individual_user_statistics['tasks']) * 100)
                individual_user_statistics['"%" of Tasks not Completed'] = '{:.2f}'.format((individual_user_statistics['uncompleted'] / individual_user_statistics['tasks']) * 100)
                individual_user_statistics['"%" of Tasks Overdue'] = '{:.2f}'.format((individual_user_statistics['overdue_tasks'] / individual_user_statistics['tasks']) * 100)
        # Within the for loop of users, the function will write the statistics into the list of dictionaries, user by user
        user_statistics.append(individual_user_statistics.copy())

    # Creating the file user_overview if it does not yet exist
    if not os.path.exists("user_overview.txt"):
        with open("user_overview.txt", "w") as default_file:
            pass

    # Writing the statistics to the user_overview file using a for loop on the user_statistics list to collect the information
    with open("user_overview.txt", 'w') as user_overview_file:
        user_overview_file.write("User Overview:\n")
        user_overview_file.write("\n")
        user_overview_file.write("Name\t\tTotal\t\tTasks\t\tTasks not yet\tTasks\t\t'%' of Tasks\t'%' of Tasks \t'%' of Tasks \t'%' of Tasks\n")
        user_overview_file.write("\t\tTasks\t\tCompleted\tCompleted\tOverdue\t\tAssigned\tCompleted\tNot Completed\tOverdue\n")
        user_overview_file.write("\n")
        for p in range(len(user_statistics)):
            user_overview_file.write(f"""{user_statistics[p]['name']}\t\t{user_statistics[p]['tasks']}\t\t{user_statistics[p]['completed']}\t\t{user_statistics[p]['uncompleted']}\t\t{user_statistics[p]['overdue_tasks']}\t\t{user_statistics[p]['"%" of Tasks Assigned']}%\t\t{user_statistics[p]['"%" of Tasks Completed']}%\t\t{user_statistics[p]['"%" of Tasks not Completed']}%\t\t{user_statistics[p]['"%" of Tasks Overdue']}%\n""")
        user_overview_file.write("\n")
        user_overview_file.write(f"Total\t\t{total_tasks}\t\t{completed_tasks}\t\t{uncompleted_tasks}\t\t{overdue_tasks}\t\t\t\t{'{:.2f}'.format(completed_task_percentage)}%\t\t{'{:.2f}'.format(incomplete_task_percentage)}%\t\t{'{:.2f}'.format(overdue_task_percentage)}%")
        user_overview_file.write("\n")
        user_overview_file.write("\n")
        user_overview_file.write("\n")
        user_overview_file.write("Note: Task are assumed overdue if not completed before the due date (i.e. tasks are due at 00:00 am on due date).")
        print()
        print("'user_overview_file.txt' created")
            

def display_statistics(task_list, total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks):
    
    # In case there are any changes, or discrepancies, the task file is updated from the task_list
    operation = update_task_file(task_list)

    # This operation calls the generate reports function to provide the user_overiew and task_overview files with up to date information
    operation = generate_reports(task_list, total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks, username_password)

    # The below code prints the statisics for users and tasks by accessing the user_overview antask_overview files and printing them on screen for the admin user.
    print()
    print("Statistics:")
    print()
    with open("task_overview.txt", 'r') as task_overview_file:
        task_overview_summary = []
        for l in task_overview_file:
            task_overview_summary = l.strip('\n')
            print(f"{task_overview_summary}")

    print()
    print()
    with open("user_overview.txt", 'r') as user_overview_file:
        user_overview_summary = []
        for l in user_overview_file:
            user_overview_summary = l.strip('\n')
            print(f"{user_overview_summary}")

    print()
    print()

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''

        operation = reg_user(username, password, username_password)

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = ""
        task_title = ""
        task_description = ""
        task_due_date = ""
        due_date_time = ""
        curr_date = ""
        new_task = ""
        operation = add_task(task_username, task_title, task_description, task_due_date, due_date_time, curr_date, new_task, task_list)

 
    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        operation = view_all(task_list)


    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        task_count = 0
        task_count_dictionary ={}
        edit_task = 0
        operation = view_mine(curr_user, task_list, task_count, task_count_dictionary)
        
    elif menu == 'gr' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''        

        total_tasks = 0
        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_tasks = 0
        operation = generate_reports(task_list, total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks, username_password)

    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

        total_tasks = 0
        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_tasks = 0
        operation = display_statistics(task_list, total_tasks, completed_tasks, uncompleted_tasks, overdue_tasks)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")