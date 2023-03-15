from ipaddress import IPv4Network

import ns.core
import ns.wifi
import ns.lte
import ns.network

from log_helper import dbg

DEBUG = True

class LteUtil:
  lte_helper = {}
  epc_helper = {}

  enb_devs = {}
  ue_devs = {}

  ue_nodes = {}
  enb_nodes = {}
  pgw_nodes = {}

  config = {}
  bearer = {}

  enbs = []
  ues = []

  def __init__(self, config, ip_util):
    self.config = config
    self.ip_util = ip_util
    self.nodemap = {}
    
    for node_id in config['nodes']:
      l2type = config['nodes'][node_id]['l2']
      # ignore non-LTE nodes
      if l2type != "lte" and l2type != "LTE":
        continue

      l2id = config['nodes'][node_id]['l2id']
      if l2id not in self.nodemap:
        self.nodemap[l2id] = {}
      self.nodemap[l2id][node_id] = config['nodes'][node_id]
    self.netmap = config['networks']

  def install(self, nodes):
    self.enbs = []
    self.ues = []

    for l2id in self.nodemap:
      # Ignore non-LTE networks
      if self.netmap[l2id]['type'] != 'LTE':
        continue
      
      enbs = []
      ues = []

      curr_nodes = self.nodemap[l2id]
      
      for _node_id in curr_nodes:
        node = curr_nodes[_node_id]

        node_id = node['id']
        node_type = node['l2conf']['type']

        if node_type == 'enb':
          enbs.append(node_id)
        elif node_type == 'ue':
          ues.append(node_id)
      
      if len(enbs) <= 0:
        dbg.err('no enb node found - lte cannot be configured.')
        return
      dbg.log(f'parsed {len(enbs)} enb nodes and {len(ues)} ue nodes in network with id {l2id}.')
      
      self.lte_helper[l2id] = ns.lte.LteHelper()
      self.epc_helper[l2id] = ns.lte.PointToPointEpcHelper()
      self.lte_helper[l2id].SetEpcHelper(self.epc_helper[l2id])

      pgw = self.epc_helper[l2id].GetPgwNode()
      self.pgw_nodes[l2id] = pgw
      iface = self.ip_util.connect(pgw)
      
      # TODO - niekedy tam mozno nebude 7.0.0.0 ked zistim jak sa to robi
      # iface sa mozno bude kurvit nwm
      self.ip_util.add_static("7.0.0.0", "255.0.0.0", iface)
      
      self.enb_nodes[l2id] = ns.network.NodeContainer()
      for enb_node in enbs:
        self.enb_nodes[l2id].Add(nodes.Get(int(enb_node)))

      self.enb_devs[l2id] = self.lte_helper[l2id].InstallEnbDevice(self.enb_nodes[l2id])

      dbg.log(f'installed {len(enbs)} enb nodes in network with id {l2id}')

      self.ue_nodes[l2id] = ns.network.NodeContainer()
      for ue_node in ues:
        self.ue_nodes[l2id].Add(nodes.Get(int(ue_node)))


      self.ue_devs[l2id] = self.lte_helper[l2id].InstallUeDevice(self.ue_nodes[l2id])
      dbg.log(f'installed {len(ues)} ue nodes in network with id {l2id}')
      for node_id in ues:
        self.ip_util.stack.Install(ns.network.NodeContainer(nodes.Get(int(node_id))))

      self.epc_helper[l2id].AssignUeIpv4Address(self.ue_devs[l2id])

      self.lte_helper[l2id].Attach(self.ue_devs[l2id], self.enb_devs[l2id].Get(0))
      


      self.enbs += enbs
      self.ues += ues


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

    self.chan = ns.wifi.YansWifiChannelHelper.Default()
    self.phy = ns.wifi.YansWifiPhyHelper()
    self.phy.Set('TxGain', ns.core.DoubleValue(256))
    self.phy.Set('RxGain', ns.core.DoubleValue(256))
    self.phy.SetChannel(self.chan.Create())
    self.wifi = ns.wifi.WifiHelper()
    self.mac = ns.wifi.WifiMacHelper()
    self.ssid = None

  def install(self, nodes):
    self.aps = []
    self.stas = []

    for l2id in self.netmap:
      # Ignore non-Wifi networks
      if self.netmap[l2id]['type'] != 'WIFI':
        continue

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
        self.ap_nodes[l2id].Add(nodes.Get(int(ap_node)))

      # isntall AP nodes
      ssid = self.netmap[l2id]['ssid']
      if self.ssid == None:
        self.ssid = ns.wifi.Ssid (ssid)

      self.mac.SetType ("ns3::ApWifiMac", "Ssid", ns.wifi.SsidValue(self.ssid))
      self.ap_devs[l2id] = self.wifi.Install(self.phy, self.mac, self.ap_nodes[l2id])

      dbg.log(f'isntalled {len(aps)} ap nodes in network with id {l2id}')

      self.sta_nodes[l2id] = ns.network.NodeContainer()
      for sta_node in stas:
        self.sta_nodes[l2id].Add(nodes.Get(int(sta_node)))
        
      # install STA nodes
      ssid = self.netmap[l2id]['ssid']
      self.mac.SetType ("ns3::StaWifiMac", "Ssid", ns.wifi.SsidValue(self.ssid), "ActiveProbing", ns.core.BooleanValue(False))
      self.sta_devs[l2id] = self.wifi.Install(self.phy, self.mac, self.sta_nodes[l2id])

      dbg.log(f'isntalled {len(stas)} sta nodes in network with id {l2id}')
      
      # Install IP stack
      for node_id in curr_nodes:
        self.ip_util.stack.Install(ns.network.NodeContainer(nodes.Get(int(node_id))))
      
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
      
      # p2p to main internet node from AP nodes
      for ap in aps:
        self.ip_util.connect(nodes.Get(ap))
      dbg.log(f'AP nodes connected to internet backbone')

      dbg.log(f'configured WIFI network with id {l2id}')
      self.aps += aps
      self.stas += stas

class PhyUtil:
  def __init__(self, config, ip_util):
    self.config = config
    self.ip_util = ip_util

    self.lte_util = LteUtil(self.config, self.ip_util)
    self.wifi_util = WifiUtil(self.config, self.ip_util)

  def install(self, nodes):
    self.nodes = nodes

    dbg.log(f'installing LTE networks...')
    self.lte_util.install(nodes)
    dbg.log(f'installing Wifi networks...')
    self.wifi_util.install(nodes)
  
  def get_devices(self):
    devices = {}

    # get enb devices
    # for l2id in self.lte_util.enb_devs:
    #   if l2id not in devices:
    #     devices[l2id] = []
    #   devices[l2id].append(
    #     self.lte_util.enb_devs[l2id]
    #   )
    
    # # get ue devices
    # for l2id in self.lte_util.ue_devs:
    #   if l2id not in devices:
    #     devices[l2id] = []
    #   devices[l2id].append(
    #     self.lte_util.ue_devs[l2id]
    #   )
    
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
