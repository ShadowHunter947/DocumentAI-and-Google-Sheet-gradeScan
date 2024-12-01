import cv2
import os
import xml.etree.ElementTree as ET
from pytesseract import pytesseract, Output

# Configure Tesseract OCR
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """
    Preprocess an image by converting it to grayscale, applying Gaussian blur, and binary thresholding.
    """
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return image, binary_image

def parse_xml_annotations(xml_path):
    """
    Parse an XML annotation file and extract the bounding boxes for labeled ROIs.
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

def detect_rois(image, binary_image, expected_labels):
    """
    Detect regions of interest (ROIs) using contours and match them with expected labels using OCR.
    """
    detected_labels = {}
    annotated_image = image.copy()

    # Perform OCR to detect labels
    ocr_data = pytesseract.image_to_data(image, output_type=Output.DICT)
    for i in range(len(ocr_data["text"])):
        text = ocr_data["text"][i].strip()
        if text in expected_labels:  # Match expected labels
            x, y, w, h = ocr_data["left"][i], ocr_data["top"][i], ocr_data["width"][i], ocr_data["height"][i]
            detected_labels[text] = (x, y, w, h)  # Save label position

    # Detect contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from bottom-up, left-to-right
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    bounding_boxes.sort(key=lambda box: (-box[1], box[0]))  # Sort by y (descending), then x (ascending)

    rois = []
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        if w > 50 and h > 50:  # Filter out small boxes
            roi = image[y:y + h, x:x + w]
            roi_name = None

            # Match ROI with the nearest detected label
            for label, (lx, ly, lw, lh) in detected_labels.items():
                if abs(y - ly) < 50 and abs(x - lx) < 200:  # Adjust thresholds as needed
                    roi_name = label
                    break

            # Save ROI with the matched name or a generic name
            roi_data = {
                "name": roi_name if roi_name else f"roi_{i}",
                "bbox": (x, y, w, h),
                "roi": roi
            }
            rois.append(roi_data)

            # Annotate image for debugging
            cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(annotated_image, roi_data["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return rois, annotated_image

def save_rois(output_dir, rois):
    """
    Save ROIs to the specified directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    for roi_data in rois:
        roi_path = os.path.join(output_dir, f"{roi_data['name']}.png")
        cv2.imwrite(roi_path, roi_data["roi"])
    print(f"ROIs saved to {output_dir}")

def save_annotated_image(output_path, annotated_image):
    """
    Save the annotated image for debugging purposes.
    """
    cv2.imwrite(output_path, annotated_image)
    print(f"Annotated image saved to {output_path}")
