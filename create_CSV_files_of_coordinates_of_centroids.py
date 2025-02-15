from skimage import io, color, filters, measure
import pandas as pd
from PIL import ImageFile
import matplotlib.pyplot as plt

# Allow loading truncated images.
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Process each annotation image.
for index_of_annotation in range(106):
    # --- Process annotation image to extract contours and centroids ---
    # Read the annotation image.
    annotation_image = io.imread(f'data/output_train_FINETUNING/annotation_{index_of_annotation}.png')
    
    # Convert annotation image to grayscale if needed.
    if len(annotation_image.shape) == 2:
        gray_annotation = annotation_image
    elif len(annotation_image.shape) == 3:
        gray_annotation = color.rgb2gray(annotation_image)
    else:
        raise Exception(f"Unsupported image dimensions: {len(annotation_image.shape)}")
    
    # Create a binary image using Otsu's thresholding.
    threshold = filters.threshold_otsu(gray_annotation)
    binary = gray_annotation > threshold  # Assuming polygons are lighter than the background.
    
    # Label connected regions.
    labeled_image = measure.label(binary)
    
    # Calculate properties for each region and extract centroids.
    properties = measure.regionprops(labeled_image)
    data = [{'x': prop.centroid[1], 'y': prop.centroid[0]} for prop in properties]
    
    # Save centroids to CSV.
    centroids_df = pd.DataFrame(data, columns=["x", "y"]).round().astype(int)
    csv_filename = f"coordinates_of_centroids_{index_of_annotation}.csv"
    centroids_df.to_csv(csv_filename, index=False)
    
    # Reload the centroids data from the CSV file.
    reloaded_centroids_df = pd.read_csv(csv_filename)
    
    # --- Load the corresponding background image and overlay annotations ---
    # Load the background image from 'data/images_to_chop/'.
    bg_image = io.imread(f'data/images_to_chop/image_{index_of_annotation}.tif')
    
    # Create a plot with the background image.
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(bg_image, cmap='gray')
    
    # Find and plot contours from the binary annotation image.
    contours = measure.find_contours(binary, level=0.5)
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2, color='yellow')
    
    # Overlay centroids (loaded from CSV) onto the background image.
    ax.scatter(reloaded_centroids_df["x"], reloaded_centroids_df["y"], 
               color='red', marker='o', s=50, label='Centroid')
    
    ax.set_title(f"Overlay for image_{index_of_annotation}")
    ax.legend()
    plt.tight_layout()
    plt.show()