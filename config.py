MOBILITY_TCL = '/home/ondro/skola/tp/sumo_to_ns3_py/ns2mobility.tcl'
CONFIG = {
  # Siete, aby sa v GUI dali vykreslit
  "networks": {
    0: {
      "id": 0,
      "color": "#00ff00",
      "ssid": "LTE net",
      "addr": "10.0.1.0/24",
      "type": "LTE"
    },
    1: {
      "id": 1,
      "color": "#0000ff",
      "ssid": "Wifi net",
      "addr": "10.0.0.0/24",
      "type": "WIFI"
    }
  },
	"nodes": {
		0: {
      "id": 0,
      "mobility": {
        "type": "ns2",
      },
			"l2id": 0,
			"l2": "lte",
			"l2conf": {
        "type": "ue"
			},
			"l3": "client/server",
			"l3conf": {
				"prot": "udp/tcp",
				"...": "..."
			}
		},
    12: {
      "id": 0,
      "mobility": {
        "type": "ns2",
      },
			"l2id": 0,
			"l2": "lte",
			"l2conf": {
        "type": "enb"
			},
			"l3": "client/server",
			"l3conf": {
				"prot": "udp/tcp",
				"...": "..."
			}
		},
    1: {
      "id": 0,
      "mobility": {
        "type": "ns2",
      },
			"l2id": 1,
			"l2": "wifi",
			"l2conf": {
        "type": "sta"
			},
			"l3": "client/server",
			"l3conf": {
				"prot": "udp/tcp",
				"...": "..."
			}
		},
    13: {
      "id": 0,
      "mobility": {
        "type": "ns2",
      },
			"l2id": 1,
			"l2": "wifi",
			"l2conf": {
        "type": "ap"
			},
			"l3": "client/server",
			"l3conf": {
				"prot": "udp/tcp",
				"...": "..."
			}
		}
  }
}

