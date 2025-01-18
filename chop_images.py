import numpy as np
import os
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
        
        # 1) Provide a geotransform that is ALMOST identity but includes
        #    a tiny translation in x and y. This prevents GDAL from ignoring it.
        non_identity_transform = Affine(
            1.0, 0.0, 0.0001,
            0.0, -1.0, 0.0001
        )
        
        # 2) Provide a dummy CRS if the input truly has none. For example:
        #    "EPSG:4326" or None if you do not want to store a CRS.
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
                
                out_filename = os.path.join(
                    output_directory,
                    f"{base_name}_{subimage_index}.tif"
                )
                
                with rasterio.open(out_filename, 'w', **tile_profile) as dst:
                    dst.write(tile)
                
                subimage_index += 1


if __name__ == "__main__":
    output_dir = "./data/chopped_images"

    for index_of_image in range(0, 105 + 1):
        input_tiff = f"./data/images_to_chop/image_{index_of_image}.tif"
        chop_tiff_into_subimages(input_tiff, output_dir, tile_size = 256)