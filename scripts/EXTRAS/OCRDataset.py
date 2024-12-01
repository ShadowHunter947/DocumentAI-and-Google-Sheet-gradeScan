import os
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import xml.etree.ElementTree as ET

class OCRDataset(Dataset):
    def __init__(self, image_folder, annotation_folder, transform=None):
        self.image_folder = image_folder
        self.annotation_folder = annotation_folder
        self.transform = transform
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        # Load image
        img_name = self.image_files[idx]
        image_path = os.path.join(self.image_folder, img_name)
        image = Image.open(image_path).convert("L")  # Convert to grayscale

        # Apply transformations
        if self.transform:
            image = self.transform(image)

        # Load annotation
        annotation_name = os.path.join(self.annotation_folder, img_name.replace('.png', '.xml'))
        label = self.parse_annotation(annotation_name)

        return image, label

    def parse_annotation(self, annotation_file):
        # This function should parse the XML annotation file and extract text for each ROI
        labels = []

        # Parse XML file
        tree = ET.parse(annotation_file)
        root = tree.getroot()

        for element in root.findall('object'):
            name = element.find('name').text  # Get the text label (e.g., Name, ID, etc.)
            labels.append(name)

        return labels
