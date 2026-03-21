# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import shutil
import subprocess
import os


def setup(py_params_dict: dict):
    # Py2hwsw dictionary describing current core
    mem_addr_w = 20
    system_w = mem_addr_w
    name = "versat_ai"
    addr_w = 32
    data_w = 32

    params = {
        # Name of the generated System
        "name": "versat_ai",
        # If should initialize memories from data in .hex files
        "init_mem": True,
        # If should include an internal memory
        "use_intmem": False,
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
        # If should include a tester system
        "include_tester": False,
        # If should include default system snippet
        "include_snippet": False,
        # CPU selection
        "cpu": "iob_vexriscv",
        "auto_uncached": True,
    }

    if True:

        def Copy(folderName):
            src = "."
            dst = f"../versat_ai_V0.8"

            srcPath = os.path.join(src, folderName)
            dstPath = os.path.join(dst, folderName)

            print(os.getcwd(), "Copied:", srcPath, dstPath)

            shutil.copytree(srcPath, dstPath, dirs_exist_ok=True)

        Copy("hardware/src")
        Copy("software")
        Copy("software/src")

    num_xbar_managers = 0
    for param_name in ["use_intmem", "use_extmem", "use_bootrom", "use_peripherals"]:
        if params[param_name]:
            num_xbar_managers += 1
    xbar_sel_w = (num_xbar_managers - 1).bit_length()

    subblocks = []

    xbar = {
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
    }

    if False:
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
            xbar["connect"] |= {f"m{num_managers}_axi_m": interface_connection}
            num_managers += 1
    xbar["num_managers"] = num_managers

    num_subordinates = 0
    # Connect xbar subordinate interfaces
    # (Lower number has higher priority in case of collision)
    xbar["connect"].update(
        {
            f"s{num_subordinates}_axi_s": "cpu_ibus",
        }
    )
    num_subordinates += 1

    xbar["connect"].update(
        {
            f"s{num_subordinates}_axi_s": "cpu_dbus",
        }
    )
    num_subordinates += 1
    xbar["num_subordinates"] = num_subordinates

    uncached_start_addr = (1 << params["fw_addr_w"]) + 1
    region_width = params["addr_w"] - xbar_sel_w
    uncached_size = (2**region_width - 2 ** params["fw_addr_w"] - 1) + 2**region_width

    ### Confs ###
    confs = []

    ### Ports ###
    ports = [
        {
            # Add new rs232 port for uart
            "name": "rs232_m",
            "descr": "iob-system uart interface",
            "signals": {
                "type": "rs232",
            },
        },
    ]
    wires = [
        {
            "name": "versat_axi",
            "descr": "Versat axi wires",
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
    ]
    subblocks += [
        xbar,
        {
            # Instantiate a UART core from: https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/hardware/iob_uart
            "core_name": "iob_uart",
            "instance_name": "UART0",
            "instance_description": "UART peripheral",
            "is_peripheral": True,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus connected automatically
                "rs232_m": "rs232_m",
            },
        },
        {
            # Instantiate a TIMER core from: https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/lib/hardware/iob_timer
            "core_name": "iob_timer",
            "instance_name": "TIMER0",
            "instance_description": "Timer peripheral",
            "is_peripheral": True,
            "parameters": {},
            "connect": {
                "clk_en_rst_s": "clk_en_rst_s",
                # Cbus connected automatically
            },
        },
        {
            "core_name": "iob_versat",
            "instance_name": "VERSAT0",
            "instance_description": "Versat accelerator",
            "is_peripheral": True,
            "parameters": {},
            "connect": {"axi_out_m": "versat_axi"},
        },
    ]
    superblocks = [
        # Tester
        {
            "core_name": "iob_soc_tester",
            "instance_name": "iob_soc_tester",
            "init_mem": params["init_mem"],
            "use_extmem": params["use_extmem"],
            "use_ethernet": params["use_ethernet"],
            "dest_dir": "tester",
        },
        # Dummy Simulation wrapper
        {
            "core_name": "versat_ai_sim",
            "instance_name": "iob_system_sim",
            "dest_dir": "hardware/simulation/src",
        },
    ]

    # Py2hwsw dictionary describing current core
    core_dict = {
        "version": "0.8",
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
            },
        },
    }

    return core_dict
