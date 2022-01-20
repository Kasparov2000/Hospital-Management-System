from hospital_details import hospital_details

import anvil.server
import anvil.pdf
import anvil.media
import datetime
import json
from pathlib import Path
import os
from send_email import *
import string

path_1 = (os.path.join(Path.cwd(), 'receipts.txt'))
path_1 = r"{}".format(path_1)

# A function to convert the logo to Blob Media understood by the API
@anvil.server.callable
def get_file():
    # Return a file from this local machine
    return anvil.media.from_file("logo2.jpg", "logo.jpg")

# A function to generate a receipt and save it to a text file, awaiting it to be returned as a pdf
def receipt_generator(product_details, receipt_number, patient_details, cash_receiver_details):
    try:
        receipt = [{'receipt': product_details,
                    'receipt_number': receipt_number,
                    'patient_details': patient_details,
                    'cash_receiver_details': cash_receiver_details,
                    'date': datetime.datetime.now().strftime('%A %d %B %Y'),
                    'time': f'{datetime.datetime.now().strftime("%I")}:{datetime.datetime.now().strftime("%M %p")}',

                    'logo': get_file(),
                    'details': hospital_details}]

        with open(path_1, 'a') as f:
            receipt[0]['logo'] = ''
            f.write(json.dumps(receipt) + "\n")
            f.close()
            print('done')

        upload_receipt()

    except Exception:
        pass

# A function to read a text file and send the data to the anvil server
def upload_receipt():
    try:
        with open(path_1, 'a') as f: 
            with open(path_1, 'r') as f:
                processed_lines = []
                lines = f.readlines()
                if len(lines) > 0:
                    for index, line in enumerate(lines):
                        receipt = json.loads(line.rstrip())
                        receipt[0]['logo'] = get_file()

                        try:
                            anvil.server.connect("4TO6M5IW3DMJKR6NMOGO7C47-GRH2ITODVPYSK6HB", quiet=True)
                            pdf = anvil.pdf.render_form("ReportForm", receipt)
                            path_2 = (os.path.join(Path.cwd(), 'receipts', f'{receipt[0]["patient_details"]["name"].replace(" ", "")}_{receipt[0]["receipt_number"]}.pdf'))
                            path_2 = r"{}".format(path_2)
                            anvil.media.write_to_file(pdf, path_2)
                            with open("receipts_queue_emails.txt", 'w') as f:
                                patient_name = f'{receipt[0]["patient_details"]["name"]}'
                                email_address = f'{receipt[0]["patient_details"]["email"]}'
                                time = f'{receipt[0]["date"]}'

                                f.write(f'{patient_name}|{email_address}|{time}|{path_2}\n')

                            processed_lines.append(line)

                        except Exception:
                            pass
                else:
                    return

            if len(processed_lines) > 0:
                for processed_line in processed_lines:
                    lines.remove(processed_line)

            with open(path_1, 'w') as f:
                    f.writelines(lines)

    except Exception:
        pass

    try:
        send_email_receipts()
    except Exception:
        pass
