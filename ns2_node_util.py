import re

# i stole this somewhere and rewrote it in python
class Ns2NodeUtility:
	filename = ""
	input_file = None
	node_times = {}

	def __init__(self, filename):
		self.filename = filename
		self.input_file = open(self.filename)

		node_ids = []
		
		for line in self.input_file:
			line = line.strip()

			r = r'\$ns_ at (\d+\.\d+) "\$node_\((\d+)\)'
			
			matches = re.findall(r, line)
			
			if len(matches) > 0:
				match = matches[0]

				new_latest = match[0]
				node_id = match[1]

				if node_id in node_ids:
					self.node_times[node_id] = (float(self.node_times[node_id][0]), float(new_latest))
				else:
					self.node_times[node_id] = (float(new_latest), float(new_latest))

				node_ids.append(node_id)

	def print_information(self):
		for key in self.node_times:
			start, end = self.node_times[key]
			print(f"node {key} started at {start} and ended at {end}.")

	def get_n_nodes(self):
		return len(self.node_times)

	def get_entry_time_for_node(self, node_id):
		if node_id not in node_times:
			raise Exception(f"node not in {self.filename}")
		return self.node_times[node_id][0]

	def get_exit_time_for_node(self, node_id):
		if node_id not in node_times:
			raise Exception(f"node not in {self.filename}")
		return self.node_times[node_id][1]

	def get_simulation_time(self):
		time = 0
		for key in self.node_times:
			_, end = self.node_times[key]
			time = max(time, end)
		return time
