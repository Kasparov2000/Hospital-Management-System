from db_model import *
import time
import datetime
import requests
import string
from countries import list_of_countries
from terminal_effects import hospital_name


# A function to register people into the HMS
def register(choice):
    main = True
    while main:
        try:
            patient = Patient()
            doctor = Doctor()
            nurse = Nurse()
            pharmacist = Pharmacist()
            receptionist = Receptionist()

            # A dictionary of the objects
            person = {'patient': patient,
                      'doctor': doctor,
                      'nurse': nurse,
                      'pharmacist': pharmacist,
                      'receptionist': receptionist}

            unregistered = True
            while unregistered:
                confirmed = False
                while not confirmed:
                    try:
                        name_validated = False
                        while not name_validated:
                            hospital_name()
                            name = input('Enter name: ')[:30]

                            if name.replace(' ', '').isalpha() or name != '':
                                name_validated = True

                            else:
                                success = False
                                while not success:
                                    try:
                                        hospital_name()
                                        option = int(input('Invalid name, exampe: "John Doe"\n1. Restart 2. Exit\nOption:    '))
                                        if option == 1:
                                            success = True
                                        elif option == 2:
                                            return False, f'Registration unsuccessful.'
                                    except ValueError:
                                        print('Invalid Input, Integers Only')

                        gender_validated = False
                        while not gender_validated:
                            try:
                                hospital_name()
                                option = int(input('1. Male 2. Female 3. Other\nOptions: '))
                                if option == 1:
                                    gender = 'male'
                                    gender_validated = True
                                elif option == 2:
                                    gender = 'female'
                                    gender_validated = True
                                elif option == 3:
                                    gender = 'Other'
                                    gender_validated = True

                            except ValueError:
                                print('Invalid Input, Integers Only')
                                time.sleep(1)

                        nationality_validated = False
                        while not nationality_validated:
                            hospital_name()
                            country = input('Enter your country of origin(Rwanda): \nCountry: ')
                            country = string.capwords(country)
                            if list_of_countries.count(country) > 0:
                                nationality_validated = True

                            else:
                                success_nationality = False
                                while not success_nationality:
                                    try:
                                        hospital_name()
                                        option = int(input(f'{country} is not recognized.\n1. Restart 2. Exit\nOption: '))

                                        if option == 1:
                                            success_nationality = True

                                        elif 2:
                                            return False, f'Registration unsuccessful.'

                                    except:
                                        print('Invalid input, integers only')
                                        time.sleep(1)

                        dob_validated = False
                        while not dob_validated:
                            hospital_name()
                            dob = input('Enter Date of birth (dd/mm/yyyy): ')
                            if len(dob[0:2]) == 2 and len(dob[3:5]) == 2 and len(dob[6:10]) == 4 and dob.count(
                                    '/') == 2 and dob[0:2].isnumeric() and dob[3:5].isnumeric() and dob[
                                                                                                    6:10].isnumeric() and 0 < int(
                                dob[0:2]) < 32 and 0 < int(dob[3:5]) < 13 and len(dob[6::]) == 4:
                                dob = datetime.datetime.strptime(dob, '%d/%m/%Y')

                                dob_limit = datetime.date(1903, 1, 2)
                                dt2 = datetime.datetime.combine(dob_limit, datetime.time(0, 0))
                                if dob < datetime.datetime.now():
                                    if dob < dt2:
                                        print('You are not the oldest person ever\nGuiness World Record: Kane Tanaka, born on Jan. 2, 1903')
                                        time.sleep(2)
                                    else:
                                        dob_validated = True
                                else:
                                    print('No one can be born in the Future')
                                    time.sleep(2)


                            else:
                                success = False
                                while not success:
                                    try:
                                        hospital_name()
                                        option = int(
                                            input('Wrong Date Format, example: 01/01/2020\n1. Restart 2. Exit\nOption:\t'))
                                        if option == 1:
                                            success = True
                                        elif option == 2:
                                            return False, f'Registration unsuccessful.'

                                    except ValueError:
                                        print('Invalid input, integers only')
                        hospital_name()
                        address = input('Enter address: ')[:30]

                        email_validated = False
                        while not email_validated:
                            hospital_name()
                            email_address = input('Enter email address: ')
                            if len(email_address) > 0 and email_address.count('@') == 1 and email_address.count('.') >= 1:
                                if email_address[1:len(email_address)].count('@') == 1 and email_address[
                                                                                           1:len(email_address)].count(
                                    '.') >= 1 and \
                                        email_address[email_address.index('@') + 1].isalpha() or email_address[
                                    email_address.index('@') + 1].isnumeric():
                                    email_exists = person[choice].__class__.objects(email_address=email_address).first()

                                    if email_exists:
                                        success = False
                                        while not success:
                                            try:
                                                hospital_name()
                                                option = int(
                                                    input(
                                                        f'Another user is already registered with the email: {email_address}\n1. Restart 2. Exit\nOption:\t'))
                                                if option == 1:
                                                    success = True
                                                elif option == 2:
                                                    return False, f'Registration unsuccessful.'
                                            except ValueError:
                                                print('Invalid Input')
                                    else:
                                        if choice == 'patient':
                                            TIMEOUT = 30
                                            success = False
                                            while not success:
                                                try:
                                                    response = requests.get(
                                                        "https://isitarealemail.com/api/email/validate",
                                                        params={'email': email_address}, timeout=TIMEOUT)

                                                except (requests.ConnectionError, requests.Timeout) as exception:
                                                    return False, f'No internet Connection, failed to validate email.'

                                                if response.json()['status'] == "valid":
                                                    email_validated = True
                                                    success = True

                                                else:
                                                    success = False
                                                    while not success:
                                                        try:
                                                            hospital_name()
                                                            option = int(
                                                                input(
                                                                    'The email format is correct but it\'s unkwown\n1. Restart 2. Exit\nOption:\t'))
                                                            if option == 1:
                                                                success = True
                                                            elif option == 2:
                                                                return False, f'Registration unsuccessful.'
                                                        except ValueError:
                                                            print('Invalid Input')


                                        else:
                                            email_validated = True

                                else:
                                    success = False
                                    while not success:
                                        try:
                                            hospital_name()
                                            option = int(
                                                input(
                                                    'Wrong email format, example: johndoe@gmail.com\n1. Restart 2. '
                                                    'Exit\nOption:\t'))
                                            if option == 1:
                                                success = True
                                            elif option == 2:
                                                return False, f'Registration unsuccessful.'

                                        except ValueError:
                                            print('Wrong Integer')
                            else:
                                success = False
                                while not success:
                                    try:
                                        hospital_name()
                                        option = int(
                                            input(
                                                'Wrong email format, example: johndoe@gmail.com\n1. Restart 2. Exit\nOption:\t'))
                                        if option == 1:
                                            success = True
                                        elif option == 2:
                                            return False, f'Registration unsuccessful.'

                                    except ValueError:
                                        print('Wrong Integer')

                        confirmed_2 = False
                        while not confirmed_2:
                            try:
                                hospital_name()
                                option = int(input(
                                    f'1. Name: {name}\n2. D.O.B: {dob}\n3. Gender {gender}\n4. Address: {address}\n5. Country of Origin: {country}\n6. Email Address: {email_address}\n\n1. Confirm 2. Edit 3. Exit\nOption: '))
                                if option == 1:
                                    confirmed = True
                                    confirmed_2 = True
                                    unregistered = False

                                elif option == 2:
                                    confirmed_2 = True

                                elif option == 3:
                                    return False, f'Registration unsuccessful.'

                            except ValueError:
                                print('Integer')


                    except ValueError:
                        print('Invalid Input')

            if not unregistered:

                person[choice].name = name
                person[choice].address = address
                person[choice].gender = gender
                person[choice].country = country
                person[choice].email_address = email_address
                person[choice].dob = dob
                person[choice].registration_date = datetime.datetime.now()


                TIMEOUT = 30
                start_time = time.time()
                success = False
                while not success:

                    try:
                        current_time = time.time()
                        running_time = current_time - start_time

                        if running_time >= TIMEOUT:
                            success = True
                            return False, f'Timeout'
                        else:
                            person[choice].save()
                            success = True
                            return True, f"{string.capwords(person[choice].name)}, {email_address}, has successfully been registered into the database"

                    except Exception:
                        pass
        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name()
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False, f'Registration unsuccessful.'
                except ValueError:
                    print('Invalid Input')


