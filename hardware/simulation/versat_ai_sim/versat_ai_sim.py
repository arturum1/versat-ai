# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):

    attributes_dict = {
        "name": "iob_uut",
        "generate_hw": True,
        "confs": [
            {
                "name": "BAUD",
                "descr": "UART baud rate",
                "type": "D",
                "val": "3000000",
            },
            {
                "name": "FREQ",
                "descr": "Clock frequency",
                "type": "D",
                "val": "100000000",
            },
            {
                "name": "SIMULATION",
                "descr": "Simulation flag",
                "type": "D",
                "val": "1",
            },
        ],
    }
    #
    # Ports
    #
    attributes_dict["ports"] = []

    #
    # Wires
    #
    attributes_dict["wires"] = []

    #
    # Subblocks
    #
    attributes_dict["subblocks"] = []

    #
    # Snippets
    #
    attributes_dict["snippets"] = []

    return attributes_dict
