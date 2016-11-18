#!/bin/bash
cd /root/github/econo/issues/angular/scripts/wifi

python3 dhcpAps.py
python3 dhcpLoadFromRadius.py
python3 dhcpLeases.py /var/lib/dhcp/dhcpd.leases
python3 generateDhcp.py

python3 radiusUsers.py

python3 generateFirewall.py
