# File: I2C_PCA9547.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 28 Apr 2020
# Rev.: 28 Apr 2020
#
# Python class for communicating with the PCA9547 8-channel I2C-bus multiplexer
# IC.
#



import McuI2C



class I2C_PCA9547:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixError         = "ERROR: {0:s}: ".format(__file__)
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel = 0                 # Debug verbosity.



    # Initialize the I2C device.
    def __init__(self, mcuI2C, slaveAddr):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.errorCount = 0
        self.accessRead = 0
        self.accessWrite = 0
        self.bytesRead = 0
        self.bytesWritten = 0



    # Write data to the PCA9547 IC.
    def write(self, data):
        if self.debugLevel >= 3:
            print(self.prefixDebug + "Writing data to the PCA9547 IC.", end='')
            self.print_details()
        ret = self.mcuI2C.ms_write(self.slaveAddr, data)
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error writing data to the PCA9547 IC!", end='')
            self.print_details()
            return ret
        self.accessWrite += 1
        self.bytesWritten += len(data)
        return 0



    # Read data from the PCA9547 IC.
    def read(self, cnt):
        if self.debugLevel >= 3:
            print(self.prefixDebug + "Reading data from the PCA9547 IC.", end='')
            self.print_details()
        ret, data = self.mcuI2C.ms_read(self.slaveAddr, cnt)
        if ret or len(data) <= 0:
            self.errorCount += 1
            print(self.prefixError + "Error reading data from the PCA9547 IC!", end='')
            self.print_details()
            print(self.prefixError + "Error code: {0:d}: ".format(ret))
            return ret, data
        self.accessRead += 1
        self.bytesRead += len(data)
        return 0, data



    # Print details.
    def print_details(self):
        print(self.prefixDetails, end='')
        print("I2C master port: {0:d}".format(self.mcuI2C.port), end='')
        print(self.separatorDetails + "Slave address: 0x{0:02x}".format(self.slaveAddr), end='')
        if self.debugLevel >= 1:
            print(self.separatorDetails + "Error count: {0:d}".format(self.errorCount), end='')
        if self.debugLevel >= 2:
            print(self.separatorDetails + "Read access count: {0:d}".format(self.accessRead), end='')
            print(self.separatorDetails + "Write access countn: {0:d}".format(self.accessWrite), end='')
        if self.debugLevel >= 2:
            print(self.separatorDetails + "Bytes read: {0:d}".format(self.bytesRead), end='')
            print(self.separatorDetails + "Bytes written: {0:d}".format(self.bytesWritten), end='')
        print()
        return 0



    # Set the multiplexer channel.
    def set_channel(self, channel):
        channel &= 0x0f
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebug + "Setting the PCA9547 multiplexer channel to 0x{0:02x}.".format(channel), end='')
            self.print_details()
        # Write data.
        ret = self.write([channel])
        # Evaluate response.
        if ret:
            print(self.prefixError + "Error setting the PCA9547 multiplexer channel to 0x{0:02x}!".format(channel), end='')
            self.print_details()
            print(self.prefixError + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Disable the multiplexer.
    def reset(self):
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebug + "Disabling PCA9547 multiplexer.", end='')
            self.print_details()
        # Write data.
        ret = self.write([0x08])
        # Evaluate response.
        if ret:
            print(self.prefixError + "Error disabling PCA9547 multiplexer!", end='')
            self.print_details()
            print(self.prefixError + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Get the current multiplexer channel.
    def get_channel(self):
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebug + "Reading the current multiplexer channel from the PCA9547 IC.", end='')
            self.print_details()
        # Read the sensor multiplexer channel.
        ret, data = self.read(1)
        # Evaluate response.
        if ret or len(data) != 1:
            print(self.prefixError + "Error reading the multiplexer channel from the PCA9547 IC!", end='')
            self.print_details()
            if ret:
                print(self.prefixError + "Reading of data returned error code {0:d}.".format(ret))
            return -1, 0xff
        return 0, ret

