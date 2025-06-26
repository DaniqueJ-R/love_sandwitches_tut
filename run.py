import gspread
from google.oauth2.service_account import Credentials

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
    Get sales figures from the user.
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
    Validates the data entered by the user to be 6 integers only. Raises ValueError if data is invalid.
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




data = get_sales_data()