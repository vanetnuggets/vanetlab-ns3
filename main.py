import sys
from ns2_node_util import Ns2NodeUtility
from ns import ns
import sys, json

from argparse import ArgumentParser
from config2 import CONFIG, MOBILITY_TCL
from log_helper import dbg

from phy_util import PhyUtil
from ip_util import IpUtil
from app_util import AppUtil
from sdn_manager import SdnManager

import context
import signal

def ezfix(signum, frame):
    print('som ta chytil ne')

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("BulkSendApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("PacketSink", ns.core.LOG_LEVEL_INFO)

def main(argv):
  signal.signal(signal.SIGALRM, ezfix)
  parser = ArgumentParser(
    prog='VanetLab ns3 scenario maker',
    description='complex ns3 scenario maker backend for VanetLab',
    epilog='caw'
  )
  parser.add_argument('-c', '--config')
  parser.add_argument('-m', '--mobility')
  parser.add_argument('-t', '--traceloc')
  parser.add_argument('-v', '--validate')

  args = parser.parse_args()

  mobility_file = str(args.mobility) if args.mobility is not None else None
  config = str(args.config) if args.config is not None else None
  traceloc = str(args.traceloc) if args.traceloc is not None else '.'
  validate = int(args.validate) if args.validate is not None else 0
  context.path = traceloc

  if mobility_file == None:
    mobility_file = MOBILITY_TCL
  
  if config is None:
    context.config = CONFIG
  else:
    with open(config, 'r') as f:
      context.config = json.loads(f.read())
  
  sim_time = context.config['max_at']
  context.init()
  
  if validate != 0:
    sim_time = 1

  node_util = Ns2NodeUtility(mobility_file)
  nnodes = node_util.get_n_nodes()
  node_util.print_information()

  dbg.log(f'ns2 mobility tcl parsed')
  dbg.log(f'number of nodes: {nnodes}, simulation time: {sim_time}')
  
  t = node_util.get_max_node()
  context.nodes = ns.network.NodeContainer()
  context.nodes.Create(t)

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
  
  dbg.log('installing physical layer...')
  context.phy_util = PhyUtil(context.config, context.ip_util)
  context.phy_util.install(context.nodes)
  dbg.log('installed physical layer')
  
  dbg.log('installing p2p connections...')
  context.ip_util.install_connections()
  dbg.log('added p2p connections...')
 
  dbg.log('installing applications...')
  context.app_util = AppUtil(context.config)
  context.app_util.install(context.nodes)
  dbg.log('applications installed')

  SdnManager()
  dbg.log('sdn added')
  
  anim = ns.netanim.AnimationInterface(f'{traceloc}/trace.xml')
  dbg.log('starting simulation')
  ns.core.Simulator.Stop(ns.core.Seconds(sim_time))
  ns.core.Simulator.Run()
  ns.core.Simulator.Destroy()
if __name__ == '__main__':
  main(sys.argv)
  sys.exit(0)
