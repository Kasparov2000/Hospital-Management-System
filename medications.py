from terminal_effects import hospital_name
import time


# A function that allows the doctor to add medicine
def medications(doctor):
    success = False
    list_of_drugs = []
    while not success:
        hospital_name(doctor)
        if len(list_of_drugs) > 0:
            for index, product in enumerate(list_of_drugs):
                print(f'\nProduct No: {index + 1}')
                for index, key in enumerate(product.keys()):
                    print(f'{index + 1}.\t{key.capitalize()}:\t{product[key]}')

        print(f'\n{"New Product" if len(list_of_drugs) <= 0 else "Another Product"}')

        success_1 = False
        while not success_1:
            try:
                name = input('Name: ')
                dosage = str(input('Dosage: '))
                quantity = int(input('Quantity: '))
                taking_instructions = str(input('Instructions: '))
                success_1 = True
            except ValueError:
                print('Invalid input')


        prescribed_drug = {'name': name,
                           'dosage': dosage,
                           'quantity': quantity,
                           'instructions': taking_instructions}
        hospital_name(doctor)
        print(f'\nProduct No: {len(list_of_drugs) + 1}\n')

        for index, key in enumerate(prescribed_drug.keys()):
            print(f'{index + 1}.\t{key.capitalize()}:\t{prescribed_drug[key]}')

        option = int(input('\n1. Confirm 2. Edit 3. Delete 4. Exit\nOption:\t'))
        hospital_name(doctor)
        if option == 1:
            list_of_drugs.append(prescribed_drug)
            success = True

        elif option == 2:
            hospital_name(doctor)
            success = False

        elif option == 3:
            hospital_name(doctor)
            success = False

        elif option == 4:
            return False

        if success:
            success_2 = False
            while not success_2:
                try:
                    hospital_name(doctor)
                    option = int(input('\n1. Add another medication 2. Submit\nOption:\t'))

                    if option == 1:
                        success = False
                        success_2 = True

                    elif option == 2:
                        return list_of_drugs

                except ValueError:
                    print('Invalid input')
                    time.sleep(1)
