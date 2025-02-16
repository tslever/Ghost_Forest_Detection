# Commmands

## Stack 4 channels in `data/output_train_FINETUNING` into 1 image.

`python stack_channels.py`


## Plot locations of nonblack pixels in `data/output_train_FINETUNING/annotation_8.png`.

`python create_CSV_file_of_RGBA_intensities.py data/output_train_FINETUNING/annotation_8.png RGBA_intensities.csv`
`python create_CSV_file_of_coordinates_and_intensities_of_nonblack_pixels.py RGBA_intensities.csv nonblack_pixels.csv 390 411`
`python plot_locations_of_nonblack_pixels.py`


## Create CSV files of coordinates of centroids and overlays.

`python create_CSV_files_of_coordinates_of_centroids_and_overlays.py`


# Plot image and centroids.

`python plot_image_and_centroids.py`


# Create images and CSV files based on chopped images and tables of centroids of trees.

`python create_images_and_csv_files_based_on_chopped_images_and_tables_of_centroids_of_trees.py`


# Plot images based on chopped image and centroids.

`python plot_images_and_centroids.py`


# Rename CSV files based on chopped tables of centroids of trees to have the same base name as their corresponding images.

`for f in data/csv_files_based_on_chopped_tables_of_centroids_of_trees/coordinates_of_centroids_*; do mv "$f" "${f//coordinates_of_centroids_/image_}"; done`


# Pipe base names of training images to `train.txt`

Run from folder with training images `for file in *; do     [ -f "$file" ] && echo "${file%.*}"; done > train.txt`.