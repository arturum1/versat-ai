# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    CSR_IF = py_params_dict["csr_if"] if "csr_if" in py_params_dict else "iob"
    NAME = py_params_dict["name"] if "name" in py_params_dict else "versat_ai_uart"
    attributes_dict = {
        "name": NAME,
        "generate_hw": True,
        "board_list": ["iob_cyclonev_gt_dk", "iob_aes_ku040_db_g"],
        "description": "The IObundle UART is a RISC-V-based Peripheral written in Verilog, which users can download for free, modify, simulate and implement in FPGA or ASIC. It is written in Verilog and includes a C software driver. The IObundle UART is a very compact IP that works at high clock rates if needed. It supports full-duplex operation and a configurable baud rate. The IObundle UART has a fixed configuration for the Start and Stop bits. More flexible licensable commercial versions are available upon request.",
        "confs": [
            {
                "name": "DATA_W",
                "type": "P",
                "val": "32",
                "min": "NA",
                "max": "NA",
                "descr": "Data bus width.",
            },
            {
                "name": "RST_POL",
                "type": "M",
                "val": "1",
                "min": "0",
                "max": "1",
                "descr": "Reset polarity.",
            },
            {
                "name": "FIFO_ADDR_W",
                "type": "P",
                "val": "8",
                "min": "NA",
                "max": "16",
                "descr": "FIFO depth (log2)",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst_s",
                "signals": {
                    "type": "iob_clk",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "rs232_m",
                "signals": {
                    "type": "rs232",
                },
                "descr": "RS232 interface",
            },
        ],
        "wires": [
            {
                "name": "softreset",
                "descr": "",
                "signals": [
                    {"name": "softreset_wr", "width": 1},
                ],
            },
            {
                "name": "div",
                "descr": "",
                "signals": [
                    {"name": "div_wr", "width": 16},
                ],
            },
            {
                "name": "txdata",
                "descr": "",
                "signals": [
                    {"name": "txdata_wdata_wr", "width": 8},
                    {"name": "txdata_wen_wr", "width": 1},
                    {"name": "txdata_ready_wr", "width": 1},
                ],
            },
            {
                "name": "txen",
                "descr": "",
                "signals": [
                    {"name": "txen_wr", "width": 1},
                ],
            },
            {
                "name": "rxen",
                "descr": "",
                "signals": [
                    {"name": "rxen_wr", "width": 1},
                ],
            },
            {
                "name": "txready",
                "descr": "",
                "signals": [
                    {"name": "txready_rd", "width": 1},
                ],
            },
            {
                "name": "rxready",
                "descr": "",
                "signals": [
                    {"name": "rxready_rd", "width": 1},
                ],
            },
            {
                "name": "rxdata",
                "descr": "",
                "signals": [
                    {"name": "rxdata_rdata_rd", "width": 8},
                    {"name": "rxdata_rvalid_rd", "width": 1},
                    {"name": "rxdata_rready_rd", "width": 1},
                    {"name": "rxdata_ren_rd", "width": 1},
                    {"name": "rxdata_ready_rd", "width": 1},
                ],
            },
            # uart core
            {
                "name": "clk_rst",
                "descr": "Clock and reset",
                "signals": [
                    {"name": "clk_i"},
                    {"name": "arst_i"},
                ],
            },
            {
                "name": "versat_ai_uart_core_reg_interface",
                "descr": "",
                "signals": [
                    {"name": "softreset_wr"},
                    {"name": "txen_wr"},
                    {"name": "rxen_wr"},
                    {"name": "read_fifo_w_en", "width": 1},
                    {"name": "txready_rd"},
                    {"name": "read_fifo_w_full", "width": 1},
                    {"name": "txdata_wdata_wr"},
                    {
                        "name": "read_fifo_w_data",
                        "width": 8,
                    },
                    {"name": "txdata_wen_wr"},
                    {"name": "div_wr"},
                ],
            },
            {
                "name": "read_fifo_write",
                "descr": "Write interface",
                "signals": [
                    {
                        "name": "read_fifo_w_en",
                    },
                    {
                        "name": "read_fifo_w_data",
                    },
                    {
                        "name": "read_fifo_w_full",
                    },
                ],
            },
            {
                "name": "read_fifo_read",
                "descr": "Read interface",
                "signals": [
                    {
                        "name": "read_fifo_r_en",
                        "width": 1,
                        "descr": "Read enable",
                    },
                    {
                        "name": "read_fifo_r_data",
                        "width": 8,
                        "descr": "Read data",
                    },
                    {
                        "name": "read_fifo_r_empty",
                        "width": 1,
                        "descr": "Read empty signal",
                    },
                ],
            },
            {
                "name": "read_ext_mem",
                "descr": "External memory interface",
                "signals": {
                    "type": "ram_t2p",
                    "prefix": "ext_mem_read_",
                    "ADDR_W": "FIFO_ADDR_W",
                    "DATA_W": 8,
                },
            },
            {
                "name": "read_fifo_level",
                "descr": "",
                "signals": [
                    {"name": "read_fifo_level", "width": "FIFO_ADDR_W+1"},
                ],
            },
            {
                "name": "fifo2rxdata",
                "descr": "",
                "signals": [
                    {"name": "fifo2rxdata_tvalid", "width": 1},
                    {"name": "rxdata_ren_rd"},
                    {"name": "rxdata_rdata_rd"},
                ],
            },
        ],
        "subblocks": [
            # iob_csrs 'control_if_s' port is connected automatically by py2hwsw
            f"""iob_csrs iob_csrs
                -d 'Control/Status Registers' 
                --no_autoaddr 
                --rw_overlap 
                -c 
                    "clk_en_rst_s":"clk_en_rst_s"
                    "softreset_o":"softreset"
                    "div_o":"div"
                    "txdata_io":"txdata"
                    "txen_o":"txen"
                    "txready_i":"txready"
                    "rxen_o":"rxen"
                    "rxready_i":"rxready"
                    "rxdata_io":"rxdata"
                --csr_if {CSR_IF}
                --csr-group uart 
                    -d 'UART software accessible registers' 
                        -r softreset:1 -t W -d 'Soft reset'  --rst_val 0 --addr 0 --log2n_items 0
                        -r div:16 -t W -d 'Bit duration in system clock cycles.' --rst_val 0 --addr 2 --log2n_items 0
                        -r txdata:8 -t W -d 'TX data.' --rst_val 0 --addr 4 --log2n_items 0 --no_autoreg
                        -r txen:1 -t W -d 'TX enable.' --rst_val 0 --addr 5 --log2n_items 0
                        -r rxen:1 -t W -d 'RX enable.' --rst_val 0 --addr 6 --log2n_items 0
                        -r txready:1 -t R -d 'TX ready to receive data.' --rst_val 0 --addr 0 --log2n_items 0
                        -r rxready:1 -t R -d 'RX ready to be read.' --rst_val 0 --addr 1 --log2n_items 0
                        -r rxdata:8 -t R -d 'RX data.' --rst_val 0 --addr 4 --log2n_items 0 --no_autoreg
            """,
            {
                "core_name": "versat_ai_uart_core",
                "instance_name": "versat_ai_uart_core_inst",
                "instance_description": "UART core driver",
                "connect": {
                    "clk_rst_s": "clk_rst",
                    "reg_interface_io": "versat_ai_uart_core_reg_interface",
                    "rs232_m": "rs232_m",
                },
            },
            {
                "core_name": "iob_fifo2axis",
                "instance_name": "fifo2axis_inst",
                "instance_description": "Sync read fifo",
                "parameters": {
                    "DATA_W": 8,
                },
                "connect": {
                    "clk_en_rst_s": (
                        "clk_en_rst_s",
                        [
                            "rst_i:softreset_wr",
                        ],
                    ),
                    "fifo_r_io": "read_fifo_read",
                    "axis_m": "fifo2rxdata",
                },
            },
            {
                "core_name": "iob_fifo_sync",
                "instance_name": "read_fifo",
                "instance_description": "Sync read fifo",
                "parameters": {
                    "W_DATA_W": 8,
                    "R_DATA_W": 8,
                    "ADDR_W": "FIFO_ADDR_W",
                },
                "connect": {
                    "clk_en_rst_s": "clk_en_rst_s",
                    "rst_i": "softreset",
                    "write_io": "read_fifo_write",
                    "read_io": "read_fifo_read",
                    "extmem_io": "read_ext_mem",
                    "fifo_o": "read_fifo_level",
                },
            },
            {
                "core_name": "iob_ram_t2p",
                "instance_name": "read_fifo_memory",
                "instance_description": "Read FIFO RAM",
                "parameters": {
                    "ADDR_W": "FIFO_ADDR_W",
                    "DATA_W": 8,
                },
                "connect": {
                    "ram_t2p_s": "read_ext_mem",
                },
            },
            # uncomment the following block to reveal a bug in py2hwsw
            #            {
            #                "core_name": "iob_sync",
            #                "instance_name": "iob_sync_inst",
            #                "instantiate": False,
            #            },
        ],
        "superblocks": [
            # Tester
            {
                "core_name": "iob_uart_tester",
                "dest_dir": "tester",
            },
            # Simulation wrapper
            {
                "core_name": "iob_uart_sim",
                "dest_dir": "hardware/simulation/src",
                "csr_if": CSR_IF,
            },
        ],
        "snippets": [
            {
                "verilog_code": """
    assign rxready_rd = fifo2rxdata_tvalid;

    // txdata Manual logic
    assign txdata_ready_wr = 1'b1;

    // rxdata Manual logic
    assign rxdata_ready_rd = 1'b1;

    assign rxdata_rvalid_rd = fifo2rxdata_tvalid;

""",
            },
        ],
    }

    return attributes_dict
