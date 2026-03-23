# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import subprocess
import os


def setup(py_params_dict):

    params = {
        # Name of the generated System
        "name": "iob_soc_tester",
        # If should initialize memories from data in .hex files
        "init_mem": int(py_params_dict.get("init_mem", True)),
        # If should include an internal memory
        "use_intmem": True,
        # If should use external memory (usually DDR)
        "use_extmem": True,
        # If should include a bootrom
        "use_bootrom": True,
        # If should include peripherals
        "use_peripherals": True,
        # If should setup ethernet ports and testbenches
        "use_ethernet": False,
        # If should setup ila
        "use_ila": int(py_params_dict.get("use_ila", False)),
        # CPU address width
        "addr_w": 32,
        # CPU data width
        "data_w": 32,
        # Memory address width
        "mem_addr_w": 20,
        # Bootrom address width
        "bootrom_addr_w": 18,
        # Firmware base address
        "fw_baseaddr": 0x00000000,
        # Firmware address width
        "fw_addr_w": 20,
        # Internal memory address width
        "intmem_addr_w": 20,
        # If should include a tester system
        "include_tester": False,
        # If should include default system snippet
        "include_snippet": False,
        # CPU selection
        "cpu": "iob_vexriscv",
        # If should use stream configuration
        "stream": int(py_params_dict.get("stream_config", False)),
    }

    # Don't copy files for other targets (like clean)
    if py_params_dict.get("py2hwsw_target", "") == "setup":
        dst = f"{py_params_dict['build_dir']}/tester/software/src/"
        os.makedirs(dst, exist_ok=True)
        src = f"../../../software/src/"
        for src_file in [
            "iob_regfileif_csrs_conf.h",
            "iob_regfileif_csrs.h",
            "iob_regfileif_csrs.c",
            "iob_regfileif_conf.h",
            "versat_ai_conf.h",
        ]:
            subprocess.run(
                [
                    "ln",
                    "-s",
                    f"{src}{src_file}",
                    f"{dst}{src_file}",
                ],
                check=True,
            )

    num_xbar_managers = 0
    for param_name in ["use_intmem", "use_extmem", "use_bootrom", "use_peripherals"]:
        if params[param_name]:
            num_xbar_managers += 1
    xbar_sel_w = (num_xbar_managers - 1).bit_length()

    ### Confs ###
    confs = []

    confs = [
        {
            "name": "SIMULATION",
            "descr": "Simulation flag",
            "type": "P",
            "val": "0",
            "min": "0",
            "max": "1",
        },
        {
            "name": "ILA",
            "descr": "Enable support for ila at the cost of a larger firmware size.",
            "type": "M",
            "val": params["use_ila"],
            "min": "0",
            "max": "1",
        },
        {
            "name": "STREAM",
            "descr": "Use stream configuration.",
            "type": "M",
            "val": params["stream"],
            "min": "0",
            "max": "1",
        },
    ]

    if params["use_ila"]:
        confs += [
            {
                "name": "ILA0_BUFFER_W",
                "type": "D",
                "val": "13",
                "min": "NA",
                "max": "NA",
                "descr": "Size of the buffer to store samples.",
            },
            {
                "name": "ILA0_SIGNAL_W",
                "type": "D",
                "val": "102",
                "min": "1",
                "max": "9999",
                "descr": "Width of the sampler signal input.",
            },
            {
                "name": "ILA0_TRIGGER_W",
                "type": "D",
                "val": "5",
                "min": "1",
                "max": "32",
                "descr": "Width of the trigger input.",
            },
        ]

    ### Ports ###
    ports = []

    ports += [
        {
            "name": "mclk_i",
            "signals": [
                {
                    "name": "mclk_i",
                    "width": "1",
                },
            ],
        },
        {
            "name": "arst_mclk_i",
            "signals": [
                {
                    "name": "arst_mclk_i",
                    "width": "1",
                },
            ],
        },
    ]

    if params["use_intmem"]:
        ports += [
            {
                "name": "external_mem_bus_m",
                "descr": "Port for connection to external 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": params["intmem_addr_w"] - 2,
                    "DATA_W": params["data_w"],
                },
            },
        ]
    if params["use_ethernet"]:
        ports += [
            {
                "name": "phy_io",
                "descr": "PHY Interface Ports",
                "signals": [
                    {
                        "name": "MTxClk_i",
                        "width": "1",
                        "descr": "Transmit Nibble or Symbol Clock. The PHY provides the MTxClk signal. It operates at a frequency of 25 MHz (100 Mbps) or 2.5 MHz (10 Mbps). The clock is used as a timing reference for the transfer of MTxD[3:0], MtxEn, and MTxErr.",
                    },
                    {
                        "name": "MTxEn_o",
                        "width": "1",
                        "descr": "Transmit Enable. When asserted, this signal indicates to the PHY that the data MTxD[3:0] is valid and the transmission can start. The transmission starts with the first nibble of the preamble. The signal remains asserted until all nibbles to be transmitted are presented to the PHY. It is deasserted prior to the first MTxClk, following the final nibble of a frame.",
                    },
                    {
                        "name": "MTxD_o",
                        "width": "4",
                        "descr": "Transmit Data Nibble. Signals are the transmit data nibbles. They are synchronized to the rising edge of MTxClk. When MTxEn is asserted, PHY accepts the MTxD.",
                    },
                    {
                        "name": "MTxErr_o",
                        "width": "1",
                        "descr": "Transmit Coding Error. When asserted for one MTxClk clock period while MTxEn is also asserted, this signal causes the PHY to transmit one or more symbols that are not part of the valid data or delimiter set somewhere in the frame being transmitted to indicate that there has been a transmit coding error.",
                    },
                    {
                        "name": "MRxClk_i",
                        "width": "1",
                        "descr": "Receive Nibble or Symbol Clock. The PHY provides the MRxClk signal. It operates at a frequency of 25 MHz (100 Mbps) or 2.5 MHz (10 Mbps). The clock is used as a timing reference for the reception of MRxD[3:0], MRxDV, and MRxErr.",
                    },
                    {
                        "name": "MRxDv_i",
                        "width": "1",
                        "descr": "Receive Data Valid. The PHY asserts this signal to indicate to the Rx MAC that it is presenting the valid nibbles on the MRxD[3:0] signals. The signal is asserted synchronously to the MRxClk. MRxDV is asserted from the first recovered nibble of the frame to the final recovered nibble. It is then deasserted prior to the first MRxClk that follows the final nibble.",
                    },
                    {
                        "name": "MRxD_i",
                        "width": "4",
                        "descr": "Receive Data Nibble. These signals are the receive data nibble. They are synchronized to the rising edge of MRxClk. When MRxDV is asserted, the PHY sends a data nibble to the Rx MAC. For a correctly interpreted frame, seven bytes of a preamble and a completely formed SFD must be passed across the interface.",
                    },
                    {
                        "name": "MRxErr_i",
                        "width": "1",
                        "descr": "Receive Error. The PHY asserts this signal to indicate to the Rx MAC that a media error was detected during the transmission of the current frame. MRxErr is synchronous to the MRxClk and is asserted for one or more MRxClk clock periods and then deasserted.",
                    },
                    {
                        "name": "MColl_i",
                        "width": "1",
                        "descr": "Collision Detected. The PHY asynchronously asserts the collision signal MColl after the collision has been detected on the media. When deasserted, no collision is detected on the media.",
                    },
                    {
                        "name": "MCrS_i",
                        "width": "1",
                        "descr": "Carrier Sense. The PHY asynchronously asserts the carrier sense MCrS signal after the medium is detected in a non-idle state. When deasserted, this signal indicates that the media is in an idle state (and the transmission can start).",
                    },
                    {
                        "name": "MDC_o",
                        "width": "1",
                        "descr": "Management Data Clock. This is a clock for the MDIO serial data channel.",
                    },
                    {
                        "name": "MDIO_o",  # TODO: Make this port bidirectional. Probably best by using two separate ports, as 'inout' may not be synthesizable.ç
                        "width": "1",
                        "descr": "Management Data Input/Output. Bi-directional serial data channel for PHY/STA communication.",
                    },
                    {
                        "name": "phy_rstn_o",
                        "width": "1",
                        "descr": "Reset signal for PHY. Duration configurable via PHY_RST_CNT parameter.",
                    },
                ],
            },
        ]

    ### Wires ###
    wires = []

    if params["use_intmem"]:
        wires += [
            {
                "name": "int_mem_axi",
                "descr": "AXI manager interface for internal memory",
                "signals": {
                    "type": "axi",
                    "prefix": "int_mem_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": f"{params['intmem_addr_w']}-2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": 1,
                },
            },
        ]

    wires += [
        {
            "name": "unused_interconnect_bits",
            "descr": "Wires to connect to unused output bits of interconnect",
            "signals": [
                {
                    "name": "unused_m0_araddr_bits",
                    "width": params["addr_w"] - params["intmem_addr_w"],
                },
                {
                    "name": "unused_m0_awaddr_bits",
                    "width": params["addr_w"] - params["intmem_addr_w"],
                },
                {
                    "name": "unused_m1_araddr_bits",
                    "width": f"{params['addr_w']} - AXI_ADDR_W",
                },
                {
                    "name": "unused_m1_awaddr_bits",
                    "width": f"{params['addr_w']} - AXI_ADDR_W",
                },
                {
                    "name": "unused_m2_araddr_bits",
                    "width": params["addr_w"] - (params["bootrom_addr_w"] + 1),
                },
                {
                    "name": "unused_m2_awaddr_bits",
                    "width": params["addr_w"] - (params["bootrom_addr_w"] + 1),
                },
                {"name": "unused_m3_araddr_bits", "width": xbar_sel_w},
                {"name": "unused_m3_awaddr_bits", "width": xbar_sel_w},
            ],
        },
        {
            "name": "reset_addr",
            "descr": "",
            "signals": [
                {"name": "reset_addr", "width": 32},
            ],
        },
        {
            "name": "rs232",
            "descr": "rs232 bus",
            "signals": {
                "type": "rs232",
                "prefix": "sut_",
            },
        },
        {
            "name": "rs232_invert",
            "descr": "Invert order of rs232 signals",
            "signals": [
                {"name": "sut_rs232_txd"},
                {"name": "sut_rs232_rxd"},
                {"name": "sut_rs232_cts"},
                {"name": "sut_rs232_rts"},
            ],
        },
        {
            "name": "uart0_interrupt",
            "descr": "",
            "signals": [
                {"name": "uart0_interrupt", "width": 1},
            ],
        },
        {
            "name": "uart1_interrupt",
            "descr": "",
            "signals": [
                {"name": "uart1_interrupt", "width": 1},
            ],
        },
    ]

    if params["use_ethernet"]:
        wires += [
            {
                "name": "ethernet_interrupt",
                "descr": "",
                "signals": [
                    {"name": "ethernet_interrupt", "width": 1},
                ],
            },
            {
                "name": "eth_axi",
                "descr": "",
                "signals": {
                    "prefix": "eth_",
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                },
            },
        ]

    if params["use_extmem"]:
        wires += [
            {
                "name": "sut_axi",
                "descr": "AXI bus to connect SUT to address_translator",
                "signals": {
                    "type": "axi",
                    "prefix": "sut_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W-2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
            },
            {
                "name": "translated_sut_axi",
                "descr": "AXI bus to connect address_translator to interconnect",
                "signals": {
                    "type": "axi",
                    "prefix": "translated_sut_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["addr_w"] - 2,
                    "DATA_W": params["data_w"],
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
            },
        ]

    if params["use_ila"]:
        wires += [
            {
                "name": "reset_combo",
                "descr": "",
                "signals": [
                    {"name": "reset_combo", "width": 1},
                ],
            },
            {
                "name": "clk_en_reset",
                "descr": "",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "cke_i"},
                    {"name": "reset_combo"},
                ],
            },
            {
                "name": "reset",
                "descr": "",
                "signals": [
                    {"name": "reset", "width": 1},
                ],
            },
            {
                "name": "watchdog0_active",
                "descr": "",
                "signals": [
                    {"name": "watchdog0_active", "width": 1},
                ],
            },
            {
                "name": "ILA0_ila",
                "descr": "",
                "signals": [
                    {
                        "name": "ILA0_signal",
                        "width": "ILA0_SIGNAL_W",
                    },
                    {
                        "name": "ILA0_trigger",
                        "width": "ILA0_TRIGGER_W",
                    },
                    {
                        "name": "ILA0_sampling_clk",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "ILA0_dma",
                "descr": "",
                "signals": [
                    {
                        "name": "ila_tdata_o",
                        "width": 32,
                    },
                    {
                        "name": "ila_tvalid_o",
                        "width": 1,
                    },
                    {
                        "name": "ila_tready_i",
                        "width": 1,
                    },
                ],
            },
        ]

    if params["stream"]:
        wires += [
            {
                "name": "axistreamin_interrupt",
                "descr": "",
                "signals": [
                    {"name": "axistreamin_interrupt", "width": 1},
                ],
            },
            {
                "name": "overflow",
                "descr": "",
                "signals": [
                    {"name": "overflow", "width": 1},
                ],
            },
            {
                "name": "axistreamout_interrupt",
                "descr": "",
                "signals": [
                    {"name": "axistreamout_interrupt", "width": 1},
                ],
            },
            {
                "name": "underflow",
                "descr": "",
                "signals": [
                    {"name": "underflow", "width": 1},
                ],
            },
            {
                "name": "axistream_in",
                "descr": "",
                "signals": [
                    {
                        "name": "axis_in_clk_i",
                        "width": "1",
                        "descr": "Clock.",
                    },
                    {
                        "name": "axis_in_cke_i",
                        "width": "1",
                        "descr": "Clock enable",
                    },
                    {
                        "name": "axis_in_arst_i",
                        "width": "1",
                        "descr": "Asynchronous and active high reset.",
                    },
                    {
                        "name": "axis_in_tdata_i",
                        "width": "32",
                        "descr": "Data.",
                    },
                    {
                        "name": "axis_in_tvalid_i",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axis_in_tready_o",
                        "width": "1",
                        "descr": "Ready.",
                    },
                    {
                        "name": "axis_in_tlast_i",
                        "width": "1",
                        "descr": "Last word.",
                    },
                ],
            },
            {
                "name": "axistream_out",
                "descr": "",
                "signals": [
                    {
                        "name": "axis_out_clk_i",
                        "width": "1",
                        "descr": "Clock.",
                    },
                    {
                        "name": "axis_out_cke_i",
                        "width": "1",
                        "descr": "Clock enable.",
                    },
                    {
                        "name": "axis_out_arst_i",
                        "width": "1",
                        "descr": "Aynchronous and active high reset.",
                    },
                    {
                        "name": "axis_out_tdata_o",
                        "width": "32",
                        "descr": "Data.",
                    },
                    {
                        "name": "axis_out_tvalid_o",
                        "width": "1",
                        "descr": "Valid.",
                    },
                    {
                        "name": "axis_out_tready_i",
                        "width": "1",
                        "descr": "Ready.",
                    },
                    {
                        "name": "axis_out_tlast_o",
                        "width": "1",
                        "descr": "Last word.",
                    },
                ],
            },
            {
                "name": "decoder_interrupt",
                "descr": "",
                "signals": [
                    {"name": "decoder_interrupt", "width": "1"},
                ],
            },
            {
                "name": "axis_clk_en_rst",
                "descr": "",
                "signals": [
                    {"name": "axis_out_clk_i"},
                    {"name": "axis_out_arst_i"},
                    {"name": "axis_out_cke_i"},
                ],
            },
            {
                "name": "axis_out_tready_i",
                "descr": "",
                "signals": [
                    {"name": "axis_out_tready_i"},
                ],
            },
            {
                "name": "sys_axis_in",
                "descr": "",
                "signals": [
                    {
                        "name": "sys_axis_in_tdata",
                        "width": 32,
                    },
                    {
                        "name": "sys_axis_in_tvalid",
                        "width": 1,
                    },
                    {
                        "name": "sys_axis_in_tready",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "sys_axis_out",
                "descr": "",
                "signals": [
                    {
                        "name": "sys_axis_out_tdata",
                        "width": 32,
                    },
                    {
                        "name": "sys_axis_out_tvalid",
                        "width": 1,
                    },
                    {
                        "name": "sys_axis_out_tready",
                        "width": 1,
                    },
                ],
            },
            {
                "name": "dma_axi",
                "descr": "",
                "signals": {
                    "prefix": "dma_",
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                },
            },
            {
                "name": "nc0_clk_gen",
                "descr": "",
                "signals": [
                    {
                        "name": "mclk_i",
                    },
                    {
                        "name": "arst_i",
                    },
                    {
                        "name": "cke_i",
                    },
                    {
                        "name": "nco0_clk_out",
                        "width": "1",
                    },
                ],
            },
            {
                "name": "nco0_clk_out",
                "descr": "",
                "signals": [
                    {"name": "nco0_clk_out"},
                ],
            },
            {
                "name": "mcke",
                "descr": "",
                "signals": [
                    {"name": "mcke", "width": 1},
                ],
            },
            {
                "name": "pulse",
                "descr": "",
                "signals": [
                    {"name": "pulse", "width": 1},
                ],
            },
            {
                "name": "edge_detect_clk_en_rst",
                "descr": "",
                "signals": [
                    {
                        "name": "mclk_i",
                    },
                    {
                        "name": "cke_i",
                    },
                    {
                        "name": "arst_mclk_i",
                    },
                ],
            },
        ]

    ### Subblocks ###
    subblocks = []

    if params["use_intmem"]:
        subblocks += [
            {
                "core_name": "iob_axi_ram",
                "instance_name": "internal_memory",
                "instance_description": "Internal memory",
                "parameters": {
                    "ID_WIDTH": "AXI_ID_W",
                    "LEN_WIDTH": "AXI_LEN_W",
                    "ADDR_WIDTH": params["intmem_addr_w"],
                    "DATA_WIDTH": "AXI_DATA_W",
                },
                "connect": {
                    "clk_i": "clk",
                    "rst_i": "rst",
                    "axi_s": (
                        "int_mem_axi",
                        [
                            "{int_mem_axi_araddr, 2'b0}",
                            "{int_mem_axi_awaddr, 2'b0}",
                            "{1'b0, int_mem_axi_arlock}",
                            "{1'b0, int_mem_axi_awlock}",
                        ],
                    ),
                    "external_mem_bus_m": "external_mem_bus_m",
                },
            },
        ]

    subblocks += [
        {
            "core_name": py_params_dict["instantiator"]["original_name"],
            "instance_name": "SUT0",
            "instance_description": "System Under Test (SUT) peripheral",
            "is_peripheral": True,
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "init_mem": params["init_mem"],
            "use_extmem": params["use_extmem"],
            "use_ethernet": params["use_ethernet"],
            "stream_config": params["stream"],
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_reset" if params["use_ila"] else "clk_en_rst_s"
                ),
                "rs232_m": "rs232",
            },
        },
    ]

    if params["use_extmem"]:
        subblocks[-1]["connect"].update(
            {
                "axi_m": "sut_axi",
            }
        )

    if params["stream"]:
        subblocks[-1]["connect"].update(
            {
                "axistream_in_io": "axistream_out",
                "axistream_out_io": "axistream_in",
                "interrupt_o": "decoder_interrupt",
            }
        )

    num_subordinates = 2
    subblocks += [
        {
            "core_name": "iob_axi_full_xbar",
            "name": params["name"] + "_axi_full_xbar",
            "instance_name": "iob_axi_full_xbar",
            "instance_description": "AXI full xbar instance",
            "parameters": {
                "ID_W": "AXI_ID_W",
                "LEN_W": "AXI_LEN_W",
            },
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_reset" if params["use_ila"] else "clk_en_rst_s"
                ),
                "rst_i": "rst",
                "s0_axi_s": "cpu_ibus",
                "s1_axi_s": "cpu_dbus",
                "m0_axi_m": (
                    "int_mem_axi",
                    [
                        "{unused_m0_araddr_bits, int_mem_axi_araddr}",
                        "{unused_m0_awaddr_bits, int_mem_axi_awaddr}",
                    ],
                ),
                "m1_axi_m": (
                    "axi_m",
                    (
                        [
                            "{unused_m1_araddr_bits, axi_araddr_o}",
                            "{unused_m1_awaddr_bits, axi_awaddr_o}",
                        ]
                        if params["use_extmem"]
                        else []
                    ),
                ),
                "m2_axi_m": (
                    "bootrom_cbus",
                    [
                        "{unused_m2_araddr_bits, bootrom_axi_araddr}",
                        "{unused_m2_awaddr_bits, bootrom_axi_awaddr}",
                    ],
                ),
                "m3_axi_m": (
                    "axi_periphs_cbus",
                    [
                        "{unused_m3_araddr_bits, periphs_axi_araddr}",
                        "{unused_m3_awaddr_bits, periphs_axi_awaddr}",
                        "periphs_axi_awlock[0]",
                        "periphs_axi_arlock[0]",
                    ],
                ),
            },
            "addr_w": params["addr_w"] - 2,
            "data_w": params["data_w"],
            "lock_w": 1,
            "num_managers": 4,
        },
    ]

    # Connect xbar subordinate interfaces
    # (Lower number has higher priority in case of collision)
    if params["use_ethernet"]:
        subblocks[-1]["connect"].update(
            {
                f"s{num_subordinates}_axi_s": (
                    "eth_axi",
                    [
                        f"eth_axi_araddr[{params['addr_w']-1}:2]",
                        "eth_axi_arlock[0]",
                        f"eth_axi_awaddr[{params['addr_w']-1}:2]",
                        "eth_axi_awlock[0]",
                    ],
                ),
            }
        )
        num_subordinates += 1

    if params["use_extmem"]:
        subblocks[-1]["connect"].update(
            {
                f"s{num_subordinates}_axi_s": "translated_sut_axi",
            }
        )
        num_subordinates += 1

    if params["stream"]:
        subblocks[-1]["connect"].update(
            {
                f"s{num_subordinates}_axi_s": (
                    "dma_axi",
                    [
                        f"dma_axi_araddr[{params['addr_w']-1}:2]",
                        "dma_axi_arlock[0]",
                        f"dma_axi_awaddr[{params['addr_w']-1}:2]",
                        "dma_axi_awlock[0]",
                    ],
                ),
            }
        )
        num_subordinates += 1

    # Set number of subordinate interfaces
    subblocks[-1]["num_subordinates"] = num_subordinates

    subblocks += [
        {  # Change vexriscv to custom configuration
            "core_name": "versat_ai_vexriscv",
            "name": params["name"] + "_" + params["cpu"],
            "instance_name": "cpu",
            "instance_description": "CPU instance. Custom version of vexriscv featuring a extension to support the clz instruction.",
            "parameters": {
                "AXI_ID_W": "1",
                "AXI_ADDR_W": params["addr_w"],
                "AXI_DATA_W": params["data_w"],
                "AXI_LEN_W": "AXI_LEN_W",
            },
            "connect": {
                "resetVector_i": "reset_addr",
                "clk_en_rst_s": (
                    "clk_en_reset" if params["use_ila"] else "clk_en_rst_s"
                ),
                "rst_i": "rst",
                "i_bus_m": (
                    "cpu_ibus",
                    [
                        "cpu_i_axi_arid[0]",
                        "cpu_i_axi_rid[0]",
                        "cpu_i_axi_awid[0]",
                        "cpu_i_axi_bid[0]",
                    ],
                ),
                "d_bus_m": (
                    "cpu_dbus",
                    [
                        "cpu_d_axi_arid[0]",
                        "cpu_d_axi_rid[0]",
                        "cpu_d_axi_awid[0]",
                        "cpu_d_axi_bid[0]",
                    ],
                ),
                "plic_interrupts_i": "interrupts",
                "plic_cbus_s": (
                    "plic_cbus",
                    ["plic_cbus_iob_addr[22-2-1:0]"],
                ),
                "clint_cbus_s": (
                    "clint_cbus",
                    ["clint_cbus_iob_addr[16-2-1:0]"],
                ),
            },
        },
        {
            "core_name": "versat_ai_uart",
            "instance_name": "UART0",
            "instance_description": "UART peripheral. This peripheral sends information about the current status of the system under test.",
            "is_peripheral": True,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_reset" if params["use_ila"] else "clk_en_rst_s"
                ),
                # Cbus connected automatically
                "rs232_m": "rs232_m",
                # "interrupt_o": "uart0_interrupt",
            },
        },
        {
            "core_name": "versat_ai_uart",
            "instance_name": "UART1",
            "instance_description": "UART interface for communication with SUT",
            "is_peripheral": True,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": (
                    "clk_en_reset" if params["use_ila"] else "clk_en_rst_s"
                ),
                # Cbus connected automatically
                "rs232_m": "rs232_invert",
                # "interrupt_o": "uart1_interrupt",
            },
        },
    ]

    if params["use_ethernet"]:
        subblocks += [
            {
                "core_name": "iob_eth",
                "instance_name": "ETH0",
                "instance_description": "Ethernet interface",
                "is_peripheral": True,
                "parameters": {
                    "SIMULATION": "SIMULATION",
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": params["addr_w"],
                    "AXI_DATA_W": params["data_w"],
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_reset" if params["use_ila"] else "clk_en_rst_s"
                    ),
                    "axi_m": (
                        "eth_axi",
                        [
                            "eth_axi_arid[0]",
                            "eth_axi_rid[0]",
                            "eth_axi_awid[0]",
                            "eth_axi_bid[0]",
                        ],
                    ),
                    "inta_o": "ethernet_interrupt",
                    "phy_io": "phy_io",
                },
            },
        ]

    if params["use_extmem"]:
        subblocks += [
            {
                "core_name": "iob_address_translator",
                "instance_name": "address_translator",
                "instance_description": "Translate addresses to access memory zones",
                "parameters": {
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": params["addr_w"] - 2,
                    "DATA_W": params["data_w"],
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
                "connect": {
                    "subordinate_s": (
                        "sut_axi",
                        [
                            "{6'b0, sut_axi_araddr}",
                            "{6'b0, sut_axi_awaddr}",
                        ],
                    ),
                    "manager_m": "translated_sut_axi",
                },
                "memory_zones": [
                    # (Start addr, End addr, Translation offset)
                    (0x00000000, 0x0FFFFFFF, 0x10000000),
                ],
            },
        ]

    if params["use_ila"]:
        subblocks += [
            {
                "core_name": "iob_ila",
                "instance_name": "ILA0",
                "instance_description": "Tester Integrated Logic Analyzer for SUT signals",
                "is_peripheral": True,
                "sampling_clk": "clk_i",  # Name of the internal system signal to use as the sampling clock
                "trigger_list": [
                    "translated_sut_axi_arvalid",
                    "translated_sut_axi_rready",
                    "translated_sut_axi_bready",
                    "translated_sut_axi_bready && translated_sut_axi_bvalid",
                ],  # List of signals to use as triggers
                "probe_list": [  # List of signals to probe
                    ("SUT0.cpu.CPU.execute_PC", 32),
                    ("translated_sut_axi_araddr", 30),
                    ("translated_sut_axi_arvalid", 1),
                    ("translated_sut_axi_arready", 1),
                    ("translated_sut_axi_rvalid", 1),
                    ("translated_sut_axi_rready", 1),
                    ("translated_sut_axi_bvalid", 1),
                    ("translated_sut_axi_bready", 1),
                ],
                "clk_counter": "1",
                "clk_width": "64",
                "parameters": {
                    "BUFFER_W": "ILA0_BUFFER_W",
                    "SIGNAL_W": "ILA0_SIGNAL_W",
                    "TRIGGER_W": "ILA0_TRIGGER_W",
                    "MONITOR": "0",
                    "MONITOR_STATE_W": "3",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # Cbus connected automatically
                    "ila_i": "ILA0_ila",
                    "dma_io": "ILA0_dma",
                },
            },
            {
                "core_name": "iob_watchdog",
                "instance_name": "WATCHDOG0",
                "instance_description": "Tester Integrated Logic Analyzer for SUT signals",
                "is_peripheral": True,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    # Cbus connected automatically
                    "active_o": "watchdog0_active",
                    "interrupt_o": "reset",
                },
            },
        ]

        subblocks += [
            {
                "core_name": "iob_axi2iob",
                "instance_name": "periphs_axi2iob",
                "instance_description": "Convert AXI to AXI lite for CLINT",
                "parameters": {
                    "AXI_ID_WIDTH": "AXI_ID_W",
                    "AXI_LEN_WIDTH": "AXI_LEN_W",
                    "ADDR_WIDTH": params["addr_w"] - 2 - 2,
                    "DATA_WIDTH": "AXI_DATA_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_reset",
                    "axi_s": (
                        "axi_periphs_cbus",
                        [
                            "periphs_axi_arlock[0]",
                            "periphs_axi_awlock[0]",
                        ],
                    ),
                    "iob_m": "iob_periphs_cbus",
                },
            },
            {
                "core_name": "iob_split",
                "name": params["name"] + "_pbus_split",
                "instance_name": "iob_pbus_split",
                "instance_description": "Split between peripherals",
                "connect": {
                    "clk_en_rst_s": "clk_en_reset",
                    "reset_i": "split_reset",
                    "input_s": "iob_periphs_cbus",
                    # Peripherals cbus connections added automatically
                },
                "num_outputs": 0,  # Num outputs configured automatically
                "addr_w": params["addr_w"] - 2 - 2,
            },
        ]

    if params["stream"]:
        subblocks += [
            {
                "core_name": "versat_ai_axistream_in",
                "instance_name": "AXISTREAMIN0",
                "instance_description": "SUT AXI input stream interface",
                "is_peripheral": True,
                "parameters": {
                    "FIFO_ADDR_W": "10",
                    # "TDATA_W": "32",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "interrupt_o": "axistreamin_interrupt",
                    "overflow_o": "overflow",
                    "axistream_io": "axistream_in",
                    "sys_axis_io": "sys_axis_in",
                },
            },
            {
                "core_name": "versat_ai_axistream_out",
                "instance_name": "AXISTREAMOUT0",
                "instance_description": "SUT AXI output stream interface",
                "is_peripheral": True,
                "parameters": {
                    "FIFO_ADDR_W": "9",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "interrupt_o": "axistreamout_interrupt",
                    "trigger_interrupt_o": "underflow",
                    "trigger_i": "pulse",
                    "axistream_io": "axistream_out",
                    "sys_axis_io": "sys_axis_out",
                },
            },
            {
                "core_name": "versat_ai_dma",
                "instance_name": "DMA0",
                "instance_description": "DMA interface",
                "is_peripheral": True,
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": params["addr_w"],
                    "AXI_DATA_W": params["data_w"],
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst",
                    "axi_m": "dma_axi",
                    "dma_input_io": "sys_axis_in",
                    "dma_output_io": "sys_axis_out",
                },
            },
            {
                "core_name": "iob_nco",
                "instance_name": "NCO0",
                "instance_description": "NCO peripheral",
                "is_peripheral": True,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "clk_gen_io": "nc0_clk_gen",
                },
            },
            {
                "core_name": "iob_edge_detect",
                "instance_name": "iob_edge_detect_inst",
                "parameters": {
                    "OUT_TYPE": '"pulse"',
                },
                "connect": {
                    "clk_en_rst_s": "edge_detect_clk_en_rst",
                    "rst_i": "rst",
                    "bit_i": "nco0_clk_out",
                    "detected_o": "mcke",
                },
            },
        ]

    ### Superblocks ###

    superblocks = [
        # Synthesis module (needed for macros)
        {
            "core_name": "iob_system_syn",
            "instance_name": "iob_system_syn",
            "dest_dir": "hardware/syn/src",
            "iob_system_params": params,
        },
        # Simulation wrapper
        {
            "core_name": "iob_soc_tester_sim",
            "instance_name": "iob_system_sim",
            "dest_dir": "hardware/simulation/src",
            "iob_system_params": params,
        },
        # FPGA wrappers added automatically
    ]

    ### Sw_modules ###
    sw_modules = [
        {
            "core_name": "iob_uart",
            "instance_name": "uart_inst",
        },
    ]

    ### Snippets ###
    snippets = ""

    snippets += """
assign reset_addr = 32'h80000000;
"""

    if params["stream"] == 0:
        snippets += """
assign interrupts = 32'b0;
"""

    if params["stream"] == 1:
        snippets += """
assign interrupts = {{30{1'b0}}, decoder_interrupt, 1'b0};

assign axis_in_clk_i = mclk_i;
assign axis_in_cke_i = mcke;
assign axis_in_arst_i = arst_mclk_i;

assign axis_out_clk_i = mclk_i;
assign axis_out_cke_i = mcke;
assign axis_out_arst_i = arst_mclk_i;
"""

    if params["use_ila"]:
        snippets += """
// Auto-generated connections for ILA0
assign ILA0_sampling_clk = clk_i;
function [31:0] ILA0_trunc_32(input [31:0] val);
    ILA0_trunc_32 = (32'h0 | val);
endfunction
function [0:0] ILA0_trunc_1(input [0:0] val);
    ILA0_trunc_1 = (1'h0 | val);
endfunction
function [29:0] ILA0_trunc_30(input [29:0] val);
    ILA0_trunc_30 = (30'h0 | val);
endfunction

assign ILA0_signal = {ILA0_trunc_1(translated_sut_axi_bready),ILA0_trunc_1(translated_sut_axi_bvalid),ILA0_trunc_1(translated_sut_axi_rready),ILA0_trunc_1(translated_sut_axi_rvalid),ILA0_trunc_1(translated_sut_axi_arready),ILA0_trunc_1(translated_sut_axi_arvalid),ILA0_trunc_30(translated_sut_axi_araddr),ILA0_trunc_32(SUT0.cpu.CPU.execute_PC)};
assign ILA0_trigger = {translated_sut_axi_bready && translated_sut_axi_bvalid,translated_sut_axi_bready,translated_sut_axi_rready,translated_sut_axi_arvalid};

assign reset_combo = reset | arst_i;
"""

    # Py2hwsw dictionary describing current core
    core_dict = {
        "version": "0.1",
        "parent": {
            "core_name": "iob_system",
            **params,
            "system_attributes": {
                # Set "is_tester" attribute to generate Makefile and flows allowing to run this core as top module
                "is_tester": True,
                "board_list": ["iob_aes_ku040_db_g", "iob_cyclonev_gt_dk"],
                "confs": confs,
                "ports": ports,
                "wires": wires,
                "subblocks": subblocks,
                "superblocks": superblocks,
                "sw_modules": sw_modules,
                "snippets": [
                    {"verilog_code": snippets},
                ],
            },
        },
    }

    return core_dict
