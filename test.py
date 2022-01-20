from mongo_setup import global_init
from db_model import *
import unittest
import datetime
from query import *


global_init(test=True)


class TestCase(unittest.TestCase):
    def add_a_doctor(self):
        # Creating a doctor object
        doctor = Doctor(name='Tafara Kasparov Mhangami', address='Kwekwe Zimbabwe',
                        gender='male', country='Zimbabwe', dob=datetime.datetime(2000, 4, 5),
                        email_address='t.mhangami@alustudent.com', registration_date=datetime.datetime.now(),
                        owing=0, salary=1000, book_count=0, visit_queue=[])
        doctor.save()

        # Checking the newly added object by using this query and checking if its identical to the one saved
        new_doctor = Doctor.objects().order_by('-registration_date').first()
        self.assertEqual(doctor, new_doctor)
        print("Test case 1 successful")


    def update_expiry_status(self):
        medicine = Medicine(batch_id=1, medicine_name='ARV', added_by="jeanne", dosage="30mg", expiry_date=datetime.datetime(2020, 4, 4),
                            expired=False, unit_price=0.05, unit_cost=0.04, quantity=1000, cost=40)
        medicine.save()

        # When the date is 2020/4/4, this method is called
        update_expiry_status()

        # Checking if the expired status has been updated
        added_medicine = Medicine.objects(batch_id=1).first().expired
        self.assertTrue(added_medicine)

        # Deleting the object
        medicine = Medicine.objects(batch_id=1).first()
        medicine.delete()
        print("Test case 2 successful")

    def dispense_drugs(self):
        medicine_1 = Medicine(batch_id=1, medicine_name='arv', added_by="jeanne", dosage="30mg",
                            expiry_date=datetime.datetime(2022, 4, 4),
                            expired=False, unit_price=0.05, unit_cost=0.04, quantity=1000, cost=40)

        medicine_2 = Medicine(batch_id=2, medicine_name='arv', added_by="jeanne", dosage="30mg",
                            expiry_date=datetime.datetime(2023, 4, 4),
                            expired=False, unit_price=0.05, unit_cost=0.04, quantity=1000, cost=40)
        medicine_1.save()
        medicine_2.save()

        # The cart to be dispensed
        cart = [{"medicine_name": "arv",
                "dosage": "30mg",
                "quantity": 1950,
                'unit_price': 0.04}]

        dispense("null", "null", test=True, cart_test=cart)

        # The total quantity of all arv's remaining
        total_quantity = Medicine.objects(medicine_name='arv').sum('quantity')

        # The total_quantity batch 2 remaining
        medicine_2_updated = Medicine.objects(batch_id=2).sum('quantity')

        self.assertEqual(50, total_quantity)

        # This shows that the stock is dispensed on FIFO basis
        self.assertEqual(50, medicine_2_updated)


        medicine_2 = Medicine.objects(batch_id=2).first()
        medicine_2.delete()

        print("Test case 3 successful")

    def add_stock(self):
        pharmacist = Pharmacist(name='Tafara Kasparov Mhangami', address='Kwekwe Zimbabwe',
                        gender='male', country='Zimbabwe', dob=datetime.datetime(2000, 4, 5),
                        email_address='t.mhangami@alustudent.com', registration_date=datetime.datetime.now(),
                        owing=0, salary=1000)
        pharmacist.save()

        add_to_stock(pharmacist)

        medicine_added = Medicine.objects(batch_id=1).first()

        medicine_objects = Medicine.objects().count()

        self.assertEqual(medicine_objects, 1)

        success = False
        while not success:
            try:
                print(f'\n\nBatch ID: {medicine_added.batch_id}\nMedicine name: {medicine_added.medicine_name}\n'
                      f'Dosage: {medicine_added.dosage}\nExpiry Date: {medicine_added.expiry_date}\nUnit Price: {medicine_added.unit_price}')
                option = int(input('1. Correct 2. Wrong\nOption: '))
                if option == 1:
                    print('Test 4 successful')
                    medicine_added.delete()
                    success = True

                elif option == 2:
                    print('Test 4 not successful')
                    medicine_added.delete()
                    success = True

            except Exception:
                print('Invalid input')

    def add_patient(self):
        # Adding a patient
        patient = Patient(name='Tafara Kasparov Mhangami', address='Kwekwe Zimbabwe',
                        gender='male', country='Zimbabwe', dob=datetime.datetime(2000, 4, 5),
                        email_address='t.mhangami@alustudent.com', registration_date=datetime.datetime.now(),
                        records=[], receipts=[], cart_unpaid=[])
        patient.save()

        # Querying for the added object
        patient_added = Patient.objects().first()

        name = patient_added.name
        to_be_reviewed = patient_added.to_be_reviewed
        to_be_consulted = patient_added.to_be_consulted
        pending_review = patient_added.pending_review

        self.assertEqual(name, 'Tafara Kasparov Mhangami')

        # Checking if the default values are set correctly
        self.assertEqual(to_be_reviewed, False)
        self.assertEqual(pending_review, False)
        self.assertEqual(to_be_consulted, True)

        patient_added.delete()
        print('Test 5 successful')


# test_case_1 = TestCase()
# test_case_1.add_a_doctor()

# test_case_2 = TestCase()
# test_case_2.update_expiry_status()

# test_case3 = TestCase()
# test_case3.dispense_drugs()

# test_case4 = TestCase()
# test_case4.add_stock()

# test_case5 = TestCase()
# test_case5.add_patient()


