import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attribute_manager import attribute_manager
import context
from log_helper import dbg 

class UdpUtil:
  clients = {}
  servers = {}

  def __init__(self, app_util):
    self.app_util = app_util
  
  def add_client(self, nodes, node, conf):
    node_id = int(node['id'])

    serv_id = conf['comm']
    port = int(conf['port'])
    start = int(conf['start'])
    stop = int(conf['stop'])

    serv_addr = ns.cppyy.gbl.getNodeIpv4(context.get_node_for_id(serv_id)).GetAddress(1,0).GetLocal()
    
    client = ns.applications.UdpEchoClientHelper(serv_addr.ConvertTo(), port)
    
    attribute_manager.install_attributes(conf, client, method='SetAttribute')
    
    app = client.Install(context.get_node_for_id(node_id))
    app.Start(ns.core.Seconds(start))
    app.Stop(ns.core.Seconds(stop))

    self.clients[node['id']] = {
      's': client,
      'a': app
    }
    dbg.log(f'installed client: {node_id} -> {serv_id} ({serv_addr}:{port}) [{start}:{stop}]')
  
  def add_server(self, nodes, node, conf):
    node_id = int(node['id'])

    port = int(conf['port'])
    start = int(conf['start'])
    stop = int(conf['stop'])

    server = ns.applications.UdpEchoServerHelper(port)
    app = server.Install(context.get_node_for_id(node_id))
    app.Start(ns.core.Seconds(start))
    app.Stop(ns.core.Seconds(stop))

    self.servers[node['id']] = {
      's': server,
      'a': app
    }

    serv_addr = ns.cppyy.gbl.getNodeIpv4(
      context.get_node_for_id(node_id)
    ).GetAddress(1,0).GetLocal()

    dbg.log(f'installed server: {node_id}, {serv_addr}:{port} [{start}:{stop}]')
