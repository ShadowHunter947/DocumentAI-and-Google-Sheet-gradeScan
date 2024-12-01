from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

# Set up credentials and client
credentials = service_account.Credentials.from_service_account_file(
    r'C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json'
)
client = documentai.DocumentProcessorServiceClient(credentials=credentials)

def clean_value(value):
    """
    Cleans up extracted values by removing line breaks and extra spaces.
    """
    if value:
        # Remove line breaks and extra spaces
        return " ".join(value.split())
    return "Unknown Value"

def process_with_document_ai(image_path):
    """
    Process a document image using Google Document AI and extract key-value pairs.
    """
    # Read image content
    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    # Define the processor name (full resource path)
    name = "projects/167088649918/locations/us/processors/914bebc7c3cc118a"

    # Prepare the raw document for processing
    raw_document = documentai.RawDocument(content=image_content, mime_type="image/png")

    # Prepare the request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    try:
        # Process the document
        result = client.process_document(request=request)
        document = result.document

        # Extract key-value pairs from `document.pages`
        key_value_pairs = {}
        for page in document.pages:
            for form_field in page.form_fields:
                key = form_field.field_name.text_anchor.content.strip() if form_field.field_name.text_anchor.content else "Unknown Key"
                value = form_field.field_value.text_anchor.content.strip() if form_field.field_value.text_anchor.content else "Unknown Value"
                
                # Clean the value to fix line breaks or split numbers
                key_value_pairs[key] = clean_value(value)

        # Print extracted key-value pairs
        print("Extracted Key-Value Pairs:")
        for key, value in key_value_pairs.items():
            print(f"{key}: {value}")

        return key_value_pairs

    except Exception as e:
        print(f"Error processing document: {e}")
        return None

# Example usage
if __name__ == "__main__":
    image_path = r"C:\Users\USER\Downloads\Dataset\preprocessed_images\image9.png"
    extracted_data = process_with_document_ai(image_path)

    # Debugging: Output extracted data
    if extracted_data:
        print("\nFinal Extracted Data:")
        for key, value in extracted_data.items():
            print(f"{key}: {value}")
