import csv
from PIL import Image
import sys

def tif_to_csv(tif_path, csv_path):
    try:
        # Open the TIFF image
        with Image.open(tif_path) as img:
            # Ensure image is in RGBA mode
            img = img.convert("RGBA")
            width, height = img.size
            pixels = img.load()

            # Open the CSV file for writing
            with open(csv_path, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                # Write the header
                csv_writer.writerow(['Red', 'Green', 'Blue', 'Alpha'])

                # Iterate over each pixel and write RGBA values
                for y in range(height):
                    for x in range(width):
                        r, g, b, a = pixels[x, y]
                        csv_writer.writerow([r, g, b, a])

        print(f"CSV file '{csv_path}' has been created successfully.")

    except FileNotFoundError:
        print(f"Error: The file '{tif_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    # python script.py input_image.tif output_data.csv

    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image.tif> <output_data.csv>")
    else:
        input_tif = sys.argv[1]
        output_csv = sys.argv[2]
        tif_to_csv(input_tif, output_csv)