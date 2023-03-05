from ns2_node_util import Ns2NodeUtility
from phy_util import PhyUtil
from ip_util import IpUtil

import ns.core
import ns.network
import ns.mobility
import ns.applications
import ns.netanim

import sys, json

from config import CONFIG, MOBILITY_TCL
from log_helper import dbg

from app_util import AppUtil

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

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
    config = CONFIG
  else:
    with open(config, 'r') as f:
      config = json.loads(f.read())
  
  sim_time = config['max_at']
  if validate != 0:
    sim_time = 1

  node_util = Ns2NodeUtility(mobility_file)
  nnodes = node_util.get_n_nodes()
  node_util.print_information()

  dbg.log(f'ns2 mobility tcl parsed')
  dbg.log(f'number of nodes: {nnodes}, simulation time: {sim_time}')

  nodes = ns.network.NodeContainer()
  nodes.Create(nnodes)

  # mobility = ns.mobility.MobilityHelper()
  # mobility.SetPositionAllocator ("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0), 
  #               "MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(5.0), "DeltaY", ns.core.DoubleValue(10.0), 
  #                                "GridWidth", ns.core.UintegerValue(3), "LayoutType", ns.core.StringValue("RowFirst"))
                                 
  # mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel", "Bounds", ns.mobility.RectangleValue(ns.mobility.Rectangle (-50, 50, -50, 50)))
  # mobility.Install(nodes)

  sumo_trace = ns.mobility.Ns2MobilityHelper(mobility_file) 
  sumo_trace.Install()  

  dbg.log('ns2 mobility configured')

  ip_util = IpUtil(config)

  phy_util = PhyUtil(config, ip_util)
  phy_util.install(nodes)

  app_util = AppUtil(config)
  app_util.install(nodes)
  
  anim = ns.netanim.AnimationInterface(f'{traceloc}/trace.xml');

  ns.core.Simulator.Stop(ns.core.Seconds(sim_time))
  ns.core.Simulator.Run()
  ns.core.Simulator.Destroy()

if __name__ == '__main__':
  main(sys.argv)