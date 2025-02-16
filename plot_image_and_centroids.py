import matplotlib.pyplot as plt
import pandas as pd
from skimage import io

# Paths to the input image and CSV file.
image_path = 'data/images_to_chop/image_8.tif'
csv_path = 'data/csv_files_of_tables_of_coordinates_of_centroids_of_trees/coordinates_of_centroids_8.csv'

# Load the background image.
bg_image = io.imread(image_path)

# Load the centroids data.
centroids_df = pd.read_csv(csv_path)

# Create a figure and axis.
fig, ax = plt.subplots(figsize=(10, 10))

# Display the image.
ax.imshow(bg_image, cmap='gray')
ax.set_title('Overlay: Image with Centroids')
ax.axis('off')

# Overlay the centroids.
ax.scatter(centroids_df["x"], centroids_df["y"],
           color='red', marker='o', s=50, label='Centroid')

# Add a legend.
ax.legend()

# Adjust layout.
plt.tight_layout()

# Save the overlay image.
output_path = 'data/overlays_of_images_polygons_and_centroids/overlay_8.png'
plt.savefig(output_path, dpi=300)
plt.close(fig)