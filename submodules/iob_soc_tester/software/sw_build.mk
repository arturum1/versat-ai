# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

#########################################
#            Embedded targets           #
#########################################
ROOT_DIR ?=..

include $(ROOT_DIR)/software/auto_sw_build.mk

# Local embedded makefile settings for custom bootloader and firmware targets.

#Function to obtain parameter named $(1) in verilog header file located in $(2)
#Usage: $(call GET_MACRO,<param_name>,<vh_path>)
GET_MACRO = $(shell grep "define $(1)" $(2) | rev | cut -d" " -f1 | rev)

#Function to obtain parameter named $(1) from iob_soc_tester_conf.vh
GET_IOB_SOC_TESTER_CONF_MACRO = $(call GET_MACRO,IOB_SOC_TESTER_$(1),$(2))

iob_soc_tester_bootrom.hex: ../../software/iob_soc_tester_preboot.bin ../../software/iob_soc_tester_boot.bin
	../../scripts/makehex.py $^ 00000080 $(call GET_IOB_SOC_TESTER_CONF_MACRO,BOOTROM_ADDR_W,../src/iob_soc_tester_conf.vh) $@

iob_soc_tester_firmware.hex: iob_soc_tester_firmware.bin
	../../scripts/makehex.py $< $(call GET_IOB_SOC_TESTER_CONF_MACRO,FW_ADDR_W,../src/iob_soc_tester_conf.vh) $@
	../../scripts/makehex.py --split $< $(call GET_IOB_SOC_TESTER_CONF_MACRO,FW_ADDR_W,../src/iob_soc_tester_conf.vh) $@

iob_soc_tester_firmware.bin: ../../software/iob_soc_tester_firmware.bin
	cp $< $@

../../software/%.bin:
	make -C ../../ fw-build

UTARGETS:=build_iob_soc_tester_software tb $(UTARGETS)
CSRS=./src/iob_uart_csrs.c

TEMPLATE_LDS=src/$@.lds

IOB_SOC_TESTER_INCLUDES=-Isrc

IOB_SOC_TESTER_CFLAGS=-O3 -nostdlib -march=rv32imac -mabi=ilp32 --specs=nano.specs -Wcast-align=strict $(USER_CFLAGS)
IOB_SOC_TESTER_LFLAGS=-Wl,-L,src,-Bstatic,-T,$(TEMPLATE_LDS),--strip-debug

# FIRMWARE SOURCES
IOB_SOC_TESTER_FW_SRC=src/iob_soc_tester_firmware.S
IOB_SOC_TESTER_FW_SRC+=src/iob_soc_tester_firmware.c
IOB_SOC_TESTER_FW_SRC+=src/iob_printf.c

# PERIPHERAL SOURCES
PERIPHERALS+=versat_ai iob_regfileif#FIXME Hack
DRIVERS=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
DRIVERS_CSR=$(addprefix src/,$(addsuffix _csrs.c,$(PERIPHERALS)))
# Only add driver files if they exist
IOB_SOC_TESTER_FW_SRC+=$(foreach file,$(DRIVERS),$(wildcard $(file)*))
IOB_SOC_TESTER_FW_SRC+=$(foreach file,$(DRIVERS_CSR),$(wildcard $(file)*))

# BOOTLOADER SOURCES
IOB_SOC_TESTER_BOOT_SRC+=src/iob_soc_tester_boot.S
IOB_SOC_TESTER_BOOT_SRC+=src/iob_soc_tester_boot.c
IOB_SOC_TESTER_BOOT_SRC+=src/iob_printf.c
IOB_SOC_TESTER_BOOT_SRC+=src/versat_ai_uart.c
IOB_SOC_TESTER_BOOT_SRC+=src/versat_ai_uart_csrs.c

# PREBOOT SOURCES
IOB_SOC_TESTER_PREBOOT_SRC=src/iob_soc_tester_preboot.S

build_iob_soc_tester_software: iob_soc_tester_firmware iob_soc_tester_boot iob_soc_tester_preboot

ifneq ($(USE_FPGA),)
T_WRAPPER_CONFS_PREFIX=iob_soc_tester_$(BOARD)
WRAPPER_CONFS_PREFIX=versat_ai_$(BOARD)
else
T_WRAPPER_CONFS_PREFIX=iob_uut
WRAPPER_CONFS_PREFIX=iob_uut
endif

iob_bsp:
	sed 's/$(T_WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' src/$(T_WRAPPER_CONFS_PREFIX)_conf.h > src/iob_bsp.h
	sed 's/$(T_WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' src/$(T_WRAPPER_CONFS_PREFIX)_conf.h > ../../software/src/$(WRAPPER_CONFS_PREFIX)_conf.h

iob_soc_tester_firmware: iob_bsp
	make $@.elf INCLUDES="$(IOB_SOC_TESTER_INCLUDES)" CFLAGS="$(IOB_SOC_TESTER_CFLAGS)" LFLAGS="$(IOB_SOC_TESTER_LFLAGS) -Wl,-Map,$@.map" SRC="${IOB_SOC_TESTER_FW_SRC}" TEMPLATE_LDS="$(TEMPLATE_LDS)";

iob_soc_tester_boot: iob_bsp
	make $@.elf INCLUDES="$(IOB_SOC_TESTER_INCLUDES)" CFLAGS="$(IOB_SOC_TESTER_CFLAGS)" LFLAGS="$(IOB_SOC_TESTER_LFLAGS) -Wl,-Map,$@.map" SRC="${IOB_SOC_TESTER_BOOT_SRC}" TEMPLATE_LDS="$(TEMPLATE_LDS)";

iob_soc_tester_preboot:
	make $@.elf INCLUDES="$(IOB_SOC_TESTER_INCLUDES)" CFLAGS="$(IOB_SOC_TESTER_CFLAGS)" LFLAGS="$(IOB_SOC_TESTER_LFLAGS) -Wl,-Map,$@.map" SRC="$(IOB_SOC_TESTER_PREBOOT_SRC)" TEMPLATE_LDS="$(TEMPLATE_LDS)" NO_HW_DRIVER=1

.PHONY: build_iob_soc_tester_software iob_bsp iob_soc_tester_firmware iob_soc_tester_boot iob_soc_tester_preboot

#########################################
#         PC emulation targets          #
#########################################
# Local pc-emul makefile settings for custom pc emulation targets.
EMUL_HDR+=iob_bsp

# SOURCES
EMUL_SRC+=src/iob_soc_tester_firmware.c
EMUL_SRC+=src/iob_printf.c

# PERIPHERAL SOURCES
EMUL_SRC+=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
EMUL_SRC+=$(addprefix src/,$(addsuffix _csrs_pc_emul.c,$(PERIPHERALS)))