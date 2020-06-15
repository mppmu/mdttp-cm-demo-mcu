# File: I2C_LTC2977.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 15 Jun 2020
# Rev.: 15 Jun 2020
#
# Python class for communicating with the LTC2977 8-channel PMBus power system
# manager IC.
#
# Hints:
# - See datasheet "ltc2977.pdf" for details.
#



import McuI2C
import I2CDevice



class I2C_LTC2977:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)
    prefixError         = "ERROR: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel          = 0     # Debug verbosity.

    # Hardware parameters.
    hwDataLenMin        = 1
    hwDataLenMax        = 2
    hwPageMin           = 0     # Lowest hardware channel/page number.
    hwPageMax           = 7     # Highest hardware channel/page number.



    # Initialize the I2C device.
    def __init__(self, mcuI2C, slaveAddr, deviceName):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.deviceName = deviceName
        self.i2cDevice = I2CDevice.I2CDevice(self.mcuI2C, self.slaveAddr, self.deviceName)
        self.i2cDevice.debugLevel = self.debugLevel
        self.prefixDebugDevice = self.prefixDebug + self.deviceName + ": "
        self.prefixErrorDevice = self.prefixError + self.deviceName + ": "
        self.errorCount = 0



    # Return the name of a command code.
    @classmethod
    def cmd_to_name(cls, cmdCode):
        if cmdCode == 0x00:
            cmdName = "page"
        elif cmdCode == 0x01:
            cmdName = "operation"
        elif cmdCode == 0x02:
            cmdName = "on/off config"
        elif cmdCode == 0x03:
            cmdName = "clear faults"
        elif cmdCode == 0x10:
            cmdName = "write protect"
        elif cmdCode <= 0xfd:
            cmdName = "unknown"
        else:
            cmdName = "*reserved*"
        return cmdName



    # Check the data length.
    def check_data_len(self, dataLen):
        if dataLen < self.hwDataLenMin or dataLen > self.hwDataLenMax:
            print(self.prefixErrorDevice + "Data length {0:d} out of valid range {1:d}..{2:d}!".\
                format(dataLen, self.hwDataLenMin, self.hwDataLenMax))
            return -1
        return 0



    # Check the page number.
    def check_page_number(self, page):
        if (page < self.hwPageMin or page > self.hwPageMax) and page != 0xff:
            print(self.prefixErrorDevice + "Hardware page number {0:d} out of valid range {1:d}..{2:d}!".\
                format(page, self.hwPageMin, self.hwPageMax))
            return -1
        return 0



    # Read command data.
    def read(self, cmdCode, dataLen):
        self.i2cDevice.debugLevel = self.debugLevel
        cmdCode &= 0xff
        cmdName = self.cmd_to_name(cmdCode)
        if self.check_data_len(dataLen):
            self.errorCount += 1
            return -1
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Reading the command 0x{0:02x} ({1:s}) data.".format(cmdCode, cmdName), end='')
            self.i2cDevice.print_details()
        # Assemble command to write.
        dataWr = []
        dataWr.append(cmdCode)
        # Write command and read data with repeated start.
        ret, dataRd = self.i2cDevice.write_read(dataWr, dataLen)
        # Evaluate response.
        if ret:
            self.errorCount += 1
            print(self.prefixErrorDevice + "Error reading the command 0x{0:02x} ({1:s}) data!".format(cmdCode, cmdName), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1, 0xff
        if not dataRd:
            self.errorCount += 1
            print(self.prefixErrorDevice + "Error reading the command 0x{0:02x} ({1:s}) data: No data received!".format(cmdCode, cmdName), end='')
            self.i2cDevice.print_details()
            return -1, 0xff
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Read the command 0x{0:02x} ({1:s}) data: ".format(cmdCode, cmdName), end='')
            for datum in dataRd:
                print("0x{0:02x} ".format(datum), end='')
            self.i2cDevice.print_details()
        return 0, dataRd



    # Write command data.
    def write(self, cmdCode, data):
        self.i2cDevice.debugLevel = self.debugLevel
        cmdCode &= 0xff
        cmdName = self.cmd_to_name(cmdCode)
        if self.check_data_len(len(data)):
            self.errorCount += 1
            return -1
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Writing command 0x{0:02x} ({1:s}) data: ".format(cmdCode, cmdName), end='')
            for datum in data:
                print("0x{0:02x} ".format(datum & 0xff), end='')
            self.i2cDevice.print_details()
        # Assemble command and data to write.
        dataWr = []
        dataWr.append(cmdCode)
        for datum in data:
            dataWr.append(datum & 0xff)
        # Write command and data.
        ret = self.i2cDevice.write(dataWr)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error writing command 0x{0:02x} ({1:s}) data!".format(cmdCode, cmdName), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Clear the write protection.
    def wp_clear(self):
        return self.write(0x10, [0x00])



    # Set the write protection to level 1:
    # Disable all writes except to the WRITE_PROTECT, PAGE, MFR_EE_UNLOCK, and STORE_USER_ALL commands.
    def wp_level_1(self):
        return self.write(0x10, [0x80])



    # Set the write protection to level 2:
    # Disable all writes except to the WRITE_PROTECT, PAGE, MFR_EE_UNLOCK, STORE_USER_ALL, OPERATION,
    # MFR_COMMAND_PLUS, MFR_PAGE_FF_MASK and CLEAR_FAULTS commands.
    def wp_level_2(self):
        return self.write(0x10, [0x40])



    # Switch off all power channles simultaneously.
    def power_off_all(self):
        ret = self.wp_level_2()
        # Make all channels respond to global page commands.
        ret |= self.write(0xe4, [0xff])
        # Write to all channels simultaneously.
        ret |= self.write(0x00, [0xff])
        # Configure the on/off behavior.
        ret |= self.write(0x02, [0x00])
        # Switch on all channels.
        ret |= self.write(0x00, [0x00])
        return ret



    # Switch on all power channles simultaneously.
    def power_on_all(self):
        ret = self.wp_level_2()
        # Make all channels respond to global page commands.
        ret |= self.write(0xe4, [0xff])
        # Write to all channels simultaneously.
        ret |= self.write(0x00, [0xff])
        # Configure the on/off behavior.
        ret |= self.write(0x02, [0x00])
        # Switch on all channels.
        ret |= self.write(0x00, [0x80])
        return ret

