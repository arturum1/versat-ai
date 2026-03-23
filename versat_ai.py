# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT

import sys


def setup(py_params_dict):

    params = {
        # Name of the generated System
        "name": "versat_ai",
        # If should initialize memories from data in .hex files
        "init_mem": int(py_params_dict.get("init_mem", True)),
        # If should include an internal memory
        "use_intmem": False,
        # If should use external memory (usually DDR)
        "use_extmem": True,
        # If should include a bootrom
        "use_bootrom": False,
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
        "fw_addr_w": 22,
        # If should include a tester system
        "include_tester": False,
        # If should include default system snippet
        "include_snippet": False,
        # CPU selection
        "cpu": "iob_vexriscv",
        "auto_uncached": True,
        # If should use stream configuration
        "stream": int(py_params_dict.get("stream_config", False)),
    }

    num_xbar_managers = 0
    for param_name in ["use_intmem", "use_extmem", "use_bootrom", "use_peripherals"]:
        if params[param_name]:
            num_xbar_managers += 1
    xbar_sel_w = (num_xbar_managers - 1).bit_length()

    ### Confs ###
    confs = [
        {
            "name": "STDIO",
            "descr": "Enable printf functions at a cost of a larger firmware size due to STDIO inclusion.",
            "type": "M",
            "val": "1",
            "min": "0",
            "max": "1",
        },
        {
            "name": "AACPLUS",
            "descr": "Enable support for the HE-AAC v2, AAC-LD, AAC-ELD v2, xHE-AAC profiles at the cost of a larger firmware size.",
            "type": "M",
            "val": "1",
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

    ### Ports ###
    ports = [
        {
            "name": "iob_csrs_cbus_s",
            "signals": {
                "type": "iob",
                "ADDR_W": ("6 - 2" if params["stream"] else "5 - 2"),
                "DATA_W": params["data_w"],
            },
            "descr": "CPU native interface",
        },
    ]

    if params["stream"]:
        ports += [
            {
                "name": "axistream_in_io",
                "descr": "AXI Stream in interface signals",
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
                "name": "axistream_out_io",
                "descr": "AXI Stream out interface signals",
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
                "name": "interrupt_o",
                "descr": "",
                "signals": [
                    {"name": "interrupt_o", "width": 1},
                ],
            },
        ]

    ### Wires ###
    wires = [
        {
            "name": "reset",
            "descr": "",
            "signals": [
                {"name": "reset", "width": 1},
            ],
        },
        {
            "name": "firm_addr",
            "descr": "",
            "signals": [
                {"name": "firm_addr", "width": 32},
            ],
        },
    ]

    if params["stream"]:
        wires += [
            {
                "name": "axis_clk_en_rst",
                "descr": "",
                "signals": [
                    {"name": "axis_in_clk_i"},
                    {"name": "axis_in_arst_i"},
                    {"name": "axis_in_cke_i"},
                ],
            },
            {
                "name": "axis_in_tvalid_i",
                "descr": "",
                "signals": [
                    {"name": "axis_in_tvalid_i"},
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
                "name": "decode_error_cause",
                "descr": "",
                "signals": [
                    {"name": "decode_error_cause", "width": 16},
                ],
            },
            {
                "name": "decode_error_interrupt",
                "descr": "",
                "signals": [
                    {"name": "decode_error_interrupt", "width": 1},
                ],
            },
            {
                "name": "axistreamin_interrupt",
                "descr": "",
                "signals": [
                    {"name": "axistreamin_interrupt", "width": 1},
                ],
            },
            {
                "name": "overflow_cause",
                "descr": "",
                "signals": [
                    {"name": "overflow_cause", "width": 1},
                ],
            },
            {
                "name": "overflow_interrupt",
                "descr": "",
                "signals": [
                    {"name": "overflow_interrupt", "width": 1},
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
                "name": "real_time_cause",
                "descr": "",
                "signals": [
                    {"name": "real_time_cause", "width": 1},
                ],
            },
            {
                "name": "real_time_interrupt",
                "descr": "",
                "signals": [
                    {"name": "real_time_interrupt", "width": 1},
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
                "name": "w_busy",
                "descr": "",
                "signals": [
                    {"name": "w_busy", "width": 1},
                ],
            },
            {
                "name": "r_busy",
                "descr": "",
                "signals": [
                    {"name": "r_busy", "width": 1},
                ],
            },
            {
                "name": "interrupt_mask",
                "descr": "",
                "signals": [
                    {"name": "interrupt_mask", "width": 3},
                ],
            },
            {
                "name": "interrupt_clear",
                "descr": "",
                "signals": [
                    {"name": "interrupt_clear", "width": 3},
                ],
            },
            {
                "name": "interrupt_status",
                "descr": "",
                "signals": [
                    {"name": "interrupt_status", "width": 18},
                ],
            },
        ]

    ### Subblocks ###
    subblocks = []

    # Memory to memory regs
    if params["stream"] == 0:
        regs = [
            {
                "name": "start",
                "type": "W",
                "n_bits": 1,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Start decoding (1) or not (0).",
            },
            {
                "name": "done",
                "type": "R",
                "n_bits": 1,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Decoder finished decoding input data (1) or not (0).",
            },
            {
                "name": "en_size",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Encoded data file size.",
            },
            {
                "name": "de_size",
                "type": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Decoded data file size.",
            },
            {
                "name": "en_buf_addr",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Memory address of encoded data buffer.",
            },
            {
                "name": "de_buf_addr",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Memory address of decoded data buffer.",
            },
            {
                "name": "de_buf_size",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Size of decoded data buffer.",
            },
            {
                "name": "rst",
                "type": "W",
                "n_bits": 1,
                "rst_val": 1,
                "log2n_items": 0,
                "autoreg": True,
                "output": True,
                "descr": "Resets the decoder (1) or not (0).",
            },
            {
                "name": "firm_addr",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "output": True,
                "descr": "Memory address of decoder firmware.",
            },
        ]

    # Stream regs
    if params["stream"] == 1:
        regs = [
            {
                "name": "ready",
                "type": "R",
                "n_bits": 1,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Decoder initialized and ready to receive data (1) or not (0).",
            },
            {
                "name": "num_ch",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Number of channels",
            },
            {
                "name": "int_buf_addr",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Memory address of internal data buffers.",
            },
            {
                "name": "int_buf_size",
                "type": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Size of internal data buffers.",
            },
            {
                "name": "out_freq_div",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Sample period in mcke cycles.",
            },
            {
                "name": "interrupt_mask",
                "type": "W",
                "n_bits": 3,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "output": True,
                "descr": "Interrupt mask (disables the respective interrupt bit when high).",
            },
            {
                "name": "interrupt_clear",
                "type": "W",
                "n_bits": 3,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "output": True,
                "descr": "Interrupt clear (clears the respective interrupt bit when high).",
            },
            {
                "name": "interrupt_status",
                "type": "R",
                "n_bits": 18,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": False,
                "descr": "Interrupt status register.",
            },
            {
                "name": "decode_time",
                "type": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Decode time.",
            },
            {
                "name": "worst_frame",
                "type": "R",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "descr": "Worst frame decoding time.",
            },
            {
                "name": "rst",
                "type": "W",
                "n_bits": 1,
                "rst_val": 1,
                "log2n_items": 0,
                "autoreg": True,
                "output": True,
                "descr": "Resets the decoder (1) or not (0).",
            },
            {
                "name": "firm_addr",
                "type": "W",
                "n_bits": 32,
                "rst_val": 0,
                "log2n_items": 0,
                "autoreg": True,
                "output": True,
                "descr": "Memory address of decoder firmware.",
            },
        ]

    subblocks += [
        {
            "core_name": "iob_regfileif",
            "instance_name": "REGFILEIF0",
            "instance_description": "The Register file interface contains registers used to configure, control and monitor the AAC decoder.",
            "is_peripheral": True,
            "internal_csr_if_widths": {
                "ADDR_W": ("6 - 2" if params["stream"] else "5 - 2"),
                "DATA_W": 32,
            },
            "external_csr_if_widths": {
                "ADDR_W": ("6 - 2" if params["stream"] else "5 - 2"),
                "DATA_W": 32,
            },
            "csrs": [
                {
                    "name": "regfileif",
                    "descr": "REGFILEIF software accessible registers.",
                    "regs": regs,
                },
            ],
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus connected automatically
                "iob_csrs_external_cbus_s": "iob_csrs_cbus_s",
                "rst_o": "reset",
                "firm_addr_o": "firm_addr",
            },
        },
    ]

    if params["stream"]:
        subblocks[-1]["ports"] = [
            {
                "name": "interrupt_status_i",
                "descr": "",
                "signals": [
                    {"name": "interrupt_status_i", "width": 18},
                ],
            },
        ]

        subblocks[-1]["connect"].update(
            {
                "interrupt_mask_o": "interrupt_mask",
                "interrupt_clear_o": "interrupt_clear",
                "interrupt_status_i": "interrupt_status",
            },
        )

        subblocks[-1][
            "verilog-snippets"
        ] = """
        assign external_interrupt_status_rdata_i = interrupt_status_i;
        assign external_interrupt_status_rvalid_i = 1'b1;
        assign external_interrupt_status_ready_i = 1'b1;

        // CPU may not write to this register
        assign internal_interrupt_status_wready_i = 1'b0;
"""

    num_subordinates = 0
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
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "rst",
            },
            "addr_w": params["addr_w"] - 2,
            "data_w": params["data_w"],
            "lock_w": 1,
        },
    ]
    full_xbar_manager_interfaces = {
        "use_intmem": (
            "int_mem_axi",
            [
                "{unused_m0_araddr_bits, int_mem_axi_araddr}",
                "{unused_m0_awaddr_bits, int_mem_axi_awaddr}",
            ],
        ),
        "use_extmem": (
            "axi_m",
            [
                "{unused_m1_araddr_bits, axi_araddr_o}",
                "{unused_m1_awaddr_bits, axi_awaddr_o}",
            ],
        ),
        "use_bootrom": (
            "bootrom_cbus",
            [
                "{unused_m2_araddr_bits, bootrom_axi_araddr}",
                "{unused_m2_awaddr_bits, bootrom_axi_awaddr}",
            ],
        ),
        "use_peripherals": (
            "axi_periphs_cbus",
            [
                "{unused_m3_araddr_bits, periphs_axi_araddr}",
                "{unused_m3_awaddr_bits, periphs_axi_awaddr}",
                "periphs_axi_awlock[0]",
                "periphs_axi_arlock[0]",
            ],
        ),
    }
    # Connect xbar manager interfaces
    num_managers = 0
    for param_name, interface_connection in full_xbar_manager_interfaces.items():
        if params[param_name]:
            subblocks[-1]["connect"] |= {f"m{num_managers}_axi_m": interface_connection}
            num_managers += 1
    subblocks[-1]["num_managers"] = num_managers

    # Connect xbar subordinate interfaces
    # (Lower number has higher priority in case of collision)
    subblocks[-1]["connect"].update(
        {
            f"s{num_subordinates}_axi_s": "cpu_ibus",
        }
    )
    num_subordinates += 1

    subblocks[-1]["connect"].update(
        {
            f"s{num_subordinates}_axi_s": "cpu_dbus",
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

    uncached_start_addr = (1 << params["fw_addr_w"]) + 1
    region_width = params["addr_w"] - xbar_sel_w
    uncached_size = (2**region_width - 2 ** params["fw_addr_w"] - 1) + 2**region_width

    subblocks += [
        {  # Change vexriscv to custom configuration
            "core_name": "versat_ai_vexriscv",
            "name": params["name"] + "_" + params["cpu"],
            "instance_name": "cpu",
            "instance_description": "RISC-V CPU instance",
            "uncached_start_addr": uncached_start_addr,
            "uncached_size": uncached_size,
            "parameters": {
                "AXI_ID_W": "1",
                "AXI_ADDR_W": params["addr_w"],
                "AXI_DATA_W": params["data_w"],
                "AXI_LEN_W": "AXI_LEN_W",
            },
            "connect": {
                "resetVector_i": "firm_addr",
                "clk_en_rst_s": "clk_en_rst_s",
                "rst_i": "reset",
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
    ]

    if params["stream"]:
        subblocks += [
            {
                "core_name": "versat_ai_axistream_in",
                "instance_name": "AXISTREAMIN0",
                "instance_description": "SUT AXI input stream interface",
                "is_peripheral": True,
                "parameters": {
                    "FIFO_ADDR_W": "4",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "interrupt_o": "axistreamin_interrupt",
                    "overflow_o": "overflow_interrupt",
                    "axistream_io": "axistream_in_io",
                    "sys_axis_io": "sys_axis_in",
                },
            },
            {
                "core_name": "versat_ai_axistream_out",
                "instance_name": "AXISTREAMOUT0",
                "instance_description": "SUT AXI output stream interface",
                "is_peripheral": True,
                "parameters": {
                    "FIFO_ADDR_W": "4",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "interrupt_o": "axistreamout_interrupt",
                    "trigger_interrupt_o": "real_time_interrupt",
                    "trigger_i": "pulse",
                    "axistream_io": "axistream_out_io",
                    "sys_axis_io": "sys_axis_out",
                },
            },
            {
                "core_name": "iob_latency_controller",
                "instance_name": "LATENCYCONTROLLER0",
                "instance_description": "Latency controller instance",
                "is_peripheral": True,
                "parameters": {
                    "DATA_W": params["data_w"],
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "pulse_clk_i": "axis_clk_en_rst",
                    "start_i": "axis_in_tvalid_i",
                    "pulse_o": "pulse",
                },
            },
            {
                "core_name": "versat_ai_dma",
                "instance_name": "DMA0",
                "instance_description": "DMA interface",
                "is_peripheral": True,
                "busy": True,
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
                    "w_busy_o": "w_busy",
                    "r_busy_o": "r_busy",
                },
            },
            {
                "core_name": "versat_ai_err_reg",
                "instance_name": "ERRORREG0",
                "instance_description": "Error register instance",
                "is_peripheral": True,
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "decode_error_o": "decode_error_cause",
                    "interrupt_o": "decode_error_interrupt",
                },
            },
            {
                "core_name": "iob_interrupt_manager",
                "instance_name": "INTERRUPTCONTROLLER0",
                "instance_description": "Interrupt controller instance",
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst",
                    "interrupt_cause_0_i": "decode_error_cause",
                    "interrupt0_i": "decode_error_interrupt",
                    "interrupt_cause_1_i": "overflow_cause",
                    "interrupt1_i": "overflow_interrupt",
                    "interrupt_cause_2_i": "real_time_cause",
                    "interrupt2_i": "real_time_interrupt",
                    "interrupt_mask_i": "interrupt_mask",
                    "interrupt_clear_i": "interrupt_clear",
                    "interrupt_status_o": "interrupt_status",
                    "interrupt_o": "interrupt_o",
                },
            },
        ]

    ### Superblocks ###

    superblocks = [
        # Tester
        {
            "core_name": "iob_soc_tester",
            "instance_name": "iob_soc_tester",
            "init_mem": params["init_mem"],
            "use_extmem": params["use_extmem"],
            "use_ethernet": params["use_ethernet"],
            "use_ila": params["use_ila"],
            "stream_config": params["stream"],
            "dest_dir": "tester",
        },
        # Dummy Simulation wrapper
        {
            "core_name": "versat_ai_sim",
            "instance_name": "iob_system_sim",
            "dest_dir": "hardware/simulation/src",
        },
        {
            "core_name": "versat_ai_sim",
            "instance_name": "iob_system_iob_aes_ku040_db_g",
            "instance_description": "FPGA wrapper for iob_aes_ku040_db_g",
            "dest_dir": "hardware/fpga/vivado/iob_aes_ku040_db_g",
        },
        {
            "core_name": "versat_ai_sim",
            "instance_name": "iob_system_iob_cyclonev_gt_dk",
            "instance_description": "FPGA wrapper for iob_cyclonev_gt_dk",
            "dest_dir": "hardware/fpga/quartus/iob_cyclonev_gt_dk",
        },
    ]

    ### Snippets ###
    snippets = ""

    if params["stream"]:
        snippets += """
        // Both of these interrupts sources have one possible cause.
        assign overflow_cause = 1'b1;
        assign real_time_cause = 1'b1;

        assign interrupts = {{29{1'b0}}, (~r_busy), axistreamin_interrupt && (~w_busy), 1'b0};
        """

    # Py2hwsw dictionary describing current core
    core_dict = {
        "version": "0.1",
        "parent": {
            "core_name": "iob_system",
            **params,
            "system_attributes": {
                "board_list": ["iob_aes_ku040_db_g", "iob_cyclonev_gt_dk"],
                "confs": confs,
                "ports": ports,
                "wires": wires,
                "subblocks": subblocks,
                "superblocks": superblocks,
                "snippets": [
                    {"verilog_code": snippets},
                ],
            },
        },
    }

    return core_dict
