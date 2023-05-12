import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracehelper import enable_trace
from attribute_manager import attribute_manager
from ipaddress import IPv4Network
from log_helper import dbg
import context

class EthernetUtil:
  eth_nodes = {}
  eth_devs = {}

  def __init__(self, config, ip_util):
    self.config = config
    self.ip_util = ip_util
    self.nodemap = {}
    
    for node_id in config['nodes']:
      l2type = config['nodes'][node_id]['l2']
      # ignore non-LTE nodes
      if l2type != "eth" and l2type != "ETH":
        continue

      l2id = config['nodes'][node_id]['l2id']
      if l2id not in self.nodemap:
        self.nodemap[l2id] = {}
      self.nodemap[l2id][node_id] = config['nodes'][node_id]
    self.netmap = config['networks']
  
  def install(self, nodes):

    for l2id in self.nodemap:
      netname = self.netmap[l2id]['ssid']
      l2type = self.netmap[l2id]['type'].lower()
      if l2type != 'eth':
        continue
      
      curr_network = self.netmap[l2id]

      self.eth_nodes[l2id] = ns.network.NodeContainer()
      
      curr_nodes = self.nodemap[l2id]
      for _node_id in curr_nodes:
        node_id = curr_nodes[_node_id]['id']
        self.eth_nodes[l2id].Add(context.get_node_for_id(node_id))
      
      csma = ns.csma.CsmaHelper()
      attribute_manager.install_attributes(curr_network, csma, 'SetAttribute')

      self.eth_devs[l2id] = csma.Install(self.eth_nodes[l2id])

      for node_id in curr_nodes:
        self.ip_util.stack.Install(ns.network.NodeContainer(context.get_node_for_id(int(node_id))))
      
      addr = self.netmap[l2id]['addr']

      net_addr = IPv4Network(addr).network_address 
      net_mask = IPv4Network(addr).netmask
      
      address = ns.internet.Ipv4AddressHelper()
      address.SetBase(
        ns.network.Ipv4Address(str(net_addr)),
        ns.network.Ipv4Mask(str(net_mask))
      )
      
      address.Assign(self.eth_devs[l2id])
      net_name = self.netmap[l2id]['ssid']

      dbg.log(f'assigned address {net_addr} {net_mask} for network {net_name}')
      dbg.log(f'network {net_name} configured.')

      enable_trace(csma, netname)
