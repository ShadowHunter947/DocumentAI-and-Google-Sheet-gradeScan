# train_crnn.py

import torch
import torch.optim as optim
from scripts.EXTRAS.crnn_model import CRNN  # Import your CRNN model from crnn_model.py
from torch.utils.data import DataLoader
from scripts.EXTRAS.OCRDataset import OCRDataset  # Assuming OCRDataset is in a separate file
from torchvision import transforms

# Set paths to the images and annotations
image_folder = r'C:\Users\USER\Downloads\Dataset\images'
annotation_folder = r'C:\Users\USER\Downloads\Dataset\annotated data'

transform = transforms.Compose([
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Initialize dataset and dataloader
dataset = OCRDataset(image_folder=image_folder, annotation_folder=annotation_folder, transform=transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# Initialize model, loss function, and optimizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = 38  # 26 letters, 10 digits, 1 blank, and 1 tick mark
model = CRNN(input_channels=1, num_classes=num_classes).to(device)


criterion = torch.nn.CTCLoss(blank=0)  
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Learning rate set to 0.001

# Step 3: Training loop
num_epochs = 3  
for epoch in range(num_epochs):
    model.train()  
    running_loss = 0.0

    for images, labels in dataloader:
        images = images.to(device)  
        labels = labels.to(device)  
       
        optimizer.zero_grad()
    
        outputs = model(images)
        
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()


    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(dataloader)}")
