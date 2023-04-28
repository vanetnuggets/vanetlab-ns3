import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attribute_manager import attribute_manager
from ipaddress import IPv4Network
from log_helper import dbg
import util
import context

class WaveUtil:
  wave_devs = {}
  wave_nodes = {}
  config = {}

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
    
    self.wavemap = {}
  
  def mac(self, l2id):
    if l2id not in self.wavemap:
      return None
    return self.wavemap[l2id]['mac']

  def phy(self, l2id):
    if l2id not in self.wavemap:
      return None
    return self.wavemap[l2id]['phy']

  def chan(self, l2id):
    if l2id not in self.wavemap:
      return None
    return self.wavemap[l2id]['chan']
  
  def ssid(self, l2id):
    if l2id not in self.wavemap:
      return None
    return self.wavemap[l2id]['ssid']

  def wave(self, l2id):
    if l2id not in self.wavemap:
      return None
    return self.wavemap[l2id]['wave']

  def install(self, nodes):
    self.aps = []
    self.stas = []

    for l2id in self.netmap:
      # Ignore non-Wifi networks
      if self.netmap[l2id]['type'] != 'WAVE':
        continue
      
      if self.wavemap.get(l2id) == None:
        dbg.log('installiing the waves.')
        # self.wavemap[l2id] = {
        #     "wave": ns.wifi.WaveHelper.Default(),
        #     "phy": ns.wifi.YansWavePhyHelper.Default(),
        #     "chan": ns.wifi.YansWifiChannelHelper.Default(),
        #     "mac": ns.wifi.QosWaveMacHelper.Default(),
        #     "ssid": self.netmap[l2id]['ssid']
        # }
        # self.phy(l2id).SetChannel(self.chan(l2id).Create())
        # self.phy(l2id).SetPcapDataLinkType(ns.wifi.WifiPhyHelper.DLT_IEEE802_11)
        # self.phy(l2id).Set("TxPowerStart", ns.core.DoubleValue(5))
        # self.phy(l2id).Set("TxPowerEnd", ns.core.DoubleValue(33))
        # self.phy(l2id).Set("TxPowerLevels", ns.core.UintegerValue(8))
        # 
        # self.wave(l2id).SetRemoteStationManager(
        #   "ns3::ConstantRateWifiManager",
        #   "DataMode", ns.core.StringValue("OfdmRate6MbpsBW10MHz"),
        #   "ControlMode", ns.core.StringValue ("OfdmRate6MbpsBW10MHz"),
        #   "NonUnicastMode", ns.core.StringValue ("OfdmRate6MbpsBW10MHz")
        # );
        
        self.wavemap[l2id] = {
          "wave": ns.wifi.Wifi80211pHelper.Default(),
          "phy": ns.wifi.YansWifiPhyHelper(),
          "chan": ns.wifi.YansWifiChannelHelper.Default(),
          "mac": ns.wifi.NqosWaveMacHelper.Default(),
          "ssid": self.netmap[l2id]['ssid']
        }
        self.phy(l2id).SetChannel(self.chan(l2id).Create())

      wave_nodes = []

      curr_nodes = self.nodemap[l2id]
      for _node_id in curr_nodes:
        node = curr_nodes[_node_id]
        node_id = node['id']
        wave_nodes.append(node_id)

      dbg.log(f'parsed {len(wave_nodes)} wave nodes in network with id {l2id}.')

      self.wave_nodes[l2id] = ns.network.NodeContainer()
      for wave_node in wave_nodes:
        self.wave_nodes[l2id].Add(context.get_node_for_id(wave_node))

      # install wave nodes
      self.wave_devs[l2id] = ns.network.NetDeviceContainer()
      
      for i, node_id in enumerate(wave_nodes):
        node = curr_nodes[str(node_id)]
        print(node['l2conf'], node_id)
        attribute_manager.install_attributes(node['l2conf'], self.phy(l2id))
        
        # install device
        wave_dev = self.wave(l2id).Install(self.phy(l2id), self.mac(l2id), self.wave_nodes[l2id])
        self.wave_devs[l2id].Add(wave_dev)

        attribute_manager.clear_attributes(node, self.phy(l2id))

      dbg.log(f'isntalled {len(wave_nodes)} wave devices in network with id {l2id}')

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
      
      address.Assign(self.wave_devs[l2id])

      net_name = self.netmap[l2id]['ssid']
      dbg.log(f'assigned address {net_addr} {net_mask} for network {net_name}')
      
      dbg.log(f'configured Wave network with id {l2id}')
