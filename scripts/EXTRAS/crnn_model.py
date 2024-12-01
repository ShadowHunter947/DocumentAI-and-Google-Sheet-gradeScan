import torch
import torch.nn as nn
import torch.nn.functional as F

class CRNN(nn.Module):
    def __init__(self, input_channels, num_classes):
        super(CRNN, self).__init__()

        self.cnn = nn.Sequential(
            nn.Conv2d(input_channels, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU()
        )

        self.rnn = nn.LSTM(256, 128, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(256, num_classes)

    def forward(self, x):
        # Pass through CNN layers
        x = self.cnn(x)
        
        # Reshape for RNN
        x = x.squeeze(2).permute(0, 2, 1)  # [batch, width, features]
        
        # Pass through RNN
        x, _ = self.rnn(x)
        
        # Apply fully connected layer
        x = self.fc(x)

        return x
