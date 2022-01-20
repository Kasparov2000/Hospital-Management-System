from registration import register
from query import *
from receipt_pdf import receipt_generator
import random
from email_validation import check_email
import string
import os
from pathlib import Path
from terminal_effects import hospital_name


def find_account_by_email(email_address):
    patient = Patient.objects(email_address=email_address).first()
    return patient


# A function for consultation
def consultation(receptionist):
    patient_queue = []
    success = False
    registration = False
    new_email = ''

    nurse_objects = list(Nurse.objects().all())

    success_1 = False
    while not success_1:
        try:
            hospital_name(receptionist)
            if len(nurse_objects) == 0:
                option = int(input("You can't proceed without having a nurse at the hospital.\nThe admin should register one into the database.\n1. Exit:\nOption: "))
                if option == 1:
                    return   
            else:
                success_1 = True

        except Exception:
            print("Invalid input")
            time.sleep(1)

    while not success:
        try:
            hospital_name(receptionist)
            options = int(input(f'Have you ever been consulted here:\n\n1.Yes 2. No 3. Exit\nOption:\t')) if registration == False else 1

            email_verified = False
            while not email_verified:
                if options == 1:
                    email_validated = False
                    while not email_validated and new_email == '':
                        hospital_name(receptionist)
                        patient_email = input('Enter email address: ')

                        if check_email(patient_email):
                            email_validated = True

                        else:
                            success_check_email = False
                            while not success_check_email:
                                try:
                                    hospital_name(receptionist)
                                    option = int(
                                        input("Email format not correct, example johndoe@gamil.com\n1. Restart 2. Exit"))
                                    if option == 1:
                                        new_email = ' '
                                        success_check_email = True


                                    elif 2:
                                        return False
                                except ValueError:
                                    print('Invalid Input')
                                    time.sleep(1)

                    print(new_email)
                    # If registration is false it means that the user already had an a/c prior to the visit,
                    # if the registration has been done successfully the new email is automatically assigned
                    patient = find_account_by_email(patient_email) if not registration else find_account_by_email(new_email)
                    if patient:
                        if patient.to_be_consulted:
                            success = False
                            while not success:
                                try:
                                    hospital_name(receptionist)
                                    amount_paid = float(input(f'Consultation Fee ($10)\nEnter the amount $xx: '))
                                    if amount_paid == 10:

                                        receipt = Receipt()
                                        consultation_receipt = {'medicine_name': 'Consultation',
                                                                'quantity': 1,
                                                                'dosage': '',
                                                                'unit_price': amount_paid,
                                                                'total_price': 1 * amount_paid}

                                        receipt.receipt_number = receipt_number_gen()
                                        receipt.purchased_items.append(consultation_receipt)
                                        receipt.total_cost = 0
                                        receipt.total_amount = 10
                                        receipt.patient_name = patient.name
                                        receipt.patient_email_address = patient.email_address
                                        receipt.till_operator_email = receptionist.email_address
                                        receipt.till_operator = receptionist.name
                                        receipt.purchase_date = datetime.datetime.now()

                                        patient_details = {'name': patient.name,
                                                           'email': patient.email_address}

                                        cash_receiver_details = {'name': receptionist.name,
                                                                'email': receptionist.email_address}
                                    
                                        nurse = random.choice(nurse_objects)

                                        receipt_generator([consultation_receipt], receipt_number_gen(), patient_details, cash_receiver_details)

                                        patient.receipts.append([consultation_receipt])

                                        status_check_up, message_check_up = pre_check_up(patient, nurse, receptionist)
                                        patient.to_be_consulted = False
                                        patient.to_be_reviewed = False
                                        patient.to_be_review = False

                                        if not save_document(patient):
                                            return

                                        if not save_document(receipt):
                                            return

                                        assigned_doctor = find_doc_with_least_bookings()
                                        assigned_doctor.visit_queue.append(patient)
                                        assigned_doctor.book_count += 1

                                        if not save_document(assigned_doctor):
                                            return

                                        if status_check_up:
                                            exit_loop = False
                                            while not exit_loop:
                                                try:
                                                    hospital_name(receptionist)
                                                    option = int(input(f'{message_check_up}\n1.Proceed\nOption: '))
                                                    if option == 1:
                                                        exit_loop = True
                                                except ValueError:
                                                    print('Invalid Input')
                                                    time.sleep(1)
                                        else:
                                            return

                                        hospital_name(receptionist)
                                        success_message = f'Payment Successful.\n\nReceipt No. {receipt.receipt_number}\nPatient Name: {patient.name}\nEmail: {patient.email_address}\nTotal Amount paid: ${amount_paid}'
                                        exit_loop = False
                                        while not exit_loop:
                                            try:
                                                hospital_name(receptionist)
                                                option = int(input(f'{success_message}\n1.Proceed\nOption: '))
                                                if option == 1:
                                                    return patient_queue
                                            except ValueError:
                                                print('Invalid Input')
                                                time.sleep(1)


                                    else:
                                        success = False
                                        while not success:
                                            try:
                                                hospital_name(receptionist)
                                                option = int(input('The amount is not equal to $10'
                                                                   '\n1.Retry 2. Exit\nOption: '))
                                                if option == 1:
                                                    success = True
                                                elif option == 2:
                                                    return False
                                            except ValueError:
                                                print('Invalid Input')
                                                time.sleep(1)
                                except ValueError:
                                    print('Invalid Input')
                                    time.sleep(1)
                        else:
                            success_1 = False
                            while not success_1:
                                try:
                                    hospital_name(receptionist)
                                    option = int(input(f'{patient.name} has already been registered for consultation.'
                                                       '\n1. Another Patient 2. Exit\nOption: '))
                                    if option == 1:
                                        success_1 = True
                                    elif option == 2:
                                        return False
                                except ValueError:
                                    print('Invalid Input')


                    else:
                        success_1 = False
                        while not success_1:
                            try:
                                hospital_name(receptionist)
                                option = int(input(f'Email {patient_email} not found'
                                                   '\n1.Retry 2. Exit\nOption: '))
                                if option == 1:
                                    success_1 = True
                                elif option == 2:
                                    return False
                            except ValueError:
                                print('Invalid Input')

                elif options == 2:
                    success_2 = False
                    while not success_2:
                        try:
                            status, response = register('patient')
                            if not status:
                                hospital_name(receptionist)
                                option = int(input(f'{response}\n1. Restart 2. Exit\nOption: '))
                                if option == 1:
                                    success_2 = True
                                elif option == 2:
                                    return False
                            else:
                                hospital_name(receptionist)
                                new_email = response.split(', ')[1]
                                option_reg = int(input(f'{response}\n1.Proceed\nOption: '))
                                if option_reg == 1:
                                    options = 1
                                    registration = True
                                    success = True
                                    success_2 = True


                        except ValueError:
                            print("Invalid input, integers only")

                elif options == 3:
                    return

        except Exception as e:
            print(e)


# A function to get the check up details
def pre_check_up(patient, nurse, receptionist):
    main = True
    while main:
        try:
            hospital_name(receptionist)
            temperature = str(input("Enter the temperature°C: "))[:5]
            temperature = float(temperature)

            hospital_name(receptionist)
            blood_pressure_systolic = str(input("Enter the Systolic blood pressure: "))[:5]
            blood_pressure_systolic = abs(float(blood_pressure_systolic))

            hospital_name(receptionist)
            blood_pressure_diastolic = str(input("Enter the Diastolic blood pressure: "))[:5]
            blood_pressure_diastolic = abs(float(blood_pressure_diastolic))

            hospital_name(receptionist)
            weight = str(input("Enter the weight (kg): "))[:5]
            weight = float(weight)
            success = False
            while not success:
                hospital_name(receptionist)

                print(f'1. Temperature:  {temperature}°C\n2. Blood Pressure:  {str(blood_pressure_systolic) +"/"+ str(blood_pressure_diastolic)}mmHg'
                      f'\n3. Weight:   {weight}kgs')

                option = int(input('\n1. Confirm 2. Edit 3. Exit\nOption: '))
                hospital_name(receptionist)
                if option == 1:
                    check_up_details = CheckUp()
                    check_up_details.receptionist_name = receptionist.name
                    check_up_details.patient_name = patient.name
                    check_up_details.systolic_bp = blood_pressure_systolic
                    check_up_details.diastolic_bp = blood_pressure_diastolic
                    check_up_details.temperature = temperature
                    check_up_details.weight = weight
                    check_up_details.timestamp = datetime.datetime.now()
                    check_up_details.patient_email_address = patient.email_address
                    check_up_details.nurse_email = nurse.email_address
                    check_up_details.nurse_name = nurse.name

                    if save_document(check_up_details):
                        return True, f'Measurements successfully registered into the database'

                    else:
                        return False, f'Measurements not successfully registered into the database.'

                elif option == 2:
                    success = True

                elif option == 3:
                    return False, f''

        except ValueError:
            print("Invalid Input")
            time.sleep(1)


# A function for review
def review(receptionist):
    email_verified = False
    success_1 = False
    while not success_1:
        try:
            hospital_name(receptionist)
            nurse_objects = list(Nurse.objects().all())
            if len(nurse_objects) == 0:
                option = int(input("You can't proceed without having a nurse at the hospital.\nThe admin should register one into the database.\n1. Exit:\nOption: "))
                if option == 1:
                    return False, f'No nurses at the hospital' 
            else:
                success_1 = True

        except Exception:
            print("Invalid input")
            time.sleep(1)
            
    while not email_verified:
        email_validated = False
        while not email_validated:
            hospital_name(receptionist)
            patient_email = input('Enter email address: ')

            if check_email(patient_email):
                email_validated = True

            else:
                success_check_email = False
                while not success_check_email:
                    try:
                        hospital_name(receptionist)
                        option = int(
                            input("Email format not correct, example johndoe@gamil.com\n1. Restart 2. Exit"))
                        if option == 1:
                            success_check_email = True

                        elif 2:
                            return False
                    except ValueError:
                        print('Invalid Input')
                        time.sleep(1)
        try:
            hospital_name(receptionist)
            patient = find_account_by_email(patient_email)
            if patient:
                if patient.to_be_reviewed:
                    nurse = random.choice(list(Nurse.objects().all()))
                    status, message_check_up = pre_check_up(patient, nurse, receptionist)
                    doctor_details = patient.records[len(patient.records) - 1]
                    doctor_email = doctor_details['details']['doctor_email']

                    doctor = Doctor.objects(email_address=doctor_email).first()

                    if doctor.book_count == 0:
                        doctor.visit_queue = []
                        doctor.visit_queue.append(patient)
                        doctor.book_count += 1
                        patient.to_be_consulted = False
                        patient.to_be_reviewed = False
                        patient.pending_review = True

                    else:
                        doctor.visit_queue.append(patient)
                        doctor.book_count += 1

                    if save_document(doctor):
                        if save_document(patient):
                            exit_loop = False
                            while not exit_loop:
                                try:
                                    hospital_name(receptionist)
                                    option = int(input(f'{message_check_up}\n1.Proceed\nOption: '))
                                    if option == 1:
                                        return True, f'{string.capwords(patient.name)}, {patient.email_address} has succesfully been registered for review. '
                                except ValueError:
                                    print('Invalid Input')
                                    time.sleep(1)
                        else:
                            path_1 = (os.path.join(Path.cwd().parent, 'rollback.txt'))
                            path_1 = r"{}".format(path_1)

                            with open(path_1, 'a') as f:
                                f.json.dumps({'doctor': patient.email_address})
                                return False, f"{string.capwords(patient.name)} has not been registered for Review due to connectivity issues."

                    return False, f"{string.capwords(patient.name)} has not been registered for Review due to connectivity issues."


                else:
                    return False, f"{string.capwords(patient.name)} is not eligible for Review."

            else:
                success = False
                while not success:
                    try:
                        hospital_name(receptionist)
                        option = int(input('Email not associated with any patient\n1. Restart 2. Exit\nOption'))
                        if option == 1:
                            success = True
                        elif 2:
                            return False, f"Patient not successfully registered for Review"
                    except ValueError:
                        print('Invalid Input')
                        time.sleep(1)

        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name(receptionist)
                    option = int(input('Cannot save the document. Make sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')


def receptionist_terminal(receptionist):
    main = True
    while main:
        try:
            hospital_name(receptionist)
            print('1. Consultation 2. Review 3. Log Out')
            option = int(input('Option: '))

            if option == 1:
                consultation(receptionist)

            elif option == 2:
                success = False
                while not success:
                    status, message = review(receptionist)
                    try:
                        hospital_name(receptionist)
                        option = int(input(f'{message}\n1. Add another 2. Exit\nOption: '))
                        if option == 1:
                            success = False
                        elif option == 2:
                            success = True

                    except ValueError:
                        print("Invalid Input")
                        time.sleep(1)

            elif option == 3:
                main = False

        except ValueError:
            print("Invalid Input")
            time.sleep(1)

