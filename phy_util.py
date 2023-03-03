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

  config = {}
  bearer = {}

  enbs = []
  ues = []

  def __init__(self, config):
    self.config = config
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
      
      self.enb_nodes[l2id] = ns.network.NodeContainer()
      for enb_node in enbs:
        self.enb_nodes[l2id].Add(nodes.Get(enb_node))

      self.lte_helper[l2id] = ns.lte.LteHelper()
      
      self.enb_devs[l2id] = self.lte_helper[l2id].InstallEnbDevice(self.enb_nodes[l2id])
      dbg.log(f'installed {len(enbs)} enb nodes in network with id {l2id}')

      self.ue_nodes[l2id] = ns.network.NodeContainer()
      for ue_node in ues:
        self.ue_nodes[l2id].Add(nodes.Get(ue_node))

      self.ue_devs[l2id] = self.lte_helper[l2id].InstallUeDevice(self.ue_nodes[l2id])
      
      dbg.log(f'installed {len(ues)} ue nodes in network with id {l2id}')

      self.enbs += enbs
      self.ues += ues

  def finish(self):
    # assign ip address magic bullshit
    # self.epc_helper[l2id].AssignUeIpv4Address(self.ue_devs[l2id])

    # # If more than one ENB dev, soemhow choose, maybe from config ? 
    # self.lte_helper[l2id].Attach(self.ue_devs[l2id], self.enb_devs[l2id].Get(0))

    # self.bearer[l2id] = ns.lte.EpsBearer(ns.lte.EpsBearer.GBR_CONV_VOICE)
    # self.lte_helper[l2id].ActivateDataRadioBearer(self.ue_devs[l2id], self.bearer[l2id])
    for l2id in self.nodemap:
      # Ignore non-LTE networks
      if self.netmap[l2id]['type'] != 'LTE':
        continue

      self.epc_helper[l2id] = ns.lte.NoBackhaulEpcHelper()
      self.lte_helper[l2id].SetEpcHelper(self.epc_helper[l2id])
      pgw = self.epc_helper[l2id].GetPgwNode()

      self.epc_helper[l2id].AssignUeIpv4Address(self.ue_devs[l2id])


    dbg.log(f'configured LTE network with id {l2id}')
    
class WifiUtil:
  wifi_helper = {}

  ap_devs = {}
  sta_devs = {}

  ap_nodes = {}
  sta_nodes = {}
  config = {}

  stas = []
  aps = []

  def __init__(self, config):
    self.config = config
    self.nodemap = {}
    for node_id in config['nodes']:
      l2id = config['nodes'][node_id]['l2id']
      if l2id not in self.nodemap:
        self.nodemap[l2id] = {}
      self.nodemap[l2id][node_id] = config['nodes'][node_id]
    self.netmap = config['networks']

    self.chan = ns.wifi.YansWifiChannelHelper.Default()
    self.phy = ns.wifi.YansWifiPhyHelper()
    self.phy.SetChannel(self.chan.Create())
    self.wifi = ns.wifi.WifiHelper()
    self.mac = ns.wifi.WifiMacHelper()
    self.ssid = None
  
  def setup_sta(self, l2id, ssid):
    if self.ssid == None:
      self.ssid = ns.wifi.Ssid (ssid)

    self.mac.SetType ("ns3::StaWifiMac", "Ssid", ns.wifi.SsidValue(self.ssid), "ActiveProbing", ns.core.BooleanValue(False))

    self.sta_devs[l2id] = self.wifi.Install(self.phy, self.mac, self.sta_nodes[l2id])
    dbg.log(f'configured wifi sta nodes in network {l2id}')

  def setup_ap(self, l2id, ssid):
    if self.ssid == None:
      self.ssid = ns.wifi.Ssid (ssid)

    self.mac.SetType ("ns3::ApWifiMac", "Ssid", ns.wifi.SsidValue(self.ssid))
    
    self.ap_devs[l2id] = self.wifi.Install(self.phy, self.mac, self.ap_nodes[l2id])
    dbg.log(f'configured wifi ap nodes in network {l2id}')


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
        self.ap_nodes[l2id].Add(nodes.Get(ap_node))
        
        # isntall AP nodes
      ssid = self.netmap[l2id]['ssid']
      self.setup_ap(l2id, ssid)

      dbg.log(f'isntalled {len(aps)} ap nodes in network with id {l2id}')

      self.sta_nodes[l2id] = ns.network.NodeContainer()
      for sta_node in stas:
        self.sta_nodes[l2id].Add(nodes.Get(sta_node))
        
      # install STA nodes
      ssid = self.netmap[l2id]['ssid']
      self.setup_sta(l2id, ssid)

      dbg.log(f'isntalled {len(stas)} sta nodes in network with id {l2id}')

      # attach stas to ap

      dbg.log(f'configured WIFI network with id {l2id}')

      self.aps += aps
      self.stas += stas

class PhyUtil:
  def __init__(self, config):
    self.config = config

    self.lte_util = LteUtil(self.config)
    self.wifi_util = WifiUtil(self.config)

  def install(self, nodes):
    self.nodes = nodes

    dbg.log(f'installing LTE networks...')
    self.lte_util.install(nodes)
    dbg.log(f'installing Wifi networks...')
    self.wifi_util.install(nodes)
  
  def get_devices(self):
    devices = {}

    # get enb devices
    for l2id in self.lte_util.enb_devs:
      if l2id not in devices:
        devices[l2id] = []
      devices[l2id].append(
        self.lte_util.enb_devs[l2id]
      )
    
    # get ue devices
    for l2id in self.lte_util.ue_devs:
      if l2id not in devices:
        devices[l2id] = []
      devices[l2id].append(
        self.lte_util.ue_devs[l2id]
      )
    
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