import sys

archivo = sys.argv[1]

f = open(archivo, 'r')

conjunto = set()

try:
    #print(f.readline())
    for line in f:
        if 'hardware ethernet' in line:
            x = (line[20:-2])
            conjunto.add(x)
    print(conjunto)
    print(len(conjunto))
finally:
    f.close()



#mac = r['callingstationid'].replace('-',':').upper()
