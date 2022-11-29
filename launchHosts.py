'''
File to launch mininet, and create three hosts on the same network'''

import mininet
from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI  # import command line input


def start():
    setLogLevel('info')

    # create a network where I can have my 3 hosts
    network = Mininet(SingleSwitchTopo(k=3))
    network.start()

    # start gathering command line input
    CLI(network)

    ''' the rest will be done through the command line prompt, 
    so no need to add anything else, this file is just for creating 3 hosts on the same network
    '''
    # close the network
    network.stop()


if __name__ == '__main__':
    start()
