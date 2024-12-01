import cv2
import matplotlib.pyplot as plt

# Load the image
image_path = image_path = "C:\\Users\\USER\\Downloads\\Dataset\\Sample Raw Data.jpeg"
image = cv2.imread(image_path)

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
plt.imshow(gray_image, cmap='gray')
plt.title('Grayscale Image')
plt.show()

# Apply binary threshold
_, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Display the binary image
plt.imshow(binary_image, cmap='gray')
plt.title('Binarized Image')
plt.show()

# Save the binarized image
cv2.imwrite('binarized_image.png', binary_image)
