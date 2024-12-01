import os
from google.cloud import vision
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

# Google Cloud Vision credentials
CREDENTIALS_PATH = r"C:/Users/USER/Downloads/examscriptassessmentusingocr-6d3c18345e34.json" # Update this
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
vision_client = vision.ImageAnnotatorClient(credentials=credentials)

# Google Sheets credentials
SHEETS_CREDENTIALS_PATH = r"C:/path/to/your/google-sheets-credentials.json"  # Update this
SPREADSHEET_ID = "your-google-sheet-id"  # Replace with your Google Sheet ID
RANGE_NAME = "Sheet1!A1"  # Specify the starting cell in the sheet

# Configure Google Sheets API
sheets_service = build('sheets', 'v4', credentials=service_account.Credentials.from_service_account_file(SHEETS_CREDENTIALS_PATH))

# Paths
roi_base_dir = "C:/Users/USER/Downloads/Dataset/rois/"
image_ids = range(10, 20)  # Images 10 to 19

# Columns for the Google Sheet
columns = ["Image ID", "Name", "ID", "Date", "Course", "Section", "Semester", "Faculty"]

# Helper: Perform OCR on an image
def detect_handwritten_text(roi_path):
    with open(roi_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.document_text_detection(image=image)
    if response.text_annotations:
        return response.text_annotations[0].description.strip()  # Return the most relevant text
    return ""  # Return empty string if no text is found

# Helper: Save data to Google Sheet
def save_to_google_sheet(data, columns):
    df = pd.DataFrame(data, columns=columns)
    values = [columns] + df.values.tolist()  # Add header row
    body = {"values": values}
    sheets_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

# Main processing
all_data = []
for image_id in image_ids:
    roi_dir = os.path.join(roi_base_dir, f"image{image_id}")
    row_data = [f"image{image_id}"]  # Initialize row with Image ID
    
    if not os.path.exists(roi_dir):
        print(f"ROI directory for image{image_id} not found.")
        continue

    # List of fields to process
    fields = ["name", "id", "date", "course", "section", "semester", "faculty"]
    for field in fields:
        roi_path = os.path.join(roi_dir, f"{field}.png")
        if os.path.exists(roi_path):
            text = detect_handwritten_text(roi_path)
            row_data.append(text)
        else:
            row_data.append("")  # Append empty string if ROI is missing

    all_data.append(row_data)

# Save to Google Sheet
save_to_google_sheet(all_data, columns)
print("Data saved to Google Sheet successfully.")
