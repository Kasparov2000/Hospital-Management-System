from query import *
from email_validation import *
from registration import register
import time


def inventory_display(pharmacist):
    main = True
    while main:
        hospital_name(pharmacist)
        inventory_dict = inventory()
        print("*********************INVENTORY STOCK***********************")
        print("    Medicine     Dosage    Price($)      Quantity")
        print("-----------------------------------------------------------")

        for index, medicine in enumerate(inventory_dict):
            print(
                f"{index + 1}.\t{medicine['_id'][0].upper()} \t{medicine['_id'][1]}     \t{medicine['Price']}      \t{medicine['Quantity']}")

        try:
            options = int(input('\n1. Refresh 2. Exit\nOption: '))
            if options == 1:
                main = True

            elif options == 2:
                main = False

        except ValueError:
            print('Invalid input, integers only')
            time.sleep(1)


def dispense_medicine(pharmacist):
    success_1 = False
    while not success_1:
        try:
            hospital_name(pharmacist)
            options_menu_1 = int(input('1. New Patient 2. Customer 3. Exit\nOption: '))
            hospital_name(pharmacist)
            if options_menu_1 == 1:
                status, message = register('patient')
                if status:
                    success_2 = False
                    while not success_2:
                        try:
                            hospital_name(pharmacist)
                            options_reg = int(input('Registration Successful\n1. Proceed\nOption: '))
                            if options_reg == 1:
                                success_2 = True

                        except ValueError:
                            print("Invalid input, integers only")
                            time.sleep(1)
                else:
                    success_3 = False
                    while not success_3:
                        try:
                            options_reg_unsc = int(input(f'{message}\n1. Restart 2. Exit\nOption: '))
                            if options_reg_unsc == 1:
                                success_3 = True
                            elif options_reg_unsc == 2:
                                success_1 = True
                                success_3 = True

                        except ValueError:
                            print("Invalid input, integers only")
                            time.sleep(1)

            elif options_menu_1 == 2:
                success_4 = False
                while not success_4:
                    hospital_name(pharmacist)
                    email_address = input('Email Address: ')

                    if check_email(email_address):
                        patient = find_patient_by_email(email_address)
                        if patient:
                            status, message = dispense(patient, pharmacist)

                            if status:
                                success_5 = False
                                while not success_5:
                                    try:
                                        hospital_name(pharmacist)
                                        options_submenu_1 = int(input(f'{message}\n1. Exit\nOption: '))
                                        if options_submenu_1 == 1:
                                            success_1 = True
                                            success_4 = True
                                            success_5 = True
                                    except ValueError:
                                        print("Invalid input, integers only")
                                        time.sleep(1)
                            else:
                                success_8 = False
                                while not success_8:
                                    try:
                                        options_submenu_2 = int(input(f'{message}\n1. Exit\nOption: '))
                                        if options_submenu_2 == 1:
                                            success_4 = True
                                            success_8 = True
                                    except ValueError:
                                        print("Invalid input, integers only")
                                        time.sleep(1)



                        else:
                            success_6 = False
                            while not success_6:
                                hospital_name(pharmacist)
                                options_submenu_2 = int(input('Email not found\n1. Restart 2. Exit\nOption: '))
                                if options_submenu_2 == 1:
                                    success_6 = True
                                elif options_submenu_2 == 2:
                                    success_4 = True
                                    success_6 = True

                    else:
                        success_3 = False
                        while not success_3:
                            try:
                                hospital_name(pharmacist)
                                options = int(input('Invalid email, example: johndoe@gmail.com\n1. Restart 2. Exit\nOptions: '))

                                if options == 1:
                                    success_3 = True
                                elif options == 2:
                                    success_3

                            except ValueError:
                                pass

            elif options_menu_1 == 3:
                return False

        except ValueError:
            print('Invalid input')

def remove_medicine(pharmacist):
    main = True
    while main:
        try:
            status, message = remove_inventory(hospital_name(pharmacist))
            hospital_name(pharmacist)
            option = int(input(f'{message}\n1. Remove Medicine 2. Exit\nOption: '))
            if option == 2:
                main = False

        except ValueError:
            print("Invalid input, integers only")
            time.sleep(1)

def add_stock(pharmacist):
    main = True
    while main:
        try:
            status, message = add_to_stock(pharmacist)
            if status:
                hospital_name(pharmacist)
                option = int(input(f'{message}\n1. Add Medicine 2. Exit\nOption: '))
                if option == 2:
                    return False

            else:
                return

        except ValueError:
            print("Invalid input, integers only")
            time.sleep(1)



def increase_existing_stock(pharmacist):
    main = True
    while main:
        hospital_name(pharmacist)
        status, message = increase_stock(pharmacist)
        main = message_handler(status, message, pharmacist)


def message_handler(status, message, pharmacist):
    main = True
    while main:
        try:
            if not status:
                hospital_name(pharmacist)
                option = int(input(f'{message}\n1. Restart 2. Exit\nOption: '))
                if option == 1:
                    return True
                elif option == 2:
                    return False
            else:
                hospital_name(pharmacist)
                option = int(input(f'{message}\n1.Proceed\nOption: '))
                if option == 1:
                    return False
        except ValueError:
            print("Invalid input, integers only")


def pharmacist_terminal(pharmacist):
    main = True
    while main:
        hospital_name(pharmacist)
        print('1. Dispense\n2. Check Medicine Details\n3. Add Stock\n4. Update Stock\n5. Remove Stock\n6. Whole Inventory\n7. Log Out')
        try:
            option = int(input('Option: '))
            if option == 1:
                dispense_medicine(pharmacist)

            elif option == 2:
                check_medicine_details(pharmacist)

            elif option == 3:
                add_stock(pharmacist)

            elif option == 4:
                increase_existing_stock(pharmacist)

            elif option == 5:
                remove_medicine(pharmacist)

            elif option == 6:
                inventory_display(pharmacist)

            elif option == 7:
                main = False

        except ValueError:
            print("Invalid input, integers only")
            time.sleep(1)

