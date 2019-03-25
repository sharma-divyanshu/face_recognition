import sys
import argparse

parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument(
    'image', type=str,
    help='path to image file, default'
)

print(parser.parse_args().image)