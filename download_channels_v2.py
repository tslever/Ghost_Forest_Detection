# This script download NAIP imagery directly to local drive. Each imagery should contain 4 bands stored in GeoTiff.

import ee
import geemap
import pandas as pd
import numpy as np
import os

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project="ghost-forest-detection")

# Define paths
df = pd.read_csv("positions_of_centroids_of_images_and_locations_in_LA_and_TX.csv")
output_dir = "./data/channels"

# Define parameters
scale = 0.6 # Target pixel resolution
img_dimension = [512, 512] # Target image dimension (pixels)
tg_crs = "EPSG:5070" # Target projection (Equal-area)


states = ee.FeatureCollection("TIGER/2018/States")
la_geometry = states.filter(ee.Filter.eq("NAME", "Louisiana")).geometry()
tx_geometry = states.filter(ee.Filter.eq("NAME", "Texas")).geometry()

# Make directory if not already exist
os.makedirs(output_dir, exist_ok = True)

def get_state_and_year(point):
    if la_geometry.contains(point).getInfo():
        return ("Louisiana", "2023")
    elif tx_geometry.contains(point).getInfo():
        return ("Texas", "2022")
    else:
        return ("Other", "2021")


for idx, row in df.iterrows():
    
    if idx > 10:
        break

    # Extract coordinates
    lat = row["Latitude"]
    lon = row["Longitude"]
    point = ee.Geometry.Point([lon, lat])
    state_name, year_str = get_state_and_year(point)

    # Filter by NAIP year
    start_date = f"{year_str}-01-01"
    end_date   = f"{year_str}-12-31"

    print(f"Index {idx} | Lat: {lat}, Lon: {lon} | State: {state_name} | Year: {year_str}")

    # Generate buffer radius using equal area projection
    buffer_radius = np.floor((scale * img_dimension[1]) / 2)
    region = point.buffer(buffer_radius, proj=tg_crs).bounds(proj=tg_crs)

    # Image data
    image_collection = (
        ee.ImageCollection("USDA/NAIP/DOQQ")
        .filterDate(start_date, end_date)
        .filterBounds(region)
    )

    if image_collection.size().getInfo() == 0:
        print(f"No images found for index {idx}. Skipping...")
        continue

    image = image_collection.mosaic()

    out_file = os.path.join(output_dir, f"naip_{idx}.tif")

    geemap.ee_export_image(
        ee_object=image,
        filename=out_file,
        scale=scale,
        region=region,
        crs=tg_crs,
        file_per_band=False,
        format="ZIPPED_GEO_TIFF",
        unzip=True,
        timeout=300
    )

    print(f"Exported: {out_file}\n")

