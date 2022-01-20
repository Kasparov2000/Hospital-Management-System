from db_model import *
from passlib.hash import pbkdf2_sha256

# A function to check if the username already exist
def check_username(username, profession):
    main = True
    while main:
        try:
            if profession != 'Admin':
                user = User.objects(user_name=username, profession=profession).first()


            else:
                user = User.objects(user_name=username).first()

            if user:
                return True, user
            else:
                return False, 0

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

# A function to hash the password
def hash_password(password):
    hashed_password = pbkdf2_sha256.hash(password)
    return hashed_password


def verify_password(password, username):
    main = True
    while main:
        try:
            hashed_password = User.objects(user_name=username).first().password
            status = pbkdf2_sha256.verify(password, hashed_password)
            if status:
                return True
            else:
                return False

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



