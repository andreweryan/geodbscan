# GeoDBSCAN: Implementing the DBSCAN clustering algorithm for geospatial coordinates

Task List
- [ ] Update README with installation, usage, etc.
- [x] Change geodbscan function args to accept df or filepath
- [x] Change function to accept multiple file types beyond CSV
- [ ] Export clustered points to GeoJSON, parquet, etc. 
- [ ] Write unit tests
- [ ] Write CLI

## Installation:


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