#!/bin/bash
cd /root/github/econo/issues/angular/scripts/wifi

python3 dhcpAps.py
python3 dhcpLoadFromRadius.py
python3 dhcpLeases.py /var/lib/dhcp/dhcpd.leases
python3 generateDhcp.py /etc/dhcp/dhcpd.conf

python3 radiusUsers.py /etc/freeradius/radius-users

python3 generateFirewall.py /etc/init.d/firewall-manual


service isc-dhcp-server restart
service freeradius restart

source /etc/init.d/firewall
