#!/usr/bin/env python3
#
# File: mcu_fw_update.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 26 Oct 2022
# Rev.: 27 Oct 2022
#
# Python script to automatically update the firmware of the ATLAS MDT Trigger
# Processor (TP) Command Module (CM) MCU from the SM SoM Zynq via the CM MCU
# bootloader.
#

import os
import serial
import sys
import time



# Auxiliary tools:
BUTool_exe_default = '/opt/BUTool/bin/BUTool.exe'
BUTool_arguments = '-a /opt/address_tables/connections.xml'
BUTool_cmd = 'write CM.CM1.CTRL.ENABLE_UC 0 \\\\n write CM.CM1.CTRL.ENABLE_UC 1 \\\\n exit'
BUTool_environment = 'export BUTOOL_AUTOLOAD_LIBRARY_LIST=":/opt/BUTool/lib/libBUTool_GenericIPBusDevice.so:/opt/BUTool/lib/libBUTool_GenericIPBusDevice.so:/opt/BUTool/lib/libBUTool_ApolloSMDevice.so"'
sflash_exe_default = '../../TivaWare/SW-TM4C-2.2.0.295/tools/sflash/sflash'
sflash_arguments = '-p 0x4000 -b 115200 -d -s 252'



# Message prefixes and separators.
prefixDebug = "DEBUG: "
prefixError = "ERROR: "



# Get command line arguments.
import argparse
parser = argparse.ArgumentParser(description='Update the firmware of the CM MCU from the SM SoM Zynq.')
parser.add_argument('-a', '--BUTool_args', action='store', type=str,
                    dest='BUTool_arguments', default=BUTool_arguments, metavar='BUTOOL_ARGS',
                    help='Arguments for the BUTool.')
parser.add_argument('-b', '--BUTool', action='store', type=str,
                    dest='BUTool_exe', default=BUTool_exe_default, metavar='BUTOOL',
                    help='BUTool used to invoke the CM MCU bootloader.')
parser.add_argument('-d', '--device', action='store', type=str,
                    dest='serialDevice', default='/dev/ttyUL1', metavar='SERIAL_DEVICE',
                    help='Serial device to access the CM MCU.')
parser.add_argument('-e', '--BUTool_env', action='store', type=str,
                    dest='BUTool_environment', default=BUTool_environment, metavar='BUTOOL_ENV',
                    help='Environment for the BUTool.')
parser.add_argument('-f', '--firmware', action='store', type=str,
                    dest='mcuFirmwareFile', default=None, metavar='FIRMWARE_FILE',
                    help='CM MCU firmware binary file.')
parser.add_argument('-s', '--sflash', action='store', type=str,
                    dest='sflash_exe', default=sflash_exe_default, metavar='SFLASH',
                    help='TI sflash tool to download the firmware via the CM MCU bootloader.')
parser.add_argument('-v', '--verbosity', action='store', type=int,
                    dest='verbosity', default="1", choices=range(0, 3),
                    help='Set the verbosity level. The default is 1.')
args = parser.parse_args()

BUTool_arguments = args.BUTool_arguments
BUTool_exe = args.BUTool_exe
BUTool_environment = args.BUTool_environment
serialDevice = args.serialDevice
mcuFirmwareFile = args.mcuFirmwareFile
sflash_exe = args.sflash_exe
if sflash_exe == sflash_exe_default:
    sflash_exe = os.path.join(os.path.dirname(sys.argv[0]), sflash_exe)
verbosity = args.verbosity



# Check if a CM MCU firmware file was specified.
if not mcuFirmwareFile:
    print(prefixError + "Please specify an CM MCU firmware file.")
    sys.exit(1)
# Check if the CM MCU firmware file exists.
if not os.path.exists(mcuFirmwareFile):
    print(prefixError + "The file `" + mcuFirmwareFile + "' does not exist!")
    sys.exit(2)
# Check if the CM MCU firmware file is readable.
if not os.access(mcuFirmwareFile, os.R_OK):
    print(prefixError + "The file `" + mcuFirmwareFile + "' is not readable!")
    sys.exit(3)
# Check if the CM MCU firmware file is a file.
if not os.path.isfile(mcuFirmwareFile):
    print(prefixError + "`" + mcuFirmwareFile + "' is not a file!")
    sys.exit(4)

# Check if the BUTool is an executable.
if not os.path.isfile(BUTool_exe) or not os.access(BUTool_exe, os.X_OK):
    print(prefixError + "`" + BUTool_exe + "' is not an executable!")
    sys.exit(5)

# Check if the sflash is an executable.
if not os.path.isfile(sflash_exe) or not os.access(sflash_exe, os.X_OK):
    print(prefixError + "`" + sflash_exe + "' is not an executable!")
    sys.exit(6)



# Open the serial port for communicating with the CM MCU.
if verbosity >= 2:
    print("Opening the serial device `" + serialDevice + "'.")
try:
    serMcu = serial.Serial(serialDevice, baudrate=115200, timeout=0.5, exclusive=True)
except:
    print(prefixError + "Cannot open the serial device `" + serialDevice + "'!")
    sys.exit(7)



# Print warning message.
print()
print("WARNING: MAKE SURE THAT NO OTHER PROGRAM IS USING `" + serialDevice + "' DURING THE FIRMWARE UPDATE!")
print()
print("CAUTION: Flashing the CM MCU firmware does interrupt the operation of the Command Module!")
print("         The Command Module FPGA, FireFly modules and clock chips will be powered off!")
print()
while True:
    print("         Do you want to continue (yes/no)? ", end='')
    choice = input().lower()
    if choice == 'yes':
        break
    if choice == 'n' or choice == 'no' or choice == '':
        print()
        print("CM MCU firmware update aborted!")
        sys.exit(8)



# Reset the CM MCU via the BUTool.
if verbosity >= 1:
    print("Resetting the CM MCU via BUTool.")
cmd = BUTool_environment + "; echo -ne " + BUTool_cmd+ " | " + BUTool_exe + " " + BUTool_arguments
if verbosity >= 2:
    print("Executing the command:")
    print(cmd)
if verbosity == 0:
    cmd += ' > /dev/null'
ret = os.system(cmd)
ret = (ret >> 8) & 0xff     # The bits bits 15..8 reflect the exit code of the system call.
if ret != 0:
    print(prefixError + "A problem occured while resetting the CM MCU! BUTool returned {0:d}.".format(ret))
    sys.exit(9)



# Wait for the CM MCU bootloader to become active.
if verbosity >= 1:
    print("Waiting for the CM MCU bootloader...")
time.sleep(0.5)
while True:
    strMcu = str(serMcu.read_all())
    if "MDT-TP CM MCU boot loader" in strMcu:
        break
time.sleep(0.5)



# Enter the CM MCU bootloader.
if verbosity >= 1:
    print("Entering the CM MCU bootloader.")
serMcu.write(b" ")  # This enters the bootloader menu.
time.sleep(0.5)
serMcu.write(b"f")  # This starts the firmware download.
time.sleep(0.5)
# Read all remaining characters from the serial device buffer.
strMcu = str(serMcu.read_all())
if verbosity >= 2:
    print(prefixDebug + "Characters received from CM MCU bootloader:")
    print(strMcu)



# Close the serial port for communicating with the CM MCU.
if verbosity >= 2:
    print("Closing the serial device `" + serialDevice + "'.")
serMcu.close()
time.sleep(0.5)



# For some unknown reason, pySerial spoils the serial device so that sflash
# will fail. This can be fixed with the stty command.
if verbosity >= 1:
    print("Set up the serial device `" + serialDevice + "' for the use with the sflash tool.")
cmd = "stty -F /dev/ttyUL1 sane"
if verbosity >= 2:
    print("Executing the command:")
    print(cmd)
if verbosity == 0:
    cmd += ' > /dev/null'
ret = os.system(cmd)
ret = (ret >> 8) & 0xff     # The bits bits 15..8 reflect the exit code of the system call.
if ret != 0:
    print(prefixError + "A problem occured while setting up the serial device! The stty tool returned {0:d}.".format(ret))
    sys.exit(10)



# Download the CM MCU firmware using the sflash untility.
if verbosity >= 1:
    print("Downloading the CM MCU firmare `" + mcuFirmwareFile +  "' over the serial device `" + serialDevice + "'.")
cmd = sflash_exe + " -c " + serialDevice + " " + sflash_arguments + " " + mcuFirmwareFile
if verbosity >= 2:
    print("Executing the command:")
    print(cmd)
if verbosity == 0:
    cmd += ' > /dev/null'
ret = os.system(cmd)
ret = (ret >> 8) & 0xff     # The bits bits 15..8 reflect the exit code of the system call.
if ret != 0:
    print(prefixError + "A problem occured while flashing the CM MCU firmware! The sflash tool returned {0:d}.".format(ret))
    sys.exit(11)

