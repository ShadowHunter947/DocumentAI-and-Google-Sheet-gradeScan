from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import openpyxl

# Set up credentials and client
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json'
)
sheets_service = build('sheets', 'v4', credentials=credentials)

# Google Sheets Configuration
SPREADSHEET_ID = '1KKL7LYWuYlnM1FJW0Keqb_QjFGbh9-GW19YI4qVebWE'

def prepare_data_for_sheet(data):
    """
    Prepare data to match the format of Google Sheets:
    - Headers in the first row.
    - Values in subsequent rows.
    """
    # Extract headers (keys) and values
    headers = list(data.keys())
    values = [data[key] for key in headers]
    return headers, values


def update_google_sheet(headers, values):
    """
    Update Google Sheets with headers (if necessary) and append row data.
    """
    try:
        # Check if headers already exist in the sheet
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Sheet1!A1:Z1"  # Check the first row
        ).execute()
        existing_headers = result.get("values", [[]])[0]

        if not existing_headers:
            # Write headers if the sheet is empty
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f"Sheet1!A1",
                valueInputOption="RAW",
                body={"values": [headers]}
            ).execute()

        # Append the new row
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Sheet1!A2",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [values]}
        ).execute()

        print(f"Data successfully inserted into Google Sheet: {SPREADSHEET_ID}")

    except HttpError as error:
        print(f"Error updating Google Sheet: {error}")
