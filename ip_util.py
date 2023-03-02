from ipaddress import IPv4Network

from ns.internet import Ipv4AddressHelper, InternetStackHelper
from ns.network import Ipv4Address, Ipv4Mask
from log_helper import dbg

class IpUtil:
  stack = {}
  netmap = {}

  def __init__(self, config):
    self.netmap = config['networks']
  
  def assign_address(self, nodes, phy_util):
    devices = phy_util.get_devices()

    self.stack = InternetStackHelper()
    self.stack.Install(nodes)

    for l2id in devices:
      addr = self.netmap[l2id]['addr']

      net_addr = IPv4Network(addr).network_address 
      net_mask = IPv4Network(addr).netmask

      
      address = Ipv4AddressHelper()
      address.SetBase(
        Ipv4Address(net_addr),
        Ipv4Mask(net_mask)
      )

      for net in devices[l2id]:
        address.Assign(net)
      
      net_name = self.netmap[l2id]['ssid']
      dbg.log(f'assigned address {net_addr} {net_mask} for network {net_name}')
