import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

class OCRDataset(Dataset):
    def __init__(self, image_folder, annotation_folder, transform=None):
        self.image_folder = image_folder
        self.annotation_folder = annotation_folder
        self.transform = transform
        self.image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]  # Adjust file extension as needed

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        # Load image
        img_name = os.path.join(self.image_folder, self.image_files[idx])
        image = Image.open(img_name).convert("L")  # Grayscale

        # Apply transformations
        if self.transform:
            image = self.transform(image)

        # Load annotation (implement a function to parse XML and extract labels)
        annotation_name = os.path.join(self.annotation_folder, self.image_files[idx].replace('.png', '.xml'))
        label = self.parse_annotation(annotation_name)

        return image, label

    def parse_annotation(self, annotation_file):
        # Custom function to read XML and extract text labels for each ROI
        # This will depend on how you have saved the annotations.
        # For simplicity, let's assume it returns a list of strings (text) for each ROI.
        labels = []  # Fill with actual parsed values
        # Parse XML file (use xml.etree.ElementTree or another XML parser)
        return labels


transform = transforms.Compose([
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
