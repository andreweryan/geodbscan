import argparse
from .geodbscan import geodbscan


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--src",
        type=str,
        required=True,
        help="File path of points to cluster.",
    )
    parser.add_argument(
        "--lat_col",
        type=str,
        default="Latitude",
        required=True,
        help="Column name containing latitude coordinate",
    )
    parser.add_argument(
        "--lon_col",
        type=str,
        default="Longitude",
        required=True,
        help="Column name containing longtiude coordinate",
    )
    parser.add_argument(
        "--epsilon",
        type=int,
        default=100,
        required=True,
        help="Max distance between two points to be considered in the neighborhood",
    )
    parser.add_argument(
        "--min_points",
        type=int,
        default=10,
        required=True,
        help="Min number of points required to constitute a cluster",
    )
    parser.add_argument(
        "--unit",
        type=str,
        default="meters",
        required=True,
        help="Earth unit for Haversine distance metric.",
    ),
    parser.add_argument(
        "--out_dir",
        required=True,
        help="Directory path to write output files to.",
    )

    args = parser.parse_args()

    geodbscan(
        args.src,
        lat_col=args.lat_col,
        lon_col=args.lon_col,
        epsilon=args.epsilon,
        min_points=args.min_points,
        unit=args.unit,
        out_dir=args.out_dir,
    )


if __name__ == "__main__":
    main()
