#!/usr/bin/env python3
#
# File: MdtTp_CM.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 04 Aug 2020
# Rev.: 08 Sep 2020
#
# Python class for accessing the ATLAS MDT Trigger Processor (TP) Command
# Module (CM) via the TI Tiva TM4C1290 MCU UART.
#



import os
import McuGpio
import McuI2C
import McuSerial
import McuUart
import I2C_DS28CM00
import I2C_LTC2977
import I2C_MCP9808
import I2C_MCP9903
import I2C_PCA9547
import I2C_Si53xx
import I2C_TCA6424A



class MdtTp_CM:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixWarning       = "WARNING: {0:s}: ".format(__file__)
    prefixError         = "ERROR: {0:s}: ".format(__file__)
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel = 0                 # Debug verbosity.

    # Hardware parameters.
    i2cBusNum           = 10



    # Initialize the Command Module class.
    def __init__(self, serialDevice, debugLevel):
        self.mcuSer = McuSerial.McuSerial(serialDevice)
        self.debugLevel = debugLevel
        self.warningCount = 0
        self.errorCount = 0
        self.init_hw()



    # Initialize the hardware components.
    def init_hw(self):
        # Define the MCU peripherals.
        self.init_hw_i2c()



    # Initialize the I2C busses and devices.
    def init_hw_i2c(self):
        # I2C buses.
        self.mcuI2C = []
        for i in range(0, self.i2cBusNum):
            self.mcuI2C.append(McuI2C.McuI2C(self.mcuSer, i))
            self.mcuI2C[i].debugLevel = self.debugLevel
            # Reset the I2C bus.
            self.mcuI2C[i].ms_reset_bus()

        # IC114: DS28CM00 silicon serial number IC.
        # I2C port 4, slave address 0x50.
        self.i2cDevice_IC114_DS28CM00 = I2C_DS28CM00.I2C_DS28CM00(self.mcuI2C[4], 0x50, "IC114 (DS28CM00)")
        self.i2cDevice_IC114_DS28CM00.debugLevel = self.debugLevel

        # MCP9808 digital temperature sensor ICs.
        # IC34 (MCP9808): I2C port 4, slave address 0x18
        self.i2cDevice_IC34_MCP9808 = I2C_MCP9808.I2C_MCP9808(self.mcuI2C[4], 0x18, "IC34 (MCP9808)")
        self.i2cDevice_IC34_MCP9808.debugLevel = self.debugLevel
        # IC35 (MCP9808): I2C port 4, slave address 0x19
        self.i2cDevice_IC35_MCP9808 = I2C_MCP9808.I2C_MCP9808(self.mcuI2C[4], 0x19, "IC35 (MCP9808)")
        self.i2cDevice_IC35_MCP9808.debugLevel = self.debugLevel
        # IC36 (MCP9808): I2C port 4, slave address 0x1a
        self.i2cDevice_IC36_MCP9808 = I2C_MCP9808.I2C_MCP9808(self.mcuI2C[4], 0x1a, "IC36 (MCP9808)")
        self.i2cDevice_IC36_MCP9808.debugLevel = self.debugLevel
        # IC37 (MCP9808): I2C port 4, slave address 0x1b
        self.i2cDevice_IC37_MCP9808 = I2C_MCP9808.I2C_MCP9808(self.mcuI2C[4], 0x1b, "IC37 (MCP9808)")
        self.i2cDevice_IC37_MCP9808.debugLevel = self.debugLevel
        # IC38 (MCP9808): I2C port 4, slave address 0x1c
        self.i2cDevice_IC38_MCP9808 = I2C_MCP9808.I2C_MCP9808(self.mcuI2C[4], 0x1c, "IC38 (MCP9808)")
        self.i2cDevice_IC38_MCP9808.debugLevel = self.debugLevel
        # Set up the configuration registers.
        self.i2cDevice_IC34_MCP9808.write_config(0x0000)
        self.i2cDevice_IC35_MCP9808.write_config(0x0000)
        self.i2cDevice_IC36_MCP9808.write_config(0x0000)
        self.i2cDevice_IC37_MCP9808.write_config(0x0000)
        self.i2cDevice_IC38_MCP9808.write_config(0x0000)
        # Set up the resolution registers.
        self.i2cDevice_IC34_MCP9808.write_resolution(0x0003)
        self.i2cDevice_IC35_MCP9808.write_resolution(0x0003)
        self.i2cDevice_IC36_MCP9808.write_resolution(0x0003)
        self.i2cDevice_IC37_MCP9808.write_resolution(0x0003)
        self.i2cDevice_IC38_MCP9808.write_resolution(0x0003)

        # IC39: MCP9903 multi-channel low-temperature remote diode sensor IC.
        # I2C port 4, slave address 0x5c
        self.i2cDevice_IC39_MCP9903 = I2C_MCP9903.I2C_MCP9903(self.mcuI2C[4], 0x5c, "IC39 (MCP9903)")
        self.i2cDevice_IC39_MCP9903.debugLevel = self.debugLevel
        # Set up the configuration registers.
        self.i2cDevice_IC39_MCP9903.write_config_0(0x00)
        self.i2cDevice_IC39_MCP9903.write_config_1(0x00)

        # I2C mux for clock I2C bus:
        # IC55 (PCA9547PW): I2C port 3, slave address 0x70
        self.i2cDevice_IC55_PCA9547PW = I2C_PCA9547.I2C_PCA9547(self.mcuI2C[3], 0x70, "IC55 (PCA9547PW)")
        self.i2cDevice_IC55_PCA9547PW.debugLevel = self.debugLevel
        # I2C clock devices.
        # IC54 (Si5341A): I2C port 3, slave address 0x74
        self.i2cDevice_IC54_Si5341A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x74, "IC54 (Si5341A)")
        self.i2cDevice_IC54_Si5341A.muxChannel = 0
        self.i2cDevice_IC54_Si5341A.regMapFile = os.path.join("config", "clock", "IC54_h74_240M-Registers.txt")
        self.i2cDevice_IC54_Si5341A.debugLevel = self.debugLevel
        # IC56 (Si5345A): I2C port 3, slave address 0x68, I2C mux port 0
        self.i2cDevice_IC56_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x68, "IC56 (Si5345A)")
        self.i2cDevice_IC56_Si5345A.muxChannel = 0
        self.i2cDevice_IC56_Si5345A.regMapFile = os.path.join("config", "clock", "IC56_h68_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC56_Si5345A.debugLevel = self.debugLevel
        # IC60 (Si5345A): I2C port 3, slave address 0x6B, I2C mux port 0
        self.i2cDevice_IC60_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6b, "IC60 (Si5345A)")
        self.i2cDevice_IC60_Si5345A.muxChannel = 0
        self.i2cDevice_IC60_Si5345A.regMapFile = os.path.join("config", "clock", "IC60_h6B_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC60_Si5345A.debugLevel = self.debugLevel
        # IC61 (Si5342A): I2C port 3, slave address 0x68, I2C mux port 1
        self.i2cDevice_IC61_Si5342A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x68, "IC61 (Si5342A)")
        self.i2cDevice_IC61_Si5342A.muxChannel = 1
        self.i2cDevice_IC61_Si5342A.regMapFile = os.path.join("config", "clock", "IC61_h68_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC61_Si5342A.debugLevel = self.debugLevel
        # IC62 (Si5345A): I2C port 3, slave address 0x69, I2C mux port 1
        self.i2cDevice_IC62_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x69, "IC62 (Si5345A)")
        self.i2cDevice_IC62_Si5345A.muxChannel = 1
        self.i2cDevice_IC62_Si5345A.regMapFile = os.path.join("config", "clock", "IC62_h69_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC62_Si5345A.debugLevel = self.debugLevel
        # IC63 (Si5345A): I2C port 3, slave address 0x6A, I2C mux port 1
        self.i2cDevice_IC63_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6a, "IC63 (Si5345A)")
        self.i2cDevice_IC63_Si5345A.muxChannel = 1
        self.i2cDevice_IC63_Si5345A.regMapFile = os.path.join("config", "clock", "IC63_h6A_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC63_Si5345A.debugLevel = self.debugLevel
        # IC81 (Si5342A): I2C port 3, slave address 0x6B, I2C mux port 1
        self.i2cDevice_IC81_Si5342A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6b, "IC81 (Si5342A)")
        self.i2cDevice_IC81_Si5342A.muxChannel = 1
        self.i2cDevice_IC81_Si5342A.regMapFile = os.path.join("config", "clock", "IC81_h6B_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC81_Si5342A.debugLevel = self.debugLevel
        # IC82 (Si5344A): I2C port 3, slave address 0x6A, I2C mux port 0
        self.i2cDevice_IC82_Si5344A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6a, "IC82 (Si5344A)")
        self.i2cDevice_IC82_Si5344A.muxChannel = 0
        self.i2cDevice_IC82_Si5344A.regMapFile = os.path.join("config", "clock", "IC82_h6A_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC82_Si5344A.debugLevel = self.debugLevel
        # IC83 (Si5342A): I2C port 3, slave address 0x68, I2C mux port 2
        self.i2cDevice_IC83_Si5342A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x68, "IC83 (Si5342A)")
        self.i2cDevice_IC83_Si5342A.muxChannel = 2
        self.i2cDevice_IC83_Si5342A.regMapFile = os.path.join("config", "clock", "IC83_h68_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC83_Si5342A.debugLevel = self.debugLevel
        # IC84 (Si5345A): I2C port 3, slave address 0x69, I2C mux port 2
        self.i2cDevice_IC84_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x69, "IC84 (Si5345A)")
        self.i2cDevice_IC84_Si5345A.muxChannel = 2
        self.i2cDevice_IC84_Si5345A.regMapFile = os.path.join("config", "clock", "IC84_h69_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC84_Si5345A.debugLevel = self.debugLevel
        # IC85 (Si5345A): I2C port 3, slave address 0x6A, I2C mux port 2
        self.i2cDevice_IC85_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6a, "IC85 (Si5345A)")
        self.i2cDevice_IC85_Si5345A.muxChannel = 2
        self.i2cDevice_IC85_Si5345A.regMapFile = os.path.join("config", "clock", "IC85_h6A_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC85_Si5345A.debugLevel = self.debugLevel



    # Send a raw command to the MCU.
    def mcu_cmd_raw(self, cmd):
        # Debug: Show command.
        if self.debugLevel >= 2:
            print(self.prefixDebug + "Sending command to the MCU: " + cmd)
        # Send command.
        self.mcuSer.send(cmd)
        # Debug: Show response.
        if self.debugLevel >= 3:
            print(self.prefixDebug + "Response from MCU:")
            print(self.mcuSer.get_full())
        # Evaluate response.
        ret = self.mcuSer.eval()
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error sending command to the MCU!")
            if self.debugLevel >= 1:
                print(self.prefixError + "Command sent to MCU: " + cmd)
                print(self.prefixError + "Response from MCU:")
                print(self.mcuSer.get_full())
            return ret, ""
        return 0, self.mcuSer.get()



    # Print details.
    def print_details(self):
        print(self.prefixDetails, end='')
        print("Command Module on serial device `" + self.mcuSer + "'.")
        if self.debugLevel >= 1:
            print(self.separatorDetails + "Warning count: {0:d}".format(self.warningCount), end='')
            print(self.separatorDetails + "Error count: {0:d}".format(self.errorCount), end='')
        if self.debugLevel >= 1:
            print(self.separatorDetails + "Read access count: {0:d}".format(self.mcuSer.accessRead), end='')
            print(self.separatorDetails + "Write access count: {0:d}".format(self.mcuSer.accessWrite), end='')
        if self.debugLevel >= 1:
            print(self.separatorDetails + "Bytes read: {0:d}".format(self.mcuSer.bytesRead), end='')
            print(self.separatorDetails + "Bytes written: {0:d}".format(self.mcuSer.bytesWritten), end='')
        print()
        return 0



    # Power up the CM.
    def power_up(self):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Powering up the CM.")
        cmd = "power all 1"
        ret = self.mcu_cmd_raw(cmd)[0]
        if ret:
            self.errorCount += 1
            print(self.prefixError + "CM power up failed!")
        return ret



    # Power down the CM.
    def power_down(self):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Powering down the CM.")
        cmd = "power all 0"
        ret = self.mcu_cmd_raw(cmd)[0]
        if ret:
            self.errorCount += 1
            print(self.prefixError + "CM power down failed!")
        return ret



    # Read the power status of the CM.
    def power_status(self):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the power status of the CM.")
        cmd = "power clock"
        ret, powerStatusStr = self.mcu_cmd_raw(cmd)
        print(powerStatusStr)
        cmd = "power kup"
        ret, powerStatusStr = self.mcu_cmd_raw(cmd)
        print(powerStatusStr)
        cmd = "power zup"
        ret, powerStatusStr = self.mcu_cmd_raw(cmd)
        print(powerStatusStr)
        cmd = "power firefly"
        ret, powerStatusStr = self.mcu_cmd_raw(cmd)
        print(powerStatusStr)
        return ret



    # Read the serial number of the board
    def serial_number(self):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the serial number from the DS28CM00 device.")
        ret, deviceFamilyCode, serialNumber, crc, crcError = self.i2cDevice_IC114_DS28CM00.read_all()
        print("Device family code: 0x{0:02x}".format(deviceFamilyCode))
        print("Serial number: 0x{0:012x}".format(serialNumber))
        print("CRC: 0x{0:02x}".format(crc))
        if crcError:
            self.errorCount += 1
            print(self.prefixError + "CRC error detected!")



    # Monitor the temperatures.
    def mon_temp(self):
        # Power modules.
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the temperatures of the power modules via the MCU ADC.")
        cmd = "temp-a"
        ret, tempStr = self.mcu_cmd_raw(cmd)
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Reading the temperatures of the power modules via the MCU ADC failed!")
        else:
            temperatures = tempStr.split(',')
            for temp in temperatures:
                print("{0:28s}: {1:s}".format(temp.split(':')[0].strip(), temp.split(':')[-1].strip()))
        # KU15P and ZU11EG.
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the temperatures of the KU15P and the ZU11EG.")
        if self.debugLevel >= 2:
            # Read the product ID, the manufacturer ID and the revision.
            print(self.prefixDebug + "{0:s} product ID: 0x{1:02x}".format(self.i2cDevice_IC39_MCP9903.deviceName, self.i2cDevice_IC39_MCP9903.read_product_id()[1]))
            print(self.prefixDebug + "{0:s} manufacturer ID: 0x{1:02x}".format(self.i2cDevice_IC39_MCP9903.deviceName, self.i2cDevice_IC39_MCP9903.read_manufacturer_id()[1]))
            print(self.prefixDebug + "{0:s} revision: 0x{1:02x}".format(self.i2cDevice_IC39_MCP9903.deviceName, self.i2cDevice_IC39_MCP9903.read_revision()[1]))
        # Read the temperatures.
        print("KU15P  : {0:19s}: {1:6.3f} degC".format(self.i2cDevice_IC39_MCP9903.deviceName, self.i2cDevice_IC39_MCP9903.read_temp_ext_1()[1]))
        print("ZU11EG : {0:19s}: {1:6.3f} degC".format(self.i2cDevice_IC39_MCP9903.deviceName, self.i2cDevice_IC39_MCP9903.read_temp_ext_2()[1]))
        # Board temperatures.
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the temperatures from local sensors on the board.")
        print("Board 1: {0:19s}: {1:6.3f} degC".format(self.i2cDevice_IC39_MCP9903.deviceName, self.i2cDevice_IC39_MCP9903.read_temp_int()[1]))
        if self.debugLevel >= 2:
            # Read the manufacturer and device ID.
            print(self.prefixDebug + "{0:s} manufacturer ID: 0x{1:04x}".format(self.i2cDevice_IC34_MCP9808.deviceName, self.i2cDevice_IC34_MCP9808.read_manufacturer_id()[1]))
            print(self.prefixDebug + "{0:s} device ID: 0x{1:04x}".format(self.i2cDevice_IC34_MCP9808.deviceName, self.i2cDevice_IC34_MCP9808.read_device_id()[1]))
        # Read the temperatures.
        print("Board 2: {0:19s}: {1:7.4f} degC".format(self.i2cDevice_IC34_MCP9808.deviceName, self.i2cDevice_IC34_MCP9808.read_temperature()[1]))
        print("Board 3: {0:19s}: {1:7.4f} degC".format(self.i2cDevice_IC35_MCP9808.deviceName, self.i2cDevice_IC35_MCP9808.read_temperature()[1]))
        print("Board 4: {0:19s}: {1:7.4f} degC".format(self.i2cDevice_IC36_MCP9808.deviceName, self.i2cDevice_IC36_MCP9808.read_temperature()[1]))
        print("Board 5: {0:19s}: {1:7.4f} degC".format(self.i2cDevice_IC37_MCP9808.deviceName, self.i2cDevice_IC37_MCP9808.read_temperature()[1]))
        print("Board 6: {0:19s}: {1:7.4f} degC".format(self.i2cDevice_IC38_MCP9808.deviceName, self.i2cDevice_IC38_MCP9808.read_temperature()[1]))



    # Reset all I2C busses.
    def i2c_reset(self):
        for i in range(0, self.i2cBusNum):
            self.mcuI2C[i].ms_reset_bus()



    # Detect devices on all I2C busses.
    def i2c_detect_devices(self):
        print("Devices found on I2C busses:")
        for i in range(0, self.i2cBusNum):
            print("Bus {0:d}: ".format(i), end='')
            ret, devAdr = self.mcuI2C[i].ms_detect_devices()
            for adr in devAdr:
                print(" 0x{0:02x}".format(adr), end='')
            print()



    # Program a single Silicon Labs clock IC from a register map file.
    def clk_prog_device_file(self, i2cDevice):
        i2cDevice.debugLevel = self.debugLevel
        muxChannel = i2cDevice.muxChannel
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Setting I2C mux for clock chips {0:s} to channel {1:d}.".format(self.i2cDevice_IC55_PCA9547PW.deviceName, muxChannel))
        self.i2cDevice_IC55_PCA9547PW.set_channel(muxChannel)
        self.i2cDevice_IC55_PCA9547PW.debugLevel = self.debugLevel
        regMapFile = i2cDevice.regMapFile
        print("Initialitzing {0:s} on I2C port {1:d} with register map file `{2:s}'.".\
            format(i2cDevice.deviceName, i2cDevice.mcuI2C.port, regMapFile))
        i2cDevice.debugLevel = self.debugLevel
        i2cDevice.config_file(regMapFile)



    # Program all clock devices.
    def clk_prog_all(self):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Initialitzing all clock chips.")
        self.clk_prog_device_file(self.i2cDevice_IC54_Si5341A)
        self.clk_prog_device_file(self.i2cDevice_IC56_Si5345A)
        self.clk_prog_device_file(self.i2cDevice_IC60_Si5345A)
        self.clk_prog_device_file(self.i2cDevice_IC61_Si5342A)
        self.clk_prog_device_file(self.i2cDevice_IC62_Si5345A)
        self.clk_prog_device_file(self.i2cDevice_IC63_Si5345A)
        self.clk_prog_device_file(self.i2cDevice_IC81_Si5342A)
        self.clk_prog_device_file(self.i2cDevice_IC82_Si5344A)
        self.clk_prog_device_file(self.i2cDevice_IC83_Si5342A)
        self.clk_prog_device_file(self.i2cDevice_IC84_Si5345A)
        self.clk_prog_device_file(self.i2cDevice_IC85_Si5345A)

