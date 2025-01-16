from skimage import io, color, filters, measure
import pandas as pd
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

for index_of_annotation in range(0, 105 + 1):

    image = io.imread(f'data/output_train_FINETUNING/annotation_{index_of_annotation}.png')

    number_of_dimensions = len(image.shape)
    if number_of_dimensions == 2:
        gray_image = image
    elif number_of_dimensions == 3:
        gray_image = color.rgb2gray(image)
    else:
        raise Exception(f"I don't know how to process an image with {number_of_dimensions} dimensions.")

    threshold = filters.threshold_otsu(gray_image)
    binary = gray_image > threshold  # I assume that polygons are lighter than background.

    ndarray_of_labels = measure.label(binary)

    properties = measure.regionprops(ndarray_of_labels)
    data = [{'x': prop.centroid[1], 'y': prop.centroid[0]} for prop in properties]

    data_frame_of_coordinate_pairs = pd.DataFrame(data)
    data_frame_of_coordinate_pairs = data_frame_of_coordinate_pairs.round().astype(int)
    data_frame_of_coordinate_pairs.to_csv(f"coordinates_of_centroids_{index_of_annotation}.csv", index = False)