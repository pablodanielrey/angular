from redmine import Redmine
import sys

host = sys.argv[1]
key = sys.argv[2]

redmine = Redmine(host, key = key, version='3.3', requests={'verify': False})


pedidos = {}


for i in redmine.issue.all():
    t = str(i.tracker)
    if t not in pedidos:
        pedidos[t] = []
    pedidos[t].append(i)


for p in pedidos.keys():
    print(p)
    print(len(pedidos[p]))
    for i in pedidos[p]:
        print(i.author)
        for c in i.custom_fields:
            print(c)
