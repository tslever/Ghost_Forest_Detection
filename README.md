# Ghost Forest Detection

This repository includes Python scripts that can be used to massage images representing channels of satellite images and annotation images into data that can be used to train, validate, and test a neural network represented by Git repository [urban-tree-detection](https://github.com/tslever/urban-tree-detection).

### Starting Point

Tom Lever created a fork of Git repository [urban-tree-detection-data](https://github.com/tslever/urban-tree-detection-data) and cloned the repository via SSH to directory `/project/SDS/capstones_yang/urban-tree-detection-data` in Rivanna.

Henry Yeung uploaded directory `transfer_Atlantic` to the root of `urban-tree-detection-data`. `transfer_Atlantic` contains subdirectories `output_eval`, `output_train_all`, `output_train_FINETUNING`, `output_val_all`, and `output_val_FINETUNING`. These subdirectories all contain grayscale images representing red, green, blue, and near infrared channels of satellite images and annotation images corresponding to those satellite images.

The grayscale images in each folder are stored as PNG files that are georeferenced, meaning they include embedded geographic metadata such as the geotransform and coordinate reference system (CRS). The numeric pixel values in these images may span a range larger than 8-bit; however, during processing (as seen in `stack_channels.py`), the data are scaled to an 8-bit range (0 - 255) to ensure consistency and compatibility.

Annotation images follow a similar format: they are georeferenced PNGs where the pixel values are used to represent vertices of polygons circumscribing dead trees. This preserved geographic metadata ensures that both satellite images and annotation images can be accurately aligned with one another.

Tom and Henry in creating `stack_channels.py` needed to use a Python package like `rasterio` that is compatible with these georeferenced images. Earlier use of other image processing libraries caused misalignment between ultimate images and CSV files.

### Stack Channels into Images

Massaging images into data may be further automated.

Tom stacked channels into 4 channel GeoTIFF images using `python stack_channels.py`. Tom hardcoded a path to each of the 5 folders above. Tom hardcoded a path to a corresponding folder of stacked images. The name of each stacked image had the string "image", the identifier associated with the relevant channels, and the extension ".tif".

### Create CSV Files of Coordinates of Centroids of Dead Trees

Tom created CSV files of coordinates of centroids of dead trees using `python create_CSV_files_of_coordinates_of_centroids_and_overlays.py`. Tom hardcoded a path to each of the 5 folders above. Tom hardcoded a path to a corresponding folder of CSV files of coordinates of centroids. The name of each CSV file had the string `coordinates_of_centroids`, the identifier associated with the relevant annotation file, and the extension ".csv".

### Create Images and CSV Files Based on Chopped Images and Tables of Centroids of Dead Trees

Tom created images and CSV files based on chopped stacked images and tables of centroids of dead trees using `python create_images_and_csv_files_based_on_chopped_images_and_tables_of_centroids_of_trees.py`. Tom hardcoded a path to each of the 5 folders of stacked images. Tom hardcoded a path to each of the 5 folders of CSV files of coordinates of centroids. Tom hardcoded a path to a corresponding folder of images based on chopped stacked images. Tom hardcoded a path to a corresponding folder of CSV files based on chopped tables of centroids of dead trees. An image based on a chopped image is a tile of the image that was chopped, padded with white pixels to be 256 x 256. The corresponding CSV file is a CSV file of coordinates of dead trees in the relevant image. The name of each output image consists of the base name of the relevant image that was chopped, `_i` where i is a tile index, and the extension of the chopped image. The name of each output CSV file consists of the base name of the CSV file with the relevant table of coordinates of centroids that was chopped, `_i`, and extension ".csv". 

### Copy Images and CSV Files Based on Chopped Images and Tables of Centroids To Final Locations

Tom copied images and CSV files based on chopped images and tables of centroids to their final locations for consumption by the neural network by using `python copy_data.py`. Tom harcoded each source folder of images or CSV files. Tom hardcoded destination folders for all images and all CSV files and listing paths.

### Transition to Git Repository `urban-tree-detection`

At this point, consider reading the instructions for training, validating, and testing the neural network found in the README of Git repository `urban-tree-detection`.
