MOBILITY_TCL = '/vlns3/ns2mobility.tcl'

CONFIG = {
  "nodes": {
    "0": {
      "id": 0,
      "l2": "wave",
      "l2conf": {
        "type": "node",
        "attributes": {
          "RxGain": "128.0",
          "TxGain": "128.0"
        }
      },
      "l2id": "0",
      "l3": "udpclient",
      "l3conf": {
        "port": "2222",
        "start": "1",
        "stop": "10",
        "interval": "1",
        "packet_size": "123",
        "max_packets": "12345",
        "comm": "2"
      },
      "mobility": {
        "0": {
          "x": 232,
          "y": 307,
          "z": 1
        },
        "2.0": {
          "x": 314.21,
          "y": 587.21,
          "z": 0
        },
        "3.0": {
          "x": 316.48,
          "y": 586.39,
          "z": 2.41
        },
        "4.0": {
          "x": 320.12,
          "y": 585.07,
          "z": 3.87
        },
        "5.0": {
          "x": 326.04,
          "y": 582.93,
          "z": 6.3
        },
        "6.0": {
          "x": 333.9,
          "y": 580.08,
          "z": 8.35
        },
        "7.0": {
          "x": 341.44,
          "y": 577.35,
          "z": 8.02
        }
      },
      "type": "basic",
      "x": 232,
      "y": 307
    },
    "1": {
      "id": 1,
      "l2": "wave",
      "l2conf": {
        "type": "node",
        "attributes": {
          "RxGain": "128.0",
          "TxGain": "128.0"
        }
      },
      "l2id": "0",
      "l3": "udpclient",
      "l3conf": {
        "comm": "2",
        "max_packets": "80",
        "port": "2222",
        "start": "1",
        "stop": "80"
      },
      "mobility": {
        "0": {
          "x": 46,
          "y": 444,
          "z": 1
        },
        "20.0": {
          "x": 430.81,
          "y": 459.38,
          "z": 0
        },
        "21.0": {
          "x": 431.24,
          "y": 460.69,
          "z": 1.38
        },
        "22.0": {
          "x": 432.11,
          "y": 463.25,
          "z": 2.7
        },
        "23.0": {
          "x": 433.43,
          "y": 467.18,
          "z": 4.14
        },
        "24.0": {
          "x": 435.56,
          "y": 473.52,
          "z": 6.69
        },
        "25.0": {
          "x": 437.99,
          "y": 480.76,
          "z": 7.64
        },
        "26.0": {
          "x": 440.19,
          "y": 487.31,
          "z": 6.9
        },
        "27.0": {
          "x": 442.33,
          "y": 493.67,
          "z": 6.72
        },
        "28.0": {
          "x": 444.65,
          "y": 500.56,
          "z": 7.27
        },
        "29.0": {
          "x": 446.89,
          "y": 507.23,
          "z": 7.04
        },
        "30.0": {
          "x": 449.06,
          "y": 513.69,
          "z": 6.81
        },
        "31.0": {
          "x": 450.64,
          "y": 518.38,
          "z": 4.95
        },
        "32.0": {
          "x": 453.13,
          "y": 524.83,
          "z": 6.93
        },
        "33.0": {
          "x": 458.13,
          "y": 530.46,
          "z": 7.59
        },
        "34.0": {
          "x": 463.72,
          "y": 534.85,
          "z": 7.11
        },
        "35.0": {
          "x": 469.83,
          "y": 539.64,
          "z": 7.77
        },
        "36.0": {
          "x": 475.93,
          "y": 544.41,
          "z": 7.74
        },
        "37.0": {
          "x": 481.6,
          "y": 548.86,
          "z": 7.21
        },
        "38.0": {
          "x": 487.43,
          "y": 553.42,
          "z": 7.4
        },
        "39.0": {
          "x": 493.43,
          "y": 558.12,
          "z": 7.62
        },
        "40.0": {
          "x": 499.11,
          "y": 562.57,
          "z": 7.22
        },
        "41.0": {
          "x": 505.07,
          "y": 567.24,
          "z": 7.57
        },
        "42.0": {
          "x": 511.04,
          "y": 571.91,
          "z": 7.58
        }
      },
      "type": "basic",
      "x": 46,
      "y": 444
    },
    "2": {
      "id": 2,
      "l2": "wave",
      "l2conf": {
        "type": "node",
        "attributes": {
          "RxGain": "128.0",
          "TxGain": "128.0"
        }
      },
      "l2id": "0",
      "l3": "udpserver",
      "l3conf": {
        "port": "2222",
        "start": "1",
        "stop": "80"
      },
      "mobility": {
        "0": {
          "x": 213,
          "y": 589,
          "z": 1
        },
        "24.0": {
          "x": 86.42,
          "y": 506.49,
          "z": 0
        },
        "25.0": {
          "x": 87.11,
          "y": 507.75,
          "z": 1.43
        },
        "26.0": {
          "x": 89.04,
          "y": 511.29,
          "z": 4.03
        },
        "27.0": {
          "x": 92.02,
          "y": 516.73,
          "z": 6.21
        },
        "28.0": {
          "x": 95.98,
          "y": 523.96,
          "z": 8.24
        },
        "29.0": {
          "x": 98.87,
          "y": 529.24,
          "z": 6.02
        },
        "30.0": {
          "x": 102.92,
          "y": 536.41,
          "z": 8.24
        },
        "31.0": {
          "x": 106.99,
          "y": 543.34,
          "z": 8.03
        },
        "32.0": {
          "x": 111.02,
          "y": 550.06,
          "z": 7.84
        },
        "33.0": {
          "x": 114.96,
          "y": 556.62,
          "z": 7.65
        },
        "34.0": {
          "x": 119.34,
          "y": 563.45,
          "z": 8.16
        },
        "35.0": {
          "x": 125.62,
          "y": 568.93,
          "z": 8.33
        },
        "36.0": {
          "x": 131.02,
          "y": 574.52,
          "z": 7.81
        }
      },
      "type": "basic",
      "x": 213,
      "y": 589
    },
    "3": {
      "id": 3,
      "l2": "wave",
      "l2conf": {
        "type": "node",
        "attributes": {
          "RxGain": "128.0",
         "TxGain": "128.0"
        }
      },
      "l2id": "0",
      "l3": None,
      "l3conf": {},
      "mobility": {
        "0": {
          "x": 88,
          "y": 679,
          "z": 1
        },
        "34.0": {
          "x": 58.35,
          "y": 456.81,
          "z": 0
        },
        "35.0": {
          "x": 59.59,
          "y": 459,
          "z": 2.51
        },
        "36.0": {
          "x": 62,
          "y": 463.21,
          "z": 4.85
        },
        "37.0": {
          "x": 65.53,
          "y": 469.42,
          "z": 7.14
        },
        "38.0": {
          "x": 69.87,
          "y": 477.02,
          "z": 8.75
        },
        "39.0": {
          "x": 73.95,
          "y": 484.17,
          "z": 8.23
        },
        "40.0": {
          "x": 75.9,
          "y": 487.6,
          "z": 3.94
        },
        "41.0": {
          "x": 79.53,
          "y": 491.81,
          "z": 5.68
        },
        "42.0": {
          "x": 86.72,
          "y": 491.74,
          "z": 7.42
        },
        "43.0": {
          "x": 94.34,
          "y": 489.42,
          "z": 7.96
        },
        "44.0": {
          "x": 101.82,
          "y": 487.14,
          "z": 7.82
        },
        "45.0": {
          "x": 109.91,
          "y": 484.67,
          "z": 8.46
        },
        "46.0": {
          "x": 117.54,
          "y": 482.34,
          "z": 7.98
        },
        "47.0": {
          "x": 125.33,
          "y": 479.97,
          "z": 8.14
        },
        "48.0": {
          "x": 133.14,
          "y": 477.59,
          "z": 8.16
        },
        "49.0": {
          "x": 141.48,
          "y": 475.05,
          "z": 8.72
        },
        "50.0": {
          "x": 148.85,
          "y": 472.8,
          "z": 7.71
        },
        "51.0": {
          "x": 151.05,
          "y": 474.56,
          "z": 3.49
        },
        "52.0": {
          "x": 148.68,
          "y": 476.2,
          "z": 3.04
        },
        "53.0": {
          "x": 144.43,
          "y": 477.49,
          "z": 4.44
        },
        "54.0": {
          "x": 138.23,
          "y": 479.38,
          "z": 6.48
        },
        "55.0": {
          "x": 130.52,
          "y": 481.73,
          "z": 8.06
        },
        "56.0": {
          "x": 122.33,
          "y": 484.23,
          "z": 8.57
        },
        "57.0": {
          "x": 113.91,
          "y": 486.79,
          "z": 8.8
        },
        "58.0": {
          "x": 106.13,
          "y": 489.16,
          "z": 8.13
        },
        "59.0": {
          "x": 98.65,
          "y": 491.45,
          "z": 7.82
        },
        "60.0": {
          "x": 90.72,
          "y": 493.86,
          "z": 8.29
        },
        "61.0": {
          "x": 84.58,
          "y": 496.1,
          "z": 6.55
        },
        "62.0": {
          "x": 83.55,
          "y": 500.88,
          "z": 5.37
        },
        "63.0": {
          "x": 86.04,
          "y": 505.8,
          "z": 5.52
        },
        "128.0": {
          "x": 89.4,
          "y": 511.93,
          "z": 7
        },
        "65.0": {
          "x": 93.13,
          "y": 518.75,
          "z": 7.77
        },
        "66.0": {
          "x": 97.16,
          "y": 526.12,
          "z": 8.4
        },
        "67.0": {
          "x": 99.13,
          "y": 529.72,
          "z": 4.1
        },
        "68.0": {
          "x": 102.34,
          "y": 535.4,
          "z": 6.53
        },
        "69.0": {
          "x": 106.27,
          "y": 542.14,
          "z": 7.79
        },
        "70.0": {
          "x": 110.78,
          "y": 549.65,
          "z": 8.77
        },
        "71.0": {
          "x": 114.96,
          "y": 556.63,
          "z": 8.14
        },
        "72.0": {
          "x": 119.27,
          "y": 563.39,
          "z": 8.04
        },
        "73.0": {
          "x": 125.96,
          "y": 569.24,
          "z": 8.89
        },
        "74.0": {
          "x": 131.3,
          "y": 574.95,
          "z": 7.85
        },
        "75.0": {
          "x": 135.71,
          "y": 582.76,
          "z": 9
        },
        "76.0": {
          "x": 138.8,
          "y": 590.86,
          "z": 8.68
        },
        "77.0": {
          "x": 141.11,
          "y": 598.45,
          "z": 7.93
        },
        "78.0": {
          "x": 143.62,
          "y": 606.68,
          "z": 8.6
        },
        "79.0": {
          "x": 146.2,
          "y": 615.16,
          "z": 8.87
        },
        "80.0": {
          "x": 148.64,
          "y": 623.19,
          "z": 8.39
        },
        "81.0": {
          "x": 150.77,
          "y": 630.29,
          "z": 7.4
        },
        "82.0": {
          "x": 153.3,
          "y": 638.51,
          "z": 8.6
        },
        "83.0": {
          "x": 155.79,
          "y": 646.25,
          "z": 8.13
        }
      },
      "type": "basic",
      "x": 88,
      "y": 679
    },
    "4": {
      "id": 4,
      "l2": "wave",
      "l2conf": {
        "type": "node",
        "attributes": {
          "RxGain": "128.0",
          "TxGain": "128.0"
        }
      },
      "l2id": "0",
      "l3": None,
      "l3conf": {},
      "mobility": {
        "0": {
          "x": 421,
          "y": 583,
          "z": 1
        },
        "28": {
          "x": 651,
          "y": 266,
          "z": 1
        },
        "29": {
          "x": 395,
          "y": 229,
          "z": 1
        },
        "40.0": {
          "x": 579.94,
          "y": 346.78,
          "z": 0
        },
        "41.0": {
          "x": 578.36,
          "y": 347.79,
          "z": 1.88
        },
        "42.0": {
          "x": 575.14,
          "y": 349.84,
          "z": 3.82
        },
        "43.0": {
          "x": 569.87,
          "y": 353.21,
          "z": 6.25
        },
        "44.0": {
          "x": 563.32,
          "y": 357.39,
          "z": 7.77
        },
        "45.0": {
          "x": 556.75,
          "y": 361.58,
          "z": 7.8
        },
        "46.0": {
          "x": 550.11,
          "y": 365.83,
          "z": 7.88
        },
        "47.0": {
          "x": 542.96,
          "y": 370.39,
          "z": 8.48
        },
        "48.0": {
          "x": 536.81,
          "y": 374.32,
          "z": 7.3
        },
        "49.0": {
          "x": 530.02,
          "y": 378.75,
          "z": 8.11
        },
        "50.0": {
          "x": 523.53,
          "y": 383.02,
          "z": 7.78
        },
        "51.0": {
          "x": 516.68,
          "y": 387.52,
          "z": 8.19
        },
        "52.0": {
          "x": 509.87,
          "y": 392,
          "z": 8.15
        },
        "53.0": {
          "x": 503.18,
          "y": 396.4,
          "z": 8.01
        },
        "54.0": {
          "x": 496.09,
          "y": 401.06,
          "z": 8.48
        },
        "55.0": {
          "x": 489.72,
          "y": 405.25,
          "z": 7.62
        },
        "56.0": {
          "x": 482.99,
          "y": 409.67,
          "z": 8.06
        },
        "57.0": {
          "x": 476.86,
          "y": 413.63,
          "z": 7.3
        },
        "58.0": {
          "x": 469.81,
          "y": 418.17,
          "z": 8.39
        },
        "59.0": {
          "x": 463.64,
          "y": 422.14,
          "z": 7.34
        },
        "60.0": {
          "x": 457.44,
          "y": 426.13,
          "z": 7.37
        },
        "61.0": {
          "x": 450.37,
          "y": 430.68,
          "z": 8.4
        },
        "62.0": {
          "x": 443.46,
          "y": 435.13,
          "z": 8.22
        },
        "63.0": {
          "x": 436.46,
          "y": 439.63,
          "z": 8.32
        },
        "128.0": {
          "x": 431.55,
          "y": 442.79,
          "z": 5.84
        },
        "65.0": {
          "x": 425.84,
          "y": 448.88,
          "z": 8.36
        },
        "66.0": {
          "x": 420,
          "y": 453.89,
          "z": 7.74
        },
        "67.0": {
          "x": 412.65,
          "y": 457.26,
          "z": 8.1
        },
        "68.0": {
          "x": 404.89,
          "y": 460.5,
          "z": 8.41
        },
        "69.0": {
          "x": 397.68,
          "y": 463.52,
          "z": 7.81
        },
        "70.0": {
          "x": 390.22,
          "y": 466.64,
          "z": 8.09
        },
        "71.0": {
          "x": 382.42,
          "y": 469.9,
          "z": 8.45
        },
        "72.0": {
          "x": 374.59,
          "y": 473.18,
          "z": 8.49
        },
        "73.0": {
          "x": 367.48,
          "y": 476.15,
          "z": 7.71
        },
        "74.0": {
          "x": 359.68,
          "y": 479.42,
          "z": 8.45
        },
        "75.0": {
          "x": 352.45,
          "y": 482.44,
          "z": 7.84
        },
        "76.0": {
          "x": 344.68,
          "y": 485.69,
          "z": 8.42
        },
        "77.0": {
          "x": 337.12,
          "y": 488.85,
          "z": 8.19
        },
        "78.0": {
          "x": 329.45,
          "y": 492.06,
          "z": 8.32
        },
        "79.0": {
          "x": 322.3,
          "y": 495.05,
          "z": 7.75
        },
        "80.0": {
          "x": 314.63,
          "y": 498.26,
          "z": 8.32
        },
        "81.0": {
          "x": 307.2,
          "y": 501.37,
          "z": 8.05
        },
        "82.0": {
          "x": 300.49,
          "y": 504.18,
          "z": 7.28
        },
        "83.0": {
          "x": 292.58,
          "y": 507.48,
          "z": 8.56
        },
        "84.0": {
          "x": 284.8,
          "y": 510.74,
          "z": 8.44
        },
        "85.0": {
          "x": 278.07,
          "y": 513.55,
          "z": 7.3
        },
        "86.0": {
          "x": 271.19,
          "y": 516.43,
          "z": 7.46
        },
        "87.0": {
          "x": 264.13,
          "y": 519.39,
          "z": 7.66
        },
        "88.0": {
          "x": 256.3,
          "y": 522.66,
          "z": 8.48
        }
      },
      "type": "basic",
      "x": 421,
      "y": 583
    },
    "5": {
      "id": 5,
      "l2": None,
      "l2conf": {},
      "l2id": -1,
      "l3": None,
      "l3conf": {},
      "mobility": {
        "0": {
          "x": 774,
          "y": 286,
          "z": 1
        }
      },
      "type": "basic",
      "x": 774,
      "y": 286
    },
    "6": {
      "id": 6,
      "l2": None,
      "l2conf": {},
      "l2id": -1,
      "l3": None,
      "l3conf": {},
      "mobility": {
        "0": {
          "x": 682,
          "y": 114,
          "z": 1
        }
      },
      "type": "basic",
      "x": 682,
      "y": 114
    },
    "7": {
      "id": 7,
      "l2": None,
      "l2conf": {},
      "l2id": -1,
      "l3": None,
      "l3conf": {},
      "mobility": {
        "0": {
          "x": 672,
          "y": 430,
          "z": 1
        }
      },
      "type": "basic",
      "x": 672,
      "y": 430
    },
    "8": {
      "id": 8,
      "l2": None,
      "l2conf": {},
      "l2id": -1,
      "l3": None,
      "l3conf": {},
      "mobility": {
        "0": {
          "x": 407,
          "y": 83,
          "z": 1
        }
      },
      "type": "basic",
      "x": 407,
      "y": 83
    },
    "9": {
      "id": 9,
      "type": "sdn",
      "mobility": {
        "0": {
          "x": 503,
          "y": 395,
          "z": 1
        }
      },
      "l2id": -1,
      "l2": None,
      "l2conf": {},
      "l3": None,
      "l3conf": {},
      "x": 503,
      "y": 395,
      "switch_nodes": [
        8
      ],
      "controller": "learning"
    }
  },
  "networks": {
    "0": {
      "addr": "10.1.1.0/24",
      "color": "#e4ff05",
      "id": "0",
      "ssid": "wave",
      "type": "WAVE"
    }
  },
  "connections": [],
  "max_at": 88,
  "routing": None
}
