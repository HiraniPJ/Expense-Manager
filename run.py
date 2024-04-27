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
 

""" Clears termnals for a clean display. """ 
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


""" Prints Introductory ASCII art for the application. """
def print_intro():
    clear_terminal()
    intro_art = text2art("Expense Manager") 
    print(intro_art)


""" Validates if the input value can be converted to the specified data type. """
def validate_input(input_value, data_type):
    try: 
        if data_type == 'int':
            value = int(input_value)
        elif data_type == 'float':   
            value = float(input_value) 
        return True, value
    except ValueError:
        return False, None    
    

""" Prompts the user to select a month. """
def get_month_selection():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
   
    print("Select a month:")
    for i, month in enumerate(months, start=1):
        print(f"{i}. {month}")
    while True:
        month_index = input("Enter the number of the month: ")   
        if month_index.isdigit() and 1 <+ int(month_index) <= 12:
            return months[int(month_index) -1]
        print("Invalid input. Please enter a valid number between 1 and 12.")


""" Allows the user to set a budget for a selected month. """
def set_monthly_budget():
    month = get_month_selection()
    while True:
        budget = input(f"Enter the budget for {month}:")
        valid, budget = validate_input(budget, 'float')     
        if valid: 
            return month, budget  
 

""" Updates the Google Sheet with the provided month and budget. """      
def update_budget_in_sheet(month, budget):    

    try:
        month_cell = expenses.find(month)
        expenses.update_cell(month_cell.row, 2, budget)    
    except gspread.exceptions.CellNotFound:
        expenses.append_row([month, budget])   


""" Prompts the user to select an expense category. """
def get_category_selection():
    categories = {
        1: "Rent",
        2: "Groceries",
        3: "Vehicle",
        4: "Cafe/Restaurant",
        5: "Online Shopping",
        6: "Other"
    }   
    print("Select a category:")
    for key, value in categories.items():
        print(f"{key}. {value}")
    while True:
        category_index = input("Enter the number of the category: ")
        if category_index.isdigit() and 1 <= int(category_index) <= len(categories):
            return categories[int(category_index)]
        print("invalid input. Please eneter a valid category number.")


""" Allows the user to log an expense for a given category. """
def log_expense(month, category):
    amount = input(f"Enter the amount spend on {category} in {month}: ")
    valid, amount_value = validate_input(amount, 'float')
    if valid:
        append_expense_to_sheet(month, category, amount)
   
""" Appends the expense data to Google Sheet under the specified month. """
def append_expense_to_sheet(month, category, amount):
    try:
        month_row = expenses.find(month).row
        category_col = expenses.find(category).col
        current_value = expenses.cell(month_row, category_col).value
        new_value = float(current_value) + amount if current_value else amount
        expenses.update_cell(month_row, category_col, new_value)
    except gspread.exceptions.CellNotFound:
        print(f"No data found for {month} or {category}, updating records. ")
        expenses.append_row([month, category, amount])


""" Prompts the user for confirmation. Returns True if confirmed. """
def confirm_action(prompt):
    response = input(prompt + " (y/n): ").lower()
    if response == 'y':
        return True
    elif response == 'n':
        return False
    else:
        print("Invalid repsonse. Please answer 'y' or 'n'.")


def main ():
    print_intro()
    month, budget = set_monthly_budget()
    update_budget_in_sheet(month, budget)
    if confirm_action("Would you like to log an expense? "):
        category = get_category_selection()
        log_expense(month, category)


if __name__=="__main__":
    main()