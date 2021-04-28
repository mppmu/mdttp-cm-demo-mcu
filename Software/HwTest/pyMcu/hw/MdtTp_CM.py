#!/usr/bin/env python3
#
# File: MdtTp_CM.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 04 Aug 2020
# Rev.: 28 Apr 2021
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
import I2C_LTM4700
import I2C_MCP9808
import I2C_MCP9903
import I2C_PCA9547
import I2C_Si53xx
import I2C_TCA6424A
import I2C_FireFly



class MdtTp_CM:

    # Message prefixes and separators.
    prefixStatus        = " - "
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixWarning       = "WARNING: {0:s}: ".format(__file__)
    prefixError         = "ERROR: {0:s}: ".format(__file__)
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel = 0                 # Debug verbosity.

    # Hardware parameters.
    i2cBusNum           = 10
    fireFlyNum          = 8



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




    # ===============================================================
    # Basic monitoring and control functions.
    # ===============================================================

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
        # FireFly temperatures.



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



    # ===============================================================
    # I2C bus.
    # ===============================================================

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

        # Power modules.
        # IC26: LTC2977 8-channel PMBus power system manager IC (KU15P).
        self.i2cDevice_IC26_LTC2977 = I2C_LTC2977.I2C_LTC2977(self.mcuI2C[1], 0x5c, "IC26 (LTC2977)")
        # IC27: LTC2977 8-channel PMBus power system manager IC (KU15P).
        self.i2cDevice_IC27_LTC2977 = I2C_LTC2977.I2C_LTC2977(self.mcuI2C[1], 0x5d, "IC27 (LTC2977)")
        # IC49: LTC2977 8-channel PMBus power system manager IC (ZU11EG).
        self.i2cDevice_IC49_LTC2977 = I2C_LTC2977.I2C_LTC2977(self.mcuI2C[0], 0x5e, "IC49 (LTC2977)")
        # IC50: LTC2977 8-channel PMBus power system manager IC (ZU11EG).
        self.i2cDevice_IC50_LTC2977 = I2C_LTC2977.I2C_LTC2977(self.mcuI2C[0], 0x5f, "IC50 (LTC2977)")
        # IC51: LTC2977 8-channel PMBus power system manager IC (ZU11EG).
        self.i2cDevice_IC51_LTC2977 = I2C_LTC2977.I2C_LTC2977(self.mcuI2C[0], 0x60, "IC51 (LTC2977)")
        # IC52: LTC2977 8-channel PMBus power system manager IC (clock).
        self.i2cDevice_IC52_LTC2977 = I2C_LTC2977.I2C_LTC2977(self.mcuI2C[3], 0x61, "IC52 (LTC2977)")
        # IC76: LTM4700 regulator with digital power system management IC (KU15P core voltage).
        self.i2cDevice_IC76_LTM4700 = I2C_LTM4700.I2C_LTM4700(self.mcuI2C[1], 0x40, "IC76 (LTM4700)")
        # IC77: LTM4700 regulator with digital power system management IC (KU15P core voltage).
        self.i2cDevice_IC77_LTM4700 = I2C_LTM4700.I2C_LTM4700(self.mcuI2C[1], 0x41, "IC77 (LTM4700)")
        # IC78: LTM4700 regulator with digital power system management IC (ZU11EG core voltage).
        self.i2cDevice_IC78_LTM4700 = I2C_LTM4700.I2C_LTM4700(self.mcuI2C[0], 0x42, "IC78 (LTM4700)")
        # IC79: LTM4700 regulator with digital power system management IC (ZU11EG core voltage).
        self.i2cDevice_IC79_LTM4700 = I2C_LTM4700.I2C_LTM4700(self.mcuI2C[0], 0x43, "IC79 (LTM4700)")
        # Set write protection for all power ICs.
        self.i2cDevice_IC26_LTC2977.wp_level_1()
        self.i2cDevice_IC27_LTC2977.wp_level_1()
        self.i2cDevice_IC49_LTC2977.wp_level_1()
        self.i2cDevice_IC50_LTC2977.wp_level_1()
        self.i2cDevice_IC51_LTC2977.wp_level_1()
        self.i2cDevice_IC52_LTC2977.wp_level_1()
        self.i2cDevice_IC76_LTM4700.wp_level_1()
        self.i2cDevice_IC77_LTM4700.wp_level_1()
        self.i2cDevice_IC78_LTM4700.wp_level_1()
        self.i2cDevice_IC79_LTM4700.wp_level_1()

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
        # IC56 (Si5345A): I2C port 3, slave address 0x68, clock I2C mux port 0
        self.i2cDevice_IC56_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x68, "IC56 (Si5345A)")
        self.i2cDevice_IC56_Si5345A.muxChannel = 0
        self.i2cDevice_IC56_Si5345A.regMapFile = os.path.join("config", "clock", "IC56_h68_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC56_Si5345A.debugLevel = self.debugLevel
        # IC60 (Si5345A): I2C port 3, slave address 0x6B, clock I2C mux port 0
        self.i2cDevice_IC60_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6b, "IC60 (Si5345A)")
        self.i2cDevice_IC60_Si5345A.muxChannel = 0
        self.i2cDevice_IC60_Si5345A.regMapFile = os.path.join("config", "clock", "IC60_h6B_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC60_Si5345A.debugLevel = self.debugLevel
        # IC61 (Si5342A): I2C port 3, slave address 0x68, clock I2C mux port 1
        self.i2cDevice_IC61_Si5342A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x68, "IC61 (Si5342A)")
        self.i2cDevice_IC61_Si5342A.muxChannel = 1
        self.i2cDevice_IC61_Si5342A.regMapFile = os.path.join("config", "clock", "IC61_h68_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC61_Si5342A.debugLevel = self.debugLevel
        # IC62 (Si5345A): I2C port 3, slave address 0x69, clock I2C mux port 1
        self.i2cDevice_IC62_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x69, "IC62 (Si5345A)")
        self.i2cDevice_IC62_Si5345A.muxChannel = 1
        self.i2cDevice_IC62_Si5345A.regMapFile = os.path.join("config", "clock", "IC62_h69_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC62_Si5345A.debugLevel = self.debugLevel
        # IC63 (Si5345A): I2C port 3, slave address 0x6A, clock I2C mux port 1
        self.i2cDevice_IC63_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6a, "IC63 (Si5345A)")
        self.i2cDevice_IC63_Si5345A.muxChannel = 1
        self.i2cDevice_IC63_Si5345A.regMapFile = os.path.join("config", "clock", "IC63_h6A_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC63_Si5345A.debugLevel = self.debugLevel
        # IC81 (Si5342A): I2C port 3, slave address 0x6B, clock I2C mux port 1
        self.i2cDevice_IC81_Si5342A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6b, "IC81 (Si5342A)")
        self.i2cDevice_IC81_Si5342A.muxChannel = 1
        self.i2cDevice_IC81_Si5342A.regMapFile = os.path.join("config", "clock", "IC81_h6B_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC81_Si5342A.debugLevel = self.debugLevel
        # IC82 (Si5344A): I2C port 3, slave address 0x6A, clock I2C mux port 0
        self.i2cDevice_IC82_Si5344A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6a, "IC82 (Si5344A)")
        self.i2cDevice_IC82_Si5344A.muxChannel = 0
        self.i2cDevice_IC82_Si5344A.regMapFile = os.path.join("config", "clock", "IC82_h6A_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC82_Si5344A.debugLevel = self.debugLevel
        # IC83 (Si5342A): I2C port 3, slave address 0x68, clock I2C mux port 2
        self.i2cDevice_IC83_Si5342A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x68, "IC83 (Si5342A)")
        self.i2cDevice_IC83_Si5342A.muxChannel = 2
        self.i2cDevice_IC83_Si5342A.regMapFile = os.path.join("config", "clock", "IC83_h68_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC83_Si5342A.debugLevel = self.debugLevel
        # IC84 (Si5345A): I2C port 3, slave address 0x69, clock I2C mux port 2
        self.i2cDevice_IC84_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x69, "IC84 (Si5345A)")
        self.i2cDevice_IC84_Si5345A.muxChannel = 2
        self.i2cDevice_IC84_Si5345A.regMapFile = os.path.join("config", "clock", "IC84_h69_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC84_Si5345A.debugLevel = self.debugLevel
        # IC85 (Si5345A): I2C port 3, slave address 0x6A, clock I2C mux port 2
        self.i2cDevice_IC85_Si5345A = I2C_Si53xx.I2C_Si53xx(self.mcuI2C[3], 0x6a, "IC85 (Si5345A)")
        self.i2cDevice_IC85_Si5345A.muxChannel = 2
        self.i2cDevice_IC85_Si5345A.regMapFile = os.path.join("config", "clock", "IC85_h6A_IN0-240M_O-240M-Registers.txt")
        self.i2cDevice_IC85_Si5345A.debugLevel = self.debugLevel

        # I2C mux for FireFly RX I2C bus:
        # IC24 (PCA9547PW): I2C port 2, slave address 0x70
        self.i2cDevice_IC24_PCA9547PW = I2C_PCA9547.I2C_PCA9547(self.mcuI2C[2], 0x70, "IC24 (PCA9547PW)")
        self.i2cDevice_IC24_PCA9547PW.debugLevel = self.debugLevel
        # FireFly RX 1..8: I2C port 2, slave address 0x54, FireFly RX I2C mux port 0..7
        self.i2cDevice_FireFly_RX = []
        for i in range(0, self.fireFlyNum):
            self.i2cDevice_FireFly_RX.append(I2C_FireFly.I2C_FireFly(self.mcuI2C[2], 0x54, "FireFly {0:d} RX".format(i+1), I2C_FireFly.I2C_FireFly.deviceTypeRX))
            self.i2cDevice_FireFly_RX[i].muxChannel = i
            self.i2cDevice_FireFly_RX[i].debugLevel = self.debugLevel

        # I2C mux for FireFly TX I2C bus:
        # IC25 (PCA9547PW): I2C port 2, slave address 0x71
        self.i2cDevice_IC25_PCA9547PW = I2C_PCA9547.I2C_PCA9547(self.mcuI2C[2], 0x71, "IC25 (PCA9547PW)")
        self.i2cDevice_IC25_PCA9547PW.debugLevel = self.debugLevel
        # FireFly TX 1..8: I2C port 2, slave address 0x50, FireFly TX I2C mux port 0..7
        self.i2cDevice_FireFly_TX = []
        for i in range(0, self.fireFlyNum):
            self.i2cDevice_FireFly_TX.append(I2C_FireFly.I2C_FireFly(self.mcuI2C[2], 0x50, "FireFly {0:d} TX".format(i+1), I2C_FireFly.I2C_FireFly.deviceTypeTX))
            self.i2cDevice_FireFly_TX[i].muxChannel = i
            self.i2cDevice_FireFly_TX[i].debugLevel = self.debugLevel



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



    # ===============================================================
    # MCU.
    # ===============================================================

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



    # ===============================================================
    # Power modules.
    # ===============================================================

    # Define the measurement names and the values of the shunt resistors.
    IC26_LTC2977_measurementNames =     ["KU15P 0.9V MGTAVCC", "KU15P 0.9V MGTAVCC", "KU15P 1.8V ADC AUX", "KU15P 1.8V ADC AUX", "KU15P 1.2V MGTAVTT", "KU15P 1.2V MGTAVTT", "KU15P 2.5V LDO", "KU15P 2.5V LDO"]
    IC26_LTC2977_currentSenseShunts =   [0, 0.04 / 2, 0, 0.04 / 2, 0, 0.01 / 2, 0, 0.08 / 2]
    IC27_LTC2977_measurementNames =     ["KU15P 1.2V DDR4", "KU15P 1.2V DDR4", "KU15P 1.8V IO", "KU15P 1.8V IO", "KU15P 1.8V MGTAUX", "KU15P 1.8V MGTAUX", "<unused>", "<unused>"]
    IC27_LTC2977_currentSenseShunts =   [0, 0.04 / 2, 0, 0.04 / 2, 0, 0.15 / 2, 0, 0]
    IC49_LTC2977_measurementNames =     ["ZU11EG 0.9V MGTAVCC", "ZU11EG 0.9V MGTAVCC", "ZU11EG 1.2V MGTAVTT", "ZU11EG 1.2V MGTAVTT", "ZU11EG 1.2V DDR4", "ZU11EG 1.2V DDR4", "ZU11EG 1.8V IO", "ZU11EG 1.8V IO"]
    IC49_LTC2977_currentSenseShunts =   [0, 0.02 / 2, 0, 0.02 / 2, 0, 0.04 / 2, 0, 0.04 / 2]
    IC50_LTC2977_measurementNames =     ["ZU11EG 2.5V LDO", "ZU11EG 2.5V LDO", "ZU11EG 3.3V MISC", "ZU11EG 3.3V MISC", "ZU11EG 0.85V MGTRAVCC", "ZU11EG 0.85V MGTRAVCC", "ZU11EG 1.8V ADC AUX", "ZU11EG 1.8V ADC AUX"]
    IC50_LTC2977_currentSenseShunts =   [0, 0.04 / 2, 0, 0.04 /2, 0, 0.15 / 2, 0, 0.15 / 2]
    IC51_LTC2977_measurementNames =     ["ZU11EG 1.1V ETH", "ZU11EG 1.1V ETH", "ZU11EG 1.8V MGTRVTT", "ZU11EG 1.8V MGTRVTT", "ZU11EG 1.8V MGTAUX", "ZU11EG 1.8V MGTAUX","<unused>", "<unused>"]
    IC51_LTC2977_currentSenseShunts =   [0, 0.15 / 2, 0, 0.15 / 2, 0, 0.15 / 2, 0, 0]
    IC52_LTC2977_measurementNames =     ["Clock 1.8V", "Clock 1.8V", "Clock 2.5V", "Clock 2.5V", "Expansion con. 1.8V", "Expansion con. 1.8V", "KU15P 3.3V MISC", "KU15P 3.3V MISC"]
    IC52_LTC2977_currentSenseShunts =   [0, 0.04 / 2, 0, 0.15 / 2, 0, 0.08 / 2, 0, 0.04 / 2]
    IC76_LTM4700_measurementNames =     ["KU15P core 1/4", "KU15P core 2/4"]
    IC77_LTM4700_measurementNames =     ["KU15P core 3/4", "KU15P core 4/4"]
    IC78_LTM4700_measurementNames =     ["ZU11EG core 1/4", "ZU11EG core 2/4"]
    IC79_LTM4700_measurementNames =     ["ZU11EG core 3/4", "ZU11EG core 4/4"]



    # Print the raw status of an LTC2977 8-channel PMBus power system manager IC.
    def power_ltc2977_status_raw(self, i2cDevice):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the status of the power module {0:s} on I2C port {1:d}.".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        ret, data = i2cDevice.read_status()
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error reading the raw status of the power module {0:s} on I2C port {1:d}!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
            return -1
        print("Status of the power module {0:s} on I2C port {1:d}:".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        print(self.prefixStatus + "{0:18s}: {1:5.2f} degC".format("Temperature", data[0]))
        print(self.prefixStatus + "{0:18s}: {1:5.2f} V".format("V_in", data[1]))
        for channel in range(i2cDevice.hwChannels):
            print(self.prefixStatus + "Channel {0:d}: {1:7s}: {2:5.2f} V".format(channel, "V_out", data[2][channel]))
        return 0



    # Print the status of an LTC2977 8-channel PMBus power system manager IC.
    def power_ltc2977_status(self, i2cDevice, measurementNames, currentSenseShunts):
        if len(measurementNames) != i2cDevice.hwChannels:
            self.errorCount += 1
            print(self.prefixError + "Error reading the status of the power module {0:s} on I2C port {1:d}: {2:d} measurement names must be provided, but only {3:d} were given!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port, i2cDevice.hwChannels, len(measurementNames)))
            return -1
        if len(currentSenseShunts) != i2cDevice.hwChannels:
            self.errorCount += 1
            print(self.prefixError + "Error reading the status of the power module {0:s} on I2C port {1:d}: {2:d} current sense values must be provided, but only {3:d} were given!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port, i2cDevice.hwChannels, len(currentSenseShunts)))
            return -1
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the status of the power module {0:s} on I2C port {1:d}.".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        ret, data = i2cDevice.read_status()
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error reading the status of the power module {0:s} on I2C port {1:d}!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
            return -1
        print("Status of the power module {0:s} on I2C port {1:d}:".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        print(self.prefixStatus + "{0:26s}: {1:5.2f} degC".format("Temperature", data[0]))
        print(self.prefixStatus + "{0:26s}: {1:5.2f} V".format("V_in", data[1]))
        for channel in range(i2cDevice.hwChannels):
            if currentSenseShunts[channel] != 0:
                value = data[2][channel] / currentSenseShunts[channel]
                unit = "A"
            else:
                value = data[2][channel]
                unit = "V"
            print(self.prefixStatus + "{0:d}: {1:23s}: {2:5.2f} {3:s}".format(channel, measurementNames[channel], value, unit))
        return 0



    # Print the raw status of an LTM4700 regulator with digital power system management IC.
    def power_ltm4700_status_raw(self, i2cDevice):
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the status of the power module {0:s} on I2C port {1:d}.".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        ret, data = i2cDevice.read_status()
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error reading the raw status of the power module {0:s} on I2C port {1:d}!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
            return -1
        print("Status of the power module {0:s} on I2C port {1:d}:".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        # Measurement of the external temperature is not supported on the CM demonstrator.
        #print(self.prefixStatus + "{0:18s}: {1:5.2f} degC".format("Temperature (ext)", data[0]))
        print(self.prefixStatus + "{0:18s}: {1:5.2f} degC".format("Temperature (int)", data[1]))
        print(self.prefixStatus + "{0:18s}: {1:5.2f} V".format("V_in", data[2]))
        # Measurement of the input current is not supported on the CM demonstrator.
        #print(self.prefixStatus + "{0:18s}: {1:5.2f} A".format("I_in", data[3]))
        for channel in range(i2cDevice.hwChannels):
            print(self.prefixStatus + "Channel {0:d}: {1:7s}: {2:5.2f} V".format(channel, "V_out", data[4][channel]))
            print(self.prefixStatus + "Channel {0:d}: {1:7s}: {2:5.2f} A".format(channel, "I_out", data[5][channel]))
        return 0



    # Print the status of an LTM4700 regulator with digital power system management IC.
    def power_ltm4700_status(self, i2cDevice, measurementNames):
        if len(measurementNames) != i2cDevice.hwChannels:
            self.errorCount += 1
            print(self.prefixError + "Error reading the status of the power module {0:s} on I2C port {1:d}: {2:d} measurement names must be provided, but only {3:d} were given!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port, i2cDevice.hwChannels, len(measurementNames)))
            return -1
        if self.debugLevel >= 1:
            print(self.prefixDebug + "Reading the status of the power module {0:s} on I2C port {1:d}.".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        ret, data = i2cDevice.read_status()
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error reading the status of the power module {0:s} on I2C port {1:d}!".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
            return -1
        print("Status of the power module {0:s} on I2C port {1:d}:".format(i2cDevice.deviceName, i2cDevice.mcuI2C.port))
        # Measurement of the external temperature is not supported on the CM demonstrator.
        #print(self.prefixStatus + "{0:18s}: {1:5.2f} degC".format("Temperature (ext)", data[0]))
        print(self.prefixStatus + "{0:18s}: {1:5.2f} degC".format("Temperature (int)", data[1]))
        print(self.prefixStatus + "{0:18s}: {1:5.2f} V".format("V_in", data[2]))
        # Measurement of the input current is not supported on the CM demonstrator.
        #print(self.prefixStatus + "{0:18s}: {1:5.2f} A".format("I_in", data[3]))
        for channel in range(i2cDevice.hwChannels):
            print(self.prefixStatus + "{0:d}: {1:23s}: {2:5.2f} V".format(channel, measurementNames[channel], data[4][channel]))
            print(self.prefixStatus + "{0:d}: {1:23s}: {2:5.2f} A".format(channel, measurementNames[channel], data[5][channel]))
        return 0



    # Print the raw status of all power modules.
    def power_module_status_raw(self):
        self.power_ltc2977_status_raw(self.i2cDevice_IC26_LTC2977)
        self.power_ltc2977_status_raw(self.i2cDevice_IC27_LTC2977)
        self.power_ltc2977_status_raw(self.i2cDevice_IC49_LTC2977)
        self.power_ltc2977_status_raw(self.i2cDevice_IC50_LTC2977)
        self.power_ltc2977_status_raw(self.i2cDevice_IC51_LTC2977)
        self.power_ltc2977_status_raw(self.i2cDevice_IC52_LTC2977)
        self.power_ltm4700_status_raw(self.i2cDevice_IC76_LTM4700)
        self.power_ltm4700_status_raw(self.i2cDevice_IC77_LTM4700)
        self.power_ltm4700_status_raw(self.i2cDevice_IC78_LTM4700)
        self.power_ltm4700_status_raw(self.i2cDevice_IC79_LTM4700)



    # Print the status of all power modules.
    def power_module_status(self):
        self.power_ltc2977_status(self.i2cDevice_IC26_LTC2977, self.IC26_LTC2977_measurementNames, self.IC26_LTC2977_currentSenseShunts)
        self.power_ltc2977_status(self.i2cDevice_IC27_LTC2977, self.IC27_LTC2977_measurementNames, self.IC27_LTC2977_currentSenseShunts)
        self.power_ltc2977_status(self.i2cDevice_IC49_LTC2977, self.IC49_LTC2977_measurementNames, self.IC49_LTC2977_currentSenseShunts)
        self.power_ltc2977_status(self.i2cDevice_IC50_LTC2977, self.IC50_LTC2977_measurementNames, self.IC50_LTC2977_currentSenseShunts)
        self.power_ltc2977_status(self.i2cDevice_IC51_LTC2977, self.IC51_LTC2977_measurementNames, self.IC51_LTC2977_currentSenseShunts)
        self.power_ltc2977_status(self.i2cDevice_IC52_LTC2977, self.IC52_LTC2977_measurementNames, self.IC52_LTC2977_currentSenseShunts)
        self.power_ltm4700_status(self.i2cDevice_IC76_LTM4700, self.IC76_LTM4700_measurementNames)
        self.power_ltm4700_status(self.i2cDevice_IC77_LTM4700, self.IC77_LTM4700_measurementNames)
        self.power_ltm4700_status(self.i2cDevice_IC78_LTM4700, self.IC78_LTM4700_measurementNames)
        self.power_ltm4700_status(self.i2cDevice_IC79_LTM4700, self.IC79_LTM4700_measurementNames)



    # ===============================================================
    # Silicon labs clock ICs.
    # ===============================================================

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



    # Program a single Silicon Labs clock IC from a register map file by its name.
    def clk_prog_device_by_name(self, clkDevName, regMapFile):
        clkDeviceList = [self.i2cDevice_IC54_Si5341A,
                         self.i2cDevice_IC56_Si5345A,
                         self.i2cDevice_IC60_Si5345A,
                         self.i2cDevice_IC61_Si5342A,
                         self.i2cDevice_IC62_Si5345A,
                         self.i2cDevice_IC63_Si5345A,
                         self.i2cDevice_IC81_Si5342A,
                         self.i2cDevice_IC82_Si5344A,
                         self.i2cDevice_IC83_Si5342A,
                         self.i2cDevice_IC84_Si5345A,
                         self.i2cDevice_IC85_Si5345A]
        clkDevice = None
        for dev in clkDeviceList:
            if clkDevName.lower() == dev.deviceName[0:4].lower():
                clkDevice = dev
                clkDevice.regMapFile = regMapFile
        if not clkDevice:
            print(self.prefixError, "Clock device '{0:s}' not valid!".format(clkDevName))
            print(self.prefixError, "Valid clock devices: ", end='')
            for dev in clkDeviceList:
                print(dev.deviceName[0:4] + " ", end='')
            print()
            return -1
        self.clk_prog_device_file(clkDevice)
        return 0



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



    # ===============================================================
    # FireFly modules.
    # ===============================================================

    # Monitor the FireFly temperatures.
    def firefly_temp(self):
        for i in range(0, self.fireFlyNum):
            # RX.
            self.i2cDevice_IC24_PCA9547PW.set_channel(self.i2cDevice_FireFly_RX[i].muxChannel)
            ret, temperature = self.i2cDevice_FireFly_RX[i].read_temperature()
            if ret == 0:
                print("{0:13s}: {1:3d} degC".format(self.i2cDevice_FireFly_RX[i].deviceName, temperature))
            # TX.
            self.i2cDevice_IC25_PCA9547PW.set_channel(self.i2cDevice_FireFly_TX[i].muxChannel)
            ret, temperature = self.i2cDevice_FireFly_TX[i].read_temperature()
            if ret == 0:
                print("{0:13s}: {1:3d} degC".format(self.i2cDevice_FireFly_TX[i].deviceName, temperature))



    # Check the FireFly number.
    def firefly_check_num(self, fireFlyNum):
        if fireFlyNum < 1 or fireFlyNum > self.fireFlyNum:
            print(self.prefixError + "FireFly number {0:d} out of range {1:d}..{2:d}!".format(fireFlyNum, 1, self.fireFlyNum))
            return -1



    # Get the status of a FireFly module.
    def firefly_status(self, fireFlyNum):
        if self.firefly_check_num(fireFlyNum):
            return -1
        fireFlyNum -= 1
        # RX.
        self.i2cDevice_IC24_PCA9547PW.set_channel(self.i2cDevice_FireFly_RX[fireFlyNum].muxChannel)
        print(self.i2cDevice_FireFly_RX[fireFlyNum].deviceName + ":")
        ret, temperature = self.i2cDevice_FireFly_RX[fireFlyNum].read_temperature()
        ret, vcc = self.i2cDevice_FireFly_RX[fireFlyNum].read_vcc()
        ret, firmwareVersion = self.i2cDevice_FireFly_RX[fireFlyNum].read_firmware_version()
        ret, vendorName = self.i2cDevice_FireFly_RX[fireFlyNum].read_vendor_name()
        ret, vendorPartNumber = self.i2cDevice_FireFly_RX[fireFlyNum].read_vendor_part_number()
        ret, vendorSerialNumber = self.i2cDevice_FireFly_RX[fireFlyNum].read_vendor_serial_number()
        print("    Temperature          : {0:d} degC".format(temperature))
        print("    VCC                  : {0:5.3f} V".format(vcc))
        print("    Firmware version     : {0:s}".format(firmwareVersion))
        print("    Vendor Name          : {0:s}".format(vendorName))
        print("    Vendor Part Number   : {0:s}".format(vendorPartNumber))
        print("    Vendor Serial Number : {0:s}".format(vendorSerialNumber))
        # TX.
        self.i2cDevice_IC25_PCA9547PW.set_channel(self.i2cDevice_FireFly_TX[fireFlyNum].muxChannel)
        print(self.i2cDevice_FireFly_TX[fireFlyNum].deviceName+ ":")
        ret, temperature = self.i2cDevice_FireFly_TX[fireFlyNum].read_temperature()
        ret, vcc = self.i2cDevice_FireFly_TX[fireFlyNum].read_vcc()
        ret, firmwareVersion = self.i2cDevice_FireFly_TX[fireFlyNum].read_firmware_version()
        ret, vendorName = self.i2cDevice_FireFly_TX[fireFlyNum].read_vendor_name()
        ret, vendorPartNumber = self.i2cDevice_FireFly_TX[fireFlyNum].read_vendor_part_number()
        ret, vendorSerialNumber = self.i2cDevice_FireFly_TX[fireFlyNum].read_vendor_serial_number()
        print("    Temperature          : {0:d} degC".format(temperature))
        print("    VCC                  : {0:5.3f} V".format(vcc))
        print("    Firmware version     : {0:s}".format(firmwareVersion))
        print("    Vendor Name          : {0:s}".format(vendorName))
        print("    Vendor Part Number   : {0:s}".format(vendorPartNumber))
        print("    Vendor Serial Number : {0:s}".format(vendorSerialNumber))



    # Get the time at temperature of a FireFly module.
    def firefly_time_at_temperature(self, fireFlyNum):
        if self.firefly_check_num(fireFlyNum):
            return -1
        fireFlyNum -= 1
        # RX.
        self.i2cDevice_IC24_PCA9547PW.set_channel(self.i2cDevice_FireFly_RX[fireFlyNum].muxChannel)
        print(self.i2cDevice_FireFly_RX[fireFlyNum].deviceName + ":")
        for i in range(0, 22):
            ret, timeAtTemperature = self.i2cDevice_FireFly_RX[fireFlyNum].read_time_at_temperature(i)
            if i == 0:
                print("       < 0 degC", end='')
            elif i == 21:
                print("     > 100 degC", end='')
            else:
                print("{0:3d} .. {1:3d} degC".format((i - 1) * 5, i * 5), end='')
            print(" : {0:10.2f} hours".format(timeAtTemperature))
        # TX.
        self.i2cDevice_IC25_PCA9547PW.set_channel(self.i2cDevice_FireFly_TX[fireFlyNum].muxChannel)
        print(self.i2cDevice_FireFly_TX[fireFlyNum].deviceName + ":")
        for i in range(0, 22):
            ret, timeAtTemperature = self.i2cDevice_FireFly_TX[fireFlyNum].read_time_at_temperature(i)
            if i == 0:
                print("       < 0 degC", end='')
            elif i == 21:
                print("     > 100 degC", end='')
            else:
                print("{0:3d} .. {1:3d} degC".format((i - 1) * 5, i * 5), end='')
            print(" : {0:10.2f} hours".format(timeAtTemperature))

