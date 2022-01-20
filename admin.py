from registration import register
from email_validation import *
from query import *
from user_authentication import hash_password
from pharmacy import message_handler
import datetime
from terminal_effects import hospital_name
from date_validation import date_validation


#  A function to provide the user the option to restart after a failed registration
def registration_failed(admin):
    resolved = False
    while not resolved:
        try:
            hospital_name(admin)
            option = int(input('Registration Failed\n\n1. Restart 2. Exit\nOptions:\t'))

            if option == 1:
                return False

            elif option == 2:
                return True

        except ValueError:
            print('Wrong Data Type')


# A function to register a staff member of the hospital
def register_staff(admin):
    success = False
    while not success:
        try:
            hospital_name(admin)
            options = int(input('Register\n\n1. Doctor\n2. Nurse\n3. Pharmacist\n4. Receptionist\nOption:   '))
            options_dict = {1: 'doctor',
                            2: 'nurse',
                            3: 'pharmacist',
                            4: 'receptionist'}

            if 0 < options <= 4:
                status, message = register(options_dict[options])
                return status, message

        except ValueError:
            print('Invalid input, integer only')
            time.sleep(1)


# A function to register a user currently within the organization
def register_user(admin):

    profession_class_list = ['Doctor',
                             'Receptionist',
                             "Pharmacist"
                             ]

    profession_class_dict = {'Doctor': Doctor,
                             'Receptionist': Receptionist,
                             "Pharmacist": Pharmacist,
                             }

    main = True
    while main:
        hospital_name(admin)
        username = input('Enter Username: ')
        email_format = False
        while not email_format:
            email = input('email: ')
            if check_email(email):
                email_format = True
            else:
                success_here = False
                while not success_here:
                    try:
                        hospital_name(admin)
                        option_1 = int(input('Incorrect email.\n1. Restart 2. Exit\nOption: '))
                        if option_1 == 1:
                            success_here = True
                        elif option_1 == 2:
                            return False, f'null'

                    except ValueError:
                        print('Value Error')
                        time.sleep(1)

        admin_priviledges_loop = True
        while admin_priviledges_loop:
            try:
                hospital_name(admin)
                option = int(input('Admin Priviledges\n1. Yes 2. No 3. Exit\nOption: '))
                if option == 1:
                    admin_priviledge = True
                    admin_priviledges_loop = False
                elif option == 2:
                    admin_priviledges_loop = False
                    admin_priviledge = False
                elif option == 3:
                    return False, f'null'

            except ValueError:
                print('Invalid Input')
                time.sleep(1)

        profession_validated = False
        while not profession_validated:
            hospital_name(admin)
            profession = input('Profession: ').capitalize()
            if profession_class_list.count(profession) == 1:
                profession_validated = True
            else:
                try:
                    hospital_name(admin)
                    option = int(input('Profession not found\n1. Restart 2. Exit\nOption: '))
                    if option == 2:
                        return False, f'null'

                except ValueError:
                    print('Value Error')
                    time.sleep(1)

        validation_loop = True
        while validation_loop:
            if profession_class_dict[profession].objects().first():
                user_object = find_user_by_email(email)
                if not user_object or user_object.profession != profession:
                    if not find_account_by_username(username):
                        password_validation = False
                        while not password_validation:
                            hospital_name(admin)
                            password = input("password: ")
                            if len(password) >= 6:
                                hospital_name(admin)
                                password_confirmation = input('confirm password: ')
                                if password == password_confirmation:
                                    user = User()
                                    user.user_name = username
                                    user.email_address = email
                                    user.admin = admin_priviledge
                                    user.registration_timestamp = datetime.datetime.now()
                                    user.profession = profession
                                    user.password = hash_password(password)
                                    user.save()
                                    return True, f'Registration Successful'

                                else:

                                    success_here_1 = False
                                    while not success_here_1:
                                        try:
                                            hospital_name(admin)
                                            option = int(input('Password does not match\n1. Restart 2. Exit\nOption: '))
                                            if option == 1:
                                                success_here_1 = True
                                            elif option == 2:
                                                return False, f'null'

                                        except ValueError:
                                            print('Value Error')
                                            time.sleep(1)
                            else:
                                success_here_2 = False
                                while not success_here_2:
                                    try:
                                        hospital_name(admin)
                                        option = input(
                                            'Password should be six characters long\n1. Restart 2. Exit\nOption: ')
                                        if option == 1:
                                            validation_loop = False
                                            success_here_2 = True
                                        elif option == 2:
                                            return False, f'null'

                                    except ValueError:
                                        print('Value Error')
                                        time.sleep(1)
                    else:
                        success_here_3 = False
                        while not success_here_3:
                            try:
                                hospital_name(admin)
                                option = int(input('Username is taken\n1. Restart 2. Exit\nOption: '))
                                if option == 1:
                                    validation_loop = False
                                    success_here_3 = True
                                elif option == 2:
                                    return False, f'Username is taken'

                            except ValueError:
                                print('Value Error')
                                time.sleep(1)

                else:
                    success_here_4 = False
                    while not success_here_4:
                        try:
                            hospital_name(admin)
                            option = int(input('Email is registered already\n1. Restart 2. Exit\nOption: '))
                            if option == 1:
                                validation_loop = False
                                success_here_4 = True
                            elif option == 2:
                                return False, f'Registration not successful'

                        except ValueError:
                            print('Value Error')
                            time.sleep(1)
            else:
                success_here_5 = False
                while not success_here_5:
                    try:
                        hospital_name(admin)
                        option = int(
                            input('The staff member is not registered in the database\n1. Restart 2. Exit\nOption: '))
                        if option == 1:
                            validation_loop = False
                            success_here_5 = True
                        elif option == 2:
                            return False, f'null'

                    except ValueError:
                        print('Value Error')
                        time.sleep(1)


# A function to change the price of a product
def change_product_price(admin):
    main = True
    while main:
        hospital_name(admin)
        status, message = update_price(admin)
        if message_handler(status, message, admin):
            main = True
        else:
            return False


# A function to check the profit of Hospital over a defined time period, it also shows cost
def check_profit(admin):
    success = False
    while not success:
        try:
            hospital_name(admin)
            option = int(input('1. Check time defined profit 2. Exit\nOption: '))
            if option == 1:
                date = date_validation(admin)
                if not date:
                    return
                else:
                    success = True

            elif option == 2:
                return

        except ValueError:
            print('Invalid input')
            time.sleep(1)

    success_2 = False
    while not success_2:
        try:
            string_format = datetime.datetime.now().strftime('%d/%m/%Y')
            delta = datetime.datetime.strptime(string_format, '%d/%m/%Y') - date
            number_of_days = delta.days
            revenue, cost, total_profit = time_defined_profit(number_of_days)

            print(f'Revenue: ${revenue}\nCost: {cost}\n{f"Total Profit: {total_profit}" if total_profit > 0 else f"Total loss: {abs(total_profit)}"}')

            option = int(input('1. Return\nOption: '))

            if option == 1:
                return


        except ValueError:
            print('Invalid input')
            time.sleep(1)


# A function to close the financial day and show how much each cash recipients has in hand
def end_of_day(admin):
    success = False
    while not success:
        try:
            hospital_name(admin)
            option = int(input('1. Settle 2. Exit\nOption: '))
            if option == 1:
                status, response, last_settlement_date = close_the_day()
                if status:
                    if len(response) != 0:
                        success_1 = False
                        while not success_1:
                            try:
                                total_revenue = 0
                                total_cost = 0
                                hospital_name(admin)

                                close = CloseDay()
                                close.admin_email = admin.email_address
                                print(f'Financial Period:\n           from {last_settlement_date.strftime("%d-%m-%y, %A %I:%M %p ")}\n           to {datetime.datetime.now().strftime("%d-%m-%y, %A %I:%M %p ")}')
                                for index, till_operator in enumerate(response):
                                    print(f'{index + 1}. {till_operator[0]} ~ ${till_operator[1]}')
                                    total_revenue += till_operator[1]
                                    total_cost += till_operator[2]
                                    close.till_operator_details.append(till_operator)

                                profit = round(total_revenue - total_cost, 2)
                                print(f'total revenue: ${total_revenue}')
                                print(f'total cost: ${total_cost}')
                                print(f'total profit: ${profit}' if profit >= 0 else f'total loss:  ${abs(profit)}')
                                close.end_of_day = datetime.datetime.now()
                                close.total_revenue = total_revenue
                                close.save()

                                option_1 = int(input("1. Exit\nOption: "))
                                if option_1 == 1:
                                    return

                            except ValueError:
                                hospital_name(admin)
                                print('Invalid input')
                    else:
                        success_2 = False
                        while not success_2:
                            try:
                                hospital_name(admin)
                                option = int(input(f'No financial activity\n           from {last_settlement_date.strftime("%d-%m-%y, %A %I:%M %p ")}\n           to {datetime.datetime.now().strftime("%d-%m-%y, %A %I:%M %p ")}\n1. Return\nOption: '))

                                if option == 1:
                                    return

                            except ValueError:
                                print("Invalid input, integers only")
                                time.sleep(1)
                else:
                    success_3 = False
                    while not success_3:
                        try:
                            hospital_name(admin)
                            option = int(input(
                                f'No financial activity\n1. Return\nOption: '))

                            if option == 1:
                                return

                        except ValueError:
                            print("Invalid input, integers only")
                            time.sleep(1)
            if option == 2:
                return


        except ValueError:
            hospital_name(admin)
            print('Invalid input')


# A terminal interface for the admin
def admin_terminal(admin):
    main = True
    while main:
        try:
            main = True
            while main:
                hospital_name(admin)
                print(
                    '1. Add new staff\n2. Add new user\n3. Change Price\n4. Financial Statistics\n5. End of day.\n6. Log Out\n')
                try:
                    option = int(input('Option: '))

                    if option == 1:
                        success_1 = False
                        while not success_1:
                            status, message = register_staff(admin)
                            try:
                                if not status:
                                    hospital_name(admin)
                                    option_2 = int(input(f'{message}\n1. Restart 2. Exit\nOption: '))
                                    if option_2 == 1:
                                        return True
                                    elif option_2 == 2:
                                        return False
                                else:
                                    hospital_name(admin)
                                    option_2 = int(input(f'{message}\n1.Proceed\nOption: '))
                                    if option_2 == 1:
                                        success_1 = True
                            except ValueError:
                                print('Value Error')
                                time.sleep(1)

                    elif option == 2:
                        success_2 = False
                        while not success_2:
                            hospital_name(admin)
                            status, message = register_user(admin)
                            try:
                                if not status:
                                    success_2 = True

                                else:
                                    success_3 = False
                                    while not success_3:
                                        hospital_name(admin)
                                        option = int(input(f'{message}\n1.Proceed\nOption: '))
                                        if option == 1:
                                            success_2 = True
                                            success_3 = True

                            except ValueError:
                                print('Value Error')
                                time.sleep(1)

                    elif option == 3:
                        hospital_name(admin)
                        if change_product_price(admin):
                            main = True

                    elif option == 4:
                        check_profit(admin)

                    elif option == 5:
                        end_of_day(admin)

                    elif option == 6:
                        return

                except ValueError:
                    print("Invalid input, integers only")
                    time.sleep(1)

        except ValueError:
            print("Invalid input, integers only")
            time.sleep(1)


