import os
import cv2
import pandas as pd
import xml.etree.ElementTree as ET
from google.cloud import vision
import io

# Set up Google Cloud Vision API client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/USER/Downloads/examscriptassessmentusingocr-6d3c18345e34.json"
client = vision.ImageAnnotatorClient()

# File paths
output_excel = "C:/Users/USER/Downloads/Dataset/exam_script_data.xlsx"
image_dir = "C:/Users/USER/Downloads/Dataset/preprocessed_images"
xml_dir = "C:/Users/USER/Downloads/Dataset/images"

# Load the existing Excel file or create a new DataFrame
if os.path.exists(output_excel):
    df = pd.read_excel(output_excel)
else:
    columns = [
        "Image Name", "Name", "ID", "Course", "Section", "Semester", "Date", "Faculty",
        "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Total",
        "Student Signature", "Faculty Signature"
    ]
    df = pd.DataFrame(columns=columns)

def parse_xml(xml_path):
    """
    Parse the XML file and extract the bounding box for each field.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    rois = {}

    for obj in root.findall('object'):
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        rois[name] = (xmin, ymin, xmax, ymax)

    return rois

def google_ocr_text_on_roi(image, roi):
    """
    Perform OCR on a specific region of interest.
    """
    # Crop the region from the image
    xmin, ymin, xmax, ymax = roi
    cropped_image = image[ymin:ymax, xmin:xmax]

    # Preprocess the cropped region
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    _, binary_roi = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Convert the cropped region to bytes for OCR
    _, buffer = cv2.imencode('.png', binary_roi)
    roi_bytes = buffer.tobytes()

    # Perform OCR on the cropped ROI
    vision_image = vision.Image(content=roi_bytes)
    response = client.document_text_detection(image=vision_image)
    text = response.full_text_annotation.text if response.full_text_annotation else ""

    return text.strip()

# List of images and corresponding XML annotations to process
image_files = ["image10.png", "image11.png", "image12.png", "image13.png"]

for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    xml_path = os.path.join(xml_dir, f"{os.path.splitext(image_file)[0]}.xml")
    
    # Load image and XML annotation
    image = cv2.imread(image_path)
    rois = parse_xml(xml_path)
    extracted_data = {"Image Name": image_file}

    # Run OCR on each ROI defined in the XML
    for field, roi in rois.items():
        text = google_ocr_text_on_roi(image, roi)
        extracted_data[field] = text
    
    # Append to DataFrame
    df = pd.concat([df, pd.DataFrame([extracted_data])], ignore_index=True)

# Save the DataFrame back to Excel
df.to_excel(output_excel, index=False)
print(f"Data saved to {output_excel}")
