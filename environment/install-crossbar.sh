#!/bin/bash
./pypy-2.6-linux_x86_64-portable/bin/pypy get-pip.py
./pypy-2.6-linux_x86_64-portable/bin/pip install crossbar[tls,msgpack,manhole,system]
