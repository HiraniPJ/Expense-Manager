import os
import gspread
import re
from google.oauth2.service_account import Credentials
from art import text2art
from prettytable import PrettyTable
from termcolor import colored


def clear_terminal():
    """Clears terminal for a clean display."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_intro():
    """Prints Introductory ASCII art for the application."""
    clear_terminal()
    intro_art = text2art("Expense")
    print(colored(intro_art, "cyan", attrs=["bold"]))


# Google Sheets Authentication
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


def validate_currency_input(amount):
    """Ensures the amount entered is a valid currency format."""
    currency_pattern = r"^£?\d+(\.\d{1,2})?$"
    return bool(re.match(currency_pattern, amount))


def get_month_selection():
    """Prompts the user to select a month."""
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    print(colored("\nSelect a month:", "white", attrs=["bold"]))
    for i, month in enumerate(months, start=1):
        print(colored(f"{i}. {month}", "yellow"))
    while True:
        try:
            month_index = int(input("Enter the month number (1-12): "))
            if 1 <= int(month_index) <= 12:
                return months[month_index - 1]
            else:
                print(colored("Invalid choice. Please enter a number between 1 and 12.", "red"))
        except ValueError:
            print(colored("Invalid input. Please enter a numeric value.", "red"))


def set_monthly_budget():
    """Allows the user to check the current budget and decide whether to update or add to it."""
    month = get_month_selection()
    month_cell = expenses.find(month, in_column=1)
    current_budget = float(expenses.cell(month_cell.row, 2).value or 0)
    print(f"💰 Current budget for {month}: £{current_budget}")

    while True:
        print(colored("\nOptions:", "grey", attrs=["bold"]))
        print("1. Update the budget (Replace old value)")
        print("2. Add to the budget")
        print("3. Keep current budget")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            new_budget = float(input(f"Enter new budget for {month}: £"))
            expenses.update_cell(month_cell.row, 2, new_budget)
            print(f"✅ Budget updated to £{new_budget} for {month}.")
            return month, new_budget

        elif choice == '2':
            add_amount = float(input(f"Enter amount to add to the budget: £"))
            new_budget = current_budget + add_amount
            expenses.update_cell(month_cell.row, 2, new_budget)
            print(f"✅ £{add_amount} added. New total budget: £{new_budget} for {month}.")
            return month, new_budget

        elif choice == '3':
            if current_budget == 0:
                print(colored("⚠️ Warning: Your budget is set to £0. Are you sure you want to continue?", "red"))
                confirm = input("Do you want to proceed without setting a budget? (y/n): ").strip().lower()
                if confirm == 'n':
                    continue
            print("Keeping the existing budget.")
            return month, current_budget

        else:
            print(colored("❌Invalid choice. Please enter 1, 2, or 3." "yellow"))


def update_budget_in_sheet(month, budget):
    """Updates the Google Sheet with the provided month and budget."""
    try:
        month = month.strip().capitalize()
        month_cell = expenses.find(month, in_column=1)
        current_budget = expenses.cell(month_cell.row, 2).value
        print(f"Current budget for {month}: £{current_budget}")
        confirm = input("Are you sure you want to update the budget? (y/n): ").lower()
        if confirm == 'y':
            expenses.update_cell(month_cell.row, 2, budget)
            print(f"Budget updated successfully for {month}.")
        else:
            print("Budget update cancelled.")
    except gspread.exceptions.CellNotFound:
        print(f"No existing budget found for {month}. You may need to add a budget first.")


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
    print(colored("\nSelect a category:", "white", attrs=["bold"]))
    for key, value in categories.items():
        print(colored(f"{key}. {value}", "blue"))
    while True:
        try:
            cat_choice = int(input("Enter the number of the category: "))
            if cat_choice in categories:
                return categories[cat_choice]
            else:
                print(colored("Invalid input. Please enter a valid category number.", "yellow"))
        except ValueError:
            print(colored("Invalid input. Please enter a numeric value.", "yellow"))


def log_expense(month):
    """Allows the user to log an expense for a given category."""
    while True:
        category = get_category_selection()
        while True:
            amount = input(f"Enter the amount spend on {category} in {month}: £")
            if validate_currency_input(amount):
                append_expense_to_sheet(month, category, float(amount))
                print(f"Expense of £{amount} logged for {category} in {month}.")
                break
            print(colored("Invalid amount. Please enter a valid number.", "yellow"))

        if not confirm_action("Would you like to log another expense? "):
            break


def append_expense_to_sheet(month, category, amount):
    """Appends the expense data to Google Sheet under the specified month."""
    try:
        month_row = expenses.find(month).row
        category_cell = expenses.find(category, in_row=1)

        if category_cell:
            category_col = category_cell.col
            current_value = expenses.cell(month_row, category_col).value
            new_value = float(current_value or 0) + amount
            expenses.update_cell(month_row, category_col, new_value)
        else:
            print(f"Category '{category}' not found. Creating a new column.")
            expenses.update_cell(1, expenses.col_count + 1, category)
            expenses.update_cell(month_row, expenses.col_count, amount)
    except gspread.exceptions.CellNotFound:
        print(f"No data found for {month} or {category}, updating records.")
        expenses.append_row([month, category, amount])


def generate_expense_report(month):
    """Generates an expense report for the given month."""
    expenses_summary = {}
    total_expenses = 0
    try:
        budget_row = expenses.find(month).row
        budget = float(expenses.cell(budget_row, 2).value or 0)

        for col in range(3, expenses.col_count + 1):
            category = expenses.cell(1, col).value
            amount = expenses.cell(budget_row, col).value
            if amount:
                amount = float(amount)
                expenses_summary[category] = amount
                total_expenses += amount

        remaining_budget = budget - total_expenses

        print(colored(f"\n📊 Expense Report for {month}:", "cyan", attrs=["bold"]))
        print(colored(f"💰 Total Budget: £{budget}", "green"))
        print(colored(f"💸 Total Expenses: £{total_expenses}", "yellow"))
        print(colored(f"💵 Remaining Budget: £{remaining_budget}", "green" if remaining_budget >= 0 else "red"))

        if remaining_budget < 0:
            print(colored("⚠️ Warning: Your expenses have exceeded your budget!", "red", attrs=["bold"]))
        else:
            print(colored("✅ Well done! You are under your budget.", "green", attrs=["bold"]))

        return expenses_summary, remaining_budget

    except gspread.exceptions.CellNotFound:
        print(colored(f"No Budget data found for {month}.", "red"))
    return {}, 0


def print_table(data, title):
    """Prints data in a pretty table format."""
    table = PrettyTable()
    table.title = title
    table.field_names = ["📌 Category", "💰 (£) Amount"]
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

    while confirm_action("Would you like to log an expense? "):
        log_expense(month)

    if confirm_action("Would you like to generate an expense report? "):
        expenses_summary, remaining_budget = generate_expense_report(month)
        report_title = f"Expense Report for {month}"
        print_table(expenses_summary, report_title)

    print(colored("👋 Exiting program. Have a great day!", "cyan", attrs=["bold"]))


if __name__ == "__main__":
    main()
