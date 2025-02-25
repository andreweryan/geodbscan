# GeoDBSCAN: Implementing the DBSCAN clustering algorithm for geospatial coordinates

Task List
- [x] Update README with installation, usage, etc.
- [x] Change geodbscan function args to accept df or filepath
- [x] Change function to accept multiple file types beyond CSV
- [x] Export clustered points to GeoJSON, parquet, etc. 
- [ ] Write unit tests
- [x] Write CLI

## Installation:
GeoDBSCAN relies on GDAL and associated geospatial packages such as geopandas, etc.
Depending on your OS and development environment, the installation of those packages varies with 
Windows being more challenging (but not impossible). Because of these complexities around
installing GDAL on Windows, Linux is the preferred OS for installation.

## Linux Installation:
On Linux, install GDAL using `apt-get` and add GDAL to your environment path
```
sudo apt-get install gdal-bin -y
sudo apt-get install libgdal-dev -y
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
```

Create and activate a new conda (or venv) environment and pip install the remainder of the dependencies using `pip install -r requirements.txt`

## Usage:

Package import usage:
```python
import pandas as pd
from geodbscan import geodbscan

df = pd.read_csv(r'test_points.csv')
out_dir = r'dbscan_output'
geodbscan(df, lat_col='X', lon_col='Y', epsilon=50, min_points=5, unit='meters', out_dir=out_dir)

```

CLI usage:

```
usage: geodbscan [-h] --src SRC --lat_col LAT_COL --lon_col LON_COL --epsilon EPSILON --min_points MIN_POINTS --unit
                 UNIT --out_dir OUT_DIR

optional arguments:
  -h, --help            show this help message and exit
  --src SRC             File path of points to cluster.
  --lat_col LAT_COL     Column name containing latitude coordinate
  --lon_col LON_COL     Column name containing longtiude coordinate
  --epsilon EPSILON     Max distance between two points to be considered in the neighborhood
  --min_points MIN_POINTS
                        Min number of points required to constitute a cluster
  --unit UNIT           Earth unit for Haversine distance metric.
  --out_dir OUT_DIR     Directory path to write output files to.
```

Example: `geodbscan --src C:\Users\andrr\Desktop\test_points.geojson --lat_col Latitude --lon_col Longitude --epsilon 50 --min_points 5 --unit meters --out_dir C:\Users\andrr\Desktop\dbscan_outputs`
