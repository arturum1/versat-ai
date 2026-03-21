`timescale 1ns / 1ps
`include "iob_soc_tester_mwrap_conf.vh"

module iob_soc_tester_mwrap #(
   parameter AXI_ID_W = `IOB_SOC_TESTER_MWRAP_AXI_ID_W,  // Don't change this parameter value!
   parameter AXI_ADDR_W = `IOB_SOC_TESTER_MWRAP_AXI_ADDR_W,  // Don't change this parameter value!
   parameter AXI_DATA_W = `IOB_SOC_TESTER_MWRAP_AXI_DATA_W,  // Don't change this parameter value!
   parameter AXI_LEN_W = `IOB_SOC_TESTER_MWRAP_AXI_LEN_W,  // Don't change this parameter value!
   parameter BOOTROM_MEM_HEXFILE = `IOB_SOC_TESTER_MWRAP_BOOTROM_MEM_HEXFILE,  // Don't change this parameter value!
   parameter EXT_MEM_HEXFILE = `IOB_SOC_TESTER_MWRAP_EXT_MEM_HEXFILE,  // Don't change this parameter value!
   parameter MEM_NO_READ_ON_WRITE = `IOB_SOC_TESTER_MWRAP_MEM_NO_READ_ON_WRITE
) (
   // clk_en_rst_s: Clock, clock enable and reset
   input                     clk_i,
   input                     cke_i,
   input                     arst_i,
   // axi_m: AXI manager interface for DDR memory
   output [AXI_ADDR_W-2-1:0] axi_araddr_o,
   output                    axi_arvalid_o,
   input                     axi_arready_i,
   input  [  AXI_DATA_W-1:0] axi_rdata_i,
   input  [           2-1:0] axi_rresp_i,
   input                     axi_rvalid_i,
   output                    axi_rready_o,
   output [    AXI_ID_W-1:0] axi_arid_o,
   output [   AXI_LEN_W-1:0] axi_arlen_o,
   output [           3-1:0] axi_arsize_o,
   output [           2-1:0] axi_arburst_o,
   output                    axi_arlock_o,
   output [           4-1:0] axi_arcache_o,
   output [           4-1:0] axi_arqos_o,
   input  [    AXI_ID_W-1:0] axi_rid_i,
   input                     axi_rlast_i,
   output [AXI_ADDR_W-2-1:0] axi_awaddr_o,
   output                    axi_awvalid_o,
   input                     axi_awready_i,
   output [  AXI_DATA_W-1:0] axi_wdata_o,
   output [AXI_DATA_W/8-1:0] axi_wstrb_o,
   output                    axi_wvalid_o,
   input                     axi_wready_i,
   input  [           2-1:0] axi_bresp_i,
   input                     axi_bvalid_i,
   output                    axi_bready_o,
   output [    AXI_ID_W-1:0] axi_awid_o,
   output [   AXI_LEN_W-1:0] axi_awlen_o,
   output [           3-1:0] axi_awsize_o,
   output [           2-1:0] axi_awburst_o,
   output                    axi_awlock_o,
   output [           4-1:0] axi_awcache_o,
   output [           4-1:0] axi_awqos_o,
   output                    axi_wlast_o,
   input  [    AXI_ID_W-1:0] axi_bid_i,
   // rs232_m: iob-system uart interface
   input                     rs232_rxd_i,
   output                    rs232_txd_o,
   output                    rs232_rts_o,
   input                     rs232_cts_i
);

   // Ports for connection with boot ROM memory
   wire          bootrom_mem_clk;
   wire [10-1:0] bootrom_mem_addr;
   wire          bootrom_mem_en;
   wire [32-1:0] bootrom_mem_r_data;
   // Port for connection to external 'iob_ram_t2p_be' memory
   wire          ext_mem_clk;
   wire [32-1:0] ext_mem_r_data;
   wire          ext_mem_r_en;
   wire [18-1:0] ext_mem_r_addr;
   wire [32-1:0] ext_mem_w_data;
   wire [18-1:0] ext_mem_w_addr;
   wire [ 4-1:0] ext_mem_w_strb;
   wire          versat_rom_clk;
   wire [10-1:0] versat_rom_addr;
   wire          versat_rom_en;
   wire [32-1:0] versat_rom_r_data;

   // Wrapped module
   iob_soc_tester #(
      .AXI_ID_W           (AXI_ID_W),
      .AXI_ADDR_W         (AXI_ADDR_W),
      .AXI_DATA_W         (AXI_DATA_W),
      .AXI_LEN_W          (AXI_LEN_W),
      .BOOTROM_MEM_HEXFILE(BOOTROM_MEM_HEXFILE),
      .EXT_MEM_HEXFILE    (EXT_MEM_HEXFILE)
   ) iob_soc_tester_inst (
      // clk_en_rst_s port: Clock, clock enable and reset
      .clk_i               (clk_i),
      .cke_i               (cke_i),
      .arst_i              (arst_i),
      // rom_bus_m port: Ports for connection with boot ROM memory
      .bootrom_mem_clk_o   (bootrom_mem_clk),
      .bootrom_mem_addr_o  (bootrom_mem_addr),
      .bootrom_mem_en_o    (bootrom_mem_en),
      .bootrom_mem_r_data_i(bootrom_mem_r_data),
      // external_mem_bus_m port: Port for connection to external 'iob_ram_t2p_be' memory
      .ext_mem_clk_o       (ext_mem_clk),
      .ext_mem_r_data_i    (ext_mem_r_data),
      .ext_mem_r_en_o      (ext_mem_r_en),
      .ext_mem_r_addr_o    (ext_mem_r_addr),
      .ext_mem_w_data_o    (ext_mem_w_data),
      .ext_mem_w_addr_o    (ext_mem_w_addr),
      .ext_mem_w_strb_o    (ext_mem_w_strb),
      // axi_m port: AXI manager interface for DDR memory
      .axi_araddr_o        (axi_araddr_o),
      .axi_arvalid_o       (axi_arvalid_o),
      .axi_arready_i       (axi_arready_i),
      .axi_rdata_i         (axi_rdata_i),
      .axi_rresp_i         (axi_rresp_i),
      .axi_rvalid_i        (axi_rvalid_i),
      .axi_rready_o        (axi_rready_o),
      .axi_arid_o          (axi_arid_o),
      .axi_arlen_o         (axi_arlen_o),
      .axi_arsize_o        (axi_arsize_o),
      .axi_arburst_o       (axi_arburst_o),
      .axi_arlock_o        (axi_arlock_o),
      .axi_arcache_o       (axi_arcache_o),
      .axi_arqos_o         (axi_arqos_o),
      .axi_rid_i           (axi_rid_i),
      .axi_rlast_i         (axi_rlast_i),
      .axi_awaddr_o        (axi_awaddr_o),
      .axi_awvalid_o       (axi_awvalid_o),
      .axi_awready_i       (axi_awready_i),
      .axi_wdata_o         (axi_wdata_o),
      .axi_wstrb_o         (axi_wstrb_o),
      .axi_wvalid_o        (axi_wvalid_o),
      .axi_wready_i        (axi_wready_i),
      .axi_bresp_i         (axi_bresp_i),
      .axi_bvalid_i        (axi_bvalid_i),
      .axi_bready_o        (axi_bready_o),
      .axi_awid_o          (axi_awid_o),
      .axi_awlen_o         (axi_awlen_o),
      .axi_awsize_o        (axi_awsize_o),
      .axi_awburst_o       (axi_awburst_o),
      .axi_awlock_o        (axi_awlock_o),
      .axi_awcache_o       (axi_awcache_o),
      .axi_awqos_o         (axi_awqos_o),
      .axi_wlast_o         (axi_wlast_o),
      .axi_bid_i           (axi_bid_i),
      // rs232_m port: iob-system uart interface
      .rs232_rxd_i         (rs232_rxd_i),
      .rs232_txd_o         (rs232_txd_o),
      .rs232_rts_o         (rs232_rts_o),
      .rs232_cts_i         (rs232_cts_i),
      // versat_rom_m port: Default description
      .versat_rom_clk_o    (versat_rom_clk),
      .versat_rom_addr_o   (versat_rom_addr),
      .versat_rom_en_o     (versat_rom_en),
      .versat_rom_r_data_i (versat_rom_r_data)
   );

   // Default description
   iob_rom_sp #(
      .DATA_W (32),
      .ADDR_W (10),
      .HEXFILE(BOOTROM_MEM_HEXFILE)
   ) bootrom_mem_mem (
      // rom_sp_s port: ROM interface
      .clk_i   (bootrom_mem_clk),
      .addr_i  (bootrom_mem_addr),
      .en_i    (bootrom_mem_en),
      .r_data_o(bootrom_mem_r_data)
   );

   // Default description
   iob_ram_t2p_be #(
      .DATA_W (32),
      .ADDR_W (18),
      .HEXFILE(EXT_MEM_HEXFILE)
   ) ext_mem_mem (
      // ram_t2p_be_s port: RAM interface
      .clk_i   (ext_mem_clk),
      .r_data_o(ext_mem_r_data),
      .r_en_i  (ext_mem_r_en),
      .r_addr_i(ext_mem_r_addr),
      .w_data_i(ext_mem_w_data),
      .w_addr_i(ext_mem_w_addr),
      .w_strb_i(ext_mem_w_strb)
   );

   // Default description
   iob_rom_sp #(
      .DATA_W (32),
      .ADDR_W (10),
      .HEXFILE("versat_ai_bootrom")
   ) versat_rom_mem (
      // rom_sp_s port: ROM interface
      .clk_i   (versat_rom_clk),
      .addr_i  (versat_rom_addr),
      .en_i    (versat_rom_en),
      .r_data_o(versat_rom_r_data)
   );


endmodule
