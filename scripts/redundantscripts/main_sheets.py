from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openpyxl

# Credentials
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json'
)

# Document AI Client
client = documentai.DocumentProcessorServiceClient(credentials=credentials)

# Google Sheets Client
sheets_service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1KKL7LYWuYlnM1FJW0Keqb_QjFGbh9-GW19YI4qVebWE'  # Replace with your spreadsheet ID

def process_document(image_path):
    """Processes a document image using Document AI and populates a Google Sheet."""

    # 1. Load the image
    with open(image_path, 'rb') as image_file:
        image_content = image_file.read()

    # 2. Create a raw document request for Document AI
    name = 'projects/examscriptassessmentusingocr/locations/us/processors/914bebc7c3cc118a'
    request = {
        "name": name,
        "raw_document": {"content": image_content, "mime_type": "image/png"},
    }

    # 3. Call Document AI API
    try:
        response = client.process_document(request=request)
        document = response.document

        # **Print the Document AI Response**
        print("Document AI Response:")
        print(document)  # This will print the entire response structure

        try:
        # Process data extraction logic here
         # Extract relevant data
            extracted_data = {}
            for entity in document.entities:
             extracted_data[entity.mention_text] = entity.confidence
        except KeyError as e:
            print(f"Missing key in Document AI response: {e}")
        except Exception as e:
            print(f"Unexpected error during extraction: {e}")
        # Print extracted data for debugging
        print(f"Extracted Data: {extracted_data}")

        # 4. Populate Google Sheet
        try:
            # Prepare data for insertion
            values = [[key, value] for key, value in extracted_data.items()]
            body = {"values": values}

            # Insert data into the sheet
            sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A1',
                valueInputOption='RAW',
                body=body
            ).execute()

            print(f"Data successfully inserted into Google Sheet: {spreadsheet_id}")

        except HttpError as error:
            print(f"Error inserting data into Google Sheet: {error}")

    except Exception as e:
        print(f"Error during Document AI processing: {e}")

       

# Example usage
image_path = r'C:\Users\USER\Downloads\Dataset\preprocessed_images\image9.png'
process_document(image_path)


