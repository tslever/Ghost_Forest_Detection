import matplotlib.pyplot as plt
from skimage import io, color, filters, measure
import pandas as pd

# Load the image
image = io.imread('data/output_train_FINETUNING/annotation_0.png')

# Display the original image
plt.figure(figsize=(8, 6))
plt.imshow(image)
plt.title('Original Image')
plt.axis('off')
plt.show()

# Convert to grayscale if the image is colored
if len(image.shape) == 3:
    gray_image = color.rgb2gray(image)
else:
    gray_image = image

# Display the grayscale image
plt.figure(figsize=(8, 6))
plt.imshow(gray_image, cmap='gray')
plt.title('Grayscale Image')
plt.axis('off')
plt.show()

# Apply Otsu's threshold to convert to binary
thresh = filters.threshold_otsu(gray_image)
binary = gray_image > thresh  # Assuming polygons are lighter than the background

# Display the binary image
plt.figure(figsize=(8, 6))
plt.imshow(binary, cmap='gray')
plt.title('Binary Image')
plt.axis('off')
plt.show()

# Label connected regions
label_image = measure.label(binary)

# Display the labeled image with boundaries
plt.figure(figsize=(8, 6))
plt.imshow(label_image, cmap='nipy_spectral')
plt.title('Labeled Image')
plt.axis('off')
plt.show()

# Extract region properties
props = measure.regionprops_table(label_image, properties=['label', 'centroid'])

# Convert the properties to a pandas DataFrame for easier handling
centroids_df = pd.DataFrame(props)

# Rename centroid columns for clarity
centroids_df.rename(columns={'centroid-0': 'centroid_y', 'centroid-1': 'centroid_x'}, inplace=True)

# Display the centroids
print("Centroids of Polygons:")
print(centroids_df)

# Plot centroids on the original image
plt.figure(figsize=(8, 6))
plt.imshow(image)
plt.title('Centroids on Original Image')
plt.axis('off')

# Plot each centroid
for index, row in centroids_df.iterrows():
    plt.plot(row['centroid_x'], row['centroid_y'], 'ro')  # Red dot for centroid
    plt.text(row['centroid_x'] + 5, row['centroid_y'] + 5, f"ID {row['label']}", color='yellow')

plt.show()