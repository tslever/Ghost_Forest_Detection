import os
import shutil


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


# Determine listing path.
if "training" in source_folder:
    listing_path = '../urban-tree-detection-data/train.txt'
elif "validation" in source_folder:
    listing_path = '../urban-tree-detection-data/val.txt'
elif "testing" in source_folder:
    listing_path = '../urban-tree-detection-data/test.txt'
else:
    raise Exception("Whether source folder contains training, validation, or testing images could not be determined.")
    

# Determine destination folder.
if "images" in source_folder:
    destination_folder = '../urban-tree-detection-data/images'
else:
    destination_folder = "../urban-tree-detection-data/csv"


if "images" in source_folder and not os.path.exists(listing_path):
    with open(listing_path, 'w') as f:
        pass


if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)


for file_name in os.listdir(source_folder):
    src_path = os.path.join(source_folder, file_name)
    dst_path = os.path.join(destination_folder, file_name)
    
    if os.path.isfile(src_path):
        shutil.copy2(src_path, dst_path)
        
        print(file_name)
        
        if "images" in source_folder:
            name_without_ext, _ = os.path.splitext(file_name)
            with open(listing_path, 'a') as train_file:
                train_file.write(name_without_ext + '\n')
