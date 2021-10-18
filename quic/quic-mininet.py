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

It uses a simple dumbbell topology. Clients connect to
the server in parallel.

Due to how quiche works this script has to be run from the quiche/examples/
directory.

The source code for quiche example client and server can be found at:
https://github.com/cloudflare/quiche/tree/master/examples
"""


class DumbbellTopo(Topo):
    def build(self, bw=100, delay='20ms', nl=4):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        # Left
        clients = list()
        for i in range(nl):
            client = self.addHost('hl{idx}'.format(idx=i+1))
            clients.append(client)
        for client in clients:
            self.addLink(client, s1, bw=bw, delay=delay)
        # Right
        hr1 = self.addHost('hr1')
        self.addLink(hr1, s2, bw=bw, delay=delay)

        self.addLink(s1, s2, bw=bw, delay=delay)


def run():
    topo = DumbbellTopo()
    net = Mininet(topo=topo, link=TCLink, autoPinCpus=True)

    net.start()
    CLI(net)
    time.sleep(1)

    clients = [
        net.get('hl1'),
        net.get('hl2'),
        net.get('hl3'),
        net.get('hl4')
    ]

    server = net.get('hr1')
    if not os.path.exists('data'):
        os.makedirs('data')

    server.cmd('sudo ./server ',
               server.IP(), ' 443 &> data/quic-server &')

    threads = list()
    for i in range(len(clients)):
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
    for i in range(5):
        client.cmd('sudo ./client ',
                   server.IP(), ' 443 &> data/quic-client-{num}-{idx} &'.format(num=num, idx=i))
        time.sleep(5)
        print(
            "*** Client {client_idx} done with iteration {idx}".format(client_idx=num, idx=i))


if __name__ == '__main__':
    run()
