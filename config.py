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
      "addr": "10.0.2.0/24",
      "type": "WIFI"
    }
  },
	"max_at": 204.0,
	"nodes": {
  	3: {
      "id": 3,
      "mobility": {
				
      },
			"l2id": 0,
			"l2": "lte",
			"l2conf": {
        "type": "ue"
			},
			"l3": "udp_echo_server",
			"l3conf": {
				"port": 4242,
				"start": 0,
				"stop": 204
			}
		},
		7: {
      "id": 7,
      "mobility": {
        "type": "ns2"
      },
			"l2id": 0,
			"l2": "lte",
			"l2conf": {
        "type": "ue"
			},
			"l3": None
		},
		13: {
			"id": 13,
			"mobility": {
				"type": "ns2",
			},
			"l2id": 0,
			"l2": "lte",
			"l2conf": {
				"type": "enb"
			},
			"l3": None
		},
    4: {
      "id": 4,
      "mobility": {
        "type": "ns2",
      },
			"l2id": 1,
			"l2": "wifi",
			"l2conf": {
        "type": "sta"
			},
			"l3": "udp_echo_client",
			"l3conf": {
				"comm": 3,
				"port": 4242,
				"start": 0,
				"stop": 204,
				"max_packets": 204
			}
		},
		5: {
      "id": 5,
      "mobility": {
        "type": "ns2",
      },
			"l2id": 1,
			"l2": "wifi",
			"l2conf": {
        "type": "sta"
			},
			"l3": None
		},
    12: {
      "id": 12,
      "mobility": {
      },
			"l2id": 1,
			"l2": "wifi",
			"l2conf": {
        "type": "ap"
			},
			"l3": None
		}
  }
}
