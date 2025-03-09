import os
import gspread
from google.oauth2.service_account import Credentials
from art import text2art
from prettytable import PrettyTable
from termcolor import colored

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
    """Clears terminal for a clean display."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_intro():
    """Prints Introductory ASCII art for the application."""
    clear_terminal()
    intro_art = text2art("Expense Manager")
    print(intro_art)


def validate_input(input_value, data_type):
    """Validates input based on the type (int for months, float for amounts)"""
    try:
        if data_type == 'int':
            value = int(input_value)
        elif data_type == 'float':
            value = float(input_value)
        return True, value
    except ValueError:
        return False, None


def get_month_selection():
    """Prompts the user to select a month."""
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    while True:
        try:
            month_index = int(input("Enter the month number (1-12): "))
            if 1 <= int(month_index) <= 12:
                return months[month_index - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            

def set_monthly_budget():
    """Allows the user to set a budget for a selected month."""
    month = get_month_selection()
    while True:
        budget = input(f"Enter the budget for {month}:")
        valid, budget = validate_input(budget, 'float')
        if valid:
            update_budget_in_sheet(month, budget)
            return month, budget
            print("Invalid amount. Please enter a valid number.")


def update_budget_in_sheet(month, budget):
    """Updates the Google Sheet with the provided month and budget."""
    try:
        month_cell = expenses.find(month)
        expenses.update_cell(month_cell.row, 2, budget)
    except gspread.exceptions.CellNotFound:
        expenses.append_row([month, budget])


def get_category_selection():
    """Prompts the user to select an expense category."""
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
        cat_list = input("Enter the number of the category: ")
        if cat_list.isdigit() and 1 <= int(cat_list) <= len(categories):
            return categories[int(cat_list)]
        print("Invalid input. Please enter a valid category number.")


def log_expense(month, category):
    """Allows the user to log an expense for a given category."""
    amount = input(f"Enter the amount spend on {category} in {month}: ")
    valid, amount_value = validate_input(amount, 'float')
    if valid:
        append_expense_to_sheet(month, category, amount_value)


def append_expense_to_sheet(month, category, amount):
    """Appends the expense data to Google Sheet under the specified month."""
    try:
        month_row = expenses.find(month).row
        category_col = expenses.find(category, in_row=1).col
        current_value = expenses.cell(month_row, category_col).value
        new_value = float(current_value or 0) + amount
        expenses.update_cell(month_row, category_col, new_value)
    except gspread.exceptions.CellNotFound:
        print(f"No data found for {month} or {category}, updating records.")
        expenses.append_row([month] + [""] * (category_col - 2) + [amount])


def generate_expense_report(month):
    """Generates an expense report for the given month."""
    expenses_summary = {}
    total_expenses = 0
    try:
        budget_row = expenses.find(month).row
        budget = float(expenses.cell(budget_row, 2).value)
        for col in range(3, 10):
            category_row = expenses.find(month).row
            category = expenses.cell(1, col).value
            amount = expenses.cell(category_row, col).value
            if amount:
                amount = float(amount)
                expenses_summary[category] = amount
                total_expenses += amount
        remaining_budget = budget - total_expenses
        print(f"\nExpense Report for {month}:")
        for category, amount in expenses_summary.items():
            print(f"{category}: £{amount}")
            print(f"Total Expenses: £{total_expenses}")
            print(f"Remaining Budget: £{remaining_budget}")
    except gspread.exceptions.CellNotFound:
        print(f"No Budget data found for {month}.")
    return expenses_summary, remaining_budget


def print_table(data, title):
    """Prints data in a pretty table format."""
    table = PrettyTable()
    table.title = title
    table.field_names = ["Category", "(£) Amount"]
    for key, value in data.items():
        table.add_row([key, f"£{value}"])
    print(table)


def confirm_action(prompt):
    """Prompts the user for confirmation. Returns True if confirmed."""
    response = input(prompt + " (y/n): ").lower()
    if response == 'y':
        return True
    elif response == 'n':
        return False
    else:
        print("Invalid response. Please answer 'y' or 'n.'")


def main():
    print_intro()
    month, budget = set_monthly_budget()
    update_budget_in_sheet(month, budget)
    if confirm_action("Would you like to log an expense? "):
        category = get_category_selection()
        log_expense(month, category)
    if confirm_action("Would you like to generate an expense report? "):
        expenses_summary, remaining_budget = generate_expense_report(month)
        report_title = f"Expense Report for {month}"
        print_table(expenses_summary, report_title)


if __name__ == "__main__":
    main()
