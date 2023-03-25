import ns.applications
import ns.core

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
    max_packets = int(conf['max_packets'])

    serv_addr = nodes.Get(int(serv_id)).GetObject(ns.internet.Ipv4.GetTypeId()).GetAddress(1,0).GetLocal()
    
    client = ns.applications.UdpEchoClientHelper(serv_addr, port)
    client.SetAttribute("MaxPackets", ns.core.UintegerValue(max_packets))
    
    app = client.Install(nodes.Get(int(node_id)))
    app.Start(ns.core.Seconds(start))
    app.Stop(ns.core.Seconds(stop))

    self.clients[node['id']] = {
      's': client,
      'a': app
    }
  
  def add_server(self, nodes, node, conf):
    node_id = int(node['id'])

    port = int(conf['port'])
    start = int(conf['start'])
    stop = int(conf['stop'])

    server = ns.applications.UdpEchoServerHelper(port)
    app = server.Install(nodes.Get(int(node_id)))
    app.Start(ns.core.Seconds(start))
    app.Stop(ns.core.Seconds(stop))

    self.servers[node['id']] = {
      's': server,
      'a': app
    }