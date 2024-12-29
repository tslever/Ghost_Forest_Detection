import csv
import sys
import os

def filter_pixels(input_csv, output_csv, width, height):
    try:
        # Check if input file exists
        if not os.path.isfile(input_csv):
            print(f"Error: The file '{input_csv}' does not exist.")
            return

        # Calculate total number of pixels
        total_pixels = width * height

        with open(input_csv, mode='r', newline='') as infile, \
             open(output_csv, mode='w', newline='') as outfile:

            reader = csv.DictReader(infile)
            fieldnames = ['X', 'Y', 'Red', 'Green', 'Blue', 'Alpha']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            writer.writeheader()

            pixel_count = 0  # To keep track of the current pixel index

            for row in reader:
                if pixel_count >= total_pixels:
                    print("Warning: More rows in CSV than expected based on image dimensions.")
                    break

                try:
                    red = int(row['Red'])
                    green = int(row['Green'])
                    blue = int(row['Blue'])
                    alpha = int(row['Alpha'])
                except ValueError:
                    print(f"Warning: Non-integer value found at row {pixel_count + 2}. Skipping this row.")
                    pixel_count += 1
                    continue

                # Calculate x and y coordinates
                y = pixel_count // width
                x = pixel_count % width

                # Apply the filtering conditions
                if (red > 0) or (green > 0) or (blue > 0) or (alpha < 255):
                    writer.writerow({
                        'X': x,
                        'Y': y,
                        'Red': red,
                        'Green': green,
                        'Blue': blue,
                        'Alpha': alpha
                    })

                pixel_count += 1

            if pixel_count < total_pixels:
                print(f"Warning: CSV has fewer rows ({pixel_count}) than expected ({total_pixels}).")

        print(f"Filtered CSV '{output_csv}' has been created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def print_usage():
    print("Usage: python filter_pixels.py <input_csv> <output_csv> <image_width> <image_height>")
    print("Example: python filter_pixels.py input.csv output.csv 1920 1080")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Error: Incorrect number of arguments.")
        print_usage()
    else:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2]
        try:
            image_width = int(sys.argv[3])
            image_height = int(sys.argv[4])
            if image_width <= 0 or image_height <= 0:
                raise ValueError
        except ValueError:
            print("Error: Image width and height must be positive integers.")
            print_usage()
            sys.exit(1)

        filter_pixels(input_csv, output_csv, image_width, image_height)