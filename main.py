from ns2_node_util import Ns2NodeUtility
from phy_util import PhyUtil

from ns.network import NodeContainer
from ns.mobility import *

from config import CONFIG
from log_helper import dbg

def main():
	mobility_file = '/home/ondro/skola/tp/sumo_to_ns3_py/ns2mobility.tcl'
	node_util = Ns2NodeUtility(mobility_file)

	nnodes = node_util.get_n_nodes()
	sim_time = node_util.get_simulation_time()

	dbg.log(f'ns2 mobility tcl parsed')
	dbg.log(f'number of nodes: {nnodes}, simulation time: {sim_time}')

	nodes = NodeContainer()
	nodes.Create(nnodes)

	sumo_trace = Ns2MobilityHelper(mobility_file) 
	sumo_trace.Install()

	dbg.log('ns2 mobility configured')

	phy_util = PhyUtil(CONFIG)
	phy_util.install(nodes)


if __name__ == '__main__':
	main()