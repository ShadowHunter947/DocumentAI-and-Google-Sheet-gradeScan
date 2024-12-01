import cv2
import numpy as np
from google.cloud import vision
import io

# Initialize the Google Cloud Vision API client
def initialize_google_vision_client(credentials_path):
    """
    Initialize the Google Cloud Vision API client.

    Args:
        credentials_path (str): Path to the Google Cloud credentials JSON file.

    Returns:
        vision.ImageAnnotatorClient: Google Vision API client instance.
    """
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return vision.ImageAnnotatorClient()


def preprocess_image(image_path):
    """
    Preprocess the image for OCR (convert to grayscale, binarize, and denoise).

    Args:
        image_path (str): Path to the input image.

    Returns:
        numpy.ndarray: Preprocessed image.
    """
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur for denoising
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Binarize the image using Otsu's thresholding
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def perform_ocr_on_image(image_path, client):
    """
    Perform OCR on an entire image using Google Vision API.

    Args:
        image_path (str): Path to the input image.
        client (vision.ImageAnnotatorClient): Google Vision API client.

    Returns:
        str: Extracted text from the image.
    """
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform OCR
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text if response.full_text_annotation else ""
    return text.strip()


def perform_ocr_on_roi(image, roi, client):
    """
    Perform OCR on a specific ROI (Region of Interest) in an image.

    Args:
        image (numpy.ndarray): Input image.
        roi (tuple): Region of interest (xmin, ymin, xmax, ymax).
        client (vision.ImageAnnotatorClient): Google Vision API client.

    Returns:
        str: Extracted text from the ROI.
    """
    xmin, ymin, xmax, ymax = roi
    cropped_roi = image[ymin:ymax, xmin:xmax]

    # Preprocess the cropped region for better OCR
    gray = cv2.cvtColor(cropped_roi, cv2.COLOR_BGR2GRAY)
    _, binary_roi = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert the cropped region to bytes for OCR
    _, buffer = cv2.imencode('.png', binary_roi)
    roi_bytes = buffer.tobytes()

    # Perform OCR on the cropped ROI
    vision_image = vision.Image(content=roi_bytes)
    response = client.document_text_detection(image=vision_image)
    text = response.full_text_annotation.text if response.full_text_annotation else ""

    return text.strip()


def annotate_image_with_text(image, rois, texts):
    """
    Annotate an image with the extracted text for each ROI.

    Args:
        image (numpy.ndarray): Input image.
        rois (dict): Dictionary of field names and their bounding boxes.
        texts (dict): Dictionary of field names and their extracted texts.

    Returns:
        numpy.ndarray: Annotated image.
    """
    annotated_image = image.copy()
    for field, (xmin, ymin, xmax, ymax) in rois.items():
        text = texts.get(field, "")
        cv2.rectangle(annotated_image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(
            annotated_image, text, (xmin, ymin - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1
        )
    return annotated_image
