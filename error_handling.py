# Functions to handle errors if there is a problem updtaing the database


def save_document(object):
    save_complete = False
    while not save_complete:
        try:
            object.save()
            return True
        except Exception as e:


            success = False
            while not success:
                try:
                    print(e)
                    option = int(input('Cannot save the document. Make sure you are connected to internet.'
                                       '\n1.Retry 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return False
                except ValueError:
                    print('Invalid Input')


def delete_document(object):
    delete_complete = False
    while not delete_complete:
        try:
            object.delete()
            return True

        except Exception:
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