from ns import *

ns.cppyy.cppdef("""
using namespace ns3;

Ptr<Ipv4> getNodeIpv4(Ptr<Node> node) { 
  return node->GetObject<Ipv4>(); 
};

Ptr<LteHelper> createLteHelper() {
  return CreateObject<LteHelper>();
};

""")

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

def main(argv):
  lte_helper = ns.core.CreateObject('LteHelper')
  epc_helper = ns.core.CreateObject('PointToPointEpcHelper')
  lte_helper.SetEpcHelper(epc_helper)

  pgw = epc_helper.GetPgwNode()

  stack = ns.internet.InternetStackHelper()



  internet = ns.internet.InternetStackHelper()
  routing = ns.dsdv.DsdvHelper()
  static_helper = ns.internet.Ipv4StaticRoutingHelper()
  rip_routing = ns.internet.RipHelper()
  routing_list = ns.internet.Ipv4ListRoutingHelper()
  routing_list.Add(static_helper, 0)
  internet.SetRoutingHelper(routing_list)

  ue_nodes = ns.network.NodeContainer()
  ue_nodes.Create(5)

  enb_nodes = ns.network.NodeContainer()
  enb_nodes.Create(1)

  csma_nodes = ns.network.NodeContainer()
  csma_nodes.Create(3)
  stack.Install(csma_nodes)
  

  print('installing stack on csma nodes')

  csma = ns.csma.CsmaHelper()
  csma_devs = csma.Install(csma_nodes)

  ipv4h = ns.network.Ipv4AddressHelper()
  ipv4h.SetBase(
    ns.network.Ipv4Address("2.0.0.0"),
    ns.network.Ipv4Mask("255.0.0.0")
  )
  cmsa_interfaces = ipv4h.Assign(csma_devs)
  
  print('install a stack on the pgw ?')
  internet.Install(pgw)
  
  p2ph = ns.point_to_point.PointToPointHelper()
  print('creating link between the pgw and remote host node')
  internet_devices = p2ph.Install(pgw, csma_nodes.Get(0))

  print('assigning ipv4 address to the created link')
  
  ipv4h.SetBase(
    ns.network.Ipv4Address("1.0.0.0"),
    ns.network.Ipv4Mask("255.0.0.0")
  )
  internet_ip_ifaces = ipv4h.Assign(internet_devices)

  print('adding static routing to the ue nodes from edge router')
  tmp = static_helper.GetStaticRouting(ns.cppyy.gbl.getNodeIpv4(csma_nodes.Get(0)))
  tmp.AddNetworkRouteTo(
    ns.network.Ipv4Address("7.0.0.0"), 
    ns.network.Ipv4Mask("255.0.0.0"),
    2
  )

  print('installing mobility on ue, enb, pgw, sgw nodes')
  mobility = ns.mobility.MobilityHelper()
  mobility.Install(ue_nodes)
  mobility.Install(enb_nodes)
  mobility.Install(pgw)

  print('installing enb devies')
  enb_devices = lte_helper.InstallEnbDevice(enb_nodes)
  print('installing ue devices')
  ue_devices = lte_helper.InstallUeDevice(ue_nodes)

  internet.Install(ue_nodes)
  print('assigning ue ipv4 addresses')
  epc_helper.AssignUeIpv4Address(ue_devices)

  # static routing possibly here ?
  print('attaching ue devices to enb')
  for i in range(5):
    lte_helper.Attach(ue_devices.Get(i))
  
  print('adding static routing to the edge router from the ue nodes')
  for i in range(5):
    tmp = static_helper.GetStaticRouting(ns.cppyy.gbl.getNodeIpv4(ue_nodes.Get(i)))
    tmp.SetDefaultRoute(epc_helper.GetUeDefaultGatewayAddress(), 1)
  
  print('installing server apps')
  echo_server = ns.applications.UdpEchoServerHelper(4242)
  server_apps = echo_server.Install(csma_nodes.Get(0))
  server_apps.Start(ns.core.Seconds(1.0))
  server_apps.Stop(ns.core.Seconds(10.0))

  address = ns.cppyy.gbl.getNodeIpv4(csma_nodes.Get(0)).GetAddress(2,0).GetLocal()
  address = address.ConvertTo()
  echo_client = ns.applications.UdpEchoClientHelper(address, 4242)
  echo_client.SetAttribute("MaxPackets", ns.core.UintegerValue(10))
  echo_client.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
  echo_client.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
  client_apps = echo_client.Install(ue_nodes.Get(4))
  client_apps.Start(ns.core.Seconds(1.0))
  client_apps.Stop(ns.core.Seconds(10.0))



  ns.core.Simulator.Stop(ns.core.Seconds(10.0))
  ns.core.Simulator.Run()
  ns.core.Simulator.Destroy()

if __name__ == '__main__':
    import sys
    main(sys.argv)


