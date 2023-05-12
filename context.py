from log_helper import dbg

path = '.'
config = None
ip_util = None
phy_util = None
app_util = None
nodes = None
_nodes_index_map = {}

def _init_nodes():
  tmp = []
  for node_id in config['nodes']:
    node_id = int(node_id)
    tmp.append(node_id)

  tmp.sort()

  for index, node_id in enumerate(tmp):
    _nodes_index_map[node_id] = index
  
  dbg.log('initialized id to node index mapping')
  

def get_node_for_id(node_id):
  index = _nodes_index_map[int(node_id)]
  return nodes.Get(int(node_id))
  # return nodes.Get(index)

def get_index_for_id(node_id):
  return _nodes_index_map[int(node_id)]

def init():
  _nodes_index_map = {}
  _init_nodes()


ENABLE_LTE = False
