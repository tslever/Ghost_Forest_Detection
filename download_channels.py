import ee
import geemap
import pandas as pd
import os


output_dir = "./data/channels"
os.makedirs(output_dir, exist_ok = True)


try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project="ghost-forest-detection")

df = pd.read_csv("positions_of_centroids_of_images_and_locations_in_LA_and_TX.csv")

states = ee.FeatureCollection("TIGER/2018/States")
la_geometry = states.filter(ee.Filter.eq("NAME", "Louisiana")).geometry()
tx_geometry = states.filter(ee.Filter.eq("NAME", "Texas")).geometry()

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

    lat = row["Latitude"]
    lon = row["Longitude"]
    point = ee.Geometry.Point([lon, lat])
    state_name, year_str = get_state_and_year(point)

    start_date = f"{year_str}-04-01"
    end_date   = f"{year_str}-10-31"

    print(f"Index {idx} | Lat: {lat}, Lon: {lon} | State: {state_name} | Year: {year_str}")

    image_collection = (ee
        .ImageCollection("USDA/NAIP/DOQQ")
        .filterDate(start_date, end_date)
        .filterBounds(point)
    )

    if image_collection.size().getInfo() == 0:
        print(f"No images found for index {idx}. Skipping...")
        continue

    for channel in ["R", "G", "B", "N"]:
        image = image_collection.median().visualize(
            bands=[channel],
            min=0,
            max=255
        )

        region = point.buffer(1_000).bounds()

        out_file = os.path.join(output_dir, f"{channel.lower()}_{idx}.tif")

        geemap.ee_export_image(
            ee_object=image,
            filename=out_file,
            scale=0.6,
            region=region,
            file_per_band=False,
            format="ZIPPED_GEO_TIFF",
            unzip=True,
            timeout=300
        )

        print(f"Exported: {out_file}\n")