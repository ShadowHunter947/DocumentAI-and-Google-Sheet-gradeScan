from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SHEETS_CREDENTIALS = r"C:\Users\USER\Downloads\sheets_credentials.json"

credentials = Credentials.from_service_account_file(SHEETS_CREDENTIALS)
service = build("sheets", "v4", credentials=credentials)

print("Google Sheets API authentication successful!")
