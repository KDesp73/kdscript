#!/usr/bin/env python3

from logger import ERRO, INFO
import utils
from preprocessor import Preprocessor
from state import State
from expressions import Program
import argparse

def add_hashmaps(hash1: dict, hash2: dict):
    for key in hash2.keys():
        hash1[key] = hash2[key]

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

    file = args.filename
    preprocessor = Preprocessor(file)
    preprocessor.run()

    state = State(file, preprocessor.state.source)
    for scope in preprocessor.scopes:
        if state.scope.scopes.head != None and scope.head != None:
            add_hashmaps(state.scope.scopes.head.data, scope.head.data)

    utils.enable_ansi_escape_codes()
    try:
        Program(state)
    except KeyboardInterrupt:
        print()
        INFO("Terminated by user")
        exit(1)



if __name__ == "__main__":
    main()
