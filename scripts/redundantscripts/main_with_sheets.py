import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from google.cloud import documentai_v1beta3 as documentai
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from scripts.docai_utils import analyze_document
import sys

# Google Document AI setup
PROJECT_ID = "167088649918"
LOCATION = "us"
PROCESSOR_ID = "914bebc7c3cc118a"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json"

# Google Sheets setup
SHEETS_CREDENTIALS = r"C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SHEETS_CREDENTIALS

SPREADSHEET_ID = "1KKL7LYWuYlnM1FJW0Keqb_QjFGbh9-GW19YI4qVebWE"
SHEET_NAME = "Extracted Data Records Sheet"

# Local Excel fallback
OUTPUT_FILE = r"C:\Users\USER\Downloads\Dataset\exam_script_data.xlsx"

# Initialize Google Sheets API
credentials = Credentials.from_service_account_file(SHEETS_CREDENTIALS)
service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

# Expected Columns
columns = [
    "Image Name", "Quiz", "Midterm 1", "Midterm 2", "Final", "Name", "ID", "Course",
    "Section", "Semester", "Date", "Faculty", "Student Signature"
]

# Initialize or load existing DataFrame for local fallback
if os.path.exists(OUTPUT_FILE):
    df = pd.read_excel(OUTPUT_FILE)
else:
    df = pd.DataFrame(columns=columns)


RANGE = 'Extracted Data Records Sheet'  # Ensure this matches the exact sheet name

def append_to_google_sheet(extracted_data_list):
    """
    Append a list of extracted data dictionaries to Google Sheets.
    """
    for extracted_data in extracted_data_list:
        # Ensure extracted_data is a dictionary
        if isinstance(extracted_data, dict):
            data = [extracted_data.get(key, "") for key in [
                "Quiz", "Midterm 1", "Midterm 2", "Final", "Name", "ID", 
                "Course", "Section", "Semester", "Date", "Faculty", "Student Signature"
            ]]
            body = {"values": [data]}
            try:
                sheet.values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range=RANGE,
                    valueInputOption="USER_ENTERED",
                    body=body,
                ).execute()
                print(f"Data successfully appended to Google Sheet: {data}")
            except Exception as e:
                print(f"Failed to append to Google Sheets: {e}")
        else:
            print("Error: Extracted data is not a dictionary.")


def process_with_document_ai(file_path):
    """
    Process a .png file using Google Document AI and extract form fields.
    """
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as f:
        content = f.read()

    name = f"projects/167088649918/locations/us/processors/914bebc7c3cc118a"
    request = {
        "name": name,
        "raw_document": {"content": content, "mime_type": "image/png"},
    }
    response = client.process_document(request=request)
    document = response.document

    extracted_data = {}
    for page in document.pages:
        for field in page.form_fields:
            try:
                field_name = "".join(
                    [segment.text for segment in field.field_name.text_anchor.text_segments]
                ).strip()
                field_value = "".join(
                    [segment.text for segment in field.field_value.text_anchor.text_segments]
                ).strip()
                extracted_data[field_name] = field_value
            except AttributeError:
                continue

    return extracted_data

    print(f"Extracted Data Type: {type(extracted_data)}")
    print(f"Extracted Data: {extracted_data}")


def process_file(file_path):
    """
    Process a single .png file and map extracted data to expected columns.
    """
    try:
        extracted_data = process_with_document_ai(file_path)
        row_data = {
            "Image Name": os.path.basename(file_path),
            "Quiz": extracted_data.get("Quiz", ""),
            "Midterm 1": extracted_data.get("Midterm 1", ""),
            "Midterm 2": extracted_data.get("Midterm 2", ""),
            "Final": extracted_data.get("Final", ""),
            "Name": extracted_data.get("Name", ""),
            "ID": extracted_data.get("ID", ""),
            "Course": extracted_data.get("Course", ""),
            "Section": extracted_data.get("Section", ""),
            "Semester": extracted_data.get("Semester", ""),
            "Date": extracted_data.get("Date", ""),
            "Faculty": extracted_data.get("Faculty", ""),
            "Student Signature": extracted_data.get("Student Signature", ""),
        }
        return row_data
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    """
    Main function to process images and save extracted data.
    """
    input_dir = r"C:\Users\USER\Downloads\Dataset\preprocessed_images"

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".png"):  # Only process PNG files
            file_path = os.path.join(input_dir, file_name)
            print(f"Processing {file_name}...")
            row_data = process_file(file_path)

            if row_data:
                # Append to Google Sheets
                try:
                    row = [row_data.get(col, "") for col in columns]
                    append_to_google_sheet(row)
                except Exception as e:
                    print(f"Failed to append to Google Sheets: {e}")

                # Append locally as a fallback
                df.loc[len(df)] = row_data

    # Save DataFrame to Excel
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
