#!/bin/bash

cd /root/github/angular/scripts/wifi

python3 dhcpAps.py
sleep 60s

python3 dhcpLoadFromRadius.py
sleep 60s

python3 dhcpLeases.py /tmp/dhcpd.leases
sleep 60s

python3 radiusUsers.py
sleep 60s

python3 generateFirewall.py
sleep 60s

python3 generateDhcp.py
sleep 60s
