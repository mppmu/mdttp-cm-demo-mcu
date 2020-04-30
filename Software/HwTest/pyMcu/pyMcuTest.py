#!/usr/bin/env python3
#
# File: pyMcuTest.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 30 Apr 2020
# Rev.: 30 Apr 2020
#
# Python script to test hardware features of the TI Tiva TM4C1290 MCU on the
# ATLAS MDT Trigger Processor (TP) Command Module (CM) over a serial port
# (UART).
#



# Append hardware classes folder to python path.
import os
import sys
thisFilePath = os.path.dirname(__file__)
if thisFilePath:
    thisFilePath += '/'
sys.path.append(thisFilePath + 'hw')



# System modules.
import time



# Hardware classes.
import McuI2C
import McuSerial
import McuUart
import I2C_PCA9547
import I2C_Si53xx



# Select tests to run.
separatorTests        = "-----"
# Preset all to fales.
testFwInfo              = False
testMcuSerial_0         = False
testI2C                 = False
testI2C_IC55_PCA9547PW  = False
testI2C_IC54_Si5341     = False
testMcuSerial_1         = False
# Set the tests to true that you want to run.
testFwInfo              = True
testMcuSerial_0         = True
testI2C                 = True
testI2C_IC55_PCA9547PW  = True
testI2C_IC54_Si5341     = True
testMcuSerial_1         = True



# Print MCU serial port info.
def mcuSerial_print_info(mcuSer):
    mcuSerPrefixDetailsBak = mcuSer.prefixDetails
    mcuSerSeparatorDetailsBak = mcuSer.separatorDetails
    mcuSerdebugLevelBak = mcuSer.debugLevel
    mcuSer.prefixDetails = ""
    mcuSer.separatorDetails = "\n"
    mcuSer.debugLevel = 1
    mcuSer.print_details()
    mcuSer.prefixDetails = mcuSerPrefixDetailsBak
    mcuSer.separatorDetails = mcuSerSeparatorDetailsBak
    mcuSer.debugLevel = mcuSerdebugLevelBak



# Run the hardware test.
def run_test(serialDevice, verbosity):
    # Open the MCU serial interface.
    mcuSer = McuSerial.McuSerial(serialDevice)
    mcuSer.debugLevel = verbosity
    mcuSer.clear()



    # Define the MCU peripherals.
    # I2C busses.
    mcuI2C = []
    for i in range(0, 10):
        mcuI2C.append(McuI2C.McuI2C(mcuSer, i))
        mcuI2C[i].debugLevel = verbosity
    # IC55 (PCA9547PW): I2C port 3, slave address 0x70
    i2cDevice_IC55_PCA9547PW = I2C_PCA9547.I2C_PCA9547(mcuI2C[3], 0x70, "IC55 (PCA9547PW)")
    # IC54 (Si5341A): I2C port 3, slave address 0x74
    i2cDevice_IC54_Si5341A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x74, "IC54 (Si5341A)")



    # Read the MCU info.
    if testFwInfo:
        print("MCU firmware info:")
        mcuSer.send("info")
        print(mcuSer.get())
        print(separatorTests)



    # Read the MCU serial port info.
    if testMcuSerial_0:
        print("MCU serial port {0:s} info:".format(mcuSer.ser.port))
        mcuSerial_print_info(mcuSer)
        print(separatorTests)



    # I2C test.
    if testI2C:
        print("I2C master port {0:d} test.".format(mcuI2C[3].port))
        # Standard access.
        mcuI2C[3].ms_write(0x70, [0x01, 0x02, 0x03])
        ret, data = mcuI2C[3].ms_read(0x70, 1)
        print("I2C data read:", end='')
        for datum in data:
            print(" 0x{0:02x}".format(datum), end='')
        print()
        # Advanced access.
        mcuI2C[3].ms_write_adv(0x70, [0x01], False, False)      # No repeated start, no stop condition.
        ret, data = mcuI2C[3].ms_read_adv(0x70, 1, True, True)  # Repeated start, stop condition.
        print("I2C data read:", end='')
        for datum in data:
            print(" 0x{0:02x}".format(datum), end='')
        print()
        print(separatorTests)



    # I2C test the IC55 (PCA9547PW).
    if testI2C_IC55_PCA9547PW:
        print("I2C test of IC55 (PCA9547PW) on I2C port {0:d}.".format(i2cDevice_IC55_PCA9547PW.mcuI2C.port))
        i2cDevice_IC55_PCA9547PW.set_channel(0)
        print("Active multiplexer channel: {0:d}".format(i2cDevice_IC55_PCA9547PW.get_channel()[1]))
        i2cDevice_IC55_PCA9547PW.set_channel(1)
        print("Active multiplexer channel: {0:d}".format(i2cDevice_IC55_PCA9547PW.get_channel()[1]))
        i2cDevice_IC55_PCA9547PW.disable()
        print("Active multiplexer channel: {0:d}".format(i2cDevice_IC55_PCA9547PW.get_channel()[1]))
        i2cDevice_IC55_PCA9547PW.set_channel(0)
        print(separatorTests)



    # I2C test of IC54 (Si5341A).
    if testI2C_IC54_Si5341:
        print("I2C test of IC54 (Si5341A) on I2C port {0:d}.".format(i2cDevice_IC54_Si5341A.mcuI2C.port))
        i2cDevice_IC54_Si5341A.config_file("config/IC54_RegMap.txt")
        print(separatorTests)



    # Read the MCU serial port info.
    if testMcuSerial_1:
        print("MCU serial port {0:s} info:".format(mcuSer.ser.port))
        mcuSerial_print_info(mcuSer)
        print(separatorTests)



# Execute the test.
if __name__ == "__main__":
    # Command line arguments.
    import argparse
    parser = argparse.ArgumentParser(description='Run an automated set of MCU tests.')
    parser.add_argument('-d', '--device', action='store', type=str,
                        dest='serialDevice', default='/dev/ttyUSB0',
                        help='Serial device to access the MCU.')
    parser.add_argument('-v', '--verbosity', action='store', type=int,
                        dest='verbosity', default="1", choices=range(0, 5),
                        help='Set the verbosity level. The default is 1.')
    args = parser.parse_args()

    # Run the hardware test.
    run_test(args.serialDevice, args.verbosity)

    print("\nBye-bye!")

