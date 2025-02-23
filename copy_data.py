import os
import shutil

# Define paths
#source_folder = '../urban-tree-detection-data/images_based_on_chopped_initial_training_images'
#source_folder = '../urban-tree-detection-data/images_based_on_chopped_many_training_images'
#source_folder = '../urban-tree-detection-data/images_based_on_chopped_initial_validation_images'
#source_folder = '../urban-tree-detection-data/images_based_on_chopped_many_validation_images'
#source_folder = '../urban-tree-detection-data/images_based_on_chopped_testing_images'
#source_folder = "../urban-tree-detection-data/csv_files_based_on_chopped_initial_training_tables_of_centroids_of_trees"
#source_folder = "../urban-tree-detection-data/csv_files_based_on_chopped_many_training_tables_of_centroids_of_trees"
#source_folder = "../urban-tree-detection-data/csv_files_based_on_chopped_initial_validation_tables_of_centroids_of_trees"
#source_folder = "../urban-tree-detection-data/csv_files_based_on_chopped_many_validation_tables_of_centroids_of_trees"
source_folder = "../urban-tree-detection-data/csv_files_based_on_chopped_testing_tables_of_centroids_of_trees"

#listing_path = '../urban-tree-detection-data/train.txt'
#listing_path = '../urban-tree-detection-data/val.txt'
#listing_path = '../urban-tree-detection-data/test.txt'

#destination_folder = '../urban-tree-detection-data/images'
destination_folder = "../urban-tree-detection-data/csv"

# Create the listing if it does not exist
# TODO: Comment out when copying CSV files.
#if not os.path.exists(listing_path):
#    with open(listing_path, 'w') as f:
#        pass  # File created

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
        
        # TODO: Comment everything after this out when copying CSV files.
        # Remove the file extension before appending
        #name_without_ext, _ = os.path.splitext(file_name)
        
        # Append the name without extension to train.txt
        #with open(listing_path, 'a') as train_file:
        #    train_file.write(name_without_ext + '\n')
