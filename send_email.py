from send_email_template import email_template
import string


# A function to send the receipts to the respective functions after the pdf has been generated by the anvil
def send_email_receipts():
    processed_lines = []
    with open('receipts_queue_emails.txt', 'a') as f:
        with open("receipts_queue_emails.txt", 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                for line in lines:
                    patient_name, email_address, time, receipt_address = line.rstrip().split('|')
                    subject = f'{string.capwords(patient_name)} ~ Receipt ~ {time}'
    
                    body = f'Dear {string.capwords(patient_name)},\n\nWe at ALU hospital wish you a speedy recovery and ' \
                           f'' \
                           f'a healthy\nlife. We assure that you will not regret using our services.' \
                           f'\n\nALU hospital appreciates your support by buying our products, thank you for the continued' \
                           f' support.\n\nPlease ' \
                           f'do not' \
                           f' forget to incorporate the instructions given by our experts when using the medicine.\n\nBest ' \
                           f'Regards\n\nALU hospital. '
    
                    receipt_address = r'{}'.format(receipt_address)
    
                    try:
                        if email_template(email_address, receipt_address, subject, body):
                            processed_lines.append(line)
    
                        else:
                            continue
    
                    except Exception as e:
                        pass
            else:
                return

    if len(processed_lines) > 0:
        for processed_line in processed_lines:
            lines.remove(processed_line)
            

        with open('receipts_queue_emails.txt', 'w') as f:
            for line in lines:
                f.write(line)


def send_email_reports():
    processed_lines = []
    with open('reports_queue_emails.txt', 'a') as s:
        with open("reports_queue_emails.txt", 'r') as f:
            lines = f.readlines()
   
            if len(lines) > 0:
                for line in lines:
                    patient_name, email_address, time, receipt_address = line.rstrip().split('|')
    
                    subject = f'{string.capwords(patient_name)} ~ Medical Report ~ {time}'
    
                    body = f'Dear {string.capwords(patient_name)},\n\nWe at ALU hospital wish you a speedy recovery and ' \
                           f'' \
                           f'a healthy\nlife. We assure that you will not regret using our services.' \
                           f'\n\nALU hospital appreciates your support by visting our doctor, thank you for the continued ' \
                           f'support.\n\nPlease ' \
                           f'do not' \
                           f' forget to incorporate the instructions given by our experts when using the medicine.\n\nBest ' \
                           f'Regards\n\nALU hospital. '
    
                    receipt_address = r'{}'.format(receipt_address)
    
                    try:
                        if email_template(email_address, receipt_address, subject, body):
                            processed_lines.append(line)

                    except Exception:
                        continue
            else:
                return

    if len(processed_lines) > 0:
        for processed_line in processed_lines:
            lines.remove(processed_line)

        with open('reports_queue_emails.txt', 'w') as f:
            f.writelines(lines)

send_email_receipts()
send_email_reports()
