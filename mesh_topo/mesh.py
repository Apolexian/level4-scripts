import os
import time
from logging import error
from threading import Thread

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Host


class MeshHostsConfig():
    def __init__(self, num_switches, nodes_per_switch):
        self.num_switches = num_switches
        self.nodes_per_switch = nodes_per_switch


class LinkConfig():
    def __init__(self, bw, delay, packet_loss):
        self.bandwidth = bw
        self.delay = delay
        self.packet_loss = packet_loss


class MeshTopo(Topo):
    def build(self, hosts_config, link_config):
        switches = []
        for i in range(hosts_config.num_switches):
            s = self.addSwitch(f's{i}')
            switches.append([s, []])
            for j in range(hosts_config.nodes_per_switch):
                h = self.addHost(f'h{i}{j}', cls=Host, defaultRoute=None)
                self.addLink(
                    switches[i][0], h, bw=link_config.bandwidth, delay=link_config.delay)
                switches[i][1].append(h)

        for s in switches:
            hosts = s[1]
            for i in range(len(hosts)):
                for j in range(i + 1, len(hosts)):
                    self.addLink(
                        hosts[i], hosts[j], bw=link_config.bandwidth, delay=link_config.delay)

        h = self.addHost('h9')
        s = self.addSwitch(f's9', failmode='standalone', stp=True)
        self.addLink(s, h, bw=link_config.bandwidth, delay=link_config.delay)
        for sw in switches:
            self.addLink(sw[0], s, bw=link_config.bandwidth,
                         delay=link_config.delay)


def run():
    hosts_config = MeshHostsConfig(2, 5)
    link_config = LinkConfig(100, '20ms', 5)
    topo = MeshTopo(hosts_config, link_config)
    net = Mininet(topo=topo, link=TCLink, autoPinCpus=True)
    net.start()

    CLI(net)
    time.sleep(1)

    broker = net.get('h9')
    clients = []
    h13 = net.get('h13')
    clients.append(h13)

    broker.cmd('./broker > data/mqtt-broker &')

    if not os.path.exists('data'):
        os.makedirs('data')

    threads = list()
    for i in range(len(clients) - 1):
        try:
            x = Thread(target=client_send, args=(clients[i], broker, i + 1))
            x.daemon = True
            threads.append(x)
            x.start()
        except error:
            print(error)

    for thread in threads:
        thread.join()

    net.stop()


def client_send(client, broker, num):
    client.cmd(
        './client ', broker.IP(), '&> data/mqtt-client-{num} &'.format(num=num))
    time.sleep(5)


if __name__ == '__main__':
    run()
