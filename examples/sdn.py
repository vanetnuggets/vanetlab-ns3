# import ns.applications
# import ns.core
# import ns.csma
# import ns.internet
# import ns.network
# import ns.openflow
from ns import *
import sys

ns.cppyy.cppdef("""
using namespace ns3;

Ptr<Ipv4> getNodeIpv4(Ptr<Node> node) {
 return node->GetObject<Ipv4>();
};
""")

verbose = False
use_drop = False
timeout = ns.core.Seconds(0)

def set_verbose(value):
    global verbose
    verbose = True
    return True

def set_drop(value):
    global use_drop
    use_drop = True
    return True

def set_timeout(value):
    global timeout
    try:
        timeout = ns.core.Seconds(float(value))
        return True
    except:
        return False

def main(argv):
    global verbose, use_drop, timeout
    cmd = ns.core.CommandLine()
    # cmd.AddValue("verbose", "Verbose (turns on logging).", ns.core.StringValue(""), set_verbose)
    # cmd.AddValue("d", "Use Drop Controller (Learning if not specified).", ns.core.StringValue(""), set_drop)
    # cmd.AddValue("drop", "Use Drop Controller (Learning if not specified).", ns.core.StringValue(""), set_drop)
    # cmd.AddValue("t", "Learning Controller Timeout (has no effect if drop controller is specified).", ns.core.StringValue(""), set_timeout)
    # cmd.AddValue("timeout", "Learning Controller Timeout (has no effect if drop controller is specified).", ns.core.StringValue(""), set_timeout)
    cmd.Parse(sys.argv)

    if verbose:
        ns.core.LogComponentEnable("OpenFlowCsmaSwitchExample", ns.core.LOG_LEVEL_INFO)
        ns.core.LogComponentEnable("OpenFlowInterface", ns.core.LOG_LEVEL_INFO)
        ns.core.LogComponentEnable("OpenFlowSwitchNetDevice", ns.core.LOG_LEVEL_INFO)

    #
    # Explicitly create the nodes required by the topology (shown above).
    #
    nodes = ns.network.NodeContainer()
    nodes.Create(4)
    # print(type(nodes.Get(1)))

    csmaSwitch = ns.network.NodeContainer()
    csmaSwitch.Create(1)
    # print(type(csmaSwitch))

    # ns.core.LogInfo("Build Topology")
    csma = ns.csma.CsmaHelper()
    csma.SetChannelAttribute("DataRate", ns.core.DataRateValue(5000000))
    csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.MilliSeconds(2)))

    # Create the csma links, from each terminal to the switch
    terminalDevices = ns.network.NetDeviceContainer()
    switchDevices = ns.network.NetDeviceContainer()

    for i in range(4):
        # link = csma.Install(ns.network.NodeContainer(nodes.Get(i), csmaSwitch))
        link = csma.Install(ns.network.NodeContainer(ns.network.NodeContainer(nodes.Get(i)), csmaSwitch))
        terminalDevices.Add(link.Get(0))
        switchDevices.Add(link.Get(1))

    # Create the switch netdevice, which will do the packet switching
    switchNode = csmaSwitch.Get(0)
    swtch = ns.openflow.OpenFlowSwitchHelper()

    if use_drop:
        # controller = ns.openflow.ofi.DropController.Create()
        controller = ns.openflow.ofi.DropController()
        swtch.Install(switchNode, switchDevices, controller)
    else:
        #controller = ns.openflow.ofi.LearningController.Create()
        controller = ns.openflow.ofi.LearningController()
        if not timeout.IsZero():
            controller.SetAttribute("ExpirationTime", ns.core.TimeValue(timeout))
        swtch.Install(switchNode, switchDevices, controller)

    # Create nodes
    nodes = ns.network.NodeContainer()
    nodes.Create(4)

    # Create links
    pointToPoint = ns.point_to_point.PointToPointHelper()
    pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
    pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))
    devices = pointToPoint.Install(nodes.Get(0), nodes.Get(1))
    devices2 = pointToPoint.Install(nodes.Get(1), nodes.Get(2))
    devices3 = pointToPoint.Install(nodes.Get(2), nodes.Get(3))

    # Add internet stack to the nodes
    internet = ns.internet.InternetStackHelper()
    internet.Install(nodes)

    # Assign IP addresses
    ipv4 = ns.internet.Ipv4AddressHelper()
    ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces = ipv4.Assign(devices)
    interfaces2 = ipv4.Assign(devices2)
    interfaces3 = ipv4.Assign(devices3)
    print(interfaces.GetAddress(1))

    # Create an OnOff application to send UDP datagrams from n0 to n1
    port = 9

    # tst
    # ns.network.InetSocketAddress(interfaces.GetAddress(1), port)
    # ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.1.2"), port))
    # ns.network.Address(ns.network.InetSocketAddress(interfaces.GetAddress(1), port))
    server_address = ns.cppyy.gbl.getNodeIpv4(nodes.Get(0)).GetAddress(1,0).GetLocal()
    client_address = ns.cppyy.gbl.getNodeIpv4(nodes.Get(2)).GetAddress(1,0).GetLocal()
    print(server_address, client_address)
    onoff = ns.applications.OnOffHelper("ns3::UdpSocketFactory", ns.network.InetSocketAddress(client_address.ConvertTo(), port))
    onoff.SetConstantRate(ns.network.DataRate("500kb/s"))
    app = onoff.Install(nodes.Get(2))
    app.Start(ns.core.Seconds(1.0))
    app.Stop(ns.core.Seconds(10.0))

    # Create an optional packet sink to receive these packets
    sink = ns.applications.PacketSinkHelper("ns3::UdpSocketFactory", ns.network.InetSocketAddress(server_address.ConvertTo() , port))
    app2 = sink.Install(nodes.Get(0))
    app2.Start(ns.core.Seconds(0.0))

    # # Create a similar flow from n3 to n0, starting at time 1.1 seconds
    onoff.SetAttribute("Remote", ns.network.AddressValue(ns.network.InetSocketAddress(interfaces.GetAddress(0), port)))
    # app3 = onoff.Install(nodes.Get(3))
    # app3.Start(ns.core.Seconds(1.1))
    # app3.Stop(ns.core.Seconds(10.0))
    # app4 = sink.Install(nodes.Get(0))
    # app4.Start(ns.core.Seconds(0.0))

    # Configure tracing
    ascii = ns.network.AsciiTraceHelper()
    pointToPoint.EnableAsciiAll(ascii.CreateFileStream("openflow-switch.tr"))
    pointToPoint.EnablePcapAll("openflow-switch", False)

    # Run
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()

if __name__ == '__main__':
    sys.exit(main(sys.argv))