#!/usr/bin/env python3
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print('Content-Type: text/html; charset=utf-8')
print()
print('<html><body><pre></pre>h€lló wörld<body></html>')
