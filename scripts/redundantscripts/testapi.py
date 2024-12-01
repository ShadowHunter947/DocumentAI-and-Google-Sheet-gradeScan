from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

CREDENTIALS_FILE = r'C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json'
SPREADSHEET_ID = '1KKL7LYWuYlnM1FJW0Keqb_QjFGbh9-GW19YI4qVebWE'

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

try:
    # Attempt to read data from the spreadsheet
    result = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    print("Google Sheets API test successful!")
    print(result)
except Exception as e:
    print("Error accessing Google Sheets API:", e)
