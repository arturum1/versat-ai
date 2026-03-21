/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

#include "iob_bsp.h"
#include "iob_uart.h"
#include "versat_ai_conf.h"
#include "versat_ai_mmap.h"

#define PROGNAME "IOb-Bootloader"

// HACK
#define IOB_BSP_BAUD 3000000
#define IOB_BSP_FREQ 100000000

int main() {

  // init uart
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);

  // connect with console
  do {
    if (iob_uart_csrs_get_txready())
      uart_putc((char)ENQ);
  } while (!iob_uart_csrs_get_rxready());

  // welcome message
  uart_puts(PROGNAME);
  uart_puts(": connected!\n");

#ifdef VERSAT_AI_USE_EXTMEM
  uart_puts(PROGNAME);
  uart_puts(": DDR in use.\n");
#endif

  // address to copy firmware to
  char *prog_start_addr = (char *)VERSAT_AI_FW_BASEADDR;

  while (uart_getc() != ACK) {
    uart_puts(PROGNAME);
    uart_puts(": Waiting for Console ACK.\n");
  }

#ifndef VERSAT_AI_INIT_MEM
  // receive firmware from host
  int file_size = 0;
  char r_fw[] = "versat_ai_firmware.bin";
  file_size = uart_recvfile(r_fw, prog_start_addr);
  uart_puts(PROGNAME);
  uart_puts(": Loading firmware...\n");

  // sending firmware back for debug
  char s_fw[] = "s_fw.bin";

  if (file_size)
    uart_sendfile(s_fw, file_size, prog_start_addr);
  else {
    uart_puts(PROGNAME);
    uart_puts(": ERROR loading firmware\n");
  }
#endif

  // run firmware
  uart_puts(PROGNAME);
  uart_puts(": Restart CPU to run user program...\n");
  uart_txwait();
}
