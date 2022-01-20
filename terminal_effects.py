import os
import string


clear_terminal = lambda: os.system('cls')

# This clears the cmd terminal and also displays the name of the person currently logged in
def hospital_name(user=False, test=False):
    if not test:
        if user:
            clear_terminal()
            print(f'Hospital         {string.capwords(user.name)}\n')

        else:
            clear_terminal()
            print(f'Hospital Management System\n')