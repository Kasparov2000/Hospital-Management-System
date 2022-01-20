from db_model import *
import json
import os
from error_handling import *
from pathlib import Path


path_1 = (os.path.join(Path.cwd(), 'null_receipts.txt'))
path_1 = r"{}".format(path_1)

# A function to nullify receipts if they are errors in updating the errors
def nullify_receipts():
    try:
        main = True
        while main:
            with open(path_1, 'r') as r:
                receipts = r.readlines()
                receipts_copy = receipts
                with open(path_1, 'w') as w:
                    if len(receipts) > 0:
                        for i in range(len(receipts)):
                            receipt_number = json.loads(receipts[i - 1].rstrip())['receipt_number']

                            null_receipt = Receipt.objects(receipt_number=receipt_number).first()
                            null_receipt.successful = False

                            if save_document(null_receipt):
                                receipts_copy.remove(receipts[i - 1])

                            else:
                                for receipt_ in receipts_copy:
                                    w.write(receipt_)
                                return False
                    else:
                        return
    except Exception as e:
        print(e)
        success = False
        while not success:
            try:
                option = int(input('Cannot save the document. Make sure you are connected to internet.'
                                   '\n1.Retry 2. Exit\nOption: '))
                if option == 1:
                    success = True
                elif option == 2:
                    return False
            except ValueError:
                print('Invalid Input')
