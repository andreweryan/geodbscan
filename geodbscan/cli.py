import argparse
from .geodbscan import geodbscan


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--arg",
        nargs="*",
        required=True,
        help="",
    )

    args = parser.parse_args()

    geodbscan(args.arg)


if __name__ == "__main__":
    main()
