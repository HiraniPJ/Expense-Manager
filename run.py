import os
import gspread
from google.oauth2.service_account import Credentials
from art import text2art

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive
    ]

def autheticaticate_google_docs():
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Expense-Manager')
expenses = SHEET.worksheet('expenses')
 
def clear_terminal():
    """ Clears termnals for a clean display. """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_intro():
    """ Prints Introductory ASCII art for the application. """
    clear_terminal()
    intro_art = text2art("Expense Manager") 
    print(intro_art)

def validate_input(input_value, data_type):
    """ Validates if the input value can be converted to the specified data type. """
    try: 
        if data_type == 'int':
            value = int(input_value)
        elif data_type == 'float':   
            value = float(input_value) 
        return True, value
    except ValueError:
        return False, None    


def main ():
    print_intro()


if __name__=="__main__":
    main()