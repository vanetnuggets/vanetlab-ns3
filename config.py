MOBILITY_TCL = '/home/ondro/skola/tp/sumo_to_ns3_py/ns2mobility.tcl'
CONFIG = {
  # Siete, aby sa v GUI dali vykreslit
  "networks": {
    "0": {
      "id": 0,
      "color": "#00ff00",
      "ssid": "LTE net",
      "addr": "10.0.1.0/24",
      "type": "LTE"
    },
    "1": {
      "id": 1,
      "color": "#0000ff",
      "ssid": "Wifi net",
      "addr": "10.0.2.0/24",
      "type": "WIFI"
    },
    "2": {
      "id": 2,
      "color": "#ffff00",
      "ssid": "Eth net",
      "addr": "10.0.3.0/24",
      "type": "ETH"
    }
  },
  "max_at": 204.0,
  "nodes": {
    "11": {
      "id": 11,
      "mobility": {},
      "l2id": -1,
      "l2": None,
      "l2conf": {},
      "l3": None
    },
    "1": {
      "id": 1,
      "mobility": {},
      "l2id": "0",
      "l2": "lte",
      "l2conf": {
        "type": "ue"
      },
      "l3": None
    },
    "2": {
      "id": 2,
      "mobility": {},
      "l2id": "0",
      "l2": "lte",
      "l2conf": {
        "type": "ue"
      },
      "l3": "udpclient",
      "l3conf": {
        "comm": "10",
        "port": 4444,
        "start": 0,
        "stop": 204,
        "attributes": {
          "MaxPackets": 2500
        }
      }
    },
    "3": {
      "id": 3,
      "mobility": {},
      "l2id": "0",
      "l2": "lte",
      "l2conf": {
        "type": "enb"
      },
      "l3": None
    },
    "11": {
      "id": 11,
      "mobility": {},
      "l2id": -1,
      "l2": None,
      "l2conf": {},
      "l3": None
    },
    "12": {
      "id": 12,
      "mobility": {},
      "l2id": "0",
      "l2": "lte",
      "l2conf": {
        "type": "pgw"
      },
      "l3": None
    },
    "4": {
      "id": 4,
      "mobility": {},
      "l2id": "1",
      "attributes": {
        "RxGain": 32.0,
        "TxGain": 32.0
      },
      "l2": "wifi",
      "l2conf": {
        "type": "sta"
      },
      "l3": "tcpclient",
      "l3conf": {
        "comm": "8",
        "port": 4242,
        "start": 0,
        "stop": 204,
        "attributes": {
          "MaxBytes": 2500
        }
      }
    },
    "5": {
      "id": 5,
      "mobility": {},
      "l2id": "1",
      "l2": "wifi",
      "l2conf": {
        "type": "sta"
      },
      "l3": None
    },
    "6": {
      "id": 6,
      "mobility": {
      },
      "l2id": "1",
      "l2": "wifi",
      "l2conf": {
        "type": "ap"
      },
      "l3": None
    },
    "7": {
      "id": 7,
      "mobility": {},
      "l2id": "2",
      "l2": "eth",
      "l2conf": {},
      "l3": None
    },
    "8": {
      "id": 8,
      "mobility": {},
      "l2id": "2",
      "l2": "eth",
      "l2conf": {},
      "l3": "tcpserver",
      "l3conf": {
        "port": 4242,
        "start": 0,
        "stop": 204
      }
    },
    "9": {
      "id": 9,
      "mobility": {},
      "l2id": "2",
      "l2": "eth",
      "l2conf": {},
      "l3": None
    },
    "10": {
      "id": 10,
      "mobility": {},
      "l2id": "2",
      "l2": "eth",
      "l2conf": {},
      "l3": "udpserver",
      "l3conf": {
        "port": 4444,
        "start": 0,
        "stop": 204
      }
    },
  },
  "connections": [{
      "node_from": "12",
      "node_to": "7",
    }, {
      "node_from": "9",
      "node_to": "6"
    }
  ],
  "routing": "olsr"
}
