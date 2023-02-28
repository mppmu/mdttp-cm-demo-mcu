#!/bin/sh
# File: setup_fe-test.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 27 Feb 2023
# Rev.: 28 Feb 2023
#
# Simple script to set up the ATLAS MDT Trigger Processor (TP) Command Module
# demonstrator for front-end (FE) tests with an attached CSM2 prototype and the
# mezzanine cards.
#
# CAUTION: The zero delay mode (ZDM) for IC56 requires the CM demonstrator V2!
#
# Clock path on the CM demonstrator V1/V2:
#   IC81, free-running mode, OUT0: 200 MHz -> KU15P C2C MGT ref. clock (pins AK10/AK9)
#                            OUT1: 200 MHz -> ZU11EG C2C MGT ref. clock (pins R10/R9)
#   IC54, free-running mode, OUT0..9: 40 MHz
#   -> KU15P (pins AP29/AP30)
#   -> ZU11EG (pins AR13/AR12)
#   -> IC56, IN0: 40 MHz, OUT0..6: 320 MHz,
#                         OUT7: 40 MHz -> KU15P (pins AT24/AU24)
#                               alternative: 320 MHz -> KU15P
#                         OUT8: 40 MHz -> ZU11EG (pins AT25/AT26)
#                               alternative: 320 MHz -> ZU11EG
#                         OUT9: unused
#                               alternative: 40 MHz -> IN3 (zero delay mode feeback)
#                                            Only available on CM demonstrator V2!
#      -> IC83, IN2: 320 MHz, OUT0..1: 320 MHz
#         -> IC84, IN0: 320 MHz, OUT0..7: 320 MHz -> KU15P FE MGT ref. clock
#                                OUT8..9: disabled
#         -> IC85, IN0: 320 MHz, OUT0..5: 320 MHz -> ZU11EG FE MGT ref. clock
#                                OUT6..9: disabled
#



cd `dirname $0`
cd ..



PY_MCU_CM="./pyMcuCm.py"
SERIAL_DEVICE="/dev/ttyUL1"
VERBOSITY="0"



# Parse command line arguments.
usage() {
    echo "Usage: `basename $0` [-d SERIAL_DEVICE] [-v VERBOSITY]" 1>&2; exit 1;
}

while getopts ":d:v:" o; do
    case "${o}" in
        d)
            SERIAL_DEVICE=${OPTARG}
            ;;
        v)
            VERBOSITY=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done



# Power up the Command Module.
echo "Power up the Command Module."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c power_up



# ===================================================================
# SM-CM AXI Chip2Chip communication.
# ===================================================================

echo "Set up the AXI bus switches."
# Info on mux-hs-sel:
# - 0x0: Both SM B2B links 1 and 2 connected to ZU11EG.
# - 0x1: SM B2B link 1 connected to KU15P, link 2 connected to ZU11EG.
# - 0x2: SM B2B link 1 connected to ZU11EG, link 2 connected to KU15P.
# - 0x3: Both SM B2B links 1 and 2 connected to KU15P.
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-sel 0x1
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-sel 0x3
# Info on mux-hs-pd:
# - 0x0: Both SM B2B links 1 and 2 active.
# - 0x1: SM B2B link 1 inactive, link 2 active.
# - 0x2: SM B2B link 1 active, link 2 inactive.
# - 0x3: Both SM B2B links 1 and 2 inactive.
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-pd 0x0

echo "Program the clock synthesizer chip IC81 (Si5342A) for the SM-CM AXI Chip2Chip communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC81 config/clock/IC81_h6B_FreeRun_O-100M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC81 config/clock/IC81_h6B_FreeRun_O-200M-Registers.txt



# ===================================================================
# LHC clock generation and fanout.
# ===================================================================

echo "Program the clock synthesizer chip IC54 (SI5341A) to generate a fixed 40 MHz clock used as source for the 40 MHz LHC clock and the syncronous 320 MHz reference clock for the front-end."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC54 config/clock/FE-Test/IC54_h74_FreeRun_O_040_040_040_040_040_040_040_040_040_040-Registers.txt

echo "Program the clock synthesizer chip IC56 (Si5345A) for the clock generation and fanout based on the LHC clock."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC56 config/clock/FE-Test/IC56_h68_IN0-040_O_320_320_320_320_320_320_320_040_040_040-ZDM-Registers.txt
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC56  config/clock/FE-Test/IC56_h68_IN0-040_O_320_320_320_320_320_320_320_040_040_unu-Registers.txt
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC56 config/clock/FE-Test/IC56_h68_IN0-040_O_320_320_320_320_320_320_320_320_320_040-ZDM-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC56 config/clock/FE-Test/IC56_h68_IN0-040_O_320_320_320_320_320_320_320_320_320_unu-Registers.txt



# ===================================================================
# Front-end reference clock generation and fanout.
# ===================================================================

echo "Program the clock synthesizer chip IC83 (Si5342A) for the fanout of the front-end reference clock."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC83 config/clock/FE-Test/IC83_h68_IN2-320_O_320_320-Registers.txt

echo "Program the clock synthesizer chip IC84 (Si5345A) for the fanout of the KU15P front-end reference clock."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC84 config/clock/FE-Test/IC84_h69_IN0-320_O_320_320_320_320_320_320_320_320_unu_unu-Registers.txt

echo "Program the clock synthesizer chip IC84 (Si5345A) for the fanout of the ZU11EG front-end reference clock."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC85 config/clock/FE-Test/IC85_h6A_IN0-320_O_320_320_320_320_320_320_unu_unu_unu_unu-Registers.txt

