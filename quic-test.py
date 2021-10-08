from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from pathlib import Path
from mininet.node import RemoteController
import os
import time

REMOTE_CONTROLLER_IP = "127.0.0.1"


class SingleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch, bw=10)


def run():
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo, link=TCLink,
                  controller=None,
                  autoStaticArp=True)
    net.addController("c0",
                      controller=RemoteController,
                      ip=REMOTE_CONTROLLER_IP,
                      port=6633)
    net.start()
    time.sleep(1)
    dumpNodeConnections(net.hosts)
    if not os.path.exists('data'):
        os.makedirs('data')
        Path('data/quic-client').touch()
        Path('data/quic-server').touch()
        Path('data/quic-ping').touch()

    client = net.get('h1')
    server = net.get('h2')

    client.cmd('ping ', server.IP(), '5006 &> data/quic-ping &')

    server.cmd('./quiche/examples/server ',
               server.IP(), ' 5006 &> data/quic-server &')
    for _ in range(5):
        client.cmd('./quiche/examples/client ',
                   server.IP(), ' 5006 &> data/quic-client &')
        time.sleep(1)

    net.stop()


if __name__ == '__main__':
    run()
