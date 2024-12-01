from document_ai import process_with_document_ai
from google_sheets import update_google_sheet, prepare_data_for_sheet

def main():
    # Path to the document image
    image_path = r"C:\Users\USER\Downloads\Dataset\preprocessed_images\image57.png"

    # Process document with Document AI
    extracted_data = process_with_document_ai(image_path)

    # Ensure extracted data is valid
    if extracted_data:
        print("\nFinal Extracted Data:")
        for key, value in extracted_data.items():
            print(f"{key}: {value}")

        # Prepare headers and row data for Google Sheets
        headers, values = prepare_data_for_sheet(extracted_data)

        # Update Google Sheets with the headers and row
        update_google_sheet(headers, values)

if __name__ == "__main__":
    main()
