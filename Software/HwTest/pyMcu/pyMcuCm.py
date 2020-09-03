#!/usr/bin/env python3
#
# File: pyMcuCm.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 29 May 2020
# Rev.: 03 Sep 2020
#
# Python script to access the ATLAS MDT Trigger Processor (TP) Command Module
# (CM) via the TI Tiva TM4C1290 MCU.
#



# Append hardware classes folder to Python path.
import os
import sys
sys.path.append(os.path.relpath(os.path.join(os.path.dirname(__file__), 'hw')))



# System modules.
import time



# Hardware classes.
import MdtTp_CM



# Message prefixes and separators.
prefixDebug             = "DEBUG: {0:s}: ".format(__file__)
prefixError             = "ERROR: {0:s}: ".format(__file__)



# ===================================================================
# Access the Command Module.
# ===================================================================

if __name__ == "__main__":
    # Command line arguments.
    import argparse
    parser = argparse.ArgumentParser(description='Run an automated set of MCU tests.')
    parser.add_argument('-c', '--command', action='store', type=str,
                        choices=['power_up', 'power_down', 'sn', 'init', 'mon_temp', 'status'],
                        dest='command', default='status',
                        help='Command to execute on the CM.')
    parser.add_argument('-d', '--device', action='store', type=str,
                        dest='serialDevice', default='/dev/ttyUL1',
                        help='Serial device to access the MCU.')
    parser.add_argument('-v', '--verbosity', action='store', type=int,
                        dest='verbosity', default="1", choices=range(0, 5),
                        help='Set the verbosity level. The default is 1.')
    args = parser.parse_args()

    command = args.command
    serialDevice = args.serialDevice
    verbosity = args.verbosity

    # Define the Command Module object.
    mdtTp_CM = MdtTp_CM.MdtTp_CM(serialDevice, verbosity)

    # Execute requested command.
    if not command:
        print("Please specify a command using the `-c' option.")
    elif command == "power_up":
        mdtTp_CM.power_up()
    elif command == "power_down":
        mdtTp_CM.power_down()
    elif command == "sn":
        mdtTp_CM.serial_number()
    elif command == "init":
        mdtTp_CM.power_up()
        mdtTp_CM.clk_prog_all()
    elif command == "mon_temp":
        mdtTp_CM.mon_temp()
    elif command == "status":
        print("Board Serial Number")
        print("===================")
        mdtTp_CM.serial_number()
        print()
        print("Power Status")
        print("============")
        mdtTp_CM.power_status()
        print()
        print("Temperatures")
        print("============")
        mdtTp_CM.mon_temp()
    else:
        print(prefixError + "Command `{0:s}' not supported!".format(command))

    print("\nBye-bye!")

