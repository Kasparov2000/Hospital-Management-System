from terminal_effects import hospital_name
import time


# function that allows a doctor to make a diagnosis
def diagnosis(doctor):
    success = False
    list_of_diagnosis = []
    while not success:
        hospital_name(doctor)
        if len(list_of_diagnosis) > 0:
            for index, diagnosis in enumerate(list_of_diagnosis):
                print(f'\nDiagnosis: {index + 1}')
                for index, key in enumerate(diagnosis.keys()):
                    print(f'{"<=>"}  {diagnosis[key]}')

        print(f'\n{"New Diagnosis" if len(list_of_diagnosis) <= 0 else "Another Diagnosis"}')
        diagnosis_input = input('Diagnosis: ')

        diagnosis_dict = {'diagnosis': diagnosis_input}
        hospital_name(doctor)
        print(f'\nDiagnosis No: {len(list_of_diagnosis) + 1}')
        for index, key in enumerate(diagnosis_dict.keys()):
            print(f'{index + 1}.\t{key}:\t{diagnosis_dict[key]}')

        option = int(input('\n1. Confirm 2. Edit 3. Delete 4. Exit\nOption:\t'))
        hospital_name(doctor)
        if option == 1:
            list_of_diagnosis.append(diagnosis_dict)
            success = True

        elif option == 2:
            success = False

        elif option == 3:
            success = False

        elif option == 4:
            return False

        if success:
            success_2 = False
            while not success_2:
                try:
                    hospital_name(doctor)
                    option = int(input('\n1. Add another diagnosis 2. Submit\nOption:\t'))

                    if option == 1:
                        success_2 = True
                        success = False

                    elif option == 2:
                        return list_of_diagnosis

                except ValueError:
                    print("Invalid Input")
                    time.sleep(1)