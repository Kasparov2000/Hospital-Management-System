import datetime

from terminal_effects import clear_terminal
import user_login as lg
from mongo_setup import global_init
from pharmacy import pharmacist_terminal
from admin import admin_terminal
from reception import *
from doctor import doctor_terminal

import random

clear_terminal()

# The main function of the program
def main():
    main_ = True
    while main_:
        try:
            hospital_name()
            status, user, profession = lg.login()

            if status:
                if profession == 'Pharmacist':
                    pharmacist_terminal(user)

                elif profession == 'Receptionist':
                    receptionist_terminal(user)

                elif profession == 'Doctor':
                    doctor_terminal(user)

                elif profession == 'Admin':
                    admin_terminal(user)

            if not status and not user and not profession:
                clear_terminal()
                print(f"\n\nSaving Changes\n\n\nKaspaGOAT Systems\n{datetime.datetime.now().year}\n©")
                time.sleep(6)
                return False

        except Exception as e:
            print(e)
        print('No internet connection')


# This minimizes keyboard interrupt error
keyboard_interrupt = False
while not keyboard_interrupt:
    try:
        global_init()
        if not main():
            break

    except KeyboardInterrupt:
        success = False
        while not success:
            try:
                hospital_name()
                options = int(input('Are you sure you want to exit? 1. Yes 2. No\nOption: '))
                if options == 1:
                    clear_terminal()
                    print(f"\n\nSaving Changes\n\n\nKaspaGOAT Systems\n{datetime.datetime.now().year}\n©")
                    time.sleep(6)
                    keyboard_interrupt = True
                    success = True

                elif 2:
                    success = True

            except (ValueError, keyboard_interrupt):
                pass


#

# import  names
# global_init()
#
# time = datetime.datetime.now()
# close = CloseDay()
# close.end_of_day = datetime.datetime.now()
# close.total_revenue = 1000
# close.admin_name = "Tafara"
# close.save()
# stop = datetime.datetime.now()
#
# print(stop - time)