#include "iob_eth_csrs.h"

// Base Address
static uint32_t base;
void iob_eth_csrs_init_baseaddr(uint32_t addr) { base = addr; }

// Core Setters and Getters
void iob_eth_csrs_set_moder(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MODER_ADDR, IOB_ETH_CSRS_MODER_W, value);
}

uint32_t iob_eth_csrs_get_moder() {
  return iob_read(base + IOB_ETH_CSRS_MODER_ADDR, IOB_ETH_CSRS_MODER_W);
}

void iob_eth_csrs_set_int_source(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_INT_SOURCE_ADDR, IOB_ETH_CSRS_INT_SOURCE_W,
            value);
}

uint32_t iob_eth_csrs_get_int_source() {
  return iob_read(base + IOB_ETH_CSRS_INT_SOURCE_ADDR,
                  IOB_ETH_CSRS_INT_SOURCE_W);
}

void iob_eth_csrs_set_int_mask(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_INT_MASK_ADDR, IOB_ETH_CSRS_INT_MASK_W, value);
}

uint32_t iob_eth_csrs_get_int_mask() {
  return iob_read(base + IOB_ETH_CSRS_INT_MASK_ADDR, IOB_ETH_CSRS_INT_MASK_W);
}

void iob_eth_csrs_set_ipgt(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_IPGT_ADDR, IOB_ETH_CSRS_IPGT_W, value);
}

uint32_t iob_eth_csrs_get_ipgt() {
  return iob_read(base + IOB_ETH_CSRS_IPGT_ADDR, IOB_ETH_CSRS_IPGT_W);
}

void iob_eth_csrs_set_ipgr1(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_IPGR1_ADDR, IOB_ETH_CSRS_IPGR1_W, value);
}

uint32_t iob_eth_csrs_get_ipgr1() {
  return iob_read(base + IOB_ETH_CSRS_IPGR1_ADDR, IOB_ETH_CSRS_IPGR1_W);
}

void iob_eth_csrs_set_ipgr2(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_IPGR2_ADDR, IOB_ETH_CSRS_IPGR2_W, value);
}

uint32_t iob_eth_csrs_get_ipgr2() {
  return iob_read(base + IOB_ETH_CSRS_IPGR2_ADDR, IOB_ETH_CSRS_IPGR2_W);
}

void iob_eth_csrs_set_packetlen(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_PACKETLEN_ADDR, IOB_ETH_CSRS_PACKETLEN_W,
            value);
}

uint32_t iob_eth_csrs_get_packetlen() {
  return iob_read(base + IOB_ETH_CSRS_PACKETLEN_ADDR, IOB_ETH_CSRS_PACKETLEN_W);
}

void iob_eth_csrs_set_collconf(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_COLLCONF_ADDR, IOB_ETH_CSRS_COLLCONF_W, value);
}

uint32_t iob_eth_csrs_get_collconf() {
  return iob_read(base + IOB_ETH_CSRS_COLLCONF_ADDR, IOB_ETH_CSRS_COLLCONF_W);
}

void iob_eth_csrs_set_tx_bd_num(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_TX_BD_NUM_ADDR, IOB_ETH_CSRS_TX_BD_NUM_W,
            value);
}

uint32_t iob_eth_csrs_get_tx_bd_num() {
  return iob_read(base + IOB_ETH_CSRS_TX_BD_NUM_ADDR, IOB_ETH_CSRS_TX_BD_NUM_W);
}

void iob_eth_csrs_set_ctrlmoder(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_CTRLMODER_ADDR, IOB_ETH_CSRS_CTRLMODER_W,
            value);
}

uint32_t iob_eth_csrs_get_ctrlmoder() {
  return iob_read(base + IOB_ETH_CSRS_CTRLMODER_ADDR, IOB_ETH_CSRS_CTRLMODER_W);
}

void iob_eth_csrs_set_miimoder(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MIIMODER_ADDR, IOB_ETH_CSRS_MIIMODER_W, value);
}

uint32_t iob_eth_csrs_get_miimoder() {
  return iob_read(base + IOB_ETH_CSRS_MIIMODER_ADDR, IOB_ETH_CSRS_MIIMODER_W);
}

void iob_eth_csrs_set_miicommand(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MIICOMMAND_ADDR, IOB_ETH_CSRS_MIICOMMAND_W,
            value);
}

uint32_t iob_eth_csrs_get_miicommand() {
  return iob_read(base + IOB_ETH_CSRS_MIICOMMAND_ADDR,
                  IOB_ETH_CSRS_MIICOMMAND_W);
}

void iob_eth_csrs_set_miiaddress(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MIIADDRESS_ADDR, IOB_ETH_CSRS_MIIADDRESS_W,
            value);
}

uint32_t iob_eth_csrs_get_miiaddress() {
  return iob_read(base + IOB_ETH_CSRS_MIIADDRESS_ADDR,
                  IOB_ETH_CSRS_MIIADDRESS_W);
}

void iob_eth_csrs_set_miitx_data(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MIITX_DATA_ADDR, IOB_ETH_CSRS_MIITX_DATA_W,
            value);
}

uint32_t iob_eth_csrs_get_miitx_data() {
  return iob_read(base + IOB_ETH_CSRS_MIITX_DATA_ADDR,
                  IOB_ETH_CSRS_MIITX_DATA_W);
}

void iob_eth_csrs_set_miirx_data(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MIIRX_DATA_ADDR, IOB_ETH_CSRS_MIIRX_DATA_W,
            value);
}

uint32_t iob_eth_csrs_get_miirx_data() {
  return iob_read(base + IOB_ETH_CSRS_MIIRX_DATA_ADDR,
                  IOB_ETH_CSRS_MIIRX_DATA_W);
}

void iob_eth_csrs_set_miistatus(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MIISTATUS_ADDR, IOB_ETH_CSRS_MIISTATUS_W,
            value);
}

uint32_t iob_eth_csrs_get_miistatus() {
  return iob_read(base + IOB_ETH_CSRS_MIISTATUS_ADDR, IOB_ETH_CSRS_MIISTATUS_W);
}

void iob_eth_csrs_set_mac_addr0(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MAC_ADDR0_ADDR, IOB_ETH_CSRS_MAC_ADDR0_W,
            value);
}

uint32_t iob_eth_csrs_get_mac_addr0() {
  return iob_read(base + IOB_ETH_CSRS_MAC_ADDR0_ADDR, IOB_ETH_CSRS_MAC_ADDR0_W);
}

void iob_eth_csrs_set_mac_addr1(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_MAC_ADDR1_ADDR, IOB_ETH_CSRS_MAC_ADDR1_W,
            value);
}

uint32_t iob_eth_csrs_get_mac_addr1() {
  return iob_read(base + IOB_ETH_CSRS_MAC_ADDR1_ADDR, IOB_ETH_CSRS_MAC_ADDR1_W);
}

void iob_eth_csrs_set_eth_hash0_adr(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_ETH_HASH0_ADR_ADDR,
            IOB_ETH_CSRS_ETH_HASH0_ADR_W, value);
}

uint32_t iob_eth_csrs_get_eth_hash0_adr() {
  return iob_read(base + IOB_ETH_CSRS_ETH_HASH0_ADR_ADDR,
                  IOB_ETH_CSRS_ETH_HASH0_ADR_W);
}

void iob_eth_csrs_set_eth_hash1_adr(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_ETH_HASH1_ADR_ADDR,
            IOB_ETH_CSRS_ETH_HASH1_ADR_W, value);
}

uint32_t iob_eth_csrs_get_eth_hash1_adr() {
  return iob_read(base + IOB_ETH_CSRS_ETH_HASH1_ADR_ADDR,
                  IOB_ETH_CSRS_ETH_HASH1_ADR_W);
}

void iob_eth_csrs_set_eth_txctrl(uint32_t value) {
  iob_write(base + IOB_ETH_CSRS_ETH_TXCTRL_ADDR, IOB_ETH_CSRS_ETH_TXCTRL_W,
            value);
}

uint32_t iob_eth_csrs_get_eth_txctrl() {
  return iob_read(base + IOB_ETH_CSRS_ETH_TXCTRL_ADDR,
                  IOB_ETH_CSRS_ETH_TXCTRL_W);
}

uint8_t iob_eth_csrs_get_tx_bd_cnt() {
  return iob_read(base + IOB_ETH_CSRS_TX_BD_CNT_ADDR, IOB_ETH_CSRS_TX_BD_CNT_W);
}

uint8_t iob_eth_csrs_get_rx_bd_cnt() {
  return iob_read(base + IOB_ETH_CSRS_RX_BD_CNT_ADDR, IOB_ETH_CSRS_RX_BD_CNT_W);
}

uint32_t iob_eth_csrs_get_tx_word_cnt() {
  return iob_read(base + IOB_ETH_CSRS_TX_WORD_CNT_ADDR,
                  IOB_ETH_CSRS_TX_WORD_CNT_W);
}

uint32_t iob_eth_csrs_get_rx_word_cnt() {
  return iob_read(base + IOB_ETH_CSRS_RX_WORD_CNT_ADDR,
                  IOB_ETH_CSRS_RX_WORD_CNT_W);
}

uint32_t iob_eth_csrs_get_rx_nbytes() {
  return iob_read(base + IOB_ETH_CSRS_RX_NBYTES_ADDR, IOB_ETH_CSRS_RX_NBYTES_W);
}

void iob_eth_csrs_set_frame_word(uint8_t value) {
  iob_write(base + IOB_ETH_CSRS_FRAME_WORD_ADDR, IOB_ETH_CSRS_FRAME_WORD_W,
            value);
}

uint8_t iob_eth_csrs_get_frame_word() {
  return iob_read(base + IOB_ETH_CSRS_FRAME_WORD_ADDR,
                  IOB_ETH_CSRS_FRAME_WORD_W);
}

uint8_t iob_eth_csrs_get_phy_rst_val() {
  return iob_read(base + IOB_ETH_CSRS_PHY_RST_VAL_ADDR,
                  IOB_ETH_CSRS_PHY_RST_VAL_W);
}

void iob_eth_csrs_set_bd(uint32_t value,int addr) {
  iob_write(base + IOB_ETH_CSRS_BD_ADDR + addr, IOB_ETH_CSRS_BD_W, value);
}

uint32_t iob_eth_csrs_get_bd(int addr) {
  return iob_read(base + IOB_ETH_CSRS_BD_ADDR + addr, IOB_ETH_CSRS_BD_W);
}

uint16_t iob_eth_csrs_get_version() {
  return iob_read(base + IOB_ETH_CSRS_VERSION_ADDR, IOB_ETH_CSRS_VERSION_W);
}
