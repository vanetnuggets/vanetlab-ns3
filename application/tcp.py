

class TcpUtil:
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
    max_bytes = int(conf['max_bytes'])

    serv_addr = ns.cppyy.gbl.getNodeIpv4(nodes.Get(int(serv_id  ))).GetAddress(1,0).GetLocal()
    
    client = ns.applications.BulkSendHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(serv_addr, port).ConvertTo())
    client.SetAttribute("MaxBytes", ns.core.UintegerValue(max_bytes))
    
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

    serv_addr = ns.cppyy.gbl.getNodeIpv4(nodes.Get(int(node_id  ))).GetAddress(1,0).GetLocal()
    
    server = ns.applications.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(serv_addr, port).ConvertTo())
    app = server.Install(nodes.Get(int(node_id)))
    app.Start(ns.core.Seconds(start))
    app.Stop(ns.core.Seconds(stop))

    self.servers[node['id']] = {
      's': server,
      'a': app
    }