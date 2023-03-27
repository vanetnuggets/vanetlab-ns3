from ipaddress import IPv4Network

from ns import ns

from log_helper import dbg
import context

class IpUtil:
  stack = {}
  netmap = {}
  _routing = None

  def __init__(self, config):
    self.netmap = config['networks']
    self.config = config

    self.mob = ns.mobility.MobilityHelper()
    self.connections = 1
    self.stack = ns.internet.InternetStackHelper()
    self._set_routing()
    self.p2p_devs = []
  
  def _set_routing(self):
    self.list = ns.internet.Ipv4ListRoutingHelper()
    
    if 'routing' not in self.config:
      dbg.log(f'no routing protocol specified, defaulting to `olsr`')
      routing = 'olsr'
    
    routing = self.config['routing'].lower()
    if routing not in ['olsr', 'aodv', 'dsdv']:
      dbg.err(f"invalid routing protocol - {routing}")
      exit(-1)

    if routing == 'olsr':
      self._routing = ns.olsr.OlsrHelper()
    
    elif routing == 'aodv':
      self._routing = ns.aodv.AodvHelper()
    
    elif routing == 'dsdv':
      self._routing = ns.dsdv.DsdvHelper()

    self.static = ns.internet.Ipv4StaticRoutingHelper()
    self.list.Add(self.static, 0)
    self.list.Add(self._routing, 100)

    self.stack.SetRoutingHelper(self.list)
    dbg.log(f'installed {routing} routing protocol.')
  
  def connect(self, node_from, node_to):
    _node_from = node_from
    _node_to = node_to

    if node_from == node_to:
      dbg.err(f'cannoct connect node {node_from} to {node_to}. they are the same node.')
      return

    if str(node_from) not in self.config['nodes']:
      dbg.err(f'node {node_from} does not exist.')
      return
    
    elif str(node_to) not in self.config['nodes']:
      dbg.err(f'node {node_to} does not exist')
      return
    
    node_from_conf = self.config['nodes'][str(node_from)]
    if 'type' in node_from_conf['l2conf'] and node_from_conf['l2conf']['type'] == 'pgw':
      l2id = node_from_conf['l2id']
      # TODO FIX LTE
      return
      node_from = context.phy_util.get_pgw_node(l2id)
      
    else:
      node_from = context.nodes.Get(node_from)
    
    node_to_conf = self.config['nodes'][str(node_to)]
    if 'type' in node_to_conf['l2conf'] and node_to_conf['l2conf']['type'] == 'pgw':
      l2id = node_from_conf['l2id']
      node_to = context.phy_util.get_pgw_node(l2id)
    else:
      node_to = context.nodes.Get(node_to)
    
    conn = ns.network.NodeContainer()
    conn.Add(node_from)
    conn.Add(node_to)
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
    dbg.log(f'added connection between node {_node_from} and node {_node_to} with ip address of {addr}::{mask}')

    return self.connections - 1
   

  # def connect(self, node):
  #   conn = ns.network.NodeContainer()
  #   conn.Add(node)
  #   conn.Add(self.root)
  #   p2p = ns.point_to_point.PointToPointHelper()
  #   p2p_dev = p2p.Install(conn)

  #   addr = f'10.{self.connections}.0.0'
  #   mask = f'255.255.255.252'

  #   address = ns.internet.Ipv4AddressHelper()
  #   address.SetBase(
  #     ns.network.Ipv4Address(addr),
  #     ns.network.Ipv4Mask(mask)
  #   )
  #   address.Assign(p2p_dev)

  #   self.p2p_devs.append(p2p_dev)
  #   self.connections += 1
  #   return self.connections - 1
  
  def add_static(self, addr, mask, iface):
    self.static.GetStaticRouting(self.root.Get(0).GetObject(ns.internet.Ipv4.GetTypeId())).AddNetworkRouteTo(
      ns.network.Ipv4Address(addr),
      ns.network.Ipv4Mask(mask),
      iface
    )

  def install_connections(self):
    conns = self.config['connections']

    for conn in conns:
      node_from = conn['node_from']
      node_to = conn['node_to']

      self.connect(int(node_from), int(node_to))