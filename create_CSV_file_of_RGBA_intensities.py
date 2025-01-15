import csv
from PIL import Image
import sys
import os

def image_to_csv(image_path, csv_path):
    try:
        # Open the image
        with Image.open(image_path) as img:
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
        print(f"Error: The file '{image_path}' was not found.")
    except IOError:
        print(f"Error: The file '{image_path}' is not a valid image or is corrupted.")
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