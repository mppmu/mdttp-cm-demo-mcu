#!/usr/bin/env python3
#
# File: pyMcuTest.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 30 Apr 2020
# Rev.: 05 May 2020
#
# Python script to test hardware features of the TI Tiva TM4C1290 MCU on the
# ATLAS MDT Trigger Processor (TP) Command Module (CM) over a serial port
# (UART).
#



# Append hardware classes folder to Python path.
import os
import sys
sys.path.append(os.path.relpath(os.path.dirname(__file__) + '/hw'))



# System modules.
import time



# Hardware classes.
import McuI2C
import McuSerial
import McuUart
import I2C_MCP9808
import I2C_MCP9903
import I2C_PCA9547
import I2C_Si53xx
import I2C_TCA6424A



# Select tests to run.
separatorTests        = "-----"
# Preset all to fales.
testFwInfo              = False
testMcuSerial_0         = False
testI2C                 = False
testI2C_IC55_PCA9547PW  = False
testI2C_IC54_Si5341     = False
testI2C_TCA6424A        = False
testI2C_MCP9808         = False
testI2C_IC39_MCP9903    = False
testMcuSerial_1         = False
# Set the tests to true that you want to run.
testFwInfo              = True
testMcuSerial_0         = True
testI2C                 = True
testI2C_IC55_PCA9547PW  = True
testI2C_IC54_Si5341     = True
testI2C_TCA6424A        = True
testI2C_MCP9808         = True
testI2C_IC39_MCP9903    = True
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



    # I2C test of IC55 (PCA9547PW, I2C multiplexer).
    if testI2C_IC55_PCA9547PW:
        # IC55 (PCA9547PW): I2C port 3, slave address 0x70
        i2cDevice_IC55_PCA9547PW = I2C_PCA9547.I2C_PCA9547(mcuI2C[3], 0x70, "IC55 (PCA9547PW)")
        i2cDevice_IC55_PCA9547PW.debugLevel = verbosity
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
        # IC54 (Si5341A): I2C port 3, slave address 0x74
        i2cDevice_IC54_Si5341A = I2C_Si53xx.I2C_Si53xx(mcuI2C[3], 0x74, "IC54 (Si5341A)")
        i2cDevice_IC54_Si5341A.debugLevel = verbosity
        print("I2C test of IC54 (Si5341A) on I2C port {0:d}.".format(i2cDevice_IC54_Si5341A.mcuI2C.port))
        i2cDevice_IC54_Si5341A.config_file("config/IC54_RegMap.txt")
        print(separatorTests)



    # I2C test of all TCA6424A I/O expander ICs (IC104..IC107).
    if testI2C_TCA6424A:
        # IC104 (TCA6424A): I2C port 9, slave address 0x22
        i2cDevice_IC104_TCA6424A = I2C_TCA6424A.I2C_TCA6424A(mcuI2C[9], 0x22, "IC104 (TCA6424A)")
        i2cDevice_IC104_TCA6424A.debugLevel = verbosity
        # IC105 (TCA6424A): I2C port 9, slave address 0x23
        i2cDevice_IC105_TCA6424A = I2C_TCA6424A.I2C_TCA6424A(mcuI2C[9], 0x23, "IC105 (TCA6424A)")
        i2cDevice_IC105_TCA6424A.debugLevel = verbosity
        # IC106 (TCA6424A): I2C port 8, slave address 0x22
        i2cDevice_IC106_TCA6424A = I2C_TCA6424A.I2C_TCA6424A(mcuI2C[8], 0x22, "IC106 (TCA6424A)")
        i2cDevice_IC106_TCA6424A.debugLevel = verbosity
        # IC107 (TCA6424A): I2C port 8, slave address 0x23
        i2cDevice_IC107_TCA6424A = I2C_TCA6424A.I2C_TCA6424A(mcuI2C[8], 0x23, "IC107 (TCA6424A)")
        i2cDevice_IC107_TCA6424A.debugLevel = verbosity
        # Configure all ports as inputs.
        i2cDevice_IC104_TCA6424A.write_config(0xffffff)
        i2cDevice_IC105_TCA6424A.write_config(0xffffff)
        i2cDevice_IC106_TCA6424A.write_config(0xffffff)
        i2cDevice_IC107_TCA6424A.write_config(0xffffff)
        # Read the logic levels of all ports.
        print("IC104 (TCA6424A) logic levels: 0x{0:06x}".format(i2cDevice_IC104_TCA6424A.read_input()[1]))
        print("IC105 (TCA6424A) logic levels: 0x{0:06x}".format(i2cDevice_IC105_TCA6424A.read_input()[1]))
        print("IC106 (TCA6424A) logic levels: 0x{0:06x}".format(i2cDevice_IC106_TCA6424A.read_input()[1]))
        print("IC107 (TCA6424A) logic levels: 0x{0:06x}".format(i2cDevice_IC107_TCA6424A.read_input()[1]))



    # I2C test of all MCP9808 digital temperature sensor ICs.
    if testI2C_MCP9808:
        # IC34 (MCP9808): I2C port 4, slave address 0x18
        i2cDevice_IC34_MCP9808 = I2C_MCP9808.I2C_MCP9808(mcuI2C[4], 0x18, "IC34 (MCP9808)")
        i2cDevice_IC34_MCP9808.debugLevel = verbosity
        # IC35 (MCP9808): I2C port 4, slave address 0x19
        i2cDevice_IC35_MCP9808 = I2C_MCP9808.I2C_MCP9808(mcuI2C[4], 0x19, "IC35 (MCP9808)")
        i2cDevice_IC35_MCP9808.debugLevel = verbosity
        # IC36 (MCP9808): I2C port 4, slave address 0x1a
        i2cDevice_IC36_MCP9808 = I2C_MCP9808.I2C_MCP9808(mcuI2C[4], 0x1a, "IC36 (MCP9808)")
        i2cDevice_IC36_MCP9808.debugLevel = verbosity
        # IC37 (MCP9808): I2C port 4, slave address 0x1b
        i2cDevice_IC37_MCP9808 = I2C_MCP9808.I2C_MCP9808(mcuI2C[4], 0x1b, "IC37 (MCP9808)")
        i2cDevice_IC37_MCP9808.debugLevel = verbosity
        # IC38 (MCP9808): I2C port 4, slave address 0x1c
        i2cDevice_IC38_MCP9808 = I2C_MCP9808.I2C_MCP9808(mcuI2C[4], 0x1c, "IC38 (MCP9808)")
        i2cDevice_IC38_MCP9808.debugLevel = verbosity
        # Set up the configuration registers.
        i2cDevice_IC34_MCP9808.write_config(0x0000)
        i2cDevice_IC35_MCP9808.write_config(0x0000)
        i2cDevice_IC36_MCP9808.write_config(0x0000)
        i2cDevice_IC37_MCP9808.write_config(0x0000)
        i2cDevice_IC38_MCP9808.write_config(0x0000)
        # Set up the resolution registers.
        i2cDevice_IC34_MCP9808.write_resolution(0x0003)
        i2cDevice_IC35_MCP9808.write_resolution(0x0003)
        i2cDevice_IC36_MCP9808.write_resolution(0x0003)
        i2cDevice_IC37_MCP9808.write_resolution(0x0003)
        i2cDevice_IC38_MCP9808.write_resolution(0x0003)
        # Read the manufacturer and device ID.
        print("IC34 (MCP9808) manufacturer ID: 0x{0:04x}".format(i2cDevice_IC34_MCP9808.read_manufacturer_id()[1]))
        print("IC34 (MCP9808) device ID: 0x{0:04x}".format(i2cDevice_IC34_MCP9808.read_device_id()[1]))
        # Read the temperatures.
        print("IC34 (MCP9808) temperature: {0:8.4f} degC".format(i2cDevice_IC34_MCP9808.read_temperature()[1]))
        print("IC35 (MCP9808) temperature: {0:8.4f} degC".format(i2cDevice_IC35_MCP9808.read_temperature()[1]))
        print("IC36 (MCP9808) temperature: {0:8.4f} degC".format(i2cDevice_IC36_MCP9808.read_temperature()[1]))
        print("IC37 (MCP9808) temperature: {0:8.4f} degC".format(i2cDevice_IC37_MCP9808.read_temperature()[1]))
        print("IC38 (MCP9808) temperature: {0:8.4f} degC".format(i2cDevice_IC38_MCP9808.read_temperature()[1]))



    # I2C test of IC39, MCP9903 multi-channel low-temperature remote diode sensor IC.
    if testI2C_IC39_MCP9903:
        # IC39 (MCP9903): I2C port 4, slave address 0x5c
        i2cDevice_IC39_MCP9903 = I2C_MCP9903.I2C_MCP9903(mcuI2C[4], 0x5c, "IC39 (MCP9903)")
        i2cDevice_IC39_MCP9903.debugLevel = verbosity
        # Set up the configuration registers.
        i2cDevice_IC39_MCP9903.write_config_0(0x00)
        i2cDevice_IC39_MCP9903.write_config_1(0x00)
        # Read the product ID, the manufacturer ID and the revision.
        print("IC39 (MCP9903) product ID: 0x{0:02x}".format(i2cDevice_IC39_MCP9903.read_product_id()[1]))
        print("IC39 (MCP9903) manufacturer ID: 0x{0:02x}".format(i2cDevice_IC39_MCP9903.read_manufacturer_id()[1]))
        print("IC39 (MCP9903) revision: 0x{0:02x}".format(i2cDevice_IC39_MCP9903.read_revision()[1]))
        # Read the temperatures.
        print("IC39 (MCP9903) internal diode temperature: {0:7.3f} degC".format(i2cDevice_IC39_MCP9903.read_temp_int()[1]))
        print("IC39 (MCP9903) external diode 1 temperature: {0:7.3f} degC".format(i2cDevice_IC39_MCP9903.read_temp_ext_1()[1]))
        print("IC39 (MCP9903) external diode 2 temperature: {0:7.3f} degC".format(i2cDevice_IC39_MCP9903.read_temp_ext_2()[1]))



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

