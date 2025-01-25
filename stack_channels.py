import numpy as np
from PIL import Image
import tifffile
import os


def load_channel(image_path):
    with Image.open(image_path) as img:
        if img.mode == 'RGB':
            r, _, _ = img.split()
            gray_img = r
            array = np.array(gray_img)
        elif img.mode == 'RGBA':
            r, _, _, _ = img.split()
            gray_img = r
            array = np.array(gray_img)
        elif img.mode == 'F':
            array_float = np.array(img, dtype = np.float32)
            max_val = array_float.max()
            if max_val > 1.0:
                scaled_array = (array_float / max_val) * 255.0
            else:
                scaled_array = array_float * 255.0
            scaled_array = np.clip(scaled_array, 0, 255).astype(np.uint8)
            return scaled_array
        elif img.mode == 'L':
            array = np.array(img)
        else:
            gray_img = img.convert('L')
            array = np.array(gray_img)
        return array


def verify_dimensions(*arrays):
    shapes = [arr.shape for arr in arrays]
    if not all(shape == shapes[0] for shape in shapes):
        raise ValueError(f"All channels must have the same dimensions. Found shapes: {shapes}")


if __name__ == "__main__":

    path_to_directory_of_channels_to_stack = r".\data\output_train_FINETUNING"
    #path_to_directory_of_channels_to_stack = r".\data\channels"

    if path_to_directory_of_channels_to_stack == r".\data\output_train_FINETUNING":
        prefix_for_channel_N = "nir_"
        suffix_of_last_channel = 105
        extension = ".png"
    if path_to_directory_of_channels_to_stack == r".\data\channels":
        prefix_for_channel_N = "n_"
        suffix_of_last_channel = 10
        extension = ".tif"
    

    for index_of_image in range(0, suffix_of_last_channel + 1):
        red_path = os.path.join(path_to_directory_of_channels_to_stack, f'r_{index_of_image}' + extension)
        green_path = os.path.join(path_to_directory_of_channels_to_stack, f'g_{index_of_image}' + extension)
        blue_path = os.path.join(path_to_directory_of_channels_to_stack, f'b_{index_of_image}' + extension)
        nir_path = os.path.join(path_to_directory_of_channels_to_stack, f'{prefix_for_channel_N}{index_of_image}' + extension)

        try:
            red_channel = load_channel(red_path)
            green_channel = load_channel(green_path)
            blue_channel = load_channel(blue_path)
            nir_channel = load_channel(nir_path)
        except Exception as e:
            print(e)
            continue

        verify_dimensions(red_channel, green_channel, blue_channel, nir_channel)

        stacked_array = np.stack([red_channel, green_channel, blue_channel, nir_channel], axis = 0)

        output_tif_path = os.path.join(path_to_directory_of_channels_to_stack, f'image_{index_of_image}.tif')
        tifffile.imwrite(
            output_tif_path,
            stacked_array,
            metadata = None,
            dtype = stacked_array.dtype
        )