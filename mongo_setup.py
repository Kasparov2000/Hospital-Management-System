import mongoengine
from terminal_effects import *


# Connecting to the mongo database
def global_init(test=False):
    clear_terminal()
    connected = False

    # They are two databases, one for testing and one for production
    database_name = "HMS" if not test else "HMStest"
    URI = f"mongodb+srv://hmassignment:assignment2021@cluster0.wigt5.mongodb.net/{database_name}?retryWrites=true&w=majority"

    MONGODB_SETTINGS = dict(
        host=URI
    )
    while not connected:
        try:
            mongoengine.register_connection(alias="HMS", name=database_name, **MONGODB_SETTINGS)
            connected = True

        except Exception:
            success = False
            while not success:
                try:
                    option = int(input('Cannot connect to the Database. Make sure you are connected to internet.'
                                       '\n1.Connect Again 2. Exit\nOption: '))
                    if option == 1:
                        success = True
                    elif option == 2:
                        return
                except ValueError:
                    print('Invalid Input')

