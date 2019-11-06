import argparse
from argparse import ArgumentTypeError
from pathlib import Path

from wrk2img import Parser, ImageGenerator


def parse_args():
    def color(value):
        if len(value) != 6:
            raise ArgumentTypeError("Invalid color. Should be hexadecimal like FFFFFF")
        else:
            return value

    parser = argparse.ArgumentParser(description="Transforming wrk results to image", usage="wrk --latency http://localhost.mono:8080 | wrk2img output.png")
    parser.add_argument("output", type=Path, help="output file")
    parser.add_argument("-b", "--background", type=color, default="FFFFFF", metavar="FFFFFF", help="background color")
    parser.add_argument("-t", "--transparent", action="store_true", help="use a transparent background")
    parser.add_argument("-l", "--log", action="store_true", help="use a log scale")
    parser.add_argument("-n", "--names", default=None, help="Comma-separated curve names in the order they are given")
    parser.add_argument("-m", "--max-latency", type=int, default=100, help="Cut-off value for the latency")
    return parser.parse_args()


def cli():
    args = parse_args()

    parser = Parser()
    image_generator = ImageGenerator(transparent=args.transparent, background=args.background, log_scale=args.log)

    curve_names = args.names.split(",") if args.names is not None else []
    data, website = parser.parse_stdin(curve_names=curve_names)
    image_generator.generate_and_save_image(data, website, args.output, latency_until=args.max_latency)


# TODO: Create another cli to generate multiple wrk2 call to one website and generate plot

if __name__ == '__main__':
    cli()
