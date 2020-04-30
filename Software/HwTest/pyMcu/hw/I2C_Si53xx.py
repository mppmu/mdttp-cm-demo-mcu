# File: I2C_Si53xx.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 29 Apr 2020
# Rev.: 30 Apr 2020
#
# Python class for communicating with Silicon Labs Si5341/40 and Si5345/44/42
# devices.
#



import os
import McuI2C
import I2CDevice



class I2C_Si53xx:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixError         = "ERROR: {0:s}: ".format(__file__)
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel = 0                 # Debug verbosity.

    # Hardware parameters.
    fileRegMapMarkComment = "#"


    # Initialize the I2C device.
    def __init__(self, mcuI2C, slaveAddr, deviceName):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.deviceName = deviceName
        self.i2cDevice = I2CDevice.I2CDevice(self.mcuI2C, self.slaveAddr, self.deviceName)
        self.i2cDevice.debugLevel = self.debugLevel



    # Load the configuration of an Si53xx IC from a register map file produced
    # with the ClockBuilder Pro software.
    def config_file(self, fileRegMapName):
        # Check if fileRegMapName is a file.
        if not os.path.isfile(fileRegMapName):
            print(self.prefixError + "The {0:s} register map file `{1:s}' is not a file!".format(self.deviceName, fileRegMapName))
            return -1
        # Check if the register map file is readable.
        if not os.access(fileRegMapName, os.R_OK):
            print(self.prefixError + "Cannot open the {0:s} register map file `{1:s}'!".format(self.deviceName, fileRegMapName))
            return -1

        fileRegMapLineCount = 0
        # Read and process the register map file.
        with open(fileRegMapName) as fileRegMap:
            for fileRegMapLine in fileRegMap:
                fileRegMapLineCount += 1
                if self.debugLevel >= 3:
                    print(self.prefixDebug + "Processing line {0:d} of the {1:s} register map file `{2:s}':".\
                        format(fileRegMapLineCount, self.deviceName, fileRegMapName))
                    print(self.prefixDebug + fileRegMapLine.strip('\n\r'))
                # Strip all leading and trailing white spaces, tabs, line feeds and carriage returns.
                lineStripped = fileRegMapLine.strip(' \t\n\r')
                # Remove comments.
                if lineStripped.find(self.fileRegMapMarkComment) >= 0:
                    lineCommentRemoved = lineStripped[0:lineStripped.find(self.fileRegMapMarkComment)].strip(' \t')
                else:
                    lineCommentRemoved = lineStripped
                # Get list of elements.
                lineElements = list(filter(None, lineCommentRemoved.split(",")))
                lineElements = list(el.strip(' \t\n\r') for el in lineElements)
                # Ignore lines without data.
                if not lineElements:
                    continue
                # Convert hexadecimal values from ??h to 0x??.
                lineElements = list("0x" + el.strip("h") if el.find("h") >= 0 else el for el in lineElements)
                # Convert to intergers.
                lineData = [int(i, 0) for i in lineElements]
                ret = self.i2cDevice.write(lineData)
                if ret:
                    print(self.prefixError + "Error sending data of register map file `{0:s}' to the {1:s}! Line number: {2:d}, Data: {3:s}".\
                        format(fileRegMapName, self.deviceName, fileRegMapLineCount, lineCommentRemoved))
                    return -1
        return 0

