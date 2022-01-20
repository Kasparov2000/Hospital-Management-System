import datetime
from mongoengine import *

import pytz
from timezone import time_zone

try:
    timezone = pytz.timezone(time_zone)
except Exception:
    timezone = pytz.timezone("Africa/Harare")

# Document to keep check up details
class CheckUp(Document):
    receptionist_name = StringField()
    patient_name = StringField()
    patient_email_address = EmailField()
    temperature = FloatField(max_length=5)
    systolic_bp = FloatField()
    diastolic_bp = FloatField()
    weight = FloatField()
    timestamp = DateTimeField()
    country = StringField(max_length=30)
    meta = {
        'db_alias': 'HMS',
        'indexes': ['patient_email_address'],
        'collection': 'checkup'}


# A Document to keep track of patient's details
class Patient(Document):
    name = StringField(required='True')
    address = StringField(max_length=30)
    dob = DateField()
    gender = StringField(max_length=6)
    email_address = EmailField(max_length=30)
    registration_date = DateTimeField()
    records = ListField()
    receipts = ListField()
    cart_unpaid = ListField()
    country = StringField(max_length=30)
    to_be_consulted = BooleanField(default=True)
    pending_review = BooleanField(default=False)
    to_be_reviewed = BooleanField(default=False)

    meta = {

        'db_alias': 'HMS',
        'indexes': ['name', 'email_address', 'records'],
        'collection': 'patient'}



class Doctor(Document):
    name = StringField(required='True', max_length=30)
    address = StringField(max_length=30)
    gender = StringField(max_length=6)
    country = StringField(max_length=30)
    dob = DateTimeField(required='True')
    email_address = EmailField(max_length=30)
    registration_date = DateTimeField()
    owing = FloatField()
    salary = FloatField()
    book_count = IntField(default=0)
    visit_queue = ListField()
    meta = {
        'db_alias': 'HMS',
        'indexes': ['email_address', 'book_count', 'visit_queue'],
        'collection': 'doctor'}


class Receptionist(Document):
    name = StringField(required='True', max_length=30)
    address = StringField(max_length=30)
    gender = StringField(max_length=7)
    dob = DateTimeField(required='True')
    country = StringField(max_length=30)
    email_address = EmailField(max_length=30)
    owing = FloatField()
    salary = FloatField()
    registration_date = DateTimeField()
    meta = {
        'db_alias': 'HMS',
        'indexes': ['email_address'],
        'collection': 'receptionist'}


class Pharmacist(Document):
    name = StringField(required='True', max_length=30)
    gender = StringField(max_length=6)
    address = StringField(max_length=30)
    dob = DateTimeField(required='True')
    country = StringField(max_length=30)
    email_address = EmailField()
    owing = FloatField()
    salary = FloatField()
    registration_date = DateTimeField()
    meta = {
        'db_alias': 'HMS',
        'indexes': ['email_address'],
        'collection': 'pharmacist'}


class Nurse(Document):
    name = StringField(required='True', max_length=30)
    gender = StringField(max_length=6)
    address = StringField()
    country = StringField(max_length=30)
    dob = DateTimeField(required='True')
    email_address = EmailField()
    owing = FloatField()
    salary = FloatField()
    registration_date = DateTimeField()
    meta = {
        'db_alias': 'HMS',
        'indexes': ['email_address'],
        'collection': 'nurse'}


# A document to keep details of medicine
class Medicine(Document):
    batch_id = IntField()
    medicine_name = StringField()
    added_by = StringField()
    dosage = StringField()
    expiry_date = DateField()
    expired = BooleanField()
    unit_price = FloatField(precision=2)
    unit_cost = FloatField()
    quantity = IntField()
    cost = FloatField(precision=2)
    meta = {
        'db_alias': 'HMS',
        'indexes': ['dosage', 'unit_cost', 'quantity', 'cost', 'expired', 'medicine_name', 'expiry_date'],
        'collection': 'medicine',
    }


class Receipt(Document):
    successful = BooleanField()
    receipt_number = StringField()
    total_amount = FloatField(precision=2)
    patient_name = StringField()
    patient_email_address = EmailField()
    purchase_date = DateTimeField(default=datetime.datetime.now(timezone))
    purchased_items = ListField(DictField())
    total_cost = FloatField(precision=2)
    till_operator = StringField()
    till_operator_email = EmailField()
    meta = {'auto_create_index': True,
            'indexes': ['receipt_number', 'total_amount', 'patient_email_address', 'receipt_number'],
            'db_alias': 'HMS',
            'collection': 'receipt'}


class CloseDay(Document):
    admin_name = StringField()
    end_of_day = DateTimeField()
    total_revenue = IntField()
    till_operator_details = ListField()
    meta = {'db_alias': 'HMS',
            'indexes': ['end_of_day']}


class User(Document):
    user_name = StringField()
    password = StringField()
    admin = BooleanField()
    date_created = DateTimeField()
    email_address = EmailField()
    profession = StringField()
    login_details = ListField()
    registration_timestamp = DateTimeField()
    meta = {
        'db_alias': 'HMS',
        'indexes': ['email_address', 'profession', 'user_name', "password", "admin"],
        'collection': 'user'}
