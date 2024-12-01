from google.cloud import vision
import io
import os
import pandas as pd
import re

# Set up Google Cloud Vision API client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\Users\USER\Downloads\Dataset\scripts\examscriptassessmentusingocr-3ccfe26ec844.json"
client = vision.ImageAnnotatorClient()

# File paths
output_excel = "C:/Users/USER/Downloads/Dataset/exam_script_data.xlsx"

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

def google_ocr_text(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform OCR
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text if response.full_text_annotation else ""
    return text.strip()

def parse_text(text):
    data = {
        "Name": "", "ID": "", "Course": "", "Section": "", "Semester": "",
        "Date": "", "Faculty": "", "Q1": "", "Q2": "", "Q3": "", "Q4": "",
        "Q5": "", "Q6": "", "Q7": "", "Q8": "", "Q9": "", "Q10": "", "Total": "",
        "Student Signature": "", "Faculty Signature": ""
    }
    
    data["Name"] = re.search(r"Name:\s*(.*)", text).group(1).strip() if re.search(r"Name:\s*(.*)", text) else ""
    data["ID"] = re.search(r"ID:\s*([\d\s]+)", text).group(1).strip() if re.search(r"ID:\s*([\d\s]+)", text) else ""
    data["Course"] = re.search(r"Course:\s*(.*?Section)", text).group(1).strip() if re.search(r"Course:\s*(.*?Section)", text) else ""
    data["Section"] = re.search(r"Section:\s*(\d+)", text).group(1).strip() if re.search(r"Section:\s*(\d+)", text) else ""
    data["Semester"] = re.search(r"Semester:\s*(\d+)", text).group(1).strip() if re.search(r"Semester:\s*(\d+)", text) else ""
    data["Date"] = re.search(r"Date:\s*([\d\s/]+)", text).group(1).strip() if re.search(r"Date:\s*([\d\s/]+)", text) else ""
    data["Faculty"] = re.search(r"Faculty:\s*(.*)", text).group(1).strip() if re.search(r"Faculty:\s*(.*)", text) else ""

    scores_match = re.findall(r"(\d+)\s*([\d]+)", text)
    if scores_match:
        for i, (question, score) in enumerate(scores_match):
            if i < 10:  # Assuming Q1 to Q10
                data[f"Q{i+1}"] = score

    data["Student Signature"] = "Yes" if "Student Signature" in text and re.search(r"Student Signature:\s*(.*)", text) else "No"
    data["Faculty Signature"] = "Yes" if "Faculty Signature" in text and re.search(r"Faculty Signature:\s*(.*)", text) else "No"
    
    return data

# Paths to preprocessed images
image_paths = [
    [
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image1.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image2.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image3.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image4.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image5.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image6.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image7.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image8.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image9.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image10.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image11.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image12.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image13.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image14.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image15.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image16.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image17.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image18.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image19.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image20.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image21.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image22.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image23.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image24.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image25.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image26.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image27.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image28.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image29.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image30.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image31.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image32.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image33.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image34.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image35.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image36.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image37.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image38.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image39.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image40.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image41.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image42.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image43.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image44.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image45.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image46.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image47.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image48.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image49.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image50.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image51.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image52.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image53.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image54.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image55.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image56.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image57.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image58.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image59.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image60.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image61.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image62.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image63.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image64.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image65.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image66.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image67.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image68.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image69.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image70.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image71.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image72.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image73.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image74.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image75.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image76.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image77.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image78.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image79.png",
    "C:/Users/USER/Downloads/Dataset/preprocessed_images/image80.png"
]

]

for image_path in image_paths:
    image_name = os.path.basename(image_path)
    extracted_text = google_ocr_text(image_path)
    parsed_data = parse_text(extracted_text)
    parsed_data["Image Name"] = image_name
    
    # Append to DataFrame
    df = pd.concat([df, pd.DataFrame([parsed_data])], ignore_index=True)

# Save the DataFrame back to Excel
df.to_excel(output_excel, index=False)
print(f"Data saved to {output_excel}")
