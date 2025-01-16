from skimage import io, color, filters, measure
import pandas as pd

for index_of_annotation in range(0, 105 + 1):

    if index_of_annotation in [3, 5, 6, 10, 11, 12, 16, 18, 20, 23, 24, 25, 27, 28, 29, 31, 32, 33, 40, 41, 43, 44, 45, 46, 47, 48, 50, 51, 58, 59, 61, 62, 64, 65, 66, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 84, 86, 87, 88, 90, 91, 92, 93, 94, 96, 97, 98, 102, 103, 104, 105]:
        # I will likely receive error, "OSError: image file is truncated (720 bytes not processed)".
        continue

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

    dictionary_of_property_names_and_values = measure.regionprops_table(ndarray_of_labels, properties=['label', 'centroid'])

    data_frame_of_properties = pd.DataFrame(dictionary_of_property_names_and_values)
    data_frame_of_properties.rename(columns={'centroid-0': 'y', 'centroid-1': 'x'}, inplace = True)

    data_frame_of_coordinate_pairs = data_frame_of_properties[["x", "y"]]
    data_frame_of_coordinate_pairs = data_frame_of_coordinate_pairs.round().astype(int)
    data_frame_of_coordinate_pairs.to_csv(f"coordinates_of_centroids_{index_of_annotation}.csv", index = False)