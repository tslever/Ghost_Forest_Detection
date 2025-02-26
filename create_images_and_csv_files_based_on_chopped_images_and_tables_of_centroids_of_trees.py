import numpy as np
import os
import pandas as pd
import rasterio
from rasterio.transform import Affine


def chop_tiff_into_subimages(
    input_tiff_path: str,
    output_directory: str,
    tile_size: int,
    prefix_of_output_file_name: str,
    index_of_image: str
):
    """
    Splits a multi-band TIFF into tile_size × tile_size subimages.
    Pads with zeros on the right/bottom if dimensions are not multiples of tile_size.
    A tile is only saved if its width and height are at least 10 pixels.
    Returns (height, width) so that the same ranges can be used to chop the CSV.
    """

    os.makedirs(output_directory, exist_ok = True)

    with rasterio.open(input_tiff_path) as src:
        image_data = src.read()
        
        num_bands = src.count
        height = src.height
        width = src.width
        
        profile = src.profile.copy()
        
        # Provide a geotransform that is ALMOST identity but includes
        # a tiny translation in x and y. This prevents GDAL from ignoring it.
        non_identity_transform = Affine(
            1.0, 0.0, 0.0001,
            0.0, -1.0, 0.0001
        )
        
        # Provide a dummy CRS if the input truly has none. For example: "EPSG:4326" or None if you do not want to store a CRS.
        dummy_crs = "EPSG:4326" # or None
        
        profile.update({
            'transform': non_identity_transform,
            'crs': dummy_crs,
            'driver': 'GTiff',
            'count': num_bands,
            'dtype': image_data.dtype
        })
        
        subimage_index = 0
        
        for row_start in range(0, height, tile_size):
            row_end = min(row_start + tile_size, height)
            
            for col_start in range(0, width, tile_size):
                col_end = min(col_start + tile_size, width)
                
                sub_height = row_end - row_start
                sub_width  = col_end - col_start
                
                if sub_height < 10 or sub_width < 10:
                    subimage_index += 1
                    continue
                
                subimage = image_data[:, row_start:row_end, col_start:col_end]
                
                tile = np.zeros(
                    (num_bands, tile_size, tile_size),
                    dtype = image_data.dtype
                )
                
                tile[:, 0:sub_height, 0:sub_width] = subimage
                
                tile_profile = profile.copy()
                tile_profile.update({
                    'height': tile_size,
                    'width':  tile_size
                })
                
                out_tiff = os.path.join(
                    output_directory,
                    f"{prefix_of_output_file_name}_{index_of_image}_{subimage_index}.tif"
                )
                
                with rasterio.open(out_tiff, 'w', **tile_profile) as dst:
                    dst.write(tile)
                
                subimage_index += 1

        return height, width


def chop_csv_into_subtables(
    input_csv_path: str,
    output_directory: str,
    tile_size: int,
    image_height: int,
    image_width: int,
    prefix_of_output_file_name: str,
    index_of_image: str
):
    """
    Splits the CSV of centroid coordinates into sub CSV files, each containing
    only the points that fall into the corresponding subimage bounding box.
    Coordinates in a sub CSV file are shifted to be relative to the corresponding sub-image's top left.
    A subtable is saved only if the corresponding image section has at least 10 pixels in both dimensions.
    """
    df = pd.read_csv(input_csv_path)
    os.makedirs(output_directory, exist_ok = True)
    subimage_index = 0

    for row_start in range(0, image_height, tile_size):
        row_end = min(row_start + tile_size, image_height)

        for col_start in range(0, image_width, tile_size):
            col_end = min(col_start + tile_size, image_width)
            
            if (row_end - row_start) < 10 or (col_end - col_start) < 10:
                subimage_index += 1
                continue

            mask = (
                (df['x'] >= col_start) & (df['x'] < col_end) &
                (df['y'] >= row_start) & (df['y'] < row_end)
            )
            sub_df = df[mask].copy()
            sub_df['x'] = sub_df['x'] - col_start
            sub_df['y'] = sub_df['y'] - row_start
            out_csv = os.path.join(
                output_directory,
                f"{prefix_of_output_file_name}_{index_of_image}_{subimage_index}.csv"
            )
            sub_df.to_csv(out_csv, index = False)
            subimage_index += 1


if __name__ == "__main__":

    tile_size = 256

    #prefix_of_output_file_name = "initial_training_image"
    #path_to_input_images = f"../urban-tree-detection-data/stacked_initial_training_images"
    #path_to_input_csv_files = f"../urban-tree-detection-data/csv_files_of_initial_training_tables_of_coordinates_of_centroids_of_trees"
    #path_to_chopped_images = f"../urban-tree-detection-data/images_based_on_chopped_initial_training_images"
    #path_to_chopped_csv_files = f"../urban-tree-detection-data/csv_files_based_on_chopped_initial_training_tables_of_centroids_of_trees"
    
    #prefix_of_output_file_name = "many_training_image"
    #path_to_input_images = f"../urban-tree-detection-data/stacked_many_training_images"
    #path_to_input_csv_files = f"../urban-tree-detection-data/csv_files_of_many_training_tables_of_coordinates_of_centroids_of_trees"
    #path_to_chopped_images = f"../urban-tree-detection-data/images_based_on_chopped_many_training_images"
    #path_to_chopped_csv_files = f"../urban-tree-detection-data/csv_files_based_on_chopped_many_training_tables_of_centroids_of_trees"

    #prefix_of_output_file_name = "initial_validation_image"
    #path_to_input_images = f"../urban-tree-detection-data/stacked_initial_validation_images"
    #path_to_input_csv_files = f"../urban-tree-detection-data/csv_files_of_initial_validation_tables_of_coordinates_of_centroids_of_trees"
    #path_to_chopped_images = f"../urban-tree-detection-data/images_based_on_chopped_initial_validation_images"
    #path_to_chopped_csv_files = f"../urban-tree-detection-data/csv_files_based_on_chopped_initial_validation_tables_of_centroids_of_trees"

    #prefix_of_output_file_name = "many_validation_image"
    #path_to_input_images = f"../urban-tree-detection-data/stacked_many_validation_images"
    #path_to_input_csv_files = f"../urban-tree-detection-data/csv_files_of_many_validation_tables_of_coordinates_of_centroids_of_trees"
    #path_to_chopped_images = f"../urban-tree-detection-data/images_based_on_chopped_many_validation_images"
    #path_to_chopped_csv_files = f"../urban-tree-detection-data/csv_files_based_on_chopped_many_validation_tables_of_centroids_of_trees"

    prefix_of_output_file_name = "testing_image"
    path_to_input_images = f"../urban-tree-detection-data/stacked_testing_images"
    path_to_input_csv_files = f"../urban-tree-detection-data/csv_files_of_testing_tables_of_coordinates_of_centroids_of_trees"
    path_to_chopped_images = f"../urban-tree-detection-data/images_based_on_chopped_testing_images"
    path_to_chopped_csv_files = f"../urban-tree-detection-data/csv_files_based_on_chopped_testing_tables_of_centroids_of_trees"

    indices = set()
    for f in os.listdir(path_to_input_images):
        if f.endswith(".tif") and ("image_" in f):
            # Extract the index: all text after the first underscore and before the last period.
            index = f.split("_", 1)[1].rsplit(".", 1)[0]
            indices.add(index)

    for index_of_image in indices:
        input_tiff_path = f"{path_to_input_images}/image_{index_of_image}.tif"
        input_csv_path = f"{path_to_input_csv_files}/coordinates_of_centroids_{index_of_image}.csv"
        
        height, width = chop_tiff_into_subimages(
            input_tiff_path,
            output_directory = path_to_chopped_images,
            tile_size = tile_size,
            prefix_of_output_file_name = prefix_of_output_file_name,
            index_of_image = index_of_image
        )

        chop_csv_into_subtables(
            input_csv_path = input_csv_path,
            output_directory = path_to_chopped_csv_files,
            tile_size = tile_size,
            image_height = height,
            image_width = width,
            prefix_of_output_file_name = prefix_of_output_file_name,
            index_of_image = index_of_image
        )
