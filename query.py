import datetime
from datetime import date, timedelta

from db_model import *
from receipt_pdf import receipt_generator
import time

from error_handling import save_document, delete_document
from minimum_mark_up import *
import mongo_setup as ms
import os
from pathlib import Path
import string
from terminal_effects import hospital_name

# A function to find the patient from the database, it returns an object of the patient. This object has all the attributes
# defined in the mongomodel
def find_patient_by_email(email_address):
    try:
        # mongoengine to get the patient object by querying with the email_address
        patient = Patient.objects(email_address=email_address).first()
        return patient


    except Exception as e:
        success = False
        while not success:
            try:
                # Since the app makes requests to a remote database, this option gives the user the option to restart
                # or undo the changes
                option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                   '\n1.Retry 2. Exit\nOption: '))
                if option == 1:
                    success = True
                elif option == 2:
                    return False
            except ValueError:
                print('Invalid Input')


# A function to find the user from the User document/table in the mongodb database
def find_user_by_email(email_address):
    main = True
    while main:
        try:

            user = User.objects(email_address=email_address).first()
            return user

        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')


# A function to find check if the username is registered, used in logging in and creating a new user
def find_account_by_username(username):
    main = True
    while main:
        try:
            user = User.objects(user_name=username).first()
            return user

        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

# A function to find the doctor with the least bookings assign a patient for consultation. This to maintain equality in
# apportionment of patients among the doctors.
def find_doc_with_least_bookings():
    main = True
    while main:
        try:
            doctor = Doctor.objects().order_by('book_count').first()

            # Mongodb automatically deletes empty arrays , this conditional statement is to check if the doctor has 0
            # bookings or not. If yes, a new empty list is created and then the patient object is appended, and the
            # the array is then saved to the cluster.
            if doctor.book_count == 0:
                doctor.visit_queue = []
                return doctor

            else:
                return doctor

        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')


# A function to check for patients medical history
def find_patient_medical_history(patient, doctor):
    loop = True
    while loop:
        try:
            patient_email = patient.email_address

            # Since check up is done before the medical records are saved, if it's 1 it means that they are no
            # medical records to show.
            med_rec_exist = len(list(CheckUp.objects(patient_email_address=patient_email)))

            # A ternary operation to create a new records if none exist, if not created an error will be raised since
            # there is no records array on the database
            patient_records = patient.records if len(patient.records) > 0 else []
            if med_rec_exist >= 1 and len(patient_records) >= 1:
                main = True
                while main:
                    max_search_results_loop = True
                    while max_search_results_loop:
                        try:
                            hospital_name(doctor)
                            # this variabe stores the maximum number of reports the doctor wants to see
                            max_search_results = int(input(f'{len(patient_records)} Patient {"report" if len(patient_records) == 1 else "reports"}.\nEnter the search results limit: '))
                            if max_search_results <= len(patient_records):
                                max_search_results_loop = False

                            else:
                                success_2 = False
                                while not success_2:
                                    try:
                                        hospital_name(doctor)
                                        option_max_search = int(input('The number exceeds the options\n1. Restart 2. Exit\nOption: '))
                                        if option_max_search == 1:
                                            success_2 = True

                                        elif option_max_search == 2:
                                            return

                                    except ValueError:
                                        print('Invalid Input, integers only')
                                        time.sleep(1)

                        except ValueError:
                            print("invalid Input")
                            time.sleep(1)

                    hospital_name(doctor)
                    print('Visitation History.')

                    # This for loop prints a small snippet of the patients medical history, the doctor then chooses the
                    # reference number
                    for index, record in enumerate(patient_records):
                        timestamp_records = str(record["details"]["date"])
                        date = datetime.datetime.strptime(timestamp_records, "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M %p")
                        doctor_name = record["details"]['doctor_name'].capitalize()
                        visit_type = record["details"]["type"].capitalize()
                        print(f'{index + 1}. {visit_type}\t\tDr.{doctor_name}\t\t{date}')

                        if (index + 1) == max_search_results:
                            all_patient_records = patient_records
                            patient_records = patient_records[:max_search_results]
                            break


                    success_1 = False
                    while not success_1:
                        try:
                            # THe reference number is entered here.
                            option = int(input('\nEnter the reference of the results you want to explore: '))
                            if option <= len(patient_records):
                                medical_record = patient_records[option - 1]
                                success_1 = True

                            else:
                                success_4 = False
                                while not success_4:
                                    try:
                                        hospital_name(doctor)
                                        option_ins_2 = int(input('The reference number exceed the search results\n1. Retry 2. Exit\nOption: '))
                                        if option_ins_2 == 1:
                                            success_4 = True

                                        elif option_ins_2 == 2:
                                            return

                                    except ValueError:
                                        print('Invalid input')
                                        time.sleep(1)

                        except ValueError:
                            print("Invalid input, integers only")

                    medical_report_loop = False
                    hospital_name(doctor)

                    # The results are displayed comprehensively
                    while not medical_report_loop:
                        temperature = medical_record["medical_report"]["check_up_details"]["temperature"]
                        bp = str(
                            f'[{str(medical_record["medical_report"]["check_up_details"]["systolic_bp"])}] / [{(str(medical_record["medical_report"]["check_up_details"]["diastolic_bp"]))}]mm Hg')
                        weight = f'{medical_record["medical_report"]["check_up_details"]["weight"]}kgs'
                        print('Measurements')
                        print(f'1.\t{bp} ~ {temperature}°C ~ {weight}')
                        print('\nDiagnosis')

                        for index, diagnosis in enumerate(medical_record['medical_report']['diagnosis']):
                            print(f"{index + 1}.  {diagnosis['diagnosis']}")

                        print('\nPrescription')
                        for index, prescription in enumerate(medical_record['medical_report']['prescribed_medicine']):
                            print(
                                f"{index + 1}.   {prescription['name'].upper()}  ~  {prescription['dosage']}  ~  {prescription['quantity']}  ~  {prescription['instructions']}")

                        success_3 = False
                        while not success_3:
                            try:
                                option_ins = int(input('\n1. Return 2. Exit\nOption: '))
                                hospital_name(doctor)
                                if option_ins == 1:
                                    patient_records = all_patient_records
                                    medical_report_loop = True
                                    success_3 = True

                                elif 2:
                                    return True, "Medical records were succesfully seen."


                            except ValueError:
                                print('Invalid Input, integers only')
                                time.sleep(1)

                        else:
                            pass
                else:
                    success_5 = False
                    while not success_5:
                        try:
                            hospital_name(doctor)
                            option = int(input('Patient has no medical records.\n1. Exit\nOption'))
                            if option == 1:
                                return False, f'Patient has no medical records'

                        except Exception:
                            print('Invalid Input, integers only')
                            time.sleep(1)

            else:
                return False, f'User has no medical records saved in the database'

        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name(doctor)
                    option = int(input(f'Error: {e}\n\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')


# A function to generate a receipt Number. The receipt number used in the HMS are of the format A00001,
# this function will make sure that when its now A99999, it steps to B00001 instead of A1000000
def receipt_number_gen():
    main = True
    while main:
        try:

            # Checking the last receipt in the database
            last_receipt = Receipt.objects.all().order_by('-receipt_number').first()

            if last_receipt:
                receipt_number = last_receipt.receipt_number

                # This strips away all the digits in receipt number, for instance in A0001, it returns 1
                numeric_filter = filter(str.isdigit, receipt_number)
                numeric_string = "".join(numeric_filter)

                alpha_filter = filter(str.isalpha, receipt_number)
                alpha_string = "".join(alpha_filter)

                numeric_increment = format(int(numeric_string) + 1, )

                # This fills the zeros, for instance on the preceding code the the new number is 2, and zeros have to be
                # added to preserve the format
                zero_filled_number = numeric_increment.zfill(len(numeric_string))

                # if the zero filled number length is not equal to numeric it means the character will be incremented
                # and concatenated to the default first number 0000000001
                if len(numeric_string) != len(zero_filled_number):
                    alpha_increment = chr(ord(alpha_string) + 1)
                    new_receipt_number = alpha_increment + str('0000000001')

                else:
                    new_receipt_number = alpha_string + str(zero_filled_number)

            else:
                new_receipt_number = 'A0000000001'

            return new_receipt_number

        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}\n\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

# This function upates the expiry status of medicine before dispensing is done, and other related things
def update_expiry_status():
    all_medicine = Medicine.objects(expired=False)
    for medicine in all_medicine:
        if medicine.expiry_date <= datetime.datetime.now().date():
            medicine.expired = True
            medicine.save()


def total_amount():
    total = Receipt.objects().sum('total_amount')
    return total

# A function to return revenue over a specified period
def time_defined_profit(time_delta):
    total_profit, revenue, cost = 0, 0, 0
    for receipt in Receipt.objects():
        if receipt.purchase_date.date() >= datetime.datetime.now().date() - timedelta(days=time_delta):
            revenue += receipt.total_amount
            cost += receipt.total_cost

    total_profit = revenue - cost
    return revenue, cost, total_profit

# A function to calculate the money that the respective till operators recieved
def close_the_day():
    recipient_details = []

    overall_details = []

    # This is when the previous financial period ended, When the first settlement is done they won't be a preceding
    # last_settlement_time, so the date of the first receipt is used
    receipt = Receipt.objects().order_by("receipt_number").first()
    last_settlement_time = CloseDay.objects().order_by("-end_of_day").first()
    if receipt:
        # This returns all the receipts after the previous financial period

        last_settlement_time = last_settlement_time.end_of_day if last_settlement_time else receipt.purchase_date

        for receipt in Receipt.objects(purchase_date__gte = last_settlement_time):
            # This checks for all the personnel who received money and appends their emails, names tuple to the recipient_details list

            if recipient_details.count((receipt.till_operator, receipt.till_operator_email)) == 0:
                recipient_details.append((receipt.till_operator, receipt.till_operator_email))


        # This checks the total amount of each of the emails and
        for till_operator in recipient_details:
            receipt_object = Receipt.objects(till_operator_email=till_operator[1], purchase_date__gte = last_settlement_time )
            total_amount = (till_operator[0], receipt_object.sum('total_amount'), receipt_object.sum('total_cost'))


            overall_details.append(total_amount)

        # it returns a tuple like [{('masimba', 'masimba@gmail.com'): 300.0}]
        return True, overall_details, last_settlement_time

    else:
        return False, f'No preceding financial period.', f'null'

# A function to check the total inventory
def inventory():
    main = True
    while main:
        try:
            update_expiry_status()
            medicine = Medicine.objects(expired=False).all()
            # a pipeline to be used for the aggregate method, it returns the total quantity of a unique product as well
            # its price
            pipeline = [
                {"$group": {"_id": ["$medicine_name", "$dosage"], "Price": {"$first": "$unit_price"},
                            "Quantity": {"$sum": "$quantity"}}},
                {"$sort": {"_id": 1}}]

            inventory_dictionary = medicine.aggregate(pipeline)

            return inventory_dictionary

        except Exception as e:
            success = False
            while not success:
                try:

                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

# A function to add to cart when the pharmacist is dispensing drugs
def add_to_cart(pharmacist):
    main = True
    while main:
        try:

            master_cart = []
            reference_dictionary = {'medicine_name': 'Medicine Name',
                                    'dosage': 'Dosage',
                                    'quantity': 'Quantity',
                                    'instructions': 'Instructions',
                                    'unit_price': 'Unit Price',
                                    'total_price': 'Total Price'}

            hospital_name(pharmacist)

            add_more = True
            while add_more:
                hospital_name(pharmacist)
                if len(master_cart) > 0:
                    for index, product in enumerate(master_cart):
                        print(f'\nProduct No: {index + 1}')
                        for index, key in enumerate(product.keys()):
                            print(f'{index + 1}.\t{reference_dictionary[key]}:\t{product[key]}')

                success_1 = False
                while not success_1:
                    success_1_ins = False
                    while not success_1_ins:
                        try:
                            
                            print(f'\n{"New Product" if len(master_cart) <= 0 else "Another Product"}')
                            medicine_name = input('Product Name: ').lower().rstrip()
                            dosage = input('Dosage: ')
                            quantity = int(input('Quantity: '))
                            instructions = input('Instructions: ')


                            cart = {'medicine_name': medicine_name.upper(),
                                    'dosage': dosage,
                                    "quantity": quantity,
                                    "instructions": instructions
                                    }

                            success_1_ins = True

                        except ValueError:
                            print("Invalid input, integers only")
                            time.sleep(1)

                    success_2 = False
                    while not success_2:
                        next_loop = False
                        try:
                            hospital_name(pharmacist)
                            print(f'\nProduct No: {len(master_cart) + 1}\n')
                            for index, key in enumerate(cart.keys()):
                                print(f'{index + 1}.\t{reference_dictionary[key]}:\t{cart[key]}')

                            option_ins_2 = int(input('\n1. Confirm 2. Edit 3. Exit\nOption:\t'))
                            hospital_name(pharmacist)
                            next_loop = True

                        except ValueError:
                            print("Invalid input, integers only")
                            time.sleep(1)

                        if next_loop:
                            if option_ins_2 == 1:
                                status, unit_price, message = check_order(cart)
                                if status:
                                    cart['unit_price'] = unit_price
                                    cart['total_price'] = cart['unit_price'] * cart['quantity']
                                    master_cart.append(cart)
                                    success_2 = True
                                    success_1 = True

                                else:
                                    success_3 = False
                                    while not success_3:
                                        try:
                                            hospital_name(pharmacist)
                                            option_ins = int(input(f"{message}\n1. Restart 2. Exit\nOption: "))
                                            if option_ins == 1:
                                                success_2 = True
                                                success_3 = True

                                            elif option_ins == 2:
                                                return


                                        except ValueError:
                                            print("Invalid input, integers only")
                                            time.sleep(1)

                            elif option_ins_2 == 2:
                                success_2 = True

                            elif option_ins_2 == 3:
                                return False

                success_4 = False
                while not success_4:
                    try:
                        hospital_name(pharmacist)
                        option_ins_3 = int(input('\n1. Add another medication 2. Delete From Cart 3. Submit\nOption:\t'))

                        if option_ins_3 == 1:
                            success_4 = True

                        elif option_ins_3 == 2:
                            if len(master_cart) > 0:
                                success_5 = False
                                while not success_5:
                                    hospital_name(pharmacist)
                                    for index, product in enumerate(master_cart):
                                        print(f'\nProduct No: {index + 1}')
                                        for index, key in enumerate(product.keys()):
                                            print(f'{index + 1}.\t{reference_dictionary[key]}:\t{product[key]}')

                                    delete_cart = input("Select the cart numbers, example (1, 2, 3)\nCart Numbers: ")
                                    delete_cart_test = delete_cart.rstrip(", ")

                                    validated = False
                                    if len(delete_cart_test) <= len(master_cart):
                                        if delete_cart_test.isdigit():
                                            if not delete_cart_test.startswith('0'):
                                                cart_indexes = list(map(lambda x: int(x), delete_cart_test))
                                                redundant_products = []
                                                for index in cart_indexes:
                                                    redundant_products.append(master_cart[index - 1])

                                                for product in redundant_products:
                                                    master_cart.remove(product)

                                                validated = True

                                                success_6 = False
                                                while not success_6:
                                                    try:
                                                        hospital_name(pharmacist)
                                                        option_ins_4 = int(input(f'Succesfully deleted:\nProduct Names: {list(map(lambda deleted_product: str(deleted_product["medicine_name"] + "-" + deleted_product["dosage"]), redundant_products))}\n\n1.Exit\nOption: '))
                                                        if option_ins_4 == 1:
                                                            success_5 = True
                                                            success_6 = True


                                                    except ValueError:
                                                        print("Invalid input, integers only")
                                                        time.sleep(1)

                                    if not validated:
                                        success_7 = False
                                        while not success_7:
                                            try:
                                                if len(master_cart) > 0:
                                                    hospital_name(pharmacist)
                                                    option_ins_5 = int(input('Invalid input\nExample <=> Product Numbers: 1, 2, 3\n\n1.Restart 2. Exit\nOption: '))
                                                    if option_ins_5 == 1:
                                                        success_7 = True
                                                    elif 2:
                                                        success_5 = True
                                                        success_7 = True

                                                if len(master_cart) == 0:
                                                    hospital_name(pharmacist)
                                                    option_ins_5 = int(input('No Product Found\n\n1.Restart\nOption: '))
                                                    if option_ins_5 == 1:
                                                        success_5 = True
                                                        success_7 = True

                                            except ValueError:
                                                print("Invalid input, integers only")
                                                time.sleep(1)

                            else:
                                success_8 = False
                                while not success_8:
                                    try:
                                        hospital_name(pharmacist)
                                        option_ins_6 = int(input("No Products in the cart\n1. Exit"))
                                        if option_ins_6 == 1:
                                            success_8 = True

                                    except ValueError:
                                        print("Invalid input, integers only")
                                        time.sleep(1)

                        elif option_ins_3 == 3:
                            return master_cart

                    except ValueError:
                        print("Invalid input, integers only")
                        time.sleep(1)

        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name(pharmacist)
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')


# A function to dispense medicine
def dispense(patient, pharmacist, test=False, cart_test=""):

    update_expiry_status()
    main = True
    while main:
        try:
            hospital_name(pharmacist, test=test)

            # The cart items comes from the 'add_to_cart' function

            if test:
                cart_items = cart_test
            else:
                cart_items = add_to_cart(pharmacist)

            if cart_items:
                total_price = round(sum(r['quantity'] * r['unit_price'] for r in cart_items), 2)

                success = False
                while not success:
                    try:
                        hospital_name(pharmacist, test=test)
                        amount_paid = round(float(input(f'Total Bill {total_price}\nPay Amount: ')), 2)

                        if amount_paid == total_price:
                            if not test:
                                patient_details = {'name': patient.name,
                                                   'email': patient.email_address}

                                pharmacist_details = {'name': pharmacist.name,
                                                      'email': pharmacist.email_address}

                                receipt = Receipt()
                                receipt_id = receipt_number_gen()
                                receipt.total_amount = float(total_price)

                                receipt.patient_name = patient_details['name']
                                receipt.patient_email_address = patient_details['email']

                                receipt.till_operator = pharmacist_details['name']
                                receipt.till_operator_email = pharmacist_details['email']
                                receipt.receipt_number = receipt_id
                                receipt.purchased_items = cart_items

                                patient.receipts.append(cart_items)
                                total_cost = update_inventory(cart_items)
                                receipt.total_cost = total_cost

                                if save_document(receipt):
                                    if save_document(patient):
                                        pass
                                    else:

                                        receipt_to_deleted = receipt.to_json()
                                        path_1 = (os.path.join(Path.cwd().parent, 'null_receipts.txt'))
                                        path_1 = r"{}".format(path_1)

                                        try:
                                            with open(path_1, 'a') as f:
                                                f.write(receipt_to_deleted + "\n")
                                                return False, f'Failed to complete action.'
                                        except Exception:
                                            pass
                                else:
                                    return False, f'Failed to complete action.'

                                receipt_generator(cart_items, receipt_id, patient_details, pharmacist_details)
                                payment_details = ""
                                for product in cart_items:
                                    payment_details += str("Product Name: " + product['medicine_name'] + "   Dosage: " + str(product['dosage']) + "    Quantity: " + str(product['quantity']) + "   Total Price: " + "$" + str(round(product['unit_price'] * product['quantity'], 2)) + "\n")
                                return True, f'Payment Successful.\n\nReceipt No. {receipt_id}\nPatient Name: {patient_details["name"]}\nEmail: {patient_details["email"]}\nTotal Amount paid: ${total_price}\nPurchased Items:\n{payment_details}'

                            else:
                                update_inventory(cart_items)
                                return
                        else:
                            success_2 = False
                            while not success_2:
                                try:
                                    hospital_name(pharmacist)
                                    option = int(input(f'Correct Amount is {total_price}\n1. Restart 2. Reserve Cart 3. Exit\nOption: '))
                                    if option == 1:
                                        success_2 = True

                                    elif option == 2:
                                        patient.cart_unpaid = cart_items
                                        if patient.save():
                                            return True, f'Cart saved, can be accessed later.'
                                    elif option == 3:
                                        return False, f'Transaction, couldn\'t be processed.'
                                except Exception:
                                    print("Invalid input, integers only")
                                    time.sleep(1)



                    except Exception as e:
                        print(e)
                        print("Invalid input, integers only")
                        time.sleep(1)

            else:
                return False, f'Dispensed Nothing'

        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name(pharmacist)
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

# A function to see if the items in the can be dispensed
def check_order(cart):
    update_expiry_status()
    main = True
    while main:
        try:
            medicine_name = cart['medicine_name'].lower()
            dosage = cart['dosage'].lower()
            quantity = cart['quantity']

            search_result = Medicine.objects(medicine_name__exact=medicine_name, expired=False)
            if search_result:
                for product in search_result:
                        if product.dosage.lower() == dosage:
                            total_qty = search_result.sum('quantity')
                            if total_qty >= quantity:
                                unit_price = product.unit_price
                                return True, unit_price, f'Order is feasible'
                            else:
                                return False, 0, f'Quantity [{cart["quantity"]}] beyond stock. Available {total_qty}'
                        else:
                            return False, 0, f'Dosage [{cart["dosage"]}] not available'

            else:
                return False, 0, f'Medicine [{cart["medicine_name"]}] not available'

        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

# A function to update the price
def update_price(admin):
    update_expiry_status()
    main = True
    while main:
        hospital_name(admin)
        medicine_name = input('Enter the medicine name: ').lower()
        dosage = input('Enter the dosage: ')

        medicines = Medicine.objects(medicine_name=medicine_name, dosage=dosage, expired=False).all()
        total_cost = 0
        total_quantity = 0

        if medicines:

            for medicine in medicines:
                total_cost += medicine.cost
                total_quantity += medicine.quantity

            unit_cost = round(total_cost / total_quantity, 2)
            success = False
            while not success:
                try:
                    success_1 = False
                    while not success_1:
                        min_mark_up = minimum_mark_up(unit_cost)
                        medicine = list(medicines)[0]
                        hospital_name(admin)
                        mark_up_unit_price = float(input(f"Current unit price is ${medicine.unit_price}\nCurrent unit cost is ${unit_cost} ~ mark up (0~1)\nMinimum mark up is {min_mark_up}: " )) if unit_cost > 0 else float(input('Enter the unit price: '))

                        if unit_cost > 0:
                            if mark_up_unit_price >= min_mark_up:
                                unit_price = round(unit_cost * (1 + mark_up_unit_price), 2)
                                success_1 = True

                            else:
                                success_ins = False
                                while not success_ins:
                                    try:
                                        hospital_name(admin)
                                        option = int(input(
                                            f'The entered mark up has no effect, minimum mark up is {round(min_mark_up * 100, 2)}%\n1 Restart 2. Exit\nOptions: '))
                                        if option == 2:
                                            return False, f'Could not complete action.'
                                        elif 1:
                                            success_ins = True

                                    except ValueError:
                                        print("Invalid input, Float only")
                                        time.sleep(1)
                        else:
                            unit_price = round(mark_up_unit_price, 2)

                    confirm = False
                    while not confirm:
                        marginal = round(unit_price - unit_cost, 2)
                        hospital_name(admin)
                        print(
                            f'Medicine name: {string.capwords(medicine_name)}\nDosage: {string.capwords(dosage)}\nUnit Price: ${unit_price}\n{"Marginal Profit: $" if marginal >= 0 else "Marginal Loss"} {marginal}')
                        try:
                            option = int(input('1. Confirm 2. Edit 3. Exit\nOption: '))
                            hospital_name(admin)
                            if option == 1:
                                for medicine in medicines:
                                    medicine.unit_price = unit_price
                                    medicine.save()



                                return True, f'Successfully changed the unit price of {string.capwords(medicine_name)} ~ {string.capwords(dosage)} to ${unit_price}'

                            elif option == 2:
                                confirm = True

                            elif option == 3:
                                return False, f"Could not complete the action."

                        except ValueError:
                            print("Invalid input, Float only")
                            time.sleep(1)

                except ValueError:
                    print("invalid input")
                    time.sleep(1)
        else:
            success_2 = False
            while not success_2:
                try:
                    hospital_name(admin)
                    option = int(input('Medicine not found.\n1. Retry 2. Exit\nOption: '))
                    if option == 1:
                        main = True
                        success_2 = True
                    elif option == 2:
                        return False, f"Could not complete the action."

                except ValueError:
                    print("Integers Only")
                time.sleep(1)


# A function to update the inventory after a dispensing
def update_inventory(cart):
    update_expiry_status()
    try:
        total_cost = 0
        for order in cart:
            inventory_database = Medicine.objects(medicine_name=order['medicine_name'].lower(), dosage=order['dosage'], expired=False).order_by('expiry_date')
            qty = order['quantity']

            processed_documents = []
            for product in inventory_database:
                if qty > 0:
                    processed_documents.append(product)
                    if product.quantity - qty > 0:
                        total_cost += product.unit_cost * qty
                        difference = product.quantity - qty
                        qty = 0
                        product.quantity = difference
                        product.save()

                    elif product.quantity - qty <= 0:
                        qty -= product.quantity
                        total_cost += product.unit_cost * qty
                        delete_document(product)

                else:
                    break

        return float(total_cost)


    except  Exception:
        success = False
        while not success:
            try:
                option = int(input('Cannot connect to the Database. Make sure you are connected to internet.'
                                   '\n1.Connect Again 2. Exit\nOption: '))
                if option == 1:
                    success = True
                elif option == 2:
                    return
            except ValueError:
                print('Invalid Input')


# A function to update the array of patients awaiting to vist the doctor
def update_consultation(doctor, patient):
    try:
        doctor = Doctor.objects(name=doctor).first()
        doctor.consultation.remove(patient)
        if save_document(doctor):
            return True, f'Successful'
        else:
            return False, f"Could not complete action, because of Connection Issues."

    except Exception as e:
        success = False
        while not success:
            try:
                option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                   '\n1.Retry 2. Exit\nOption: '))
                if option == 1:
                    success = True
                elif option == 2:
                    return False
            except ValueError:
                print('Invalid Input')

# A function to increase the stock of existing products
def increase_stock(pharmacist):
    update_expiry_status()
    main = True
    while main:
        try:
            hospital_name(pharmacist)
            medicine_name_raw = input("Medicine name: ").rstrip()
            medicine_name = medicine_name_raw.lower()

            dosage_raw = input("Dosage: ")
            dosage= dosage_raw.lower().rstrip()
            medicine_object = Medicine.objects()
            existing_medicine = medicine_object(medicine_name=medicine_name, dosage=dosage).first()

            if existing_medicine:
                preceding_batchId = Medicine.objects.all().order_by('-batch_id').first()
                batch_id = int(preceding_batchId.batch_id) + 1 if preceding_batchId else 1
                expiry_date_validated = False
                while not expiry_date_validated:
                    hospital_name(pharmacist)
                    expiry_date = input('Expiry Date (dd/mm/yyyy): ')
                    if len(expiry_date[0:2]) == 2 and len(expiry_date[3:5]) == 2 and len(
                            expiry_date[6:10]) == 4 and expiry_date.count(
                            '/') == 2 and expiry_date[0:2].isnumeric() and expiry_date[3:5].isnumeric() and expiry_date[
                                                                                                            6:10].isnumeric() and 0 < int(
                        expiry_date[0:2]) < 32 and 0 < int(expiry_date[3:5]) < 13:
                        expiry_date = datetime.datetime.strptime(expiry_date, '%d/%m/%Y')
                        if expiry_date < datetime.datetime.now():
                            print("You can't add expired drugs.")
                            time.sleep(1)
                        else:
                            expiry_date_validated = True
                    else:
                        success = False
                        while not success:
                            try:
                                hospital_name(pharmacist)
                                option = int(input('Wrong Date Format, example: 01/01/2020\n1. Restart 2. Exit\nOption:\t'))
                                if option == 1:
                                    success = True
                                elif option == 2:
                                    return False, f"Could not complete the transaction."

                            except ValueError:
                                print("Invalid input, integers only")
                                time.sleep(1)

                cost_validated = False
                while not cost_validated:
                    try:
                        cost = round(float(input('Cost ($): ')), 2)
                        if cost < 0:
                            cost_validated_ins = False
                            while not cost_validated_ins:
                                hospital_name(pharmacist)
                                option = input('Cost can not be less than $0.00\n1. Restart 2. Exit\nOption: ')
                                if option == 1:
                                    cost_validated_ins = True
                                if option == 2:
                                    cost_validated = True
                                    main = False
                                    cost_validated_ins = True
                        elif cost > 1000000000000000:
                            print(f'Quantity: {cost} is above the limit [ $1 000 000 000 000 000]')
                            time.sleep(2)

                        else:
                            cost_validated = True

                    except ValueError:
                        print("Invalid input, float only")
                        time.sleep(1)

                quantity_validated = False
                while not quantity_validated:
                    try:
                        hospital_name(pharmacist)
                        quantity = int(input('Quantity: '))
                        unit_cost = round(cost / float(quantity), 2) if cost != 0 else f'Null'
                        if quantity < 0:
                            quantity_validated_ins = False
                            while not quantity_validated_ins:
                                option = input('Quantity cannot be less than 0 units.\n1. Restart 2. Exit\nOption: ')
                                if option == 1:
                                    quantity_validated_ins = True
                                if option == 2:
                                    quantity_validated = True
                                    main = False
                                    quantity_validated_ins = True

                        elif quantity > float(100000000000):
                            print(f'Quantity: {quantity} is above the limit [1 000 000 000]')
                            time.sleep(2)

                        if unit_cost != 'Null':
                            if round(cost / float(quantity), 2) < 0.00:
                                print('Unit cost should be above $0.00')
                                time.sleep(2)
                            else:
                                quantity_validated = True


                        else:
                            quantity_validated = True

                    except ValueError:
                        print('Invalid input')
                        time.sleep(1)

                confirm = False
                while not confirm:
                    hospital_name(pharmacist)
                    print(
                        f'Batch ID: {batch_id}\nMedicine name: {medicine_name}\nDosage: {dosage}\nQuantity {quantity}\nCost: ${cost}')
                    try:
                        option = int(input('1. Confirm 2. Edit 3. Exit\nOption: '))
                        if option == 1:
                            new_medicine = Medicine()
                            new_medicine.medicine_name = medicine_name
                            new_medicine.added_by = pharmacist.name
                            new_medicine.expiry_date = expiry_date
                            new_medicine.expired = False
                            new_medicine.unit_price = existing_medicine.unit_price
                            new_medicine.unit_cost = round(cost/quantity, 2)
                            new_medicine.quantity = int(quantity)
                            new_medicine.dosage = existing_medicine.dosage
                            new_medicine.cost = cost
                            new_medicine.batch_id = batch_id
                            if save_document(new_medicine):
                                hospital_name(pharmacist)
                                return True, f'Successfully added Batch ID:{batch_id}, {quantity} units {medicine_name_raw.upper()} to stock'
                            else:
                                hospital_name(pharmacist)
                                return False, f"Could not complete action, because of Connection Issues."

                        elif option == 2:
                            confirm = True

                        elif option == 3:
                            return False, f"Could not complete the transaction."

                    except ValueError:
                        print("Invalid input, Float only")
                        time.sleep(1)
            else:
                success_3 = False
                while not success_3:
                    try:
                        hospital_name(pharmacist)
                        option = int(input(f'Medicine name: {medicine_name_raw.upper()} ~ {dosage} is not in Stock, add it afresh.\n1. Restart 2. Exit\nOption: '))
                        if option == 1:
                            success_3 = True
                        elif option == 2:
                            return False, f'Medicine does not exists in database'

                    except ValueError:
                        print('Invalid input, integers only')
                        time.sleep(1)

        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name(pharmacist)
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

# A function to add new stock
def add_to_stock(pharmacist):
    update_expiry_status()
    main = True
    while main:
        try:
            hospital_name(pharmacist)
            medicine_name_raw = input('Medicine name: ').rstrip()
            medicine_name = medicine_name_raw.lower()
            medicine_object = Medicine.objects()
            dosage_raw = input('Dosage: ').rstrip()
            dosage = dosage_raw.lower()
            medicine_exist = medicine_object(medicine_name=medicine_name, dosage=dosage, expired=False)
            if not medicine_exist:
                preceding_batchId = Medicine.objects.all().order_by('-batch_id').first()
                batch_id = int(preceding_batchId.batch_id) + 1 if preceding_batchId else 1

                expiry_date_validated = False
                while not expiry_date_validated:
                    hospital_name(pharmacist)
                    expiry_date = input('Expiry Date (dd/mm/yyyy): ')
                    if len(expiry_date[0:2]) == 2 and len(expiry_date[3:5]) == 2 and len(expiry_date[6:10]) == 4 and expiry_date.count(
                            '/') == 2 and expiry_date[0:2].isnumeric() and expiry_date[3:5].isnumeric() and expiry_date[
                                                                                            6:10].isnumeric() and 0 < int(
                        expiry_date[0:2]) < 32 and 0 < int(expiry_date[3:5]) < 13:
                        expiry_date = datetime.datetime.strptime(expiry_date, '%d/%m/%Y')
                        if expiry_date < datetime.datetime.now():
                            print("You can't add expired drugs.")
                        else:
                            expiry_date_validated = True
                    else:
                        success = False
                        while not success:
                            try:
                                hospital_name(pharmacist)
                                option = int(input('Wrong Date Format, example: 01/01/2020\n1. Restart 2. Exit\nOption:\t'))
                                if option == 1:
                                    success = True
                                elif option == 2:
                                    return False, f'Could not complete action'

                            except ValueError:
                                print("Invalid input, integers only")
                                time.sleep(1)

                cost_validated = False
                while not cost_validated:
                    try:
                        hospital_name(pharmacist)
                        cost = round(float(input('Cost ($): ')), 2)
                        if cost < 0:
                            cost_validated_ins = False
                            while not cost_validated_ins:
                                hospital_name(pharmacist)
                                option = input('Cost can not be less than $0.00\n1. Restart 2. Exit\nOption: ')
                                if option == 1:
                                    cost_validated_ins = True
                                if option == 2:
                                    cost_validated = True
                                    main = False
                                    cost_validated_ins = True
                        elif cost > 1000000000000000:
                            print(f'Quantity: {cost} is above the limit [ $1 000 000 000 000 000]')
                            time.sleep(2)

                        else:
                            cost_validated = True

                    except ValueError:
                        print("Invalid input, float only")
                        time.sleep(1)

                quantity_validated = False
                while not quantity_validated:
                    try:
                        hospital_name(pharmacist)
                        quantity = int(input('Quantity: '))
                        unit_cost = round(cost / float(quantity), 2) if cost != 0 else f'Null'
                        if quantity < 0:
                            quantity_validated_ins = False
                            while not quantity_validated_ins:
                                hospital_name(pharmacist)
                                option = input('Quantity cannot be less than 0 units.\n1. Restart 2. Exit\nOption: ')
                                if option == 1:
                                    quantity_validated_ins = True
                                if option == 2:
                                    quantity_validated = True
                                    main = False
                                    quantity_validated_ins = True

                        elif quantity > float(100000000000):
                            hospital_name(pharmacist)
                            print(f'Quantity: {quantity} is above the limit [1 000 000 000]')
                            time.sleep(2)

                        if unit_cost != 'Null':
                            hospital_name(pharmacist)
                            if round(cost/float(quantity),2) < 0.00:
                                hospital_name(pharmacist)
                                print('Unit cost should be above $0.00')
                                time.sleep(2)
                            else:
                                quantity_validated = True


                        else:
                            quantity_validated = True

                    except Exception as e:
                        print(e)
                        time.sleep(1)

                unit_cost_val = False
                while not unit_cost_val:
                    try:
                        if unit_cost != 'Null' and unit_cost != 0:
                            success_mark_up = False
                            while not success_mark_up:
                                try:

                                    min_mark = round(minimum_mark_up(unit_cost), 2)

                                    hospital_name(pharmacist)
                                    mark_up = float(
                                        input(f'Unit Cost is {unit_cost}\nMark up(0.25 is 25%)\nMin mark up is {round(min_mark * 100, 2)}%\nMark up: '))

                                    mark_up_validated = False
                                    while not mark_up_validated:
                                        if 0 <= mark_up:
                                            unit_price = round(unit_cost + (unit_cost * mark_up), 2)
                                            if min_mark <= mark_up:
                                                success_mark_up = True
                                                unit_cost_val = True
                                                mark_up_validated = True
                                            else:
                                                success_ins = False
                                                while not success_ins:
                                                    try:
                                                        hospital_name(pharmacist)
                                                        option = int(input(f'The entered mark up has no effect, minimum mark up is {round(minimum_mark_up(unit_cost) *100, 2)}%\n1 Restart 2. Exit\nOptions: '))
                                                        if option == 2:
                                                            return False, f'Could not complete action.'
                                                        elif 1:
                                                            mark_up_validated = True
                                                            success_ins = True
                                                    except ValueError:
                                                        print("Invalid input, Float only")
                                                        time.sleep(1)
                                        else:
                                            success_ins_2 = False
                                            while not success_ins_2:
                                                try:
                                                    hospital_name(pharmacist)
                                                    options = int(input('Enter a valid range of mark_up up.\n1. Restart 2. Exit'))
                                                    if options == 1:
                                                        success_ins_2 = True
                                                    elif 2:
                                                        return False, f'Could not complete action.'

                                                except ValueError:
                                                    print("Invalid input, Float only")
                                                    time.sleep(1)

                                except ValueError:
                                    print("Invalid input, Float only")
                                    time.sleep(1)
                        else:
                            success_2 = False
                            while not success_2:
                                try:
                                    hospital_name(pharmacist)
                                    unit_price = round(float(input('Enter the unit price: ')), 2)
                                    unit_cost_val = True
                                    success_2 = True
                                except ValueError:
                                    print("Invalid input, Float only")
                                    time.sleep(1)

                    except ValueError:
                        pass

                confirm = False
                while not confirm:
                    hospital_name(pharmacist)
                    print(f'Batch ID: {batch_id}\nMedicine name: {medicine_name_raw.upper()}\nDosage: {dosage_raw}\nExpiry Date: {expiry_date}\nUnit Price: {unit_price}')
                    try:
                        option = int(input('1. Confirm 2. Edit 3. Exit\nOption: '))
                        if option == 1:
                            medicine = Medicine()
                            medicine.medicine_name = medicine_name
                            medicine.expiry_date = expiry_date
                            medicine.added_by = pharmacist.name
                            medicine.expired = False
                            medicine.unit_price = unit_price
                            medicine.unit_cost = round(cost/quantity, 2)
                            medicine.quantity = int(quantity)
                            medicine.dosage = dosage
                            medicine.cost = cost
                            medicine.batch_id = batch_id

                            if save_document(medicine):
                                return True, f'Successfully added {batch_id} - {medicine_name_raw.upper()} ~ {dosage} to stock'
                            else:
                                return False, f"Could not complete the transaction, because of Connection Issues."

                        elif option == 2:
                            confirm = True

                        elif option == 3:
                            return False, f"Could not complete the action."

                    except ValueError:
                        print("Invalid input, Float only")
                        time.sleep(1)
            else:
                success_3 = False
                while not success_3:
                    try:
                        hospital_name(pharmacist)
                        option = int(input(f'{medicine_name.upper()} ~ {dosage} is already in Stock.\n1. Restart 2. Exit\nOption: '))
                        if option == 1:
                            success_3 = True
                        elif option == 2:
                            return False, f"Could not complete the action."

                    except ValueError:
                        print('Invalid input, integers only')
                        time.sleep(1)

        except Exception as e:
            success = False
            while not success:
                try:
                    hospital_name(pharmacist)
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False, f'Could not complete action'
                except ValueError:
                    print('Invalid Input')

# A fucntion to remove stock
def remove_inventory(user):
    complete = False
    while not complete:
        try:
            hospital_name(user)
            batch_id = input("Enter the batch_id: ")
            batch = Medicine.objects(batch_id=batch_id).first()
            if batch:
                success = False
                while not success:
                    try:
                        hospital_name(user)
                        option = int(input(f"Are you sure you want to delete:\n\tBatch ID  <=> {batch_id}\n\tProduct <=> {batch.medicine_name}\n\tDosage <=> {batch.dosage}\n\tExpiry Date <=> {str(batch.expiry_date)}\n1. Yes 2. No\nOption: "))
                        if option == 1:
                            delete_document(batch)
                            return True, f'Successfully deleted Batch No. {batch_id}'
                        elif option == 2:
                            return False, f'Did not deleted Batch No. {batch_id}'

                    except ValueError:
                        print("Integers Only")
                        time.sleep(1)
            else:
                return False, f'Did not find Batch No. {batch_id}'


        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')

#A function to check detais og a single product
def check_medicine_details(user):
    update_expiry_status()
    main = True
    while main:
        try:
            hospital_name(user)
            medicine_name = input("Medicine name: ").lower().rstrip()
            dosage = input("Dosage: ").lower().rstrip()
            medicine_name = Medicine.objects(medicine_name=medicine_name, dosage=dosage)
            if medicine_name:
                hospital_name(user)
                print(f'Total Quantity: {medicine_name.sum("quantity")}, Price ${medicine_name.first().unit_price}')
                success = False
                while not success:
                    try:
                        option = int(input('1. Check Another 2. Exit\nOption: '))
                        if option == 1:
                            success = True

                        if option == 2:
                            main = False
                            success = True

                    except ValueError:
                        print("Integers Only")
                        time.sleep(1)
            else:
                success_2 = False
                while not success_2:
                    try:
                        hospital_name(user)
                        option = int(input('Medicine not found.\n1. Retry 2. Exit\nOption: '))
                        if option == 1:
                            main = True
                            success_2 = True
                        elif option == 2:
                            main = False
                            success_2 = True

                    except ValueError:
                        print("Integers Only")
                    time.sleep(1)

        except Exception as e:
            success = False
            while not success:
                try:
                    option = int(input(f'Error: {e}.\nMake sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')
