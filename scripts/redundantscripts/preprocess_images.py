import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

# Directory paths
input_dir = "C:/Users/USER/Downloads/Dataset/images"  # Path to your images
output_dir = "C:/Users/USER/Downloads/Dataset/preprocessed_images"  # Path to save preprocessed images

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def preprocess_image(image_path, output_path):
    # Load image
    image = cv2.imread(image_path)
    
    # Step 1: Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Step 2: Binarization using Otsu’s Thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Step 3: Noise Reduction using Gaussian Blur
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)
    
    # Save the preprocessed image
    cv2.imwrite(output_path, blurred)
    print(f"Processed image saved at: {output_path}")

# Loop through all images in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".png"):  # Process only .png files
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Preprocess and save
        preprocess_image(input_path, output_path)
