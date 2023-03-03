from ns2_node_util import Ns2NodeUtility
from phy_util import PhyUtil
from ip_util import IpUtil

import ns.network
import ns.mobility
import ns.applications
import ns.netanim

from config import CONFIG, MOBILITY_TCL
from log_helper import dbg

from app_util import AppUtil

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

def main():
	mobility_file = MOBILITY_TCL
	node_util = Ns2NodeUtility(mobility_file)

	nnodes = node_util.get_n_nodes()
	sim_time = node_util.get_simulation_time()

	node_util.print_information()

	dbg.log(f'ns2 mobility tcl parsed')
	dbg.log(f'number of nodes: {nnodes}, simulation time: {sim_time}')

	nodes = ns.network.NodeContainer()
	nodes.Create(nnodes)

	sumo_trace = ns.mobility.Ns2MobilityHelper(mobility_file) 
	sumo_trace.Install()

	# mobility = ns.mobility.MobilityHelper()
	# mobility.SetPositionAllocator ("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0), 
	# 							"MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(5.0), "DeltaY", ns.core.DoubleValue(10.0), 
  #                                "GridWidth", ns.core.UintegerValue(3), "LayoutType", ns.core.StringValue("RowFirst"))
                                 
	# mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
	# mobility.Install(nodes)

	dbg.log('ns2 mobility configured')

	phy_util = PhyUtil(CONFIG)
	phy_util.install(nodes)

	ip_util = IpUtil(CONFIG)
	ip_util.assign_address(nodes, phy_util)
	ip_util.connect(nodes, phy_util.get_enb_node_ids())
	ip_util.connect(nodes, phy_util.get_ap_node_ids())
	

	ip_util.populate()

	app_util = AppUtil(CONFIG)
	app_util.install(nodes)

	anim = ns.netanim.AnimationInterface('trace.xml');

	ns.core.Simulator.Stop(ns.core.Seconds(204))
	ns.core.Simulator.Run()
	ns.core.Simulator.Destroy()

if __name__ == '__main__':
	main()