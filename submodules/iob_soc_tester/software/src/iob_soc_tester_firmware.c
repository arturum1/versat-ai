/* Includes */
#include "iob_bsp.h"
#include "iob_soc_tester_conf.h"
#include "iob_soc_tester_mmap.h"
#include "versat_ai_conf.h"

#include "iob_printf.h"
#include "stdlib.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "iob_regfileif_csrs.h"
#include "versat_ai_uart.h"

void init_peripherals() {
  // init uart1 (connected to the SUT)
  uart_init(UART1_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);

  // init uart0
  uart_init(UART0_BASE, IOB_BSP_FREQ / IOB_BSP_BAUD);
  printf_init(&uart_putc);

  // Init SUT (connected through REGFILEIF)
  iob_regfileif_csrs_init_baseaddr(SUT0_BASE);
}

void relay_messages() {
  uint8_t c;

  versat_ai_uart_csrs_init_baseaddr(UART1_BASE);
  c = uart_getc();
  versat_ai_uart_csrs_init_baseaddr(UART0_BASE);
  uart_putc(c);
}

void test_loop() {
  while (!iob_regfileif_csrs_get_done()) {
    relay_messages();
  }

  // Print remaining messages
  while (versat_ai_uart_csrs_get_rxready()) {
    relay_messages();
  }
}

int main() {
  init_peripherals();
  iob_regfileif_csrs_set_firm_addr((int)VERSAT_AI_FW_BASEADDR);
  iob_regfileif_csrs_set_rst(0);
  iob_regfileif_csrs_set_start(1);

  test_loop();

  uart_puts("\n");
  uart_puts("[Tester]: Finished processing\n");

  uart_puts("[Tester]: 123\n");

  // End UART1 connection with SUT
  versat_ai_uart_csrs_init_baseaddr(UART1_BASE);
  uart_finish();

  // Switch back to UART0
  versat_ai_uart_csrs_init_baseaddr(UART0_BASE);

  // End UART0 connection
  uart_finish();

  return 0;
}
