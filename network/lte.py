import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attribute_manager import attribute_manager
from tracehelper import enable_trace
from ipaddress import IPv4Network
from log_helper import dbg
import context

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
      

      self.lte_helper[l2id] = ns.core.CreateObject('LteHelper')
      self.epc_helper[l2id] = ns.core.CreateObject('PointToPointEpcHelper')
      self.lte_helper[l2id].SetEpcHelper(self.epc_helper[l2id])
      pgw = self.epc_helper[l2id].GetPgwNode()
      pgw_nodes = ns.network.NodeContainer()
      pgw_nodes.Add(pgw)
      # TODO add constant position to PGW node from `mobility` attribute

      self.pgw_nodes[l2id] = pgw_nodes
      # iface = self.ip_util.connect(pgw)
      # TODO - niekedy tam mozno nebude 7.0.0.0 ked zistim jak sa to robi
      # iface sa mozno bude kurvit nwm

      self.enb_nodes[l2id] = ns.network.NodeContainer()
      for enb_node in enbs:
        self.enb_nodes[l2id].Add(context.get_node_for_id(enb_node))
      self.enb_devs[l2id] = self.lte_helper[l2id].InstallEnbDevice(self.enb_nodes[l2id])

      dbg.log(f'installed {len(enbs)} enb nodes in network with id {l2id}')

      self.ue_nodes[l2id] = ns.network.NodeContainer()
      for ue_node in ues:
        self.ue_nodes[l2id].Add(context.get_node_for_id(ue_node))


      self.ue_devs[l2id] = self.lte_helper[l2id].InstallUeDevice(self.ue_nodes[l2id])
      dbg.log(f'installed {len(ues)} ue nodes in network with id {l2id}')
      for node_id in ues:
        self.ip_util.install_stack(node_id)

      self.epc_helper[l2id].AssignUeIpv4Address(self.ue_devs[l2id])

      # for node_id in ues:
      #   node = self.ue_nodes[l2id].Get(node_id)
      #   context.ip_util.static.GetStaticRouting(ns.cppyy.gbl.getNodeIpv4(node)).SetDefaultRoute(self.epc_helper[l2id].GetUeDefaultGatewayAddress(), 1)

      self.lte_helper[l2id].Attach(self.ue_devs[l2id], self.enb_devs[l2id].Get(0))
      
      self.enbs += enbs
      self.ues += ues
      netname = self.netmap[l2id]['ssid']
      dbg.log(f'configured LTE network')

      self.lte_helper[l2id].EnableTraces()

      # enable_trace(self.lte_helper[l2id], netname)
