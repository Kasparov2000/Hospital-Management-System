import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# A function to check if the email is in the correct format
def check_email(email):
    if re.fullmatch(regex, email):
        return True

    else:
        return False
