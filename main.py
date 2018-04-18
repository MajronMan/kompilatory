import sys
from matrix_parser import MatrixParser

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, 'r') as f:
        parser = MatrixParser()
        parser.run(f.read())
