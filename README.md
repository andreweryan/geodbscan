# GeoDBSCAN: Implementing the DBSCAN clustering algorithm for geospatial coordinates

Task List
- [ ] Update README with installation, usage, etc.
- [ ] Change geodbscan function args to accept df or filepath
- [ ] Change function to accept multiple file types beyond CSV
- [ ] Export clustered points to GeoJSON, parquet, etc. 
- [ ] Write unit tests
- [ ] Write CLI

```python
import pandas as pd
from geodbscan import geodbscan

df = pd.read_csv(r'test_points.csv')
out_dir = r'dbscan_output'
geodbscan(df, lat_col='X', lon_col='Y', epsilon=50, min_samples=5, unit='meters', out_dir=out_dir)

```