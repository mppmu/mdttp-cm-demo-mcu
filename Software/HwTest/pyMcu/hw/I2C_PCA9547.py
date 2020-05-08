# File: I2C_PCA9547.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 28 Apr 2020
# Rev.: 08 May 2020
#
# Python class for communicating with the PCA9547 8-channel I2C-bus multiplexer
# IC.
#



import McuI2C
import I2CDevice



class I2C_PCA9547:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)
    prefixError         = "ERROR: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel          = 0     # Debug verbosity.

    # Hardware parameters.
    hwChannelMin        = 0x00  # Lowest hardware channel number.
    hwChannelMax        = 0x0f  # Highest hardware channel number.



    # Initialize the I2C device.
    def __init__(self, mcuI2C, slaveAddr, deviceName):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.deviceName = deviceName
        self.i2cDevice = I2CDevice.I2CDevice(self.mcuI2C, self.slaveAddr, self.deviceName)
        self.i2cDevice.debugLevel = self.debugLevel
        self.prefixDebugDevice = self.prefixDebug + self.deviceName + ": "
        self.prefixErrorDevice = self.prefixError + self.deviceName + ": "



    # Check the channel number.
    def check_channel_number(self, port):
        if port < self.hwChannelMin or port > self.hwChannelMax:
            print(self.prefixErrorDevice + "Hardware channel number {0:d} out of valid range {1:d}..{2:d}!".\
                format(port, self.hwChannelMin, self.hwChannelMax))
            return -1
        return 0



    # Set the multiplexer channel.
    def set_channel(self, channel):
        self.i2cDevice.debugLevel = self.debugLevel
        if self.check_channel_number(channel):
            return -1
        channel &= 0x0f
        channel |= 0x08     # Set the enable bit.
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Setting the channel to 0x{0:02x}.".format(channel), end='')
            self.i2cDevice.print_details()
        # Write data.
        ret = self.i2cDevice.write([channel])
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error setting the channel to 0x{0:02x}!".format(channel), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Disable the multiplexer.
    def disable(self):
        self.i2cDevice.debugLevel = self.debugLevel
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Disabling all channels.", end='')
            self.i2cDevice.print_details()
        # Write data.
        ret = self.i2cDevice.write([0x08])
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error disabling all channels!", end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Get the current multiplexer channel.
    def get_channel(self):
        self.i2cDevice.debugLevel = self.debugLevel
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Reading the current multiplexer channel.", end='')
            self.i2cDevice.print_details()
        # Read the sensor multiplexer channel.
        ret, data = self.i2cDevice.read(1)
        # Evaluate response.
        if ret or len(data) != 1:
            print(self.prefixErrorDevice + "Error reading the multiplexer channel!", end='')
            self.i2cDevice.print_details()
            if ret:
                print(self.prefixErrorDevice + "Reading of data returned error code {0:d}.".format(ret))
            return -1, 0xff
        return 0, data

