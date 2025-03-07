import os
from PIL import Image

# Set the maximum allowed size
max_size = (261, 261)

# Specify the folder containing the images
folder_path = '../urban-tree-detection-data/stacked_testing_images'

# Loop over each file in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Try opening the file as an image
    try:
        with Image.open(file_path) as img:
            # Check if the image exceeds the max dimensions
            if img.width > 257 or img.height > 256:
                raise Exception(f"Image {file_path} has width {img.width} and height {img.height}.")
            else:
                print(f"{filename} is within the allowed dimensions: {img.size}")
    except IOError:
        # Skip files that are not images
        #print(f"Skipping {filename}: not a valid image file.")
        pass
