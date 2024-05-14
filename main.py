import json # import json module so we can work with json files
import os   # import os module so we can clear the screen
import time # import time module so we can use sleep function


display_username = '' # global variable that stores the username of the logged in user


# FUNCTIONS ============================================================================================================
clear = lambda: os.system('clear')  # function that clears the screen
clear()                             # call this function to clear function

def main_menu(): # main function that runs at the start of the program
    while True:
        print('1. Register')
        print('2. Login')
        print('3. Exit')
        choice = input('\nEnter your choice: ')
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print('Invalid choice')

def register(): # function that registers a user and inputs the username and password into a json file (into the database with profiles)
    while True:
        username = input('Enter a username (or "exit" to quit): ')
        if username == 'exit':
            break
        password = input('Enter a password: ')
        user = {'username': username,'password': password}
        with open('users.json', 'a') as file:
            json.dump(user, file)
            file.write('\n')
            clear()
        print('User registered successfully!')
        time.sleep(2)
        clear()
        main_menu()

def login(): # function that lets the user log in
    global display_username
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    display_username = username
    with open(('users.json'), 'r') as file: # open the json file in read mode
        for line in file:
            user = json.loads(line)
            if user['username'] == username and user['password'] == password:
                print('Logged in successfully!')
                time.sleep(2)
                clear()
                logged_in_menu()
                break
        else:
            print('Invalid username or password')

def logged_in_menu(): # function that displays the menu for the logged in user
    while True:
        global display_username
        print(f'Welcome {display_username}!\n')
        print('1. Add a song')
        print('2. Play a song')
        print('3. Logout')
        choice = input('\nEnter your choice: ')
        if choice == '1':
            print('This page is under construction')
            time.sleep(2)
            clear()
        elif choice == '2':
            print('This page is under construction')
            time.sleep(2)
            clear()
        elif choice == '3':
            clear()
            return
        else:
            print('Invalid choice')

# PROGRAM STARTS HERE ============================================================================================================

main_menu() # call to main function