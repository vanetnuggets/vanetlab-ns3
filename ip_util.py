from ipaddress import IPv4Network

import ns.internet
import ns.network
import ns.point_to_point
import ns.mobility
import ns.olsr

from log_helper import dbg

class IpUtil:
  stack = {}
  netmap = {}
  root = None

  def __init__(self, config):
    self.netmap = config['networks']
    self.root = ns.network.NodeContainer()
    self.root.Create(1)

    self.mob = ns.mobility.MobilityHelper()
    self.mob.Install(self.root)

    self.connections = 1
    self.stack = ns.internet.InternetStackHelper()

    self.list = ns.internet.Ipv4ListRoutingHelper()
    
    self.olsr = ns.olsr.OlsrHelper()
    self.static = ns.internet.Ipv4StaticRoutingHelper()

    self.list.Add(self.static, 0)
    self.list.Add(self.olsr, 100)

    self.stack.SetRoutingHelper(self.list)

    self.stack.Install(self.root)
    self.p2p_devs = []

  def connect(self, node):
    conn = ns.network.NodeContainer()
    conn.Add(node)
    conn.Add(self.root)
    p2p = ns.point_to_point.PointToPointHelper()
    p2p_dev = p2p.Install(conn)

    addr = f'10.{self.connections}.0.0'
    mask = f'255.255.255.252'

    address = ns.internet.Ipv4AddressHelper()
    address.SetBase(
      ns.network.Ipv4Address(addr),
      ns.network.Ipv4Mask(mask)
    )
    address.Assign(p2p_dev)

    self.p2p_devs.append(p2p_dev)
    self.connections += 1
  