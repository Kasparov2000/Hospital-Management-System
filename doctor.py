from medications import medications
from diagnosis import diagnosis
from query import *
from email_validation import check_email
import string
from terminal_effects import *
import json
from reports import upload_medical_report


# A function with the functionalities a doctor needs to keep records of a patient, prescribe medicine etc
def visit(doctor):
    main = True
    while main:
        doctor = Doctor.objects(email_address=doctor.email_address).first()
        book_count = doctor.book_count
        if book_count > 0:
            patients = Doctor.objects(email_address=doctor.email_address).first().visit_queue
            hospital_name(doctor)
            print('Patient queue')

            for index, patient in enumerate(patients):
                print(f'{index + 1}. {patient.name}  {"Consultation" if not patient.pending_review else "Review"}')

            success = False
            while not success:
                try:
                    options = int(input('\nChoose patient from Queue\nEnter[0]to exit\n\nOption: '))
                    hospital_name(doctor)

                    if options == 0:
                        return

                    if 0 < options <= len(patients):

                        patient = patients[options - 1]
                        check_up_details = CheckUp.objects(patient_email_address=patient.email_address).order_by('-timestamp').first()
                        visit_type = "Review" if patient.pending_review else "Consultation"
                        temperature = f'{check_up_details.temperature}°C'
                        weight = f'{check_up_details.weight}kg'
                        bp = f'{str(check_up_details.systolic_bp)}/{str(check_up_details.diastolic_bp)} mm Hg'

                        patient_diagnosis = ''
                        prescribed_medicine = ''

                        success_5 = False
                        next_stage = False
                        while not success_5:
                            try:
                                hospital_name(doctor)
                                options_ins = int(input(f'{string.capwords(patient.name)} ~ {visit_type} \n{temperature}  ~  {weight} ~  {bp}\n1. Diagnosis 2. Prescription 3. Medical History 4. Submit 5. Exit\nOption: '))

                                if options_ins == 1:
                                    patient_diagnosis = diagnosis(doctor)

                                elif options_ins == 2:
                                    prescribed_medicine = medications(doctor)

                                elif options_ins == 3:
                                    medical_history(patient, doctor)

                                elif options_ins == 4:
                                    next_stage = True

                                    success_5 = True

                                elif options_ins == 5:
                                    success = True
                                    success_5 = True


                            except ValueError:
                                print('Invalid input')
                                time.sleep(2)

                        if not patient_diagnosis:
                            patient_diagnosis = {}

                        if not prescribed_medicine:
                            prescribed_medicine = {}

                        while next_stage:
                            consultation_details = {'details': {'date': datetime.datetime.now(),
                                                                   'doctor_name': doctor.name,
                                                                   'doctor_email': doctor.email_address,
                                                                    'type': visit_type},

                                                    'patient_details': {'patient_name': patient.name,
                                                                       'patient_email': patient.email_address},

                                                   'medical_report': {'diagnosis': patient_diagnosis,
                                                                      'prescribed_medicine': prescribed_medicine,
                                                                    'check_up_details': {'temperature': float(check_up_details.temperature),
                                                                                        'systolic_bp': float(check_up_details.systolic_bp),
                                                                                    'diastolic_bp': float(check_up_details.diastolic_bp),
                                                                                    'weight': float(check_up_details.weight)}
                                                                    }
                                                    }

                            details = consultation_details["details"]
                            details["date"] = str(consultation_details['details']["date"])

                            prescribed_medicine = consultation_details['medical_report']["prescribed_medicine"]
                            recordings = consultation_details['medical_report']['check_up_details']
                            diagnosis_report = consultation_details["medical_report"]['diagnosis']
                            patient_name = consultation_details['patient_details']['patient_name']
                            patient_email = consultation_details['patient_details']['patient_email']

                            medical_report = [{
                                        'hospital_name': 'ALU Hospital',
                                        'hospital_email': "africanleadershiphospital@gmail.com",
                                        'patient_details': {'patient_name': patient_name,
                                                           'patient_email': patient_email},
                                        'name': patient_name,
                                        'details': details,
                                               'prescribed_medicine': prescribed_medicine,
                                               'recordings': recordings,
                                               'diagnosis': diagnosis_report,
                                               'logo': ''}]

                            with open("reports.txt", 'a') as f:
                                f.write(json.dumps(medical_report) + "\n")

                            patient.pending_review = False if visit_type == "Consultation" else False
                            patient.to_be_consulted = False if visit_type == "Consultation" else True
                            patient.to_be_reviewed = True if visit_type == "Consultation" else False

                            print("Saving details...")
                            patient.records.append(consultation_details)
                            doctor.visit_queue.remove(patient)
                            doctor.book_count -= 1

                            upload_medical_report()
                            save_document(doctor)
                            save_document(patient)

                            success_6 = False
                            while not success_6:
                                try:
                                    hospital_name(doctor)
                                    option4 = int(input(f'{string.capwords(patient.name)} medical record has successfully been added to the database.\n1. Proceed\nOption: '))
                                    if option4 == 1:
                                        return True
                                except ValueError:
                                    print('Invalid Input')
                                    time.sleep(1)

                    else:
                        hospital_name(doctor)
                        option1 = f'You can only choose [1.]'
                        option2 = f'Choose an option from [{len(patients)}.] - to [{len(patients)}]'

                        print(f'{option1 if len(patients) == 1 else option2 }')
                except ValueError:
                    pass
        else:
            success_4 = False
            while not success_4:
                try:
                    hospital_name(doctor)
                    option3 = int(input('Currently no patients in the queue.\n1. Exit\nOption: '))
                    if option3 == 1:
                        return False

                except ValueError:
                    print('Invalid Input')
                    time.sleep(1)

# A function to check the past medical history of a patient
def medical_history(patient, doctor):
    main = True
    while main:
        status, patient = find_patient_medical_history(patient, doctor)
        success = False
        while not success:
            try:
                hospital_name(doctor)
                option = int(input(f'{patient}\n1. Restart 2. Exit\nOption: '))
                if option == 1:
                    return True
                elif 2:
                    return False

            except ValueError:
                print('Invalid Input')
                time.sleep(1)


def medical_history_terminal(doctor):
    main = True
    while main:
        email_validation = False
        while not email_validation:
            success_1 = False

            while not success_1:
                try:
                    hospital_name(doctor)
                    email_address = input("Enter the patient email address: ")
                    if not check_email(email_address):
                        option = int(input('Email address is incorrect, example johndoe@gmail.com\n1. Retry 2. Exit\nOption: '))
                        if option == 1:
                            success_1 = False
                        else:
                            return False, f'null'
                    else:
                        email_validation = True
                        success_1 = True

                except ValueError:
                    print('Invalid Input')
                    time.sleep(1)

        patient = find_patient_by_email(email_address)
        if patient:
            return True, patient

        else:
            success_2 = False
            while not success_2:
                try:
                    hospital_name(doctor)
                    option_2 = int(input('Patient not found\n1. Retry 2. Exit\nOption: \n'))
                    if option_2 == 1:
                        success_2 = True
                    elif option_2 == 2:
                        return False, f'null'


                except ValueError:
                    print('Invalid Input')
                    time.sleep(1)


def doctor_terminal(doctor):
    success = False
    while not success:
        try:
            hospital_name(doctor)
            options = int(input('1. Consultation\\Review \n2. Medical History\n3. Log Out\nOptions: '))
            if options == 1:
                visit(doctor)

            elif options == 2:
                sub_main = True
                while sub_main:
                    status, patient = medical_history_terminal(doctor)
                    if status:
                        if not medical_history(patient, doctor):
                            sub_main = False
                    else:
                        sub_main = False

            elif options == 3:
                success = True

        except ValueError:
            print('Invalid Input')
            time.sleep(1)

