import os
import time
from logging import error
from threading import Thread

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.topo import Topo

"""
This file provides a script to run the example client and server of quiche.

It uses a simple topology with 3 clients and one server. Clients connect to
the server in parallel.

Due to how quiche works this script has to be run from the quiche/examples/
directory.

The source code for quiche example client and server can be found at:
https://github.com/cloudflare/quiche/tree/master/examples
"""


class SingleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('switch1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch, bw=10)


def run():
    num_clients = 4
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo=topo, host=CPULimitedHost,
                  link=TCLink, autoPinCpus=True)

    net.start()
    CLI(net)
    time.sleep(1)

    clients = list()
    for i in range(num_clients - 1):
        client = net.get('h{idx}'.format(idx=i + 1))
        clients.append(client)

    server = net.get('h4')

    if not os.path.exists('data'):
        os.makedirs('data')

    server.cmd('sudo ./server ',
               server.IP(), ' 443 &> data/quic-server &')

    threads = list()
    for i in range(num_clients - 1):
        try:
            x = Thread(target=client_send, args=(clients[i], server, i + 1))
            x.daemon = True
            threads.append(x)
            x.start()
        except error:
            print(error)

    for thread in threads:
        thread.join()

    net.stop()


def client_send(client, server, num):
    print(client)
    for i in range(5):
        client.cmd('sudo ./client ',
                   server.IP(), ' 443 &> data/quic-client-{num}-{idx} &'.format(num=num, idx=i))
        time.sleep(5)
        print(
            "*** Client {client_idx} done with iteration {idx}".format(client_idx=num, idx=i))


if __name__ == '__main__':
    run()
