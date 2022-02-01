import os
import time
from logging import error
from threading import Thread

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.topo import Topo

class MeshHostsConfig():
    def __init__(self, num_switches, nodes_per_switch):
        self.num_switches = num_switches
        self.nodes_per_switch = nodes_per_switch

class MeshTopo(Topo):
    def build(self, hosts_config, bw=100, delay='20ms', nl=4):
        switches = []
        for i in range(hosts_config.num_switches):
            s = self.addSwitch(f's{i}', failmode='standalone', stp=True)
            switches.append([s, []])
            for j in range(hosts_config.nodes_per_switch):
                h = self.addHost(f'h{i}{j}')
                self.addLink(switches[i][0], h, bw=bw, delay=delay)
                switches[i][1].append(h)
        
        for i in range(len(switches)):
            for j in range(i + 1, len(switches)):
                self.addLink(switches[i][0], switches[j][0], bw=bw, delay=delay)
        
        for s in switches:
            hosts = s[1]
            for i in range(len(hosts)):
                for j in range(i + 1, len(hosts)):
                    self.addLink(hosts[i], hosts[j], bw=bw, delay=delay)
        
        h = self.addHost('h9')
        s = self.addSwitch(f's9', failmode='standalone', stp=True)
        self.addLink(s, h, bw=bw, delay=delay)
        for sw in switches:
            self.addLink(sw[0], s, bw=bw, delay=delay)

def run():
    hosts_config = MeshHostsConfig(3, 4)
    topo = MeshTopo(hosts_config)
    net = Mininet(topo=topo, link=TCLink, autoPinCpus=True)

    net.start()
    CLI(net)
    time.sleep(1)
    
    broker = net.get('h9')
    clients = []
    h_22 = net.get('h22')
    h_12 = net.get('h12')
    clients.append(h_22)
    clients.append(h_12)

    if not os.path.exists('data'):
        os.makedirs('data')

    broker.cmd('./broker/target/release/broker > data/mqtt-broker &')

    threads = list()
    for i in range(len(clients)):
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
    for i in range(5):
        client.cmd('./client/target/release/client ', broker.IP(),
                   '> data/mqtt-client-{num}-{idx} &'.format(num=num, idx=i))
        time.sleep(5)
        print(
            "*** Client {client_idx} done with iteration {idx}".format(client_idx=num, idx=i))


if __name__ == '__main__':
    run()