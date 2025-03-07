import os
import shutil

list_of_paths = [
    '../urban-tree-detection-data/images_based_on_chopped_initial_training_images',
    '../urban-tree-detection-data/images_based_on_chopped_many_training_images',
    '../urban-tree-detection-data/images_based_on_chopped_initial_validation_images',
    '../urban-tree-detection-data/images_based_on_chopped_many_validation_images',
    '../urban-tree-detection-data/images_based_on_chopped_testing_images',
    "../urban-tree-detection-data/csv_files_based_on_chopped_initial_training_tables_of_centroids_of_trees",
    "../urban-tree-detection-data/csv_files_based_on_chopped_many_training_tables_of_centroids_of_trees",
    "../urban-tree-detection-data/csv_files_based_on_chopped_initial_validation_tables_of_centroids_of_trees",
    "../urban-tree-detection-data/csv_files_based_on_chopped_many_validation_tables_of_centroids_of_trees",
    "../urban-tree-detection-data/csv_files_based_on_chopped_testing_tables_of_centroids_of_trees"
]


#for source_folder in list_of_paths:
for source_folder in [list_of_paths[i] for i in [0,2,4,5,7,9]]: #SUBSETTING FOR WHEN WE WANT SMALLER DATASET

    # Determine listing path based on the type (training, validation, testing)
    if "training" in source_folder:
        listing_path = '../urban-tree-detection-data/train.txt'
    elif "validation" in source_folder:
        listing_path = '../urban-tree-detection-data/val.txt'
    elif "testing" in source_folder:
        listing_path = '../urban-tree-detection-data/test.txt'
    else:
        raise Exception("Could not determine whether the source folder is training, validation, or testing.")

    # Determine the destination folder and whether we need to write to a listing.
    if "images" in source_folder:
        destination_folder = '../urban-tree-detection-data/images'
        write_listing = True
    else:
        destination_folder = "../urban-tree-detection-data/csv"
        write_listing = False  # Only image base names are added to the listing.

    # Create an empty listing file if needed (for images) and if it doesn't already exist.
    if write_listing and not os.path.exists(listing_path):
        open(listing_path, 'w').close()

    # Ensure the destination folder exists.
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Loop over files in the source folder.
    for file_name in os.listdir(source_folder):
        src_path = os.path.join(source_folder, file_name)
        dst_path = os.path.join(destination_folder, file_name)

        if os.path.isfile(src_path):
            try:
                shutil.copy2(src_path, dst_path)
            except Exception as e:
                print(f"Error copying {file_name}: {e}")
                continue

            # Only add to the listing if the file now exists in the destination folder.
            if os.path.exists(dst_path):
                print(f"Copied: {file_name}")
                if write_listing:
                    name_without_ext, _ = os.path.splitext(file_name)
                    with open(listing_path, 'a') as listing_file:
                        listing_file.write(name_without_ext + '\n')
            else:
                raise Exception(f"Failed to copy {file_name}; skipping listing update.")