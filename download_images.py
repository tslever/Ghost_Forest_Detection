import ee
import geemap
import pandas as pd

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project = "ghost-forest-detection")

df = pd.read_csv("positions_of_centroids_of_images_and_locations_in_LA_and_TX.csv")

start_date = '2021-04-01'
end_date   = '2021-10-31'

for idx, row in df.iterrows():
    if idx > 10:
        break

    lat = row['Latitude']
    lon = row['Longitude']
    
    point = ee.Geometry.Point([lon, lat])
    region = point.buffer(1_000).bounds()
    
    image_collection = ee.ImageCollection("COPERNICUS/S2_HARMONIZED").filterDate(start_date, end_date).filterBounds(point)

    if image_collection.size().getInfo() == 0:
        print(f"No images found for index {idx}. Skipping...")
        continue

    image = image_collection.median().visualize(
        bands = ['B4', 'B3', 'B2'],
        min = 0,
        max = 3000
    )
    
    out_file = f"satellite_image_{idx}.tif"
    geemap.ee_export_image(
        ee_object = image,
        filename = out_file,
        scale = 1,
        crs = None,
        crs_transform = None,
        region = region,
        dimensions = None,
        file_per_band = False,
        format = "ZIPPED_GEO_TIFF",
        unzip = True,
        unmask_value = None,
        timeout = 300,
        proxies = None
    )
    
    print(f"Exported: {out_file}")