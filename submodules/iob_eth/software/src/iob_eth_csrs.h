#ifndef H_IOB_ETH_CSRS_CSRS_H
#define H_IOB_ETH_CSRS_CSRS_H

#include <stdint.h>

// used address space width
#define IOB_ETH_CSRS_CSRS_ADDR_W 12

// Addresses
#define IOB_ETH_CSRS_MODER_ADDR 0
#define IOB_ETH_CSRS_INT_SOURCE_ADDR 4
#define IOB_ETH_CSRS_INT_MASK_ADDR 8
#define IOB_ETH_CSRS_IPGT_ADDR 12
#define IOB_ETH_CSRS_IPGR1_ADDR 16
#define IOB_ETH_CSRS_IPGR2_ADDR 20
#define IOB_ETH_CSRS_PACKETLEN_ADDR 24
#define IOB_ETH_CSRS_COLLCONF_ADDR 28
#define IOB_ETH_CSRS_TX_BD_NUM_ADDR 32
#define IOB_ETH_CSRS_CTRLMODER_ADDR 36
#define IOB_ETH_CSRS_MIIMODER_ADDR 40
#define IOB_ETH_CSRS_MIICOMMAND_ADDR 44
#define IOB_ETH_CSRS_MIIADDRESS_ADDR 48
#define IOB_ETH_CSRS_MIITX_DATA_ADDR 52
#define IOB_ETH_CSRS_MIIRX_DATA_ADDR 56
#define IOB_ETH_CSRS_MIISTATUS_ADDR 60
#define IOB_ETH_CSRS_MAC_ADDR0_ADDR 64
#define IOB_ETH_CSRS_MAC_ADDR1_ADDR 68
#define IOB_ETH_CSRS_ETH_HASH0_ADR_ADDR 72
#define IOB_ETH_CSRS_ETH_HASH1_ADR_ADDR 76
#define IOB_ETH_CSRS_ETH_TXCTRL_ADDR 80
#define IOB_ETH_CSRS_TX_BD_CNT_ADDR 84
#define IOB_ETH_CSRS_RX_BD_CNT_ADDR 88
#define IOB_ETH_CSRS_TX_WORD_CNT_ADDR 92
#define IOB_ETH_CSRS_RX_WORD_CNT_ADDR 96
#define IOB_ETH_CSRS_RX_NBYTES_ADDR 100
#define IOB_ETH_CSRS_FRAME_WORD_ADDR 104
#define IOB_ETH_CSRS_PHY_RST_VAL_ADDR 108
#define IOB_ETH_CSRS_BD_ADDR 1024
#define IOB_ETH_CSRS_VERSION_ADDR 2048

// Data widths (bit)
#define IOB_ETH_CSRS_MODER_W 32
#define IOB_ETH_CSRS_INT_SOURCE_W 32
#define IOB_ETH_CSRS_INT_MASK_W 32
#define IOB_ETH_CSRS_IPGT_W 32
#define IOB_ETH_CSRS_IPGR1_W 32
#define IOB_ETH_CSRS_IPGR2_W 32
#define IOB_ETH_CSRS_PACKETLEN_W 32
#define IOB_ETH_CSRS_COLLCONF_W 32
#define IOB_ETH_CSRS_TX_BD_NUM_W 32
#define IOB_ETH_CSRS_CTRLMODER_W 32
#define IOB_ETH_CSRS_MIIMODER_W 32
#define IOB_ETH_CSRS_MIICOMMAND_W 32
#define IOB_ETH_CSRS_MIIADDRESS_W 32
#define IOB_ETH_CSRS_MIITX_DATA_W 32
#define IOB_ETH_CSRS_MIIRX_DATA_W 32
#define IOB_ETH_CSRS_MIISTATUS_W 32
#define IOB_ETH_CSRS_MAC_ADDR0_W 32
#define IOB_ETH_CSRS_MAC_ADDR1_W 32
#define IOB_ETH_CSRS_ETH_HASH0_ADR_W 32
#define IOB_ETH_CSRS_ETH_HASH1_ADR_W 32
#define IOB_ETH_CSRS_ETH_TXCTRL_W 32
#define IOB_ETH_CSRS_TX_BD_CNT_W 8
#define IOB_ETH_CSRS_RX_BD_CNT_W 8
#define IOB_ETH_CSRS_TX_WORD_CNT_W 32
#define IOB_ETH_CSRS_RX_WORD_CNT_W 32
#define IOB_ETH_CSRS_RX_NBYTES_W 32
#define IOB_ETH_CSRS_FRAME_WORD_W 8
#define IOB_ETH_CSRS_PHY_RST_VAL_W 8
#define IOB_ETH_CSRS_BD_W 32
#define IOB_ETH_CSRS_VERSION_W 16

// Base Address
void iob_eth_csrs_init_baseaddr(uint32_t addr);

// IO read and write function prototypes
void iob_write(uint32_t addr, uint32_t data_w, uint32_t value);
uint32_t iob_read(uint32_t addr, uint32_t data_w);

// Core Setters and Getters
void iob_eth_csrs_set_moder(uint32_t value);
uint32_t iob_eth_csrs_get_moder();
void iob_eth_csrs_set_int_source(uint32_t value);
uint32_t iob_eth_csrs_get_int_source();
void iob_eth_csrs_set_int_mask(uint32_t value);
uint32_t iob_eth_csrs_get_int_mask();
void iob_eth_csrs_set_ipgt(uint32_t value);
uint32_t iob_eth_csrs_get_ipgt();
void iob_eth_csrs_set_ipgr1(uint32_t value);
uint32_t iob_eth_csrs_get_ipgr1();
void iob_eth_csrs_set_ipgr2(uint32_t value);
uint32_t iob_eth_csrs_get_ipgr2();
void iob_eth_csrs_set_packetlen(uint32_t value);
uint32_t iob_eth_csrs_get_packetlen();
void iob_eth_csrs_set_collconf(uint32_t value);
uint32_t iob_eth_csrs_get_collconf();
void iob_eth_csrs_set_tx_bd_num(uint32_t value);
uint32_t iob_eth_csrs_get_tx_bd_num();
void iob_eth_csrs_set_ctrlmoder(uint32_t value);
uint32_t iob_eth_csrs_get_ctrlmoder();
void iob_eth_csrs_set_miimoder(uint32_t value);
uint32_t iob_eth_csrs_get_miimoder();
void iob_eth_csrs_set_miicommand(uint32_t value);
uint32_t iob_eth_csrs_get_miicommand();
void iob_eth_csrs_set_miiaddress(uint32_t value);
uint32_t iob_eth_csrs_get_miiaddress();
void iob_eth_csrs_set_miitx_data(uint32_t value);
uint32_t iob_eth_csrs_get_miitx_data();
void iob_eth_csrs_set_miirx_data(uint32_t value);
uint32_t iob_eth_csrs_get_miirx_data();
void iob_eth_csrs_set_miistatus(uint32_t value);
uint32_t iob_eth_csrs_get_miistatus();
void iob_eth_csrs_set_mac_addr0(uint32_t value);
uint32_t iob_eth_csrs_get_mac_addr0();
void iob_eth_csrs_set_mac_addr1(uint32_t value);
uint32_t iob_eth_csrs_get_mac_addr1();
void iob_eth_csrs_set_eth_hash0_adr(uint32_t value);
uint32_t iob_eth_csrs_get_eth_hash0_adr();
void iob_eth_csrs_set_eth_hash1_adr(uint32_t value);
uint32_t iob_eth_csrs_get_eth_hash1_adr();
void iob_eth_csrs_set_eth_txctrl(uint32_t value);
uint32_t iob_eth_csrs_get_eth_txctrl();
uint8_t iob_eth_csrs_get_tx_bd_cnt();
uint8_t iob_eth_csrs_get_rx_bd_cnt();
uint32_t iob_eth_csrs_get_tx_word_cnt();
uint32_t iob_eth_csrs_get_rx_word_cnt();
uint32_t iob_eth_csrs_get_rx_nbytes();
void iob_eth_csrs_set_frame_word(uint8_t value);
uint8_t iob_eth_csrs_get_frame_word();
uint8_t iob_eth_csrs_get_phy_rst_val();
void iob_eth_csrs_set_bd(uint32_t value,int addr);
uint32_t iob_eth_csrs_get_bd(int addr);
uint16_t iob_eth_csrs_get_version();

#endif // H_IOB_ETH_CSRS__CSRS_H
