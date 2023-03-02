from ns.network import *
from ns.lte import *
from ns.mobility import MobilityHelper
from log_helper import dbg

DEBUG = True

class LteUtil:
	lte_helper = {}
	mobility = {}

	enb_devs = {}
	ue_devs = {}

	ue_nodes = {}
	enb_nodes = {}

	config = {}

	def __init__(self, config):
		self.config = config
		self.nodemap = {}
		for node_id in config['nodes']:
			l2id = config['nodes'][node_id]['l2id']
			if l2id not in self.nodemap:
				self.nodemap[l2id] = []
			self.nodemap[l2id].append(config['nodes'][node_id])
		self.netmap = config['networks']

	def install(self, nodes):
		for l2id in self.nodemap:
			# Ignore non-LTE networks
			if self.netmap[l2id]['type'] != 'LTE':
					continue

			enbs = []
			ues = []

			curr_nodes = self.nodemap[l2id]
			for node in curr_nodes:
					node_id = node['id']
					node_type = node['l2conf']['type']

					if node_type == 'enb':
							enbs.append(node_id)
					elif node_type == 'ue':
							ues.append(node_id)
			
			dbg.log(f'parsed {len(enbs)} enb nodes and {len(ues)} ue nodes in network with id {l2id}.')
			
			self.enb_nodes[l2id] = NodeContainer()
			for enb_node in enbs:
				self.enb_nodes[l2id].Add(nodes.Get(enb_node))

			self.lte_helper[l2id] = LteHelper()
			self.enb_devs[l2id] = self.lte_helper[l2id].InstallEnbDevice(self.enb_nodes[l2id])
			dbg.log(f'installed {len(enbs)} enb nodes in network with id {l2id}')

			self.ue_nodes[l2id] = NodeContainer()
			for ue_node in ues:
				self.ue_nodes[l2id].Add(nodes.Get(ue_node))

			self.ue_devs[l2id] = self.lte_helper[l2id].InstallUeDevice(self.ue_nodes[l2id])
			
			dbg.log(f'installed {len(ues)} ue nodes in network with id {l2id}')

			# If more than one ENB dev, soemhow choose, maybe from config ? 
			self.lte_helper[l2id].Attach(self.ue_devs[l2id], self.enb_devs[l2id].Get(0))
			dbg.log(f'configured LTE network with id {l2id}')

class PhyUtil:
	def __init__(self, config):
		self.config = config

		self.lte_util = LteUtil(self.config)

	def install(self, nodes):
			dbg.log(f'installing LTE networks...')
			self.lte_util.install(nodes)
