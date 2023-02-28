#!/bin/sh
# File: setup_sm-cm.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 23 Mar 2021
# Rev.: 28 Feb 2023
#
# Simple script to set up the ATLAS MDT Trigger Processor (TP) SM-CM AXI
# Chip2Chip communication.
#
# Clock path on the CM demonstrator V1/V2:
#   IC81, free-running mode, OUT0: 200 MHz -> KU15P C2C MGT ref. clock (pins AK10/AK9)
#                            OUT1: 200 MHz -> ZU11EG C2C MGT ref. clock (pins R10/R9)
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

# Info on mux-hs-sel:
# - 0x0: Both SM B2B links 1 and 2 connected to ZU11EG.
# - 0x1: SM B2B link 1 connected to KU15P, link 2 connected to ZU11EG.
# - 0x2: SM B2B link 1 connected to ZU11EG, link 2 connected to KU15P.
# - 0x3: Both SM B2B links 1 and 2 connected to KU15P.
echo "Set up the AXI bus switches."
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-sel 0x1
# Info on mux-hs-pd:
# - 0x0: Both SM B2B links 1 and 2 active.
# - 0x1: SM B2B link 1 inactive, link 2 active.
# - 0x2: SM B2B link 1 active, link 2 inactive.
# - 0x3: Both SM B2B links 1 and 2 inactive.
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c mcu_cmd_raw -p gpio mux-hs-pd 0x0

echo "Program the clock synthesizer chip IC81 (Si5342A) for the SM-CM AXI Chip2Chip communication."
#${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC81 config/clock/IC81_h6B_FreeRun_O-100M-Registers.txt
${PY_MCU_CM} -d ${SERIAL_DEVICE} -v ${VERBOSITY} -c clk_setup -p IC81 config/clock/IC81_h6B_FreeRun_O-200M-Registers.txt

