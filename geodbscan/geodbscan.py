import os
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.cluster import DBSCAN


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
    df,
    lat_col="latitude",
    lon_col="longitude",
    epsilon=100,
    min_points=10,
    unit="meters",
    out_dir=None,
):
    """
    Args:
        df (pd.DataFrame): Pandas DataFrame of geospatial points to cluster
        epsilon (int): Max distance between two points to be considered in the neighborhood
        min_points (int): Min number of points required to constitute a cluster
        unit (str): Earth unit for Haversine distance metric.
        out_dir (str): Directory path to write output files to.
    Returns:
        cluster_outputs (pd.DataFrame) : DataFrame with label of cluster each point is assigned to. Currently, points identified as noise (cluster -1) are removed as they did not meet the criteria for a cluster
    """

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if unit == "miles":
        units = 3959.87433
    elif unit == "feet":
        units = 20908136.4624
    elif unit == "kilometers":
        units = 6372.8
    elif unit == "meters":
        units = 6372800
    else:
        raise ValueError("Units not specified.")

    eps = epsilon / units

    coordinates = df[[lat_col, lon_col]].values

    dbsc = DBSCAN(
        eps=eps, min_samples=min_points, algorithm="ball_tree", metric="haversine"
    ).fit(np.radians(coordinates))

    cluster_labels = dbsc.labels_

    num_clusters = len(set(dbsc.labels_))

    print(
        f"Clustered {len(df)} points to {num_clusters} for {100*(1 - float(num_clusters) / len(df))} compression"
    )

    """
    Silhouette Coefficient:
    This metric is bounded between -1 (poor clustering) and +1 (good clustering). Scores around 0 indicate overlapping clusters.
    """
    print(
        "Silhouette coefficient: {:0.03f}".format(
            metrics.silhouette_score(coordinates, cluster_labels)
        )
    )

    """
    Calinski-Harabaz Score:
    The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.
    """
    print(
        "Calinski-Harabaz Score: {:0.03f}".format(
            metrics.calinski_harabasz_score(coordinates, cluster_labels)
        )
    )

    # # Turn the clusters into a pandas series,where each element is a cluster of points
    dbsc_clusters = pd.Series(
        [coordinates[cluster_labels == n] for n in range(num_clusters)]
    )

    # # Get the centroid of each cluster
    centroids = dbsc_clusters.map(get_centroid)

    # # Unzip the list of centroid points (lat, long) tuples into separate lat and long lists
    cent_lats, cent_longs = zip(*centroids)

    # # Create a new df of one representative point for each cluster
    centroids_df = pd.DataFrame({"longitude": cent_longs, "latitude": cent_lats})
    centroid_path = os.path.join(out_dir, "cluster_counts.csv")
    centroids_df.to_csv(
        centroid_path,
        index=True,
        index_label=["cluster_label"],
        header=[lat_col, lon_col],
    )  # need to export to geospatial format

    # # Filter out the noise (points not assigned to a cluster)
    df["cluster_labels"] = cluster_labels
    cluster_counts = df["cluster_labels"].value_counts()
    count_path = os.path.join(out_dir, "cluster_counts.csv")
    cluster_counts.to_csv(
        count_path, index=True, index_label=["cluster_label"], header=["count"]
    )

    # # Output data with cluster assignments
    df_filtered = df[cluster_labels > -1]  # -1 is noise
    cluster_outputs = pd.DataFrame(df_filtered)
    cluster_path = os.path.join(out_dir, "cluster_outputs.csv")
    cluster_outputs.to_csv(
        cluster_path, index=False, header=True
    )  # need to export to geospatial format

    return cluster_outputs
