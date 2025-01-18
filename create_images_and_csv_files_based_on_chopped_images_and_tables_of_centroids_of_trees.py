import numpy as np
import os
import pandas as pd
import rasterio
from rasterio.transform import Affine


def chop_tiff_into_subimages(
    input_tiff_path: str,
    output_directory: str,
    tile_size: int
):
    """
    Splits a multi-band TIFF into tile_size × tile_size subimages.
    Pads with zeros on the right/bottom if dimensions are not multiples of tile_size.
    Returns (height, width) so that the same ranges can be used to chop the CSV.
    """

    base_name_with_ext = os.path.basename(input_tiff_path)
    base_name, extension = os.path.splitext(base_name_with_ext)

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
                
                subimage = image_data[:, row_start:row_end, col_start:col_end]
                
                tile = np.zeros(
                    (num_bands, tile_size, tile_size),
                    dtype = image_data.dtype
                )
                
                sub_height = row_end - row_start
                sub_width  = col_end - col_start
                tile[:, 0:sub_height, 0:sub_width] = subimage
                
                tile_profile = profile.copy()
                tile_profile.update({
                    'height': tile_size,
                    'width':  tile_size
                })
                
                out_tiff = os.path.join(
                    output_directory,
                    f"{base_name}_{subimage_index}.tif"
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
    image_width: int
):
    """
    Splits the CSV of centroid coordinates into sub CSV files, each containing
    only the points that fall into the corresponding subimage bounding box.
    Coordinates in a sub CSV file are shifted to be relative to the corresponding sub-image's top left.
    """
    base_name_with_ext = os.path.basename(input_csv_path)
    base_name, extension = os.path.splitext(base_name_with_ext)
    df = pd.read_csv(input_csv_path)
    os.makedirs(output_directory, exist_ok = True)
    subimage_index = 0
    for row_start in range(0, image_height, tile_size):
        row_end = min(row_start + tile_size, image_height)

        for col_start in range(0, image_width, tile_size):
            col_end = min(col_start + tile_size, image_width)

            mask = (
                (df['x'] >= col_start) & (df['x'] < col_end) &
                (df['y'] >= row_start) & (df['y'] < row_end)
            )
            sub_df = df[mask].copy()
            sub_df['x'] = sub_df['x'] - col_start
            sub_df['y'] = sub_df['y'] - row_start
            out_csv = os.path.join(
                output_directory,
                f"{base_name}_{subimage_index}.csv"
            )
            sub_df.to_csv(out_csv, index = False)
            subimage_index += 1


if __name__ == "__main__":

    tile_size = 256
    tiff_output_dir = "./data/images_based_on_chopped_images"
    csv_output_dir = "./data/chopped_csvs"

    for index_of_image in range(0, 105 + 1):
        input_tiff_path = f"./data/images_to_chop/image_{index_of_image}.tif"
        input_csv_path = f"./data/coordinates_of_centroids_of_trees_in_images_to_chop/coordinates_of_centroids_{index_of_image}.csv"
        
        height, width = chop_tiff_into_subimages(
            input_tiff_path,
            output_directory = tiff_output_dir,
            tile_size = tile_size
        )

        chop_csv_into_subtables(
            input_csv_path = input_csv_path,
            output_directory = csv_output_dir,
            tile_size = tile_size,
            image_height = height,
            image_width = width
        )