import sys
from state import State
from expressions import Program

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: python3 src/main.py <file>")
        exit(1)

    Program(State(sys.argv[1], 0))
