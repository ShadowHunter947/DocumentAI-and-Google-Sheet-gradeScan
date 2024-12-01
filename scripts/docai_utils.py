import os
from google.cloud import documentai_v1 as documentai

# Set up Document AI client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/USER/Downloads/Dataset/scripts/examscriptassessmentusingocr-3ccfe26ec844.json"
client = documentai.DocumentProcessorServiceClient()

# Document AI configurations
PROJECT_ID = "167088649918"  # Your Google Cloud Project ID
LOCATION = "us"  # Replace with your processor location
PROCESSOR_ID = "914bebc7c3cc118a"  # Your Form Parser Processor ID

def analyze_document(file_path):
    """
    Analyze a document using the Document AI Form Parser Processor.
    Args:
        file_path (str): Path to the local document file.
    Returns:
        dict: Extracted key-value pairs.
    """
    # Load the document content
    with open(file_path, "rb") as file:
        content = file.read()

    # Configure the Document AI request
    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
    document = {"content": content, "mime_type": "application/pdf" if file_path.endswith(".pdf") else "image/png"}
    request = {"name": name, "raw_document": document}

    # Process the document
    result = client.process_document(request=request)
    document = result.document

    # Extract key-value pairs
    extracted_data = {}
    for entity in document.entities:
        extracted_data[entity.type_] = entity.mention_text

    return extracted_data
