# File: I2C_Si53xx.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 29 Apr 2020
# Rev.: 29 Apr 2020
#
# Python class for communicating with Silicon Labs Si5341/40 and Si5345/44/42
# devices.
#



import os
import McuI2C



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
    def __init__(self, mcuI2C, slaveAddr):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.errorCount = 0
        self.accessRead = 0
        self.accessWrite = 0
        self.bytesRead = 0
        self.bytesWritten = 0



    # Write data to the Si53xx IC.
    def write(self, data):
        if self.debugLevel >= 3:
            print(self.prefixDebug + "Writing data to the Si53xx IC.", end='')
            self.print_details()
        ret = self.mcuI2C.ms_write(self.slaveAddr, data)
        if ret:
            self.errorCount += 1
            print(self.prefixError + "Error writing data to the Si53xx IC!", end='')
            self.print_details()
            return ret
        self.accessWrite += 1
        self.bytesWritten += len(data)
        return 0



    # Read data from the Si53xx IC.
    def read(self, cnt):
        if self.debugLevel >= 3:
            print(self.prefixDebug + "Reading data from the Si53xx IC.", end='')
            self.print_details()
        ret, data = self.mcuI2C.ms_read(self.slaveAddr, cnt)
        if ret or len(data) <= 0:
            self.errorCount += 1
            print(self.prefixError + "Error reading data from the Si53xx IC!", end='')
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



    # Load the configuration of an Si53xx IC from a register map file produced
    # with the ClockBuilder Pro software.
    def config_file(self, fileRegMapName):
        # Check if fileRegMapName is a file.
        if not os.path.isfile(fileRegMapName):
            print(self.prefixError + "The Si53xx register map file `{0:s}' is not a file!".format(fileRegMapName))
            return -1
        # Check if the register map file is readable.
        if not os.access(fileRegMapName, os.R_OK):
            print(self.prefixError + "Cannot open the Si53xx register map file `{0:s}'!".format(fileRegMapName))
            return -1

        fileRegMapLineCount = 0
        # Read and process the register map file.
        with open(fileRegMapName) as fileRegMap:
            for fileRegMapLine in fileRegMap:
                fileRegMapLineCount += 1
                if self.debugLevel >= 3:
                    print(self.prefixDebug + "Processing line {0:d} of Si53xx register map file `{1:s}':".\
                        format(fileRegMapLineCount, fileRegMapName))
                    print(self.prefixDebug + fileRegMapLine.strip('\n\r'))
                # Strip all leading and trailing white spaces, tabs, line feeds and carriage returns.
                lineStripped = fileRegMapLine.strip(' \t\n\r')
                # Remove comments.
                if lineStripped.find(self.fileRegMapMarkComment) >= 0:
                    lineCommentRemoved = lineStripped[0:lineStripped.find(self.fileRegMapMarkComment)].strip(' \t')
                else:
                    lineCommentRemoved = lineStripped
                # Get list of elements.
                lineElements = list(filter(None, lineCommentRemoved.replace("\t", " ").split(",")))
                # Ignore lines without data.
                if not lineElements:
                    continue
                # Convert hexadecimal values from ??h to 0x??.
                lineElements = list("0x" + el.strip("h") if el.find("h") >= 0 else el for el in lineElements)
                # Convert to intergers.
                lineData = [int(i, 0) for i in lineElements]
                ret = self.write(lineData)
                if ret:
                    print(self.prefixError + "Error sending data of register map file `{0:s}' to Si53xx IC! Line number: {1:d}, Data: {2:s}".
                        format(fileRegMapName, fileRegMapLineCount, lineCommentRemoved))
                    return -1
        return 0


