from logger import ERRO
from state import State
from expressions import Program
import argparse

def main():
    args_parser = argparse.ArgumentParser(
            prog='kdscript',
            description='A simple interpreter',
            epilog='Made by KDesp73')

    args_parser.add_argument('filename')

    args_parser.add_argument(
            '-v', '--version',
            action='version',
            version='kdscript 0.0.1 (beta)',
            help='print executable version')

    args = args_parser.parse_args()

    if args.filename.rsplit('.', 1)[1] != "kd":
        ERRO("Invalid file extension", "Use '*.kd'")
        exit(1)

    Program(State(args.filename, 0))


if __name__ == "__main__":
    main()
