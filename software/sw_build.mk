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

#Function to obtain parameter named $(1) from versat_ai_conf.vh
GET_VERSAT_AI_CONF_MACRO = $(call GET_MACRO,VERSAT_AI_$(1),$(2))

versat_ai_firmware.hex: versat_ai_firmware.bin
	../../scripts/makehex.py $< $(call GET_VERSAT_AI_CONF_MACRO,MEM_ADDR_W,../src/versat_ai_conf.vh) $@
	../../scripts/makehex.py --split $< $(call GET_VERSAT_AI_CONF_MACRO,MEM_ADDR_W,../src/versat_ai_conf.vh) $@

versat_ai_firmware.bin: ../../software/versat_ai_firmware.bin
	cp $< $@

../../software/%.bin:
	make -C ../../ fw-build

UTARGETS+=build_versat_ai_software tb
CSRS=./src/iob_uart_csrs.c

TEMPLATE_LDS=src/$@.lds

VERSAT_AI_INCLUDES=-I. -Isrc

VERSAT_AI_CFLAGS=-O3 -nostdlib -march=rv32imac -mabi=ilp32 --specs=nano.specs -Wcast-align=strict $(USER_CFLAGS)
VERSAT_AI_LFLAGS=-Wl,-L,src,-Bstatic,-T,$(TEMPLATE_LDS),--strip-debug

# FIRMWARE SOURCES
VERSAT_AI_FW_SRC=src/versat_ai_firmware.S
VERSAT_AI_FW_SRC+=src/versat_ai_firmware.c
VERSAT_AI_FW_SRC+=src/iob_printf.c

#VERSAT_AI_MEM2MEM_SRC=src/versat_ai_mem2mem.c
#VERSAT_AI_STREAM_SRC=src/versat_ai_stream.c
#VERSAT_AI_FW_PLUS_SRC += $(AACDEC_SRC_EXTRA) $(ARITHCODING_SRC) $(FDK_SRC_EXTRA) $(SACDEC_SRC) $(SBRDEC_SRC)

# PERIPHERAL SOURCES
PERIPHERALS+=iob_regfileif_inverted#FIXME Hack
DRIVERS=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
DRIVERS_CSR=$(addprefix src/,$(addsuffix _csrs.c,$(PERIPHERALS)))
# Only add driver files if they exist
VERSAT_AI_FW_SRC+=$(foreach file,$(DRIVERS),$(wildcard $(file)*))
VERSAT_AI_FW_SRC+=$(foreach file,$(DRIVERS_CSR),$(wildcard $(file)*))

build_versat_ai_software: versat_ai_firmware

ifneq ($(USE_FPGA),)
WRAPPER_CONFS_PREFIX=versat_ai_$(BOARD)
else
WRAPPER_CONFS_PREFIX=iob_uut
endif

# Function conditionally appends additional source files to a variable
# Usage: $(call ADD_SRCS,<target_value>,<flag_value>,<variable_name>,<base_sources>,<additional_sources>)
# ADD_SRCS = $(eval $(3) := $(if $(filter $(1),$(2)),$(4) $(5),$(4)))

iob_bsp:
	sed 's/$(WRAPPER_CONFS_PREFIX)/IOB_BSP/Ig' src/$(WRAPPER_CONFS_PREFIX)_conf.h > src/iob_bsp.h

versat_ai_firmware: iob_bsp
	#$(call ADD_SRCS,0,$(call GET_VERSAT_AI_CONF_MACRO,STREAM,../hardware/src/versat_ai_conf.vh),VERSAT_AI_FW_SRC,$(VERSAT_AI_FW_SRC),$(VERSAT_AI_MEM2MEM_SRC))
	#$(call ADD_SRCS,1,$(call GET_VERSAT_AI_CONF_MACRO,STREAM,../hardware/src/versat_ai_conf.vh),VERSAT_AI_FW_SRC,$(VERSAT_AI_FW_SRC),$(VERSAT_AI_STREAM_SRC))
	#$(call ADD_SRCS,1,$(call GET_VERSAT_AI_CONF_MACRO,AACPLUS,../hardware/src/versat_ai_conf.vh),VERSAT_AI_FW_SRC,$(VERSAT_AI_FW_SRC),$(VERSAT_AI_FW_PLUS_SRC))
	make $@.elf INCLUDES="$(VERSAT_AI_INCLUDES)" CFLAGS="$(VERSAT_AI_CFLAGS)" LFLAGS="$(VERSAT_AI_LFLAGS) -Wl,-Map,$@.map" SRC="${VERSAT_AI_FW_SRC}" TEMPLATE_LDS="$(TEMPLATE_LDS)";

.PHONY: build_versat_ai_software iob_bsp versat_ai_firmware

#########################################
#         PC emulation targets          #
#########################################
# Local pc-emul makefile settings for custom pc emulation targets.
EMUL_HDR+=iob_bsp

# SOURCES
EMUL_SRC+=src/versat_ai_firmware.c
EMUL_SRC+=src/iob_printf.c

# PERIPHERAL SOURCES
EMUL_SRC+=$(addprefix src/,$(addsuffix .c,$(PERIPHERALS)))
EMUL_SRC+=$(addprefix src/,$(addsuffix _csrs_pc_emul.c,$(PERIPHERALS)))