import ns.applications
import ns.core

class AppUtil:
  config = {}

  def __init__(self, config):
    self.config = config
    self.servers = {}
    self.clients = {}
  
  def install(self, all_nodes):
    nodes = self.config['nodes']
    for node_id in nodes:
      node = nodes[node_id]

      if node['l3'] is None:
        continue
      
      l3conf = nodes[node_id]['l3conf']
      if node['l3'] == 'udp_echo_client':
        serv_id = l3conf['comm']
        port = l3conf['port']
        start = l3conf['start']
        stop = l3conf['stop']
        max_packets = l3conf['max_packets']

        serv_addr = all_nodes.Get(serv_id).GetObject(ns.internet.Ipv4.GetTypeId()).GetAddress(1,0).GetLocal()
        
        # client = ns.applications.UdpEchoClient()
        # client.SetRemote(serv_addr, port)
        # client.SetStartTime(ns.core.Seconds(start))
        # client.SetStopTime(ns.core.Seconds(stop))
        # client.SetAttribute("MaxPackets", ns.core.UintegerValue(max_packets))
        # all_nodes.Get(node_id).AddApplication(client)
        client = ns.applications.UdpEchoClientHelper(serv_addr, port)
        client.SetAttribute("MaxPackets", ns.core.UintegerValue(max_packets))
        
        app = client.Install(all_nodes.Get(node_id))
        print('isntalling CLIENT on', node_id, 'sending to', serv_id)
        app.Start(ns.core.Seconds(start))
        app.Stop(ns.core.Seconds(stop))

        self.clients[node['id']] = {
          's': client,
          'a': app
        }

      if node['l3'] == 'udp_echo_server':
        port = l3conf['port']
        start = l3conf['start']
        stop = l3conf['stop']

        # server = ns.applications.UdpEchoServer()
        # server.SetAttribute("Port", ns.core.UintegerValue(port))        
        # server.SetStartTime(ns.core.Seconds(start))
        # server.SetStopTime(ns.core.Seconds(stop))

        # all_nodes.Get(node_id).AddApplication(server)

        server = ns.applications.UdpEchoServerHelper(port)
        app = server.Install(all_nodes.Get(node_id))
        print('isntalling SERVER on', node_id)
        app.Start(ns.core.Seconds(start))
        app.Stop(ns.core.Seconds(stop))

        self.servers[node['id']] = {
          's': server,
          'a': app
        }
        