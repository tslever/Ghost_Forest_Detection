import os
import shutil

# Define paths
source_folder = '../urban-tree-detection-data/images_based_on_chopped_initial_training_images'
destination_folder = '../urban-tree-detection/images'
train_file_path = '../urban-tree-detection/train.txt'

# Create the train.txt file if it does not exist
if not os.path.exists(train_file_path):
    with open(train_file_path, 'w') as f:
        pass  # File created

# Ensure the destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Loop over each file in the source folder
for file_name in os.listdir(source_folder):
    src_path = os.path.join(source_folder, file_name)
    dst_path = os.path.join(destination_folder, file_name)
    
    # Check if it's a file (skip directories)
    if os.path.isfile(src_path):
        # Copy the file
        shutil.copy2(src_path, dst_path)
        
        # Print the file name
        print(file_name)
        
        # Remove the file extension before appending
        name_without_ext, _ = os.path.splitext(file_name)
        
        # Append the name without extension to train.txt
        with open(train_file_path, 'a') as train_file:
            train_file.write(name_without_ext + '\n')
