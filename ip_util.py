from ipaddress import IPv4Network

import ns.internet
import ns.network
import ns.point_to_point
import ns.mobility

from log_helper import dbg

class IpUtil:
  stack = {}
  netmap = {}
  node = None

  def __init__(self, config):
    self.netmap = config['networks']
    self.node = ns.network.NodeContainer()
    self.node.Create(1)

    self.mob = ns.mobility.MobilityHelper()
    self.mob.Install(self.node)

    self.connections = 1
    self.stack = ns.internet.InternetStackHelper()
    self.stack.Install(self.node)
    self.p2p_devs = []
  
  def assign_address(self, nodes, phy_util):
    self.devices = phy_util.get_devices()

    
    self.stack.Install(nodes)

    for l2id in self.devices:
      addr = self.netmap[l2id]['addr']

      net_addr = IPv4Network(addr).network_address 
      net_mask = IPv4Network(addr).netmask

      address = ns.internet.Ipv4AddressHelper()
      address.SetBase(
        ns.network.Ipv4Address(net_addr),
        ns.network.Ipv4Mask(net_mask)
      )

      for net in self.devices[l2id]:
        address.Assign(net)
      
      net_name = self.netmap[l2id]['ssid']
      dbg.log(f'assigned address {net_addr} {net_mask} for network {net_name}')

  def connect(self, nodes, node_ids):
    for node_id in node_ids:
      node = nodes.Get(node_id)

      conn = ns.network.NodeContainer()
      conn.Add(node)
      conn.Add(self.node)
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
      dbg.log(f'node {node_id} connected to the internet')
  
  def populate(self):
    ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()
    dbg.log(f'global routing table populated')