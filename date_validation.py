import datetime
from terminal_effects import hospital_name
import time


# A function to check if the date is in the correct format, for instance checking if the date is not 13/13/2021
def date_validation(name):
    date_validated = False
    while not date_validated:
        hospital_name(name)
        date = input('Enter the starting date (dd/mm/yyyy): ')
        if len(date[0:2]) == 2 and len(date[3:5]) == 2 and len(date[6:10]) == 4 and date.count(
                '/') == 2 and date[0:2].isnumeric() and date[3:5].isnumeric() and date[
                                                                                  6:10].isnumeric() and 0 < int(
            date[0:2]) < 32 and 0 < int(date[3:5]) < 13:

            date_object = datetime.datetime.strptime(date, '%d/%m/%Y')
            
            if date_object > datetime.datetime.now():
                success = False
                while not success:
                    try:
                        option = int(input('Please enter a retrospective date\n1. Retry 2. exit'))
                        if option == 1:
                            success = True
                        elif option == 2:
                            return False

                    except ValueError:
                        print('Invalid input')
                        time.sleep(1)
                print('Please enter a valid date')
                time.sleep(2)
            
            else:
                return date_object
