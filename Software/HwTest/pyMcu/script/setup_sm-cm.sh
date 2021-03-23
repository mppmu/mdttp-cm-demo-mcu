#!/bin/sh
# File: setup_sm-cm.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 23 Mar 2021
# Rev.: 23 Mar 2021
#
# Simple script to set up the ATLAS MDT Trigger Processor (TP) SM-CM AXI
# Chip2Chip communication.
#



cd `dirname $0`
cd ..



PY_MCU_CM="./pyMcuCm.py"
SERIAL_DEVICE="/dev/ttyUL1"
VERBOSITY="0"



echo "Power up the Command Module."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c power_up

echo "Set up the AXI bus switches."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-sel 0x01
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-pd  0x00

echo "Program the clock synthesizer chip IC81 (Si5342A) for the AXI Chip2Chip communication."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC81 config/clock/IC81_h6B_FreeRun_O-200M-Registers.txt

