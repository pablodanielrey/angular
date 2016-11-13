
"""

    ----------------------------
    Las redes wifi dentro de económicas están divididas en:

        10.x.0.0/17 ----> alumnos y accesos normales
        10.x.128.0/19 --> autoridades
        10.x.160.0/19 --> eventos
        10.x.192.0/19 --> video conferencias
        10.x.224.0/19 --> systemas admin
            10.x.224.0/26 ---> rango dinámico provisorio (10.x.224.1 -- 10.x.224.62)

    estas subredes valen a la hora de asignar ips fijas a macs y polítias de firewall.
    para el ruteo se hace suppernetting a la 10.x.0.0/16
    el gateway siempre es la ultima de la red.

        10.x.255.254 -- gateway
    -----------------------------


"""
import ipaddress

def wifiNetworks():
    ''' retorna las redes wifi de la facultad '''
    networks = [
        '10.8',
        '10.9',
        '10.10',
        '10.11',
        '10.12',
        '10.14',
        '10.15',
        '10.17',
        '10.18',
        '10.19',
        '10.20',
        '10.26'
    ]
    return [ipaddress.ip_network(n + '.0.0/16') for n in networks]

def wifiSubnets(n):
    ''' retorna las subredes determinadas para la facultad '''
    subn = list(n.subnets(new_prefix=17))
    general = subn[0]
    subn = list(subn[1].subnets(new_prefix=19))
    authorities = subn[0]
    events = subn[1]
    voip = subn[2]
    admin = subn[3]
    dynamic = list(subn[3].subnets(new_prefix=26))[0]

    return {
        'network': n,
        'general': general,
        'authorities': authorities,
        'events': events,
        'voip': voip,
        'admin': admin,
        'dynamic': dynamic
    }

def wifiDynamicRange(subnets):
    return {
        'start': subnets['dynamic'].network_address + 1,
        'end': subnets['dynamic'].broadcast_address - 1
    }

def gateway(n):
    return n.broadcast_address - 1
