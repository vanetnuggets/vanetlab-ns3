from ns import *

# cierna magia
ns.cppyy.cppdef("""
using namespace ns3;

Ptr<Ipv4> getNodeIpv4(Ptr<Node> node) { 
  return node->GetObject<Ipv4>(); 
};
""")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attribute_manager import attribute_manager
import context