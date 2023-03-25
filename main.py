from ns2_node_util import Ns2NodeUtility


import ns.core
import ns.network
import ns.mobility
import ns.applications
import ns.netanim

import sys, json

from config import CONFIG, MOBILITY_TCL
from log_helper import dbg

from phy_util import PhyUtil
from ip_util import IpUtil
from app_util import AppUtil

import context

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("BulkSendApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("PacketSink", ns.core.LOG_LEVEL_INFO)

def main(argv):
  cmd = ns.core.CommandLine()
  
  cmd.config = ""
  cmd.mobility = ""
  cmd.traceloc = "."
  cmd.validate = 0

  cmd.AddValue("config", "VanetLab config to load")
  cmd.AddValue("mobility", "ns2 mobility tcl to use")
  cmd.AddValue("traceloc", "path where netanim trace should be saved")
  cmd.AddValue("validate", "only validates the scenario if true")

  cmd.Parse(sys.argv)

  mobility_file = str(cmd.mobility)
  config = str(cmd.config)
  traceloc = str(cmd.traceloc)
  validate = int(cmd.validate)

  if mobility_file == "":
    mobility_file = MOBILITY_TCL
  
  if config == "":
    context.config = CONFIG
  else:
    with open(config, 'r') as f:
      context.config = json.loads(f.read())
  
  sim_time = context.config['max_at']
  if validate != 0:
    sim_time = 1

  node_util = Ns2NodeUtility(mobility_file)
  nnodes = node_util.get_n_nodes()
  node_util.print_information()

  dbg.log(f'ns2 mobility tcl parsed')
  dbg.log(f'number of nodes: {nnodes}, simulation time: {sim_time}')
  
  context.nodes = ns.network.NodeContainer()
  context.nodes.Create(nnodes)

  # mobility = ns.mobility.MobilityHelper()
  # mobility.SetPositionAllocator ("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0), 
  #               "MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(5.0), "DeltaY", ns.core.DoubleValue(10.0), 
  #                                "GridWidth", ns.core.UintegerValue(3), "LayoutType", ns.core.StringValue("RowFirst"))
                                 
  # mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
  # mobility.Install(nodes)

  sumo_trace = ns.mobility.Ns2MobilityHelper(mobility_file) 
  sumo_trace.Install()  

  dbg.log('ns2 mobility configured')

  context.ip_util = IpUtil(context.config)

  context.phy_util = PhyUtil(context.config, context.ip_util)
  context.phy_util.install(context.nodes)

  context.ip_util.install_connections()
  
  context.app_util = AppUtil(context.config)
  context.app_util.install(context.nodes)
  
  
  anim = ns.netanim.AnimationInterface(f'{traceloc}/trace.xml');

  ns.core.Simulator.Stop(ns.core.Seconds(sim_time))
  ns.core.Simulator.Run()
  ns.core.Simulator.Destroy()

if __name__ == '__main__':
  main(sys.argv)
  exit(0)