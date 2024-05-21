import sys
from state import State
from expressions import Program

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: python3 src/main.py <file>")
        exit(1)

    path = sys.argv[1]

    if path.split('.')[1] != "kd":
        print("ERROR: invalid file extension. Use '*.kd'")

    Program(State(path, 0))
