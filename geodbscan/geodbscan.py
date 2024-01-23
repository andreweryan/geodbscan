import os
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn import metrics
from datetime import datetime
from sklearn.cluster import DBSCAN

import warnings

warnings.filterwarnings("ignore")


def get_centroid(cluster):
    """
    Calculate the centroid of a GeoDBSCAN cluster

    Args:
        cluster (list): List of cluster coordinates.
    Returns:
        centroid (float): Centroid of DBSCAN cluster

    """
    cluster_ary = np.asarray(cluster)
    centroid = cluster_ary.mean(axis=0)
    return centroid


def geodbscan(
    src,
    lat_col="latitude",
    lon_col="longitude",
    epsilon=100,
    min_points=10,
    unit="meters",
    workers=-1,
    out_dir=None,
    export_format="parquet",
):
    """
    Args:
        src (str, pd.DataFrame): Filepath or Pandas DataFrame of geospatial points to cluster
        epsilon (int): Max distance between two points to be considered in the neighborhood
        min_points (int): Min number of points required to constitute a cluster
        unit (str): Earth unit for Haversine distance metric.
        workers (int): Number of processors to use.
        out_dir (str): Directory path to write output files to.
        export_format (str): Format of output files (parquet or geojson), default=parquet (geoparquet)
    Returns:
        cluster_outputs (pd.DataFrame) : DataFrame with label of cluster each point is assigned to. Currently, points identified as noise (cluster -1) are removed as they did not meet the criteria for a cluster
    """

    if isinstance(src, pd.DataFrame):
        df = src
    elif isinstance(src, gpd.GeoDataFrame):
        df = src
        if not df.columns.isin([lat_col, lon_col]).any():
            df = pd.concat([df, df.centroid.x, df.centroid.y], axis=1)
            df.rename({0: lat_col, 1: lon_col}, axis=1, inplace=True)
        df = pd.DataFrame(df)
    elif isinstance(src, str) and src.endswith((".GeoJSON", ".geojson")):
        df = gpd.read_file(src)
        if not df.columns.isin([lat_col, lon_col]).any():
            df = pd.concat([df, df.centroid.x, df.centroid.y], axis=1)
            df.rename({0: lat_col, 1: lon_col}, axis=1, inplace=True)
        df = pd.DataFrame(df)
    elif isinstance(src, str) and src.endswith((".parquet")):
        df = gpd.read_parquet(src)
        if not df.columns.isin([lat_col, lon_col]).any():
            df = pd.concat([df, df.centroid.x, df.centroid.y], axis=1)
            df.rename({0: lat_col, 1: lon_col}, axis=1, inplace=True)
        df = pd.DataFrame(df)
    elif isinstance(src, str) and src.endswith((".CSV", ".csv")):
        df = pd.read_csv(src)
    else:
        raise ValueError("Source data not found or data reader not implemented.")

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    earth_radius = {
        "kilometers": 6371.009,
        "meters": 6371009,
        "miles": 3958.7614581,
        "feet": 20902260.49876800925,
    }

    r = earth_radius.get(unit)

    if not r:
        raise ValueError("Units not specified.")

    eps = epsilon / r

    coordinates = df[[lat_col, lon_col]].values

    start_time = datetime.now()
    print(f"Starting DBSCAN at {start_time}")

    dbsc = DBSCAN(
        eps=eps,
        min_samples=min_points,
        algorithm="ball_tree",
        metric="haversine",
        n_jobs=workers,
    ).fit(np.radians(coordinates))

    end_time = datetime.now()
    print(f"DBSCAN finished in {end_time - start_time}, starting post-processing.")

    cluster_labels = dbsc.labels_
    num_clusters = len(set(dbsc.labels_))

    print(f"Clustered {len(df)} points to {num_clusters} clusters.")

    # # Turn the clusters into a pandas series, where each element is a cluster of points
    dbsc_clusters = pd.Series(
        [coordinates[cluster_labels == n] for n in range(num_clusters)]
    )

    # # Get the centroid of each cluster
    centroids = dbsc_clusters.map(get_centroid)

    # # Unzip the list of centroid points (lat, long) tuples into separate lat and long lists
    cent_lats, cent_longs = zip(*centroids)

    # # Filter out the noise (points not assigned to a cluster), Output data with cluster assignments
    df["cluster_label"] = cluster_labels
    df_filtered = df[cluster_labels > -1]  # -1 is noise
    cluster_outputs = gpd.GeoDataFrame(
        df_filtered,
        geometry=gpd.points_from_xy(df_filtered[lon_col], df_filtered[lat_col]),
        crs="EPSG:4326",
    )
    if export_format == "parquet":
        cluster_parquet_path = os.path.join(out_dir, "cluster_outputs.parquet")
        cluster_outputs.to_parquet(cluster_parquet_path)
    else:
        cluster_geojson_path = os.path.join(out_dir, "cluster_outputs.geojson")
        cluster_outputs.to_file(cluster_geojson_path)

    # # get cluster counts
    cluster_counts = pd.DataFrame(df["cluster_label"].value_counts(), columns=["count"])
    cluster_counts.reset_index(inplace=True)
    cluster_counts = cluster_counts[cluster_counts["cluster_label"] > -1]
    cluster_counts["cluster_label"] = cluster_counts["cluster_label"].astype(int)
    cluster_counts.sort_values(by="cluster_label", ascending=True, inplace=True)

    # # Create a new df of one representative point for each cluster
    centroids_df = pd.DataFrame({"longitude": cent_longs, "latitude": cent_lats})
    centroids_df.index.rename("cluster_label", inplace=True)
    centroids_df.reset_index(inplace=True)
    centroids_df["cluster_label"] = centroids_df["cluster_label"].astype(int)
    centroids_df = pd.merge(centroids_df, cluster_counts, on="cluster_label")
    centroids_gdf = gpd.GeoDataFrame(
        centroids_df,
        geometry=gpd.points_from_xy(centroids_df[lon_col], centroids_df[lat_col]),
        crs="EPSG:4326",
    )
    if export_format == "parquet":
        centroid_parquet_path = os.path.join(out_dir, "cluster_centroids.parquet")
        centroids_gdf.to_parquet(centroid_parquet_path)
    else:
        centroid_geojson_path = os.path.join(out_dir, "cluster_centroids.geojson")
        centroids_gdf.to_file(centroid_geojson_path)

    return cluster_outputs
