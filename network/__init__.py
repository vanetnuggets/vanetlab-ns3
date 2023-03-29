from ns import *

ns.cppyy.cppdef("""
Ptr<LteHelper> createLteHelper() {
  return CreateObject<LteHelper>();
};
""")

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from attribute_manager import attribute_manager
from ipaddress import IPv4Network
from log_helper import dbg
import context