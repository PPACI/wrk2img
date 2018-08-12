import argparse
from pathlib import Path

from wrk2img import Parser, ImageGenerator


def parse_args():
    parser = argparse.ArgumentParser(description="Transforming wrk results to image", usage="wrk --latency http://localhost:8080 | wrk2img output.png")
    parser.add_argument("output", type=Path, help="output file")
    parser.add_argument("-b", "--background", type=str, help="background color")
    parser.add_argument("-t", "--transparent", type=str, help="use a transparent background")
    return parser.parse_args()


def cli():
    parser = Parser()
    image_generator = ImageGenerator()
    args = parse_args()

    data = parser.parse_stdin()
    # TODO: convert data to matplotlib
    # TODO: save matplotlib


if __name__ == '__main__':
    cli()
