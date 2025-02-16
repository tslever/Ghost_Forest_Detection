import csv
import rasterio
import sys
import os
import numpy as np

def image_to_csv(image_path, csv_path):
    try:
        # Open the image using rasterio.
        with rasterio.open(image_path) as dataset:
            # Read all bands; shape: (bands, height, width)
            bands = dataset.read()
            band_count, height, width = bands.shape

            # Handle a single-band (grayscale) image:
            if band_count == 1:
                # For a grayscale image, replicate the single channel to R, G, and B.
                gray = bands[0]
                r = gray
                g = gray
                b = gray
                # Add an alpha channel with full opacity.
                a = 255 * np.ones((height, width), dtype=gray.dtype)
                # Stack the channels to form an RGBA image.
                bands = np.stack([r, g, b, a])
                band_count = 4

            # Handle an image with 3 bands (assumed to be RGB):
            elif band_count == 3:
                # Add an alpha channel with full opacity.
                alpha = 255 * np.ones((height, width), dtype=bands.dtype)
                bands = np.vstack([bands, alpha[np.newaxis, ...]])
                band_count = 4

            # For images with 4 or more bands, only keep the first 4 bands.
            elif band_count > 4:
                bands = bands[:4]

            # Open the CSV file for writing.
            with open(csv_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write the header.
                csv_writer.writerow(['Red', 'Green', 'Blue', 'Alpha'])

                # Iterate over each pixel and write RGBA values.
                # Note: bands are organized as (band, height, width)
                for y in range(height):
                    for x in range(width):
                        r = bands[0, y, x]
                        g = bands[1, y, x]
                        b = bands[2, y, x]
                        a = bands[3, y, x]
                        csv_writer.writerow([r, g, b, a])

        print(f"CSV file '{csv_path}' has been created successfully.")

    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def is_supported_image(file_path):
    supported_extensions = ['.png', '.tif', '.tiff']
    _, ext = os.path.splitext(file_path.lower())
    return ext in supported_extensions

if __name__ == "__main__":
    # Example usage:
    # python script.py input_image.tif output_data.csv
    # or
    # python script.py input_image.png output_data.csv

    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image.png/tif> <output_data.csv>")
    else:
        input_image = sys.argv[1]
        output_csv = sys.argv[2]
        
        if not is_supported_image(input_image):
            print("Error: Unsupported file format. Please provide a PNG or TIF image.")
            sys.exit(1)
        
        image_to_csv(input_image, output_csv)