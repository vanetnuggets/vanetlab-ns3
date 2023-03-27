from ns import *

ns.cppyy.cppdef("""
Ptr<LteHelper> createLteHelper() {
  return CreateObject<LteHelper>();
};
""")