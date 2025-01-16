import numpy as np
from PIL import Image
import tifffile
import os

# Define the paths to the input channel images
base_path = 'data/output_train_FINETUNING/'
red_path = os.path.join(base_path, 'r_0.png')
green_path = os.path.join(base_path, 'g_0.png')
blue_path = os.path.join(base_path, 'b_0.png')
nir_path = os.path.join(base_path, 'nir_0.png')

# Enhanced load_channel function with proper scaling for 'F' mode images
def load_channel(image_path, channel_name=''):
    """
    Loads an image, converts it to grayscale if necessary, scales the pixel values,
    and returns as a numpy array with dtype uint8.
    Includes debug information to help identify issues.
    """
    try:
        with Image.open(image_path) as img:
            print(f"\nLoading {channel_name} channel from '{image_path}'")
            print(f"Original image mode: {img.mode}")
            
            # Handle different image modes
            if img.mode == 'RGB':
                print("Image mode is RGB. Extracting the Red channel.")
                r, g, b = img.split()
                gray_img = r
                array = np.array(gray_img)
            elif img.mode == 'RGBA':
                print("Image mode is RGBA. Extracting the Red channel and ignoring Alpha.")
                r, g, b, a = img.split()
                gray_img = r
                array = np.array(gray_img)
            elif img.mode == 'F':
                print("Image mode is 'F' (floating point). Scaling pixel values.")
                array_float = np.array(img, dtype=np.float32)
                print(f"{channel_name} channel array shape: {array_float.shape}")
                print(f"{channel_name} channel array dtype: {array_float.dtype}")
                print(f"{channel_name} channel array min value: {array_float.min()}")
                print(f"{channel_name} channel array max value: {array_float.max()}")

                # Determine scaling factor
                max_val = array_float.max()
                if max_val > 1.0:
                    print(f"Max value {max_val} > 1.0. Normalizing to [0, 255].")
                    scaled_array = (array_float / max_val) * 255.0
                else:
                    print("Max value <= 1.0. Scaling by 255 to convert to [0, 255].")
                    scaled_array = array_float * 255.0
                
                # Clip values to [0, 255] and convert to uint8
                scaled_array = np.clip(scaled_array, 0, 255).astype(np.uint8)
                print(f"{channel_name} channel scaled array min value: {scaled_array.min()}")
                print(f"{channel_name} channel scaled array max value: {scaled_array.max()}")
                return scaled_array
            elif img.mode == 'L':
                print("Image mode is already grayscale ('L').")
                array = np.array(img)
            else:
                print(f"Unsupported image mode '{img.mode}'. Converting to grayscale ('L').")
                gray_img = img.convert('L')
                array = np.array(gray_img)
            
            print(f"{channel_name} channel array shape: {array.shape}")
            print(f"{channel_name} channel array dtype: {array.dtype}")
            print(f"{channel_name} channel array min value: {array.min()}")
            print(f"{channel_name} channel array max value: {array.max()}")
            return array
    except Exception as e:
        print(f"Error loading {channel_name} channel from '{image_path}': {e}")
        return None

# Load each channel with debug information
red_channel = load_channel(red_path, 'Red')
print(red_channel)
green_channel = load_channel(green_path, 'Green')
print(green_channel)
blue_channel = load_channel(blue_path, 'Blue')
print(blue_channel)
nir_channel = load_channel(nir_path, 'NIR')

# Check if any channel failed to load
if (red_channel is None) or (green_channel is None) or (blue_channel is None) or (nir_channel is None):
    raise ValueError("One or more channels failed to load. Please check the debug output for details.")

# Verify that all channels have the same dimensions
def verify_dimensions(*arrays):
    """
    Verifies that all numpy arrays have the same shape.
    """
    shapes = [arr.shape for arr in arrays]
    if not all(shape == shapes[0] for shape in shapes):
        raise ValueError(f"All channels must have the same dimensions. Found shapes: {shapes}")
    else:
        print("\nAll channels have matching dimensions.")

verify_dimensions(red_channel, green_channel, blue_channel, nir_channel)

# Stack the channels into a multi-band array
# The order will be Red, Green, Blue, NIR
# Stack along the first axis to get shape (4, height, width)
stacked_array = np.stack([red_channel, green_channel, blue_channel, nir_channel], axis=0)

# Optionally, verify the stacked array
print(f"\nStacked array shape: {stacked_array.shape}")
print(f"Stacked array dtype: {stacked_array.dtype}")

# Define the output TIFF path
output_tif_path = os.path.join(base_path, 'image_0.tif')

# Save the stacked array as a multi-band TIFF
tifffile.imwrite(
    output_tif_path,
    stacked_array,
    metadata=None,              # Optional: add metadata if needed
    dtype=stacked_array.dtype   # Data type of the image
)

print(f"\nSuccessfully saved the stacked TIFF image to '{output_tif_path}'")