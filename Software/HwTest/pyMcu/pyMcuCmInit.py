#!/usr/bin/env python3
#
# File: pyMcuCmInit.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 29 May 2020
# Rev.: 30 May 2020
#
# Python script to initialize the ATLAS MDT Trigger Processor (TP) Command
# Module (CM) via the TI Tiva TM4C1290 MCU.
#



# Append hardware classes folder to Python path.
import os
import sys
sys.path.append(os.path.relpath(os.path.join(os.path.dirname(__file__), 'hw')))



# System modules.
import time



# Hardware classes.
import McuI2C
import McuSerial
import McuUart
import I2C_DS28CM00
import I2C_MCP9808
import I2C_MCP9903
import I2C_PCA9547
import I2C_Si53xx
import I2C_TCA6424A



# Message prefixes and separators.
separatorTests          = "-----"
prefixDebug             = "DEBUG: {0:s}: ".format(__file__)
prefixError             = "ERROR: {0:s}: ".format(__file__)



# Print MCU serial port info.
def mcuSerial_print_info():
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



# ===================================================================
# Switch on/off power domains.
# ===================================================================

# Power on the clocks, SPF+, expansion connector, 12 Pin header and sensors.
def power_on_misc():
    pass



# Power on the KU15P FPGA.
def power_on_kup():
    pass



# Power on the ZU11EG SoC.
def power_on_zup():
    pass



# Power on the FireFly optical transceivers.
def power_on_firefly():
    pass



# Power off the clocks, SPF+, expansion connector, 12 Pin header and sensors.
def power_off_misc():
    pass



# Power off the KU15P FPGA.
def power_off_kup():
    pass



# Power off the ZU11EG SoC.
def power_off_zup():
    pass



# Power off the FireFly optical transceivers.
def power_off_firefly():
    pass



# ===================================================================
# Initialize the clock generators.
# ===================================================================

# Initialize a clock IC with a register map file.
def init_clock_device_file(i2cDevice, muxChannel, regMapFile):
    # I2C mux for clock I2C bus:
    # IC55 (PCA9547PW): I2C port 3, slave address 0x70
    i2cDevice_IC55_PCA9547PW = I2C_PCA9547.I2C_PCA9547(mcuI2C[3], 0x70, "IC55 (PCA9547PW)")
    i2cDevice_IC55_PCA9547PW.debugLevel = verbosity

    i2cDevice.debugLevel = verbosity
    if verbosity >= 1:
        print("Setting I2C mux for clock chips {0:s} to channel {1:d}.".format(i2cDevice_IC55_PCA9547PW.deviceName, muxChannel))
    i2cDevice_IC55_PCA9547PW.set_channel(muxChannel)
    if verbosity >= 1:
        print("Initialitzing {0:s} on I2C port {1:d} with register map file '{2:s}'.".\
            format(i2cDevice.deviceName, i2cDevice.mcuI2C.port, regMapFile))
    i2cDevice.config_file(regMapFile)



# Initialize all clock ICs.
def init_clocks():
    # IC54 (Si5341A): I2C port 3, slave address 0x74
    i2cDevice_IC54_Si5341A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x74, "IC54 (Si5341A)")
    regMapFile = os.path.join("config", "clock", "IC54_h74_240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC54_Si5341A, 0, regMapFile)

    # IC56 (Si5345A): I2C port 3, slave address 0x68, I2C mux port 0
    i2cDevice_IC56_Si5345A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x68, "IC56 (Si5345A)")
    regMapFile = os.path.join("config", "clock", "IC56_h68_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC56_Si5345A, 0, regMapFile)

    # IC60 (Si5345A): I2C port 3, slave address 0x6B, I2C mux port 0
    i2cDevice_IC60_Si5345A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x6b, "IC60 (Si5345A)")
    regMapFile = os.path.join("config", "clock", "IC60_h6B_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC60_Si5345A, 0, regMapFile)

    # IC61 (Si5342A): I2C port 3, slave address 0x68, I2C mux port 1
    i2cDevice_IC61_Si5342A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x68, "IC61 (Si5342A)")
    regMapFile = os.path.join("config", "clock", "IC61_h68_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC61_Si5342A, 1, regMapFile)

    # IC62 (Si5345A): I2C port 3, slave address 0x69, I2C mux port 1
    i2cDevice_IC62_Si5345A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x69, "IC62 (Si5345A)")
    regMapFile = os.path.join("config", "clock", "IC62_h69_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC62_Si5345A, 1, regMapFile)

    # IC63 (Si5345A): I2C port 3, slave address 0x6A, I2C mux port 1
    i2cDevice_IC63_Si5345A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x6a, "IC63 (Si5345A)")
    regMapFile = os.path.join("config", "clock", "IC63_h6A_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC63_Si5345A, 1, regMapFile)

    # IC81 (Si5342A): I2C port 3, slave address 0x6B, I2C mux port 1
    i2cDevice_IC81_Si5342A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x6b, "IC81 (Si5342A)")
    regMapFile = os.path.join("config", "clock", "IC81_h6B_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC81_Si5342A, 1, regMapFile)

    # IC82 (Si5344A): I2C port 3, slave address 0x6A, I2C mux port 0
    i2cDevice_IC82_Si5344A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x6a, "IC82 (Si5344A)")
    regMapFile = os.path.join("config", "clock", "IC82_h6A_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC82_Si5344A, 0, regMapFile)

    # IC83 (Si5342A): I2C port 3, slave address 0x68, I2C mux port 2
    i2cDevice_IC83_Si5342A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x68, "IC83 (Si5342A)")
    regMapFile = os.path.join("config", "clock", "IC83_h68_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC83_Si5342A, 2, regMapFile)

    # IC84 (Si5345A): I2C port 3, slave address 0x69, I2C mux port 2
    i2cDevice_IC84_Si5345A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x69, "IC84 (Si5345A)")
    regMapFile = os.path.join("config", "clock", "IC84_h69_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC84_Si5345A, 2, regMapFile)

    # IC85 (Si5345A): I2C port 3, slave address 0x6A, I2C mux port 2
    i2cDevice_IC85_Si5345A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x6a, "IC85 (Si5345A)")
    regMapFile = os.path.join("config", "clock", "IC85_h6A_IN0-240M_O-240M-Registers.txt")
    init_clock_device_file(i2cDevice_IC85_Si5345A, 2, regMapFile)



# ===================================================================
# Initialize the Command Module.
# ===================================================================

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

    serialDevice = args.serialDevice
    verbosity = args.verbosity

    # Open the MCU serial interface.
    mcuSer = McuSerial.McuSerial(serialDevice)
    mcuSer.debugLevel = verbosity
    mcuSer.clear()

    # Define the MCU peripherals.
    # I2C buses.
    mcuI2C = []
    for i in range(0, 10):
        mcuI2C.append(McuI2C.McuI2C(mcuSer, i))
        mcuI2C[i].debugLevel = verbosity

    # Initialize the hardware test.
    power_on_misc()
    power_on_kup()
    power_on_zup()
    power_on_firefly()
    init_clocks()

    # Print MCU serial port info.
    if verbosity >= 1:
        print("MCU serial port '{0:s}' info:".format(mcuSer.ser.port))
        mcuSerial_print_info()

    print("\nBye-bye!")

