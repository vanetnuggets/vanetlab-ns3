from ns import *

# cierna magia
ns.cppyy.cppdef("""
using namespace ns3;

Ptr<Ipv4> getNodeIpv4(Ptr<Node> node) { 
  return node->GetObject<Ipv4>(); 
};
""")