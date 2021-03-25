#!/bin/sh
# File: monitor_power_temp.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 02 Sep 2020
# Rev.: 04 Sep 2020
#
# Simple script to monitor power and temperatures of the ATLAS MDT Trigger
# Processor (TP) Command Module.
#



cd `dirname $0`
cd ..



while [ 1 ]; do
#    date +"%Y%m%d %H%M%S"
    date +"%d.%m.%Y %H:%M:%S"
#    ipmitool -H 192.168.0.2 -P "" -t 0x92 sensor | grep "PIM400KZ Current"
    ./pyMcuCm.py -d "/dev/ttyUL1" -v0 -c mon_temp | grep "KU15P\|ZU11EG"
    echo
done

