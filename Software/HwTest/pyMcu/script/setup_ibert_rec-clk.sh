#!/bin/sh
# File: setup_ibert_rec-clk.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 23 Mar 2021
# Rev.: 20 Apr 2021
#
# Simple script to set up the ATLAS MDT Trigger Processor (TP) Command Module
# for Xilinx IBERT tests, using the recovered clock from the FELIX IBERT module
# for the front-end IBERT module.
#
# Reference clock path on the CM cemonstrator V1:
#   IC54, free-running mode, OUT: 40 MHz
#   -> IC82, IN0: 40 MHz, OUT: 240 MHz
#   -> KU15P FELIX IBERT, MGTREFCLK0: 240 MHz -> rxoutclock: 120 MHz
#   -> Multiplexer for recovered LHC clock (IC57)
#   -> IC56, IN3: 120 MHz, OUT: 40 MHz
#   -> IC83, IN2:  40 MHz, OUT: 40 MHz
#       +-> IC84, IN0: 40 MHz, OUT: 320 MHz -> KU15P FE IBERT, MGTREFCLK0: 320 MHz
#       +-> IC85, IN0: 40 MHz, OUT: 320 MHz -> ZU11EG FE IBERT, MGTREFCLK0: 320 MHz
#



cd `dirname $0`
cd ..



PY_MCU_CM="./pyMcuCm.py"
SERIAL_DEVICE="/dev/ttyUL1"
VERBOSITY="0"



echo "Power up the Command Module."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c power_up

echo "Program the clock synthesizer chip IC54 (SI5341A) to generate a fixed 40 MHz clock used as source for the 240 MHz reference clock for the FELIX IBERT."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC54 config/clock/IBERT-Test/IC54_h74_FreeRun_O-40M-Registers.txt

echo "Program the clock synthesizer chip IC60 (Si5345A) for the sector logic (SL) communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC60 config/clock/IBERT-Test/IC60_h6B_IN2-40M_O-320M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC60 config/clock/IBERT-Test/IC60_h6B_IN2-40M_O-320M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC61 (Si5342A) for the neighbor exchange (CM2CM) communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC61 config/clock/IBERT-Test/IC61_h68_IN2-40M_O-320M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC61 config/clock/IBERT-Test/IC61_h68_IN2-40M_O-320M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC62 (Si5345A) for the KU15P-ZU11EG (C2C) communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC62 config/clock/IBERT-Test/IC62_h69_IN2-40M_O-320M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC62 config/clock/IBERT-Test/IC62_h69_IN2-40M_O-320M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC63 (Si5345A) for the SFP+ / legacy TTC communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC63 config/clock/IBERT-Test/IC63_h6A_IN2-40M_O-320M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC63 config/clock/IBERT-Test/IC63_h6A_IN2-40M_O-320M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC82 (Si5344A) for the FELIX communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC82 config/clock/IBERT-Test/IC82_h6A_FreeRun_O-240M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC82 config/clock/IBERT-Test/IC82_h6A_IN0-40M_O-240M_No-OOF-Registers.txt

echo "Set up the multiplexer for the recovered LHC clock to use the recovered LHC clock from the KU15P."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-clk-sel 0

echo "Program the clock synthesizer chip IC56 (Si5345A) to generate a 40 MHz LHC clock from the 120 MHz recovered clock from the FELIX IBERT on its input 3."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC56 config/clock/IBERT-Test/IC56_h68_IN3-120M_O-40M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC56 config/clock/IBERT-Test/IC56_h68_IN3-120M_O-40M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC83 (Si5342A) to generate a 40 MHz LHC clock from the 40 MHz LHC clock on its input 2."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC83 config/clock/IBERT-Test/IC83_h68_IN2-40M_O-40M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC83 config/clock/IBERT-Test/IC83_h68_IN2-40M_O-40M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC84 (Si5345A) for the front-end (FE) communication using the KU15P."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC84 config/clock/IBERT-Test/IC84_h69_IN0-40M_O-320M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC84 config/clock/IBERT-Test/IC84_h69_IN0-40M_O-320M_No-OOF-Registers.txt

echo "Program the clock synthesizer chip IC85 (Si5345A) for the front-end (FE) communication using the ZU11EG."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC85 config/clock/IBERT-Test/IC85_h6A_IN0-40M_O-320M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC85 config/clock/IBERT-Test/IC85_h6A_IN0-40M_O-320M_No-OOF-Registers.txt

