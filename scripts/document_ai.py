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
    return " ".join(value.split()) if value else "Unknown Value"

def process_with_document_ai(image_path):
    """
    Process a document image using Google Document AI and extract key-value pairs.
    """
    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    processor_name = "projects/167088649918/locations/us/processors/914bebc7c3cc118a"
    raw_document = documentai.RawDocument(content=image_content, mime_type="image/png")
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    try:
        # Process the document
        response = client.process_document(request=request)
        document = response.document

        # Extract key-value pairs
        key_value_pairs = {}
        for page in document.pages:
            for form_field in page.form_fields:
                key = form_field.field_name.text_anchor.content.strip() if form_field.field_name.text_anchor.content else "Unknown Key"
                value = form_field.field_value.text_anchor.content.strip() if form_field.field_value.text_anchor.content else "Unknown Value"
                key_value_pairs[key] = clean_value(value)

        return key_value_pairs

    except Exception as e:
        print(f"Error processing document: {e}")
        return None
