from user_authentication import *
import time
from terminal_effects import *


# function to login
def login():
    main = True
    while main:
        try:
            hospital_name()
            options = int(input('1. Doctor\n2. Receptionist\n3. Pharmacist\n4. Admin\n5. Exit\nOption: '))
            if options == 5:
                return False, False, False

            profession_class = {1: Doctor,
                                   2: Receptionist,
                                   3: Pharmacist}

            profession_dict = {1: 'Doctor',
                               2: 'Receptionist',
                               3: 'Pharmacist',
                               4: 'Admin'}


            profession_class_admin = {'Doctor': Doctor,
                                'Receptionist': Receptionist,
                                'Pharmacist': Pharmacist}


            success = False
            count = 0
            if 0 < options <= 5:
                while not success:
                    try:
                        hospital_name()
                        username = input('Username: ')
                        password = input('Enter Password: ')

                        try:
                            profession = profession_dict[options]
                            success = False
                            count += 1
                            status, user = check_username(username, profession)
                            if status:
                                if verify_password(password, username):
                                    # authentication for non admins is different
                                    if 0 < options < 4:
                                        success_4 = False
                                        while not success_4:
                                            try:
                                                user = profession_class[options].objects(email_address=user.email_address).first()
                                                return True, user, profession

                                            except Exception:
                                                success_5 = False
                                                while not success_5:
                                                    try:
                                                        hospital_name()
                                                        option = int(input(
                                                            'Login aunthetication failed. Make sure you are connected to internet.'
                                                            '\n1.Retry 2. Exit\nOption: '))
                                                        if option == 1:
                                                            success_5 = True
                                                        elif option == 2:
                                                            return False, f'null', f'null'
                                                    except ValueError:
                                                        print('Invalid Input')

                                    else:

                                        success_6 = False
                                        while not success_6:
                                            try:
                                                # Admin authentication
                                                admin = User.objects(user_name=username, admin=True).first()
                                                if admin:
                                                    profession = admin.profession
                                                    user = profession_class_admin[profession].objects(
                                                        email_address=admin.email_address).first()
                                                    profession = "Admin"
                                                    print(admin)
                                                    return True, user, profession
                                                else:
                                                    success_1 = False
                                                    while not success_1:
                                                        try:
                                                            hospital_name()
                                                            option = int(input('Invalid Login Details\n1. Retry 2. Exit\nOption: '))
                                                            if option == 1:
                                                                success_6 = False
                                                                success_1 = True


                                                            elif option == 2:
                                                                return False, f'Login Unsuccessful', f'null'
                                                        except ValueError:
                                                            print("Invalid input, integers only")
                                                            time.sleep(1)
                                            except Exception:
                                                success_7 = False
                                                while not success_7:
                                                    try:
                                                        hospital_name()
                                                        option = int(input(
                                                            'Login aunthetication failed. Make sure you are connected to internet.'
                                                            '\n1.Retry 2. Exit\nOption: '))
                                                        if option == 1:
                                                            success_7 = True
                                                        elif option == 2:
                                                            return False, f'null', f'null'
                                                    except ValueError:
                                                        print('Invalid Input')

                                else:
                                    success_2 = False
                                    while not success_2:
                                        try:
                                            hospital_name()
                                            option = int(input('Invalid Login Details\n1. Retry 2. Exit\nOption: '))
                                            if option == 1:
                                                success_2 = True

                                            elif option == 2:
                                                return False, f'Login Unsuccessful', f'null'
                                        except ValueError:
                                            print("Invalid input, integers only")
                                            time.sleep(1)

                            else:
                                success_3 = False
                                while not success_3:
                                    try:
                                        hospital_name()
                                        option = int(input('Invalid Login Details\n1. Retry 2. Exit\nOption: '))
                                        if option == 1:
                                            success_3 = True

                                        elif option == 2:
                                            return False, f'Invalid login details', f'null'
                                    except ValueError:
                                        print("Invalid input, integers only")
                                        time.sleep(1)

                        except ValueError:
                            print("Invalid input, integers only")
                            time.sleep(1)

                    except ValueError:
                        print("Invalid input, integers only")
                        time.sleep(1)

        except ValueError:
            print("Invalid input, integers only")
            time.sleep(1)
