import shutil
import subprocess
import os


def setup(py_params_dict):
    params = {
        # Name of the generated System
        "name": "iob_soc_tester",
        # If should initialize memories from data in .hex files
        "init_mem": True,
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
        # CPU address width
        "addr_w": 32,
        # CPU data width
        "data_w": 32,
        # Memory address width
        "mem_addr_w": 20,
        # Bootrom address width
        "bootrom_addr_w": 12,
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
    }

    if False:
        # Don't copy files for other targets (like clean)
        if py_params_dict.get("py2hwsw_target", "") == "setup":
            dst = f"{py_params_dict['build_dir']}/tester/software/src/"
            os.makedirs(dst, exist_ok=True)
            src = f"../../../software/src/"
            for src_file in [
                # "iob_regfileif_csrs_conf.h",
                # "iob_regfileif_csrs.h",
                # "iob_regfileif_csrs.c",
                # "iob_regfileif_conf.h",
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

    addr_w = 32
    data_w = 32

    ports = []

    if True:
        ports += [
            {
                "name": "versat_rom_m",
                "signals": {
                    "type": "rom_sp",
                    "prefix": "versat_rom_",
                    "ADDR_W": params["bootrom_addr_w"] - 2,
                    "DATA_W": params["data_w"],
                },
            },
        ]

    if False:
        ports += [
            # {
            #     "name": "versat_rom_m",
            #     "signals" : {
            #         "type": "rom_sp",
            #         "prefix": "versat_rom_",
            #         "ADDR_W": params["bootrom_addr_w"] - 2,
            #         "DATA_W": params["data_w"],
            #     }
            # },
            {
                "name": "external_mem_bus_m",
                "descr": "Port for connection to external 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": params["mem_addr_w"] - 2,
                    "DATA_W": params["data_w"],
                },
            },
        ]

    wires = []
    if True:
        wires += [
            {
                "name": "sut_rs232",
                "descr": "rs232 bus for SUT",
                "signals": {
                    "type": "rs232",
                    "prefix": "sut_",
                },
            },
            {
                "name": "sut_rs232_inverted",
                "descr": "Invert order of rs232 signals",
                "signals": [
                    {"name": "sut_rs232_txd"},
                    {"name": "sut_rs232_rxd"},
                    {"name": "sut_rs232_cts"},
                    {"name": "sut_rs232_rts"},
                ],
            },
            {
                "name": "versat_ai",
                "descr": "Versat ai wires",
                "signals": {
                    "type": "axi",
                    "prefix": "versat_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": addr_w,
                    "DATA_W": data_w,
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
            },
            {
                "name": "translated_versat_ai",
                "descr": "Translated Versat ai wires (SUT sees upper part of memory only)",
                "signals": {
                    "type": "axi",
                    "prefix": "translated_versat_",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": addr_w,
                    "DATA_W": data_w,
                    "LEN_W": "AXI_LEN_W",
                    "LOCK_W": "1",
                },
            },
        ]

    subblocks = []
    subblocks += [
        {
            # Instantiate SUT (usually iob_system or a child of it)
            "core_name": "versat_ai",
            "instance_name": "SUT",
            "instance_description": "System Under Test (SUT) to be verified by this tester.",
            # "is_peripheral": True,  # Only applies if SUT has CSRs (via regfileif).
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus (if any) is connected automatically
                "rs232_m": "sut_rs232",
                "axi_m": "versat_ai",
                "rom_bus_m": "versat_rom_m",
                # "versat_mem_bus_m": "versat_mem_bus_m"
            },
        },
        {
            # Instantiate a UART core to communicate with SUT
            "core_name": "iob_uart",
            "instance_name": "UART1",
            "instance_description": "UART peripheral for communication with SUT.",
            "is_peripheral": True,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus connected automatically
                "rs232_m": "sut_rs232_inverted",
            },
        },
    ]

    if True:
        subblocks += [
            {
                "core_name": "iob_axi_full_xbar",
                "name": "iob_soc_tester_axi_full_xbar",
                "instance_name": "iob_axi_full_xbar",
                "instance_description": "AXI full xbar instance",
                "parameters": {
                    "ID_W": "AXI_ID_W",
                    "LEN_W": "AXI_LEN_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "rst",
                    "s0_axi_s": "cpu_ibus",
                    "s1_axi_s": "cpu_dbus",
                    "s2_axi_s": "translated_versat_ai",
                    "m0_axi_m": (
                        "int_mem_axi",
                        [
                            "{unused_m0_araddr_bits, int_mem_axi_araddr}",
                            "{unused_m0_awaddr_bits, int_mem_axi_awaddr}",
                        ],
                    ),
                    "m1_axi_m": (
                        "axi_m",
                        [
                            "{unused_m1_araddr_bits, axi_araddr_o}",
                            "{unused_m1_awaddr_bits, axi_awaddr_o}",
                        ],
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
                "addr_w": 30,
                "data_w": 32,
                "lock_w": 1,
                "num_managers": 4,
                "num_subordinates": 3,
            },
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
                        "versat_ai",
                        [
                            "{6'b0, sut_axi_araddr}",
                            "{6'b0, sut_axi_awaddr}",
                        ],
                    ),
                    "manager_m": "translated_versat_ai",
                },
                "memory_zones": [
                    # (Start addr, End addr, Translation offset)
                    (0x00000000, 0x0FFFFFFF, 0x10000000),
                ],
            },
        ]

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
        ports += [
            {
                "name": "external_mem_bus_m",
                "descr": "Port for connection to external 'iob_ram_t2p_be' memory",
                "signals": {
                    "type": "ram_t2p_be",
                    "prefix": "ext_mem_",
                    "ADDR_W": params["mem_addr_w"] - 2,
                    "DATA_W": params["data_w"],
                },
            },
        ]

    # Py2hwsw dictionary describing current core
    core_dict = {
        "version": "0.8",
        "parent": {
            "core_name": "iob_system",
            **params,
            "system_attributes": {
                # Set "is_tester" attribute to generate Makefile and flows allowing to run this core as top module
                "is_tester": True,
                "board_list": ["iob_aes_ku040_db_g", "iob_cyclonev_gt_dk"],
                "wires": wires,
                "subblocks": subblocks,
                "ports": ports,
            },
        },
    }

    return core_dict
