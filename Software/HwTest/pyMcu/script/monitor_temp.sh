#!/bin/sh
# File: monitor_temp.sh
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 02 Sep 2020
# Rev.: 26 Mar 2021
#
# Simple script to monitor temperatures of the ATLAS MDT Trigger Processor (TP)
# Command Module.
#



cd `dirname $0`
cd ..



while [ 1 ]; do
#    date +"%Y%m%d %H%M%S"
    date +"%d.%m.%Y %H:%M:%S"
    ./pyMcuCm.py -d "/dev/ttyUL1" -v0 -c mon_temp | grep "KU15P\|ZU11EG"
    echo
done

