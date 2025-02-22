from skimage import io, color, filters, measure
import pandas as pd
from PIL import ImageFile
import matplotlib.pyplot as plt
import os
import rasterio

# Allow loading truncated images.
ImageFile.LOAD_TRUNCATED_IMAGES = True

#folder_with_annotation_images = "../urban-tree-detection-data/transfer_Atlantic/output_train_FINETUNING"
#path_to_csv_files = f"../urban-tree-detection-data/csv_files_of_initial_tables_of_coordinates_of_centroids_of_trees"
folder_with_annotation_images = "../urban-tree-detection-data/transfer_Atlantic/output_train_all"
path_to_csv_files = f"../urban-tree-detection-data/csv_files_of_many_tables_of_coordinates_of_centroids_of_trees"

indices = set()
for f in os.listdir(folder_with_annotation_images):
    if f.endswith(".png") and ("annotation_" in f):
        # Extract the index (e.g., "0" from "annotation_0.png")
        index = f.split("_")[-1].split(".")[0]
        indices.add(index)

# Process each annotation image.
for index_of_annotation in indices:
    # --- Process annotation image to extract contours and centroids ---
    # Read the annotation image.
    annotation_image = rasterio.open(f'{folder_with_annotation_images}/annotation_{index_of_annotation}.png').read(1)
    
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
    labeled_image = measure.label(binary, connectivity=2) # Use 8-way connectivity
    
    # Calculate properties for each region and extract centroids.
    properties = measure.regionprops(labeled_image)
    data = [{'x': prop.centroid[1], 'y': prop.centroid[0]} for prop in properties]
    
    # Save centroids to CSV.
    centroids_df = pd.DataFrame(data, columns=["x", "y"]).round().astype(int)
    if not os.path.exists(path_to_csv_files):
        os.makedirs(path_to_csv_files)
    csv_filename = f"{path_to_csv_files}/coordinates_of_centroids_{index_of_annotation}.csv"
    centroids_df.to_csv(csv_filename, index=False)
    
    '''
    # Reload the centroids data from the CSV file.
    reloaded_centroids_df = pd.read_csv(csv_filename)
    
    # --- Load the corresponding background image and overlay annotations ---
    # Load the background image from 'data/output_train_FINETUNING/'.
    bg_image = io.imread(f'data/images_to_chop/image_{index_of_annotation}.tif')
    
    # Find contours from the binary annotation image.
    contours = measure.find_contours(binary, level=0.5)
    
    # Create a figure with two subplots: left for the original image, right for the overlay.
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left subplot: Original background image.
    axes[0].imshow(bg_image, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    # Right subplot: Background image with overlays.
    axes[1].imshow(bg_image, cmap='gray')
    # Plot polygon contours.
    for contour in contours:
        axes[1].plot(contour[:, 1], contour[:, 0], linewidth=2, color='yellow')
    # Overlay centroids.
    axes[1].scatter(reloaded_centroids_df["x"], reloaded_centroids_df["y"], 
                    color='red', marker='o', s=50, label='Centroid')
    axes[1].set_title('Overlay with Polygons and Centroids')
    axes[1].legend()
    axes[1].axis('off')
    
    plt.tight_layout()
    
    # Save the figure to a file.
    output_filename = f'data/overlays_of_images_polygons_and_centroids/overlay_{index_of_annotation}.png'
    plt.savefig(output_filename, dpi=300)
    plt.close(fig)
    '''
