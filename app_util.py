import ns.applications
import ns.core

from dubak_translator import Lookup
from application.tcp import TcpUtil
from application.udp import UdpUtil

from log_helper import dbg

class AppUtil:
  config = {}

  def __init__(self, config):
    self.config = config
    self.udp_helper = UdpUtil(self)
    self.tcp_helper = TcpUtil(self)
  
  def install(self, all_nodes):
    nodes = self.config['nodes']
    for node_id in nodes:
      node = nodes[node_id]

      if node['l3'] is None:
        continue
      
      if node['l3'] not in Lookup:
        dbg.warn(f'app {node["l3"]} not implemented.')
        continue

      l3type = Lookup[node['l3']]

      l3conf = nodes[node_id]['l3conf']
      if l3type == 'udp_echo_client':
        self.udp_helper.add_client(all_nodes, node, l3conf)

      if l3type == 'udp_echo_server':
        self.udp_helper.add_server(all_nodes, node, l3conf)
      
      if l3type == 'tcp_client':
        self.tcp_helper.add_client(all_nodes, node, l3conf)
      
      elif l3type == 'tcp_server':
        self.tcp_helper.add_server(all_nodes, node, l3conf)
