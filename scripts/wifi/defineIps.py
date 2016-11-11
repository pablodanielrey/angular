

if __name__ == '__main__':

    import sys

    init = int(sys.argv[1])
    final = int(sys.argv[2])
    dev = sys.argv[3]

    if init > final:
        sys.exit(1)

    with open(sys.argv[4], 'w') as f:
        while init <= final:
            f.write("""
                up   ip addr add 163.10.17.{0}/25 dev {1} label {1}:{0}
                down ip addr del 163.10.17.{0}/25 dev {1} label {1}:{0}
            """.format(init, dev))
            init = init + 1
