# File: I2C_MCP9808.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 04 May 2020
# Rev.: 08 May 2020
#
# Python class for communicating with the MCP9808 digital temperature sensor
# IC.
#



import McuI2C
import I2CDevice



class I2C_MCP9808:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)
    prefixError         = "ERROR: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel          = 0     # Debug verbosity.

    # Hardware parameters.
    hwPointerMin        = 0x00
    hwPointerMax        = 0x08



    # Initialize the I2C device.
    def __init__(self, mcuI2C, slaveAddr, deviceName):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.deviceName = deviceName
        self.i2cDevice = I2CDevice.I2CDevice(self.mcuI2C, self.slaveAddr, self.deviceName)
        self.i2cDevice.debugLevel = self.debugLevel
        self.prefixDebugDevice = self.prefixDebug + self.deviceName + ": "
        self.prefixErrorDevice = self.prefixError + self.deviceName + ": "



    # Check the register pointer value.
    def check_pointer(self, pointer):
        if pointer < self.hwPointerMin or pointer > self.hwPointerMax:
            print(self.prefixErrorDevice + "Pointer register value {0:d} out of valid range {1:d}..{2:d}!".\
                format(pointer, self.hwPointerMin, self.hwPointerMax))
            return -1
        return 0



    # Return the name of a register pointer.
    @classmethod
    def pointer_to_name(cls, pointer):
        if pointer == 0x00:
            regName = "*reserved for future use*"
        elif pointer == 0x01:
            regName = "configuration"
        elif pointer == 0x02:
            regName = "alert temperature upper boundary trip"
        elif pointer == 0x03:
            regName = "alert temperature lower boundary trip"
        elif pointer == 0x04:
            regName = "critical temperature trip"
        elif pointer == 0x05:
            regName = "temperature"
        elif pointer == 0x06:
            regName = "manufacturer ID"
        elif pointer == 0x07:
            regName = "the device ID"
        elif pointer == 0x08:
            regName = "resolution"
        else:
            regName = "*reserved*"
        return regName + " register"



    # Read a register value.
    def read_reg(self, pointer):
        self.i2cDevice.debugLevel = self.debugLevel
        if self.check_pointer(pointer):
            return -1, 0xffff
        regName = self.pointer_to_name(pointer)
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Reading the value of the {0:s}, pointer address 0x{1:02x}.".format(regName, pointer), end='')
            self.i2cDevice.print_details()
        # Assemble command to write.
        dataWr = []
        dataWr.append(pointer)
        # Write command and read data with repeated start.
        ret, dataRd = self.i2cDevice.write_read(dataWr, 2)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error reading the value of the {0:s}, pointer address 0x{1:02x}!".format(regName, pointer), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1, 0xffff
        if len(dataRd) != 2:
            print(self.prefixErrorDevice + "Error reading the value of the {0:s}, pointer address 0x{1:02x}: Incorrect amount of data received!".\
                format(regName, pointer), end='')
            self.i2cDevice.print_details()
            return -1, 0xffff
        # Calculate the value.
        value  = (dataRd[0] & 0xff) << 8    # Data byte 0: MSB.
        value |=  dataRd[1] & 0xff          # Data byte 1: LSB.
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Read the value of the {0:s}, pointer address 0x{1:02x}: 0x{2:04x}.".format(regName, pointer, value), end='')
            self.i2cDevice.print_details()
        return 0, value



    # Write a register value.
    def write_reg(self, pointer, value):
        self.i2cDevice.debugLevel = self.debugLevel
        if self.check_pointer(pointer):
            return -1
        regName = self.pointer_to_name(pointer)
        value &= 0xffff     # Limit to 16 bits.
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Writing 0x{0:04x} to the {1:s}, pointer address 0x{2:02x}.".format(value, regName, pointer), end='')
            self.i2cDevice.print_details()
        # Assemble command and data to write.
        dataWr = []
        dataWr.append(pointer)
        dataWr.append((value >> 8) & 0xff)  # Data byte 0: MSB.
        dataWr.append(value & 0xff)         # Data byte 1: LSB.
        # Write command and data.
        ret = self.i2cDevice.write(dataWr)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error writing 0x{0:04x} to the {1:s}, pointer address 0x{2:02x}!".\
                format(value, regName, pointer), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Convert a raw value to a temperature value.
    @classmethod
    def raw_to_temperature(cls, raw):
        if (raw >> 12) & 0x1:
            raw = ~raw + 1
            sign = -1
        else:
            sign = 1
        temperature = sign * (((raw >> 4) & 0xff) + (raw & 0xf) * (0.0625))
        return temperature



    # Convert a temperature value to a raw value.
    @classmethod
    def temperature_to_raw(cls, temperature):
        raw = int(abs(temperature) / 0.0625) & 0xfff
        if temperature < 0:
            raw = (~raw + 1) & 0x1fff
        return raw



    # Read the reserved for future use register.
    def read_rfu(self):
        ret, value = self.read_reg(0x00)
        return ret, value



    # Read the configuration register.
    def read_config(self):
        ret, value = self.read_reg(0x01)
        return ret, value



    # Read the alert temperature upper boundary trip register.
    def read_t_upper(self):
        ret, value = self.read_reg(0x02)
        temperature = self.raw_to_temperature(value)
        return ret, temperature



    # Read the alert temperature lower boundary trip register.
    def read_t_lower(self):
        ret, value = self.read_reg(0x03)
        temperature = self.raw_to_temperature(value)
        return ret, temperature



    # Read the critical temperature trip register.
    def read_t_crit(self):
        ret, value = self.read_reg(0x04)
        temperature = self.raw_to_temperature(value)
        return ret, temperature



    # Read the temperature register.
    def read_temperature(self):
        ret, value = self.read_reg(0x05)
        temperature = self.raw_to_temperature(value)
        alerts = (value >> 13) & 0x7
        return ret, temperature, alerts



    # Read the manufacturer ID register.
    def read_manufacturer_id(self):
        ret, value = self.read_reg(0x06)
        return ret, value



    # Read the device ID register.
    def read_device_id(self):
        ret, value = self.read_reg(0x07)
        return ret, value



    # Read the resolution register.
    def read_resolution(self):
        ret, value = self.read_reg(0x08)
        return ret, value



    # Write the configuration register.
    def write_config(self, value):
        ret = self.write_reg(0x01, value)
        return ret



    # Write the alert temperature upper boundary trip register.
    def wirte_t_upper(self, value):
        ret = self.write_reg(0x02, self.temperature_to_raw(value))
        return ret



    # Write the alert temperature lower boundary trip register.
    def write_t_lower(self, value):
        ret = self.write_reg(0x03, self.temperature_to_raw(value))
        return ret



    # Write the critical temperature trip register.
    def write_t_crit(self, value):
        ret = self.write_reg(0x04, self.temperature_to_raw(value))
        return ret



    # Write the resolution register.
    def write_resolution(self, value):
        ret = self.write_reg(0x08, value)
        return ret

