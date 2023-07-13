#!/usr/bin/env python3
#
# File: pyMcuCm.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 29 May 2020
# Rev.: 14 Feb 2023
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
                        choices=['power_up', 'power_down', 'power_detail', 'sn', 'init', 'status', 'mon_temp',
                                 'mcu_cmd_raw',
                                 'i2c_reset', 'i2c_detect',
                                 'pm_status', 'pm_status_raw',
                                 'clk_setup',
                                 'firefly_temp', 'firefly_temp_time', 'firefly_status', 'clk_status_regs'],
                        dest='command', default='status',
                        help='Command to execute on the CM.')
    parser.add_argument('-d', '--device', action='store', type=str,
                        dest='serialDevice', default='/dev/ttyUL1', metavar='SERIAL_DEVICE',
                        help='Serial device to access the MCU.')
    parser.add_argument('-p', '--parameters', action='store', type=str, nargs='*',
                        dest='commandParameters', default=None, metavar='PARAMETER',
                        help='Parameter(s) for the selected command.')
    parser.add_argument('-v', '--verbosity', action='store', type=int,
                        dest='verbosity', default="1", choices=range(0, 5),
                        help='Set the verbosity level. The default is 1.')
    args = parser.parse_args()

    command = args.command
    commandParameters = args.commandParameters
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
    elif command == "power_detail":
        mdtTp_CM.power_status_detail()
    elif command == "sn":
        mdtTp_CM.serial_number()
    elif command == "init":
        mdtTp_CM.power_up()
        mdtTp_CM.init_hw()
        mdtTp_CM.clk_prog_all()
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
    elif command == "mon_temp":
        mdtTp_CM.mon_temp()
    elif command == "mcu_cmd_raw":
        if commandParameters:
            ret, response = mdtTp_CM.mcu_cmd_raw(" ".join(commandParameters))
            print(response)
        else:
            print(prefixError, "Please specify the raw MCU command.")
    elif command == "i2c_reset":
        mdtTp_CM.i2c_reset()
    elif command == "i2c_detect":
        mdtTp_CM.i2c_detect_devices()
    elif command == "pm_status":
        mdtTp_CM.power_module_status()
    elif command == "pm_status_raw":
        mdtTp_CM.power_module_status_raw()
    elif command == "clk_setup":
        if commandParameters:
            if len(commandParameters) != 2:
                print(prefixError, "Please specify the clock IC number and the register map file.")
                print(prefixError, "E.g.: -p IC54 config/clock/IC54_h74_240M-Registers.txt")
            else:
                mdtTp_CM.clk_prog_device_by_name(commandParameters[0], commandParameters[1])
        else:
            mdtTp_CM.clk_prog_all()
    elif command == "firefly_temp":
        mdtTp_CM.firefly_temp()
    elif command == "firefly_temp_time":
        if commandParameters:
            mdtTp_CM.firefly_time_at_temperature(int(commandParameters[0]))
        else:
            for i in range(1, mdtTp_CM.fireFlyNum + 1):
                mdtTp_CM.firefly_time_at_temperature(i)
                print()
    elif command == "firefly_status":
        if commandParameters:
            mdtTp_CM.firefly_status(int(commandParameters[0]))
        else:
            for i in range(1, mdtTp_CM.fireFlyNum + 1):
                mdtTp_CM.firefly_status(i)
                print()
    elif command == "clk_status_regs":
        mdtTp_CM.clk_print_status_all()    
    else:
        print(prefixError + "Command `{0:s}' not supported!".format(command))

    print("\nBye-bye!")

