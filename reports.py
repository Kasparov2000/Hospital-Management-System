import anvil.server
import anvil.pdf
import anvil.media
import datetime
import json
from pathlib import Path
import os
from send_email import *


@anvil.server.callable
def get_file():
    # Return a file from this local machine
    return anvil.media.from_file("logo2.jpg", "logo.jpg")


# A function to upload the receipt to the anvil server
def upload_medical_report():
    processed_lines = []
    with open("reports.txt", 'a') as f:
        with open("reports.txt", 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                for index, line in enumerate(lines):
                    report = json.loads(line.rstrip())
                    report[0]['logo'] = get_file()
                    try:
                        anvil.server.connect("4TO6M5IW3DMJKR6NMOGO7C47-GRH2ITODVPYSK6HB", quiet=True)
                        pdf = anvil.pdf.render_form("medical", report)
                        time = str(datetime.datetime.now()).replace('-', '').replace(' ', '').replace(":", '').replace('.', '')
                        path_2 = (os.path.join(Path.cwd(), 'medical_reports',
                                               f'{report[0]["name"].replace(" ", "")}_medical_report_{time}.pdf'))
                        path_2 = r"{}".format(path_2)
                        anvil.media.write_to_file(pdf, path_2)

                        with open('reports_queue_emails.txt', 'a') as f:
                            name = report[0]['patient_details']['patient_name']
                            email = report[0]['patient_details']['patient_email']
                            date = report[0]['details']["date"]

                            f.write(f"{name}|{email}|{date}|{path_2}\n")

                        processed_lines.append(line)

                    except Exception:
                        continue

            else:
                return

    try:
        send_email_reports()
    except Exception:
        pass

    if len(processed_lines) > 0:
        for processed_line in processed_lines:
            lines.remove(processed_line)


        with open('reports.txt', 'w') as f:
            f.writelines(lines)


upload_medical_report()






