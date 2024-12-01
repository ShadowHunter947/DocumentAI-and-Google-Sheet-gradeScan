from scripts.EXTRAS.OCRDataset import OCRDataset  # Adjust if the file is in a different location
from torchvision import transforms
from torch.utils.data import DataLoader


# Define transformations
transform = transforms.Compose([
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

image_folder = r'C:\Users\USER\Downloads\Dataset\images'          # Replace "USER" with your actual username
annotation_folder = r'C:\Users\USER\Downloads\Dataset\annotated data'  # Replace "USER" with your actual username

# Initialize the dataset and dataloader
dataset = OCRDataset(image_folder=image_folder, annotation_folder=annotation_folder, transform=transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True, pin_memory=True)
  # Adjust batch size as needed
