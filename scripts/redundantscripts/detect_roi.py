import cv2
import os
import pytesseract  # Install pytesseract: pip install pytesseract
from pytesseract import Output

# Directory paths
image_dir = "C:/Users/USER/Downloads/Dataset/images/"  # Input exam script images
output_base_dir = "C:/Users/USER/Downloads/Dataset/rois/"  # Base directory for ROI folders

# Tesseract OCR configuration (adjust the path to Tesseract executable if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Predefined ROI labels to match
expected_labels = ["Name", "ID", "Course", "Section", "Semester", "Date", "Faculty", 
                   "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "total", 
                   "student_signature", "faculty_signature"]

# Process each image in the input directory
for image_file in os.listdir(image_dir):
    if image_file.endswith(".png"):  # Process only PNG files
        image_path = os.path.join(image_dir, image_file)
        image_name = os.path.splitext(image_file)[0]

        # Create a directory for the ROIs of this image
        output_dir = os.path.join(output_base_dir, image_name)
        os.makedirs(output_dir, exist_ok=True)

        # Load the image
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Preprocess the image
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Perform OCR to detect labels
        ocr_data = pytesseract.image_to_data(image, output_type=Output.DICT)
        detected_labels = {}
        for i in range(len(ocr_data["text"])):
            text = ocr_data["text"][i].strip()
            if text in expected_labels:  # Match expected labels
                x, y, w, h = ocr_data["left"][i], ocr_data["top"][i], ocr_data["width"][i], ocr_data["height"][i]
                detected_labels[text] = (x, y, w, h)  # Save label position

        # Find contours for ROI detection
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours from bottom-up, left-to-right
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        bounding_boxes.sort(key=lambda box: (-box[1], box[0]))  # Sort by y (descending), then x (ascending)

        # Annotate and save ROIs
        annotated_image = image.copy()
        for i, (x, y, w, h) in enumerate(bounding_boxes):
            if w > 50 and h > 50:  # Filter out small boxes
                roi = gray_image[y:y + h, x:x + w]

                # Match ROI with the nearest detected label
                roi_name = None
                for label, (lx, ly, lw, lh) in detected_labels.items():
                    if abs(y - ly) < 50 and abs(x - lx) < 200:  # Adjust thresholds as needed
                        roi_name = label
                        break

                # Save ROI with the matched name or a generic name
                if roi_name:
                    roi_path = os.path.join(output_dir, f"{roi_name}.png")
                else:
                    roi_name = f"roi_{i}"  # Assign generic name if no label matches
                    roi_path = os.path.join(output_dir, f"{roi_name}.png")

                cv2.imwrite(roi_path, roi)

                # Annotate the image for debugging
                cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(annotated_image, roi_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Save the annotated image
        annotated_image_path = os.path.join(output_dir, f"annotated_{image_name}.png")
        cv2.imwrite(annotated_image_path, annotated_image)
        print(f"Annotated image saved for {image_file}: {annotated_image_path}")

        print(f"ROIs for {image_file} saved to {output_dir}")

        # Optional: Visualize the annotated image for debugging
        cv2.imshow("Annotated Image", annotated_image)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()
