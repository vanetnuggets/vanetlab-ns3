from ipaddress import IPv4Network

from ns import ns

from log_helper import dbg

from network.eth import EthernetUtil
from network.lte import LteUtil
from network.wifi import WifiUtil

class PhyUtil:
  def __init__(self, config, ip_util):
    self.config = config
    self.ip_util = ip_util

    self.lte_util = LteUtil(self.config, self.ip_util)
    self.wifi_util = WifiUtil(self.config, self.ip_util)
    self.eth_util = EthernetUtil(self.config, self.ip_util)

  def install(self, nodes):
    self.nodes = nodes

    dbg.log(f'installing LTE networks...')
    self.lte_util.install(nodes)

    dbg.log(f'installing Wifi networks...')
    self.wifi_util.install(nodes)

    dbg.log(f'installing Eth networks...')
    self.eth_util.install(nodes)
  
  def get_devices(self):
    devices = {}

    # get spa devices
    for l2id in self.wifi_util.sta_devs:
      if l2id not in devices:
        devices[l2id] = []
      devices[l2id].append(
        self.wifi_util.sta_devs[l2id]
      )

    # get ap devices
    for l2id in self.wifi_util.ap_devs:
      if l2id not in devices:
        devices[l2id] = []
      devices[l2id].append(
        self.wifi_util.ap_devs[l2id]
      )

    return devices
    
  def get_enb_node_ids(self):
    return self.lte_util.enbs
  
  def get_ap_node_ids(self):
    return self.wifi_util.aps
  
  def get_pgw_nodes(self):
    arr = []
    for l2id in self.lte_util.pgw_nodes:
      arr.append(self.lte_util.pgw_nodes[l2id])
    return arr
  
  def get_pgw_node(self, l2id):
    try:
      node = self.lte_util.pgw_nodes[l2id].Get(0)
      return node
    except KeyError as e:
      return None