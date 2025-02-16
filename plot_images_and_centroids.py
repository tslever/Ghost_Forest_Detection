import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# List of image indices to loop over
indices = [0, 1, 2, 3]

# Create a figure with 2 rows and 2 columns of subplots, sharing x and y axes
fig, axes = plt.subplots(2, 2, figsize=(12, 12), sharex=True, sharey=True)
axes = axes.flatten()  # Flatten to iterate easily

for ax, idx in zip(axes, indices):
    # Define file paths for the current image and CSV file.
    image_path = f"data/images_based_on_chopped_images/image_8_{idx}.tif"
    csv_path = f"data/csv_files_based_on_chopped_tables_of_centroids_of_trees/image_8_{idx}.csv"
    
    # Load the image using plt.imread
    img = plt.imread(image_path)
    
    # Load the CSV file containing the centroid coordinates
    df = pd.read_csv(csv_path)
    
    # Display the image
    ax.imshow(img)
    
    # Overlay the centroids
    ax.scatter(df['x'], df['y'], s=50, c='red', edgecolors='white', linewidths=0.5)
    
    # Set the title for the subplot
    ax.set_title(f"image_8_{idx}.tif", pad=2)
    
    # Optionally, remove axis labels to further minimize spacing
    ax.set_xlabel("")
    ax.set_ylabel("")

# Remove tick labels for inner subplots to reduce clutter
for ax in axes:
    ax.tick_params(labelbottom=False, labelleft=False)

# Adjust the layout so subplots are as close as possible
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0, hspace=0)
plt.show()