/*
 * SPDX-FileCopyrightText: 2024 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_soc_tester_conf.h"
#include "iob_soc_tester_mmap.h"
#include "versat_ai_uart.h"
#ifndef IOB_SOC_TESTER_INIT_MEM
#include "iob_printf.h"
//#include "iob_eth.h"
//#include "iob_eth_rmac.h"
#endif

#define PROGNAME "IOb-Bootloader"

#if IOB_SOC_TESTER_ILA == 1
#include "iob_ila.h"
#include "iob_ila_csrs.h"
#include "iob_watchdog.h"
#endif

#ifndef IOB_SOC_TESTER_INIT_MEM
void clear_cache() {
  // Delay to ensure all data is written to memory
  for (unsigned int i = 0; i < 10; i++)
    asm volatile("nop");
  // Flush VexRiscv CPU internal cache
  asm volatile(".word 0x500F" ::: "memory");
}

// Send signal by uart to receive file by ethernet
uint32_t uart_recvfile_ethernet(const char *file_name) {

  uart_puts(UART_PROGNAME);
  uart_puts(": requesting to receive file by ethernet\n");

  // send file receive by ethernet request
  uart_putc(0x13);

  // send file name (including end of string)
  uart_puts(file_name);
  uart_putc(0);

  // receive file size
  uint32_t file_size = uart_getc();
  file_size |= ((uint32_t)uart_getc()) << 8;
  file_size |= ((uint32_t)uart_getc()) << 16;
  file_size |= ((uint32_t)uart_getc()) << 24;

  // send ACK before receiving file
  uart_putc(ACK);

  return file_size;
}
#endif

int main() {

  // init uart
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);

#if IOB_SOC_TESTER_ILA == 1
  iob_ila_csrs_init_baseaddr(ILA0_BASE);
  ila_disable_all_triggers();
  watchdog_init(WATCHDOG0_BASE);
  if (watchdog_time_tu(1000000) > 0) {
    goto end;
  }
#endif

  // connect with console
  do {
    if (versat_ai_uart_csrs_get_txready())
      uart_putc((char)ENQ);
  } while (!versat_ai_uart_csrs_get_rxready());

  // welcome message
  uart_puts(PROGNAME);
  uart_puts(": connected!\n");

#ifdef IOB_SOC_TESTER_USE_EXTMEM
  uart_puts(PROGNAME);
  uart_puts(": DDR in use. Program runs from internal memory.\n");
#endif

  while (uart_getc() != ACK) {
    uart_puts(PROGNAME);
    uart_puts(": Waiting for Console ACK.\n");
  }

#ifndef IOB_SOC_TESTER_INIT_MEM
  printf_init(&uart_putc);
  // init console eth
  // eth_init(ETH0_BASE, &clear_cache);
  uart_puts("[Tester]: Waiting for ethernet PHY reset to finish...\n\n");
  // eth_wait_phy_rst();

  // address to copy tester firmware to
  char *tester_start_addr = (char *)IOB_SOC_TESTER_FW_BASEADDR;

  uart_puts(PROGNAME);
  uart_puts(": Loading tester firmware.\n");
  // receive data from host via ethernet
  int file_size = 0;
  char tester_fw[] = "iob_soc_tester_firmware.bin";
  // file_size = uart_recvfile_ethernet(tester_fw);
  // eth_rcv_file((char *)tester_start_addr, file_size);
  uart_recvfile(tester_fw, (char *)tester_start_addr);

  // address to copy SUT firmware to
  char *sut_start_addr = (char *)EXTMEM_BASE;

  uart_puts(PROGNAME);
  uart_puts(": Loading sut firmware.\n");
  // receive firmware from host
  char sut_fw[] = "versat_ai_firmware.bin";
  // file_size = uart_recvfile_ethernet(sut_fw);
  // eth_rcv_file((char *)sut_start_addr, file_size);
  uart_recvfile(sut_fw, (char *)sut_start_addr);
#endif

end:
  // run firmware
  uart_puts(PROGNAME);
  uart_puts(": Restart CPU to run user program...\n");
  uart_txwait();
}
