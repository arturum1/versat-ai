# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

## Synchronizers
#set_property ASYNC_REG TRUE [get_cells -hier {*iob_r_data_o*[*]}]
#set_property ASYNC_REG TRUE [get_cells -hier {*iob_rn_data_o*[*]}]

## Clock groups
set_clock_groups -asynchronous -group {mmcm_clkout1} -group {mmcm_clkout2}
