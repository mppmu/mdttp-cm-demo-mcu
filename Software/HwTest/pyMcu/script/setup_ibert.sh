#!/bin/sh
# File: setup_ibert.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 23 Mar 2021
# Rev.: 14 Feb 2023
#
# Simple script to set up the ATLAS MDT Trigger Processor (TP) Command Module
# for Xilinx IBERT tests.
#



cd `dirname $0`
cd ..



PY_MCU_CM="./pyMcuCm.py"
SERIAL_DEVICE="/dev/ttyUL1"
VERBOSITY="0"



echo "Power up the Command Module."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c power_up
# Wait some time so that the newly powered devices are ready for operation.
sleep 0.2

echo "Program the clock synthesizer chip IC60 (Si5345A) for the sector logic (SL) communication."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC60 config/clock/IBERT-Test/IC60_h6B_FreeRun_O-100M-Registers.txt

echo "Program the clock synthesizer chip IC61 (Si5342A) for the neighbor exchange (CM2CM) communication."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC61 config/clock/IBERT-Test/IC61_h68_FreeRun_O-100M-Registers.txt

echo "Program the clock synthesizer chip IC62 (Si5345A) for the KU15P-ZU11EG (C2M) communication."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC62 config/clock/IBERT-Test/IC62_h69_FreeRun_O-100M-Registers.txt

echo "Program the clock synthesizer chip IC63 (Si5345A) for the SFP+ / legacy TTC communication."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC63 config/clock/IBERT-Test/IC63_h6A_FreeRun_O-100M-Registers.txt

echo "Program the clock synthesizer chip IC82 (Si5344A) for the FELIX communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC82 config/clock/IBERT-Test/IC82_h6A_FreeRun_O-100M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC82 config/clock/IBERT-Test/IC82_h6A_FreeRun_O-240M-Registers.txt

echo "Program the clock synthesizer chip IC84 (Si5345A) for the front-end (FE) communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC84 config/clock/IBERT-Test/IC84_h69_FreeRun_O-100M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC84 config/clock/IBERT-Test/IC84_h69_FreeRun_O-320M-Registers.txt

echo "Program the clock synthesizer chip IC85 (Si5345A) for the front-end (FE) communication."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC85 config/clock/IBERT-Test/IC85_h6A_FreeRun_O-100M-Registers.txt

