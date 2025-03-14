import os
import rasterio
import numpy as np

# Input folder with georeferenced PNGs
#input_folder = "../urban-tree-detection-data/transfer_Atlantic/output_train_FINETUNING"
#input_folder = "../urban-tree-detection-data/transfer_Atlantic/output_train_all"
#input_folder = "../urban-tree-detection-data/transfer_Atlantic/output_val_FINETUNING"
#input_folder = "../urban-tree-detection-data/transfer_Atlantic/output_val_all"
input_folder = "../urban-tree-detection-data/transfer_Atlantic/output_eval"

# Output folder for stacked TIFFs
#output_folder = "../urban-tree-detection-data/stacked_initial_training_images"
#output_folder = "../urban-tree-detection-data/stacked_many_training_images"
#output_folder = "../urban-tree-detection-data/stacked_initial_validation_images"
#output_folder = "../urban-tree-detection-data/stacked_many_validation_images"
output_folder = "../urban-tree-detection-data/stacked_testing_images"

os.makedirs(output_folder, exist_ok = True)

# Function to scale data to 0 - 255
def scale_to_8bit_global(data):
    if data.dtype != np.uint8: # Only scale if not already 8-bit
        data_min, data_max = np.nanmin(data), np.nanmax(data)
        if data_max > data_min:  # Avoid division by zero
            data = 255 * (data - data_min) / (data_max - data_min)
        data = data.astype(np.uint8)
    return data

indices = set()
for f in os.listdir(input_folder):
    if f.endswith(".png") and any(prefix in f for prefix in ("r_", "g_", "b_", "nir_")):
        # Extract the index: all text after the first underscore and before the last period.
        index = f.split("_", 1)[1].rsplit(".", 1)[0]
        indices.add(index)

# Loop through each index and process the corresponding images
for index in sorted(indices, key = lambda x: str(x)):
    # File paths for the input PNGs
    r_path = os.path.join(input_folder, f"r_{index}.png")
    g_path = os.path.join(input_folder, f"g_{index}.png")
    b_path = os.path.join(input_folder, f"b_{index}.png")
    nir_path = os.path.join(input_folder, f"nir_{index}.png")

    # Check if all required files exist
    if not all(os.path.exists(p) for p in [r_path, g_path, b_path, nir_path]):
        print(f"Skipping index {index}: Missing files")
        continue

    # Output path for the stacked 4-band GeoTIFF
    output_path = os.path.join(output_folder, f"image_{index}.tif")

    # Read the first band (e.g., r_0.png) to get metadata
    with rasterio.open(r_path) as src:
        meta = src.meta.copy()
        transform = src.transform
        crs = src.crs

        # Update metadata for a 4-band TIFF
        meta.update({
            "count": 4,  # Number of bands (RGBN)
            "dtype": "uint8",  # Force output to 8-bit
            "photometric": "RGB"  # Ensure no transparency
        })

    # Read all bands into a list
    stacked_data = []
    for band_path in [r_path, g_path, b_path, nir_path]:
        with rasterio.open(band_path) as src:
            # Ensure spatial properties match the first image
            assert src.transform == transform, f"Geotransform mismatch in {band_path}!"
            assert src.crs == crs, f"CRS mismatch in {band_path}!"
            # Read only the first band (index 1) to ignore transparency
            band_data = src.read(1)
            stacked_data.append(band_data)

    # Stack all bands into a single array
    stacked_data = np.stack(stacked_data, axis = 0)

    # Scale the entire stacked image to 0-255
    stacked_data = scale_to_8bit_global(stacked_data)

    # Write the stacked 4-band GeoTIFF (no transparency)
    with rasterio.open(output_path, "w", **meta) as dst:
        dst.write(stacked_data)

    print(f"Stacked 4-band GeoTIFF saved to: {output_path}")
