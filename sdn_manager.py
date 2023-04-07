from ns import ns
from log_helper import dbg
import context

class SdnManager:
    def __init__(self) -> None:
        config = context.config
        for node_id in config['nodes']:
            if config['nodes'][node_id].get('type') == 'sdn':
                dbg.log(f'creating ovs_switch from node_id: {node_id}')
                SdnSwitch(sw_id=node_id)

class SdnSwitch:
    def __init__(self, sw_id) -> None:
        self.sw_id = sw_id
        self.config = context.config
        self.neighbor_ids = self.config['nodes'][sw_id]['switch_nodes']
        self.terminalDevices = None
        self.switchDevices = None
        self.swtch = None
        
        self._setup()

    def _setup(self) -> None:
        # CONTAINER INITIALIZATION
        switch_c = context.get_node_for_id(self.sw_id)
        neighbors_c = [context.get_node_for_id(i) for i in self.neighbor_ids] 
        
        # CREATING LINKS
        csma = ns.csma.CsmaHelper()
        csma.SetChannelAttribute("DataRate", ns.core.DataRateValue(5000000))
        csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.MilliSeconds(2)))

        # Create the csma links, from each terminal to the switch
        self.terminalDevices = ns.network.NetDeviceContainer()
        self.switchDevices = ns.network.NetDeviceContainer()

        for neighbor in range(len(neighbors_c)):
            link = csma.Install(ns.network.NodeContainer(ns.network.NodeContainer(neighbor), switch_c))
            self.terminalDevices.Add(link.Get(0))
            self.switchDevices.Add(link.Get(1))

        # CREATING SWITCH   
        self.swtch = ns.openflow.OpenFlowSwitchHelper()
        
        if self.config['nodes'][self.sw_id]['controller'] == 'drop':
            controller = ns.openflow.ofi.DropController()
            self.swtch.Install(switch_c, self.switchDevices, controller)
        elif self.config['nodes'][self.sw_id]['controller'] == 'learning':
            controller = ns.openflow.ofi.LearningController()
            # if not timeout.IsZero():
            #     controller.SetAttribute("ExpirationTime", ns.core.TimeValue(timeout))
            self.swtch.Install(switch_c, self.switchDevices, controller)
        else:
            dbg.err('you have to specify controller type')
        dbg.log(f'switch_id: {self.sw_id} installed')