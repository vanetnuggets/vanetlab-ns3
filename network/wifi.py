import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tracehelper import enable_trace
from attribute_manager import attribute_manager
from ipaddress import IPv4Network
from log_helper import dbg
import util
import context

class WifiUtil:
  wifi_helper = {}

  ap_devs = {}
  sta_devs = {}

  ap_nodes = {}
  sta_nodes = {}
  config = {}

  stas = []
  aps = []

  def __init__(self, config, ip_util):
    self.config = config
    self.nodemap = {}
    self.ip_util = ip_util

    for node_id in config['nodes']:
      l2id = config['nodes'][node_id]['l2id']
      if l2id not in self.nodemap:
        self.nodemap[l2id] = {}
      self.nodemap[l2id][node_id] = config['nodes'][node_id]
    self.netmap = config['networks']
    
    self.wifimap = {}
    # self.chan = ns.wifi.YansWifiChannelHelper.Default()
    # self.phy = ns.wifi.YansWifiPhyHelper()
    # self.phy.Set('TxGain', ns.core.DoubleValue(256))
    # self.phy.Set('RxGain', ns.core.DoubleValue(256))
    # self.phy.SetChannel(self.chan.Create())
    
    # self.wifi = ns.wifi.WifiHelper()
    # self.mac = ns.wifi.WifiMacHelper()
    # self.ssid = None
  
  def mac(self, l2id):
    if l2id not in self.wifimap:
      return None
    return self.wifimap[l2id]['mac']

  def phy(self, l2id):
    if l2id not in self.wifimap:
      return None
    return self.wifimap[l2id]['phy']

  def chan(self, l2id):
    if l2id not in self.wifimap:
      return None
    return self.wifimap[l2id]['chan']
  
  def ssid(self, l2id):
    if l2id not in self.wifimap:
      return None
    return self.wifimap[l2id]['ssid']

  def wifi(self, l2id):
    if l2id not in self.wifimap:
      return None
    return self.wifimap[l2id]['wifi']

  def set_standard(self, l2id, node_id):
    standard = self.nodemap[l2id][str(node_id)]['l2conf'].get('standard')
    if standard == None:
        dbg.warn('wifi node {node_id} has unspecified standard, defaulting to 802.11n')
        standard = '802.11n'
    
    ns_standard = util.get_wifi_standard(standard)
    if ns_standard != None:
        self.wifi(l2id).SetStandard(ns_standard)
    else:
        dbg.err(f'unknown network standard {standard} for node {node_id}.')

  def install(self, nodes):
    self.aps = []
    self.stas = []

    for l2id in self.netmap:
      # Ignore non-Wifi networks
      if self.netmap[l2id]['type'] != 'WIFI':
        continue
      
      if self.wifimap.get(l2id) == None:
        self.wifimap[l2id] = {
            "wifi": ns.wifi.WifiHelper(),
            "phy": ns.wifi.YansWifiPhyHelper(),
            "chan": ns.wifi.YansWifiChannelHelper.Default(),
            "mac": ns.wifi.WifiMacHelper(),
            "ssid": self.netmap[l2id]['ssid']
        }
        self.phy(l2id).SetChannel(self.chan(l2id).Create())
        
      aps = []
      stas = []

      curr_nodes = self.nodemap[l2id]
      for _node_id in curr_nodes:
        node = curr_nodes[_node_id]
        node_id = node['id']
        node_type = node['l2conf']['type']

        if node_type == 'ap':
          aps.append(node_id)
        elif node_type == 'sta':
          stas.append(node_id)

      if len(aps) <= 0:
        dbg.err('no AP node found - wifi cannot be configured.')
        return

      dbg.log(f'parsed {len(stas)} sta nodes and {len(aps)} ap nodes in network with id {l2id}.')

      self.ap_nodes[l2id] = ns.network.NodeContainer()
      for ap_node in aps:
        self.ap_nodes[l2id].Add(context.get_node_for_id(ap_node))

      # isntall AP nodes
      ssid = self.netmap[l2id]['ssid']
      self.mac(l2id).SetType ("ns3::ApWifiMac", "Ssid", ns.wifi.SsidValue(self.ssid(l2id)))
      self.ap_devs[l2id] = ns.network.NetDeviceContainer()
      
      for node_id in aps:
        node = curr_nodes[str(node_id)]

        attribute_manager.install_attributes(node['l2conf'], self.phy(l2id))
        
        self.set_standard(l2id, node_id)
        # install device
        ap_dev = self.wifi(l2id).Install(self.phy(l2id), self.mac(l2id), self.ap_nodes[l2id])
        self.ap_devs[l2id].Add(ap_dev)

        attribute_manager.clear_attributes(node, self.phy(l2id))

      dbg.log(f'isntalled {len(aps)} ap nodes in network with id {l2id}')

      self.sta_nodes[l2id] = ns.network.NodeContainer()
      for sta_node in stas:
        self.sta_nodes[l2id].Add(context.get_node_for_id(sta_node))
        
      # install STA nodes
      ssid = self.netmap[l2id]['ssid']
      self.mac(l2id).SetType ("ns3::StaWifiMac", "Ssid", ns.wifi.SsidValue(self.ssid(l2id)), "ActiveProbing", ns.core.BooleanValue(False))
      
      self.sta_devs[l2id] = ns.network.NetDeviceContainer()
      for node_id in stas:
        node = curr_nodes[str(node_id)]
        attribute_manager.install_attributes(node, self.phy(l2id))
        self.set_standard(l2id, node_id)
        sta_dev = self.wifi(l2id).Install(self.phy(l2id), self.mac(l2id), self.sta_nodes[l2id])
        self.sta_devs[l2id].Add(sta_dev)
        attribute_manager.clear_attributes(node, self.phy(l2id))

      dbg.log(f'isntalled {len(stas)} sta nodes in network with id {l2id}')
      
      # Install IP stack
      for node_id in curr_nodes:
        self.ip_util.stack.Install(ns.network.NodeContainer(context.get_node_for_id(node_id)))
      
      addr = self.netmap[l2id]['addr']

      net_addr = IPv4Network(addr).network_address 
      net_mask = IPv4Network(addr).netmask
      
      address = ns.internet.Ipv4AddressHelper()
      address.SetBase(
        ns.network.Ipv4Address(str(net_addr)),
        ns.network.Ipv4Mask(str(net_mask))
      )
      
      address.Assign(self.ap_devs[l2id])
      address.Assign(self.sta_devs[l2id])

      net_name = self.netmap[l2id]['ssid']
      dbg.log(f'assigned address {net_addr} {net_mask} for network {net_name}')
      
      dbg.log(f'configured WIFI network with id {l2id}')
      self.aps += aps
      self.stas += stas

      enable_trace(self.phy(l2id), self.ssid(l2id))

