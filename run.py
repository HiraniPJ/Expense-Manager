import os
import gspread
from google.oauth2.service_account import Credentials
from art import text2art

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


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
    
def get_month_selection():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
   
    print("Select a month:")
    for i, month in enumerate(months, start=1):
        print(f"{i}. {month}")
    while True:
        month_index = input("nter the number of the month: ")   
        if month_index.isdigit() and 1 <+ int(month_index) <= 12:
            return months[int(month_index) -1]
        print("Invalid input. Please enter a valid number between 1 and 12.")

def set_monthly_budget():
    month = get_month_selection()
    while True:
        budget = input(f"nter the budget for {month}:")
        valid, budget_value = validate_input(budget, 'float')     
        if valid: return month, budget_value    
    

def main ():
    print_intro()


if __name__=="__main__":
    main()