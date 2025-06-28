import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales figures from the user. will loop until valid data is entered. 
    Valid date is 6 integers separated by commas.
    Returns a list of integers representing the sales data.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should contain 6 numbers, seperated by commas.")
        print("Example: 23,83,13,24,53,3,\n")

        data_string = input("Enter data here: ")

        sales_data = data_string.split(",")

        if validate_data(sales_data):
            print("Data is Valid!")
            break
    
    return sales_data

def validate_data(values):
    """
    Validates the data entered by the user to be 6 integers only. 
    Raises ValueError if data is invalid.
    """
    try:
        [int(values) for values in values]
        if len(values) != 6:
            raise ValueError(
                f"You provided {len(values)}, but 6 values are needed"
            )
    except ValueError as e:
        print(f"Invalid date: {e}, please check your date and try again.")
        return False
    
    return True

#Refactored the update_sales_worksheet and update_surplus_worksheet functions into one function called update_worksheet
# The original functions were commented out to avoid confusion, but can be uncommented if needed.

# def update_sales_worksheet(data):
#     """
#     Updates the sales worksheet with the data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")
        
# def update_surplus_worksheet(data):
#     """
#     Updates the surplus worksheet with the data from calculate_surplus.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet_name):
    """
    Recives a list of integers to be added to a worksheet.
    Updates the relevant worksheet with the relevant lists.
    """
    print(f"Updating {worksheet_name} worksheets...\n")
    worksheet_to_update = SHEET.worksheet(worksheet_name)
    worksheet_to_update.append_row(data)
    print(f"{worksheet_name} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Calculate the surplus data based on the sales data fom the sheet. 
    Surplus is the difference between the stock and sales.
    e.g. stock (8) - sales (10) = surplus (-2)
    """
    print("Calculating surplus data...\n")
    stock_data = SHEET.worksheet("stock").get_all_values()
    # pprint(stock_data)
    stock_row = stock_data[-1]

    surplus_data = []
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def main():
    """"
    Runs all main funcitons
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] # convert sales data sting to integers from get_sales_data() 
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")



print("Welcome to Love Sandwitches Data Automation!")
main()