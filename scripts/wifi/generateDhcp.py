
import inject
from model.dhcp.dhcp import Dhcp, DhcpHost, DhpNetwork


if __name__ == '__main__':

    d = Dhcp()

    reg = inject.instance(Registry)
    conn = Connection(reg.getRegistry('dcsys'))
    con = conn.get()
    try:
        Connection.readOnly(con)
        d.hosts = DhcpHost.findAll(con)
        d.networks = DhcpNetwork.findAll(con)
    finally:
        conn.put(con)

    with open('/tmp/p.txt','w') as f:
        d.toFile(f)
