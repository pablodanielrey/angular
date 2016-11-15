import sys

archivo = sys.argv[1]

with open(archivo, 'r') as f:
    print(f.read())
