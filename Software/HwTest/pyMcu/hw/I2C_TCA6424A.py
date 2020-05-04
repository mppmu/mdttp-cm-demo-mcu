# File: I2C_TCA6424A.py
# Auth: M. Fras, Electronics Division, MPI for Physics, Munich
# Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
# Date: 04 May 2020
# Rev.: 04 May 2020
#
# Python class for communicating with the TCA6424A I2C and SMBus I/O expander
# IC.
#
# Hints:
# - See datasheet "TCA6424A.pdf" for details.
# - Input Port Registers:
#   The Input Port registers (registers 0, 1 and 2) reflect the incoming logic
#   levels of the pins, regardless of whether the pin is defined as an input or
#   an output by the Configuration register.They act only on read operation.
#   Writes to these registers have no effect. The default value(X) is
#   determined by the externally applied logic level. Before a read operation,a
#   write transmission is sent with the command byte to indicate to the I2C
#   device that the Input Port register will be accessed next.
# - Output Port Registers:
#   The Output Port registers (registers 4, 5 and 6) shows the outgoing logic
#   levels of the pins defined as outputs by the Configuration register. Bit
#   values in these registers haven o effect on pins defined as inputs.In turn,
#   reads from these registers reflect the value that is in the flip-flop
#   controlling the output selection, NOT the actual pin value.
# - Polarity Inversion Registers:
#   The Polarity Inversion registers (registers 8, 9 and 10) allow polarity
#   inversion of pins defined as inputs by the Configuration register. If a bit
#   in these registers is set (written with 1), the corresponding port pin's
#   polarity is inverted. If a bit in these registers is cleared (written with
#   a 0), the corresponding port pin's original polarity is retained.
# - Configuration Registers:
#   The Configuration registers (registers 12, 13 and 14) configure the
#   direction of the I/O pins.If a bit in these registers is set to 1, the
#   corresponding port pin is enabled as an input with a high-impedance output
#   driver. If a bit in these registers is cleared to 0, the corresponding port
#   pin is enabled as an output.
#



import McuI2C
import I2CDevice



class I2C_TCA6424A:

    # Message prefixes and separators.
    prefixDetails       = " - "
    separatorDetails    = " - "
    prefixDebug         = "DEBUG: {0:s}: ".format(__file__)
    prefixError         = "ERROR: {0:s}: ".format(__file__)

    # Debug configuration.
    debugLevel          = 0     # Debug verbosity.

    # Hardware parameters.
    hwPortMin           = 0     # Lowest hardware port number.
    hwPortMax           = 2     # Highest hardware port number.



    # Initialize the I2C device.
    def __init__(self, mcuI2C, slaveAddr, deviceName):
        self.mcuI2C = mcuI2C
        self.slaveAddr = slaveAddr
        self.deviceName = deviceName
        self.i2cDevice = I2CDevice.I2CDevice(self.mcuI2C, self.slaveAddr, self.deviceName)
        self.i2cDevice.debugLevel = self.debugLevel
        self.prefixDebugDevice = self.prefixDebug + self.deviceName + ": "
        self.prefixErrorDevice = self.prefixError + self.deviceName + ": "



    # Return the name of a register.
    @classmethod
    def reg_to_name(cls, regAdr):
        if regAdr & 0x0c == 0x00:
            regName = "input logic levels"
        elif regAdr & 0x0c == 0x04:
            regName = "output logic levels"
        elif regAdr & 0x0c == 0x08:
            regName = "polarity inversion register"
        elif regAdr & 0x0c == 0x0c:
            regName = "configuration register"
        else:
            regName = "*reserved*"
        return regName



    # ===============================================================
    # Single port operations.
    # ===============================================================

    # Check the port number.
    def check_port_number(self, port):
        if port < self.hwPortMin or port > self.hwPortMax:
            print(self.prefixErrorDevice + "Hardware port number {0:d} out of valid range {1:d}..{2:d}!".\
                format(port, self.hwPortMin, self.hwPortMax))
            return -1
        return 0



    # Read register value of a port.
    def read_reg_port(self, port, offsetReg):
        self.i2cDevice.debugLevel = self.debugLevel
        if self.check_port_number(port):
            return -1, 0xff
        regName = self.reg_to_name(offsetReg)
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Reading the {0:s} of port {1:d}.".format(regName, port), end='')
            self.i2cDevice.print_details()
        # Assemble command to write.
        dataWr = []
        dataWr.append(port + offsetReg)
        # Write command and read data with repeated start.
        ret, dataRd = self.i2cDevice.write_read(dataWr, 1)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error reading the {0:s} of port {1:d}!".format(regName, port), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1, 0xff
        if not dataRd:
            print(self.prefixErrorDevice + "Error reading the {0:s} of port {1:d}: No data received!".format(regName, port), end='')
            self.i2cDevice.print_details()
            return -1, 0xff
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Read the {0:s} of port {1:d}: 0x{2:02x}.".format(regName, port, dataRd[0]), end='')
            self.i2cDevice.print_details()
        return 0, dataRd[0]



    # Write register value of a port.
    def write_reg_port(self, port, offsetReg, value):
        self.i2cDevice.debugLevel = self.debugLevel
        if self.check_port_number(port):
            return -1
        regName = self.reg_to_name(offsetReg)
        value &= 0xff       # Limit to 8 bits.
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Writing value 0x{0:02x} to the {1:s} of port {2:d}.".format(value, regName, port), end='')
            self.i2cDevice.print_details()
        # Assemble command and data to write.
        dataWr = []
        dataWr.append(port + offsetReg)
        dataWr.append(value)
        # Write command and data.
        ret = self.i2cDevice.write(dataWr)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error writing value 0x{0:02x} to the {1:s} of port {2:d}!".format(value ,regName, port), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Read the input logic levels of a port.
    def read_input_port(self, port):
        ret, value = self.read_reg_port(port, 0x00)
        return ret, value



    # Read the output logic levels of a port.
    def read_output_port(self, port):
        ret, value = self.read_reg_port(port, 0x04)
        return ret, value



    # Read the polarity inversion register of a port.
    def read_polarity_port(self, port):
        ret, value = self.read_reg_port(port, 0x08)
        return ret, value



    # Read the configuration register of a port.
    def read_config_port(self, port):
        ret, value = self.read_reg_port(port, 0x0c)
        return ret, value



    # Write the output logic levels of a port.
    def write_output_port(self, port, value):
        ret = self.write_reg_port(port, 0x04, value)
        return ret



    # Write the polarity inversion register of a port.
    def write_polarity_port(self, port, value):
        ret = self.write_reg_port(port, 0x08, value)
        return ret



    # Write the configuration register of a port.
    def write_config_port(self, port, value):
        ret = self.write_reg_port(port, 0x0c, value)
        return ret



    # ===============================================================
    # Operations for all ports at once.
    # ===============================================================

    # Read register value of all ports.
    def read_reg(self, offsetReg):
        self.i2cDevice.debugLevel = self.debugLevel
        regName = self.reg_to_name(offsetReg)
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Reading the {0:s} of all ports.".format(regName), end='')
            self.i2cDevice.print_details()
        # Assemble command to write.
        dataWr = []
        dataWr.append(0x80 | (offsetReg & 0x7c))    # Set auto-increment bit 0x80.
        # Write command and read data with repeated start.
        ret, dataRd = self.i2cDevice.write_read(dataWr, 3)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error reading the {0:s} of all ports!".format(regName), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1, 0xffffff
        if len(dataRd) != 3:
            print(self.prefixErrorDevice + "Error reading the {0:s} of all ports: Incorrect amount of data received!".format(regName), end='')
            self.i2cDevice.print_details()
            return -1, 0xffffff
        # Calculate value for all ports.
        value  =  0xff & dataRd[0]          # Port 0.
        value |= (0xff & dataRd[1]) << 8    # Port 1.
        value |= (0xff & dataRd[2]) << 16   # Port 2.
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Read the {0:s} of all ports: 0x{1:06x}.".format(regName, value), end='')
            self.i2cDevice.print_details()
        return 0, value



    # Write register value of all ports.
    def write_reg(self, offsetReg, value):
        self.i2cDevice.debugLevel = self.debugLevel
        regName = self.reg_to_name(offsetReg)
        value &= 0xffffff   # Limit to 24 bits.
        # Debug info.
        if self.debugLevel >= 2:
            print(self.prefixDebugDevice + "Writing value 0x{0:06x} to the {1:s} of all ports.".format(value, regName), end='')
            self.i2cDevice.print_details()
        # Assemble command and data to write.
        dataWr = []
        dataWr.append(0x80 | (offsetReg & 0x7c))    # Set auto-increment bit 0x80.
        dataWr.append(value & 0xff)                 # Port 0.
        dataWr.append((value >> 8) & 0xff)          # Port 1.
        dataWr.append((value >> 16) & 0xff)         # Port 2.
        # Write command and data.
        ret = self.i2cDevice.write(dataWr)
        # Evaluate response.
        if ret:
            print(self.prefixErrorDevice + "Error writing value 0x{0:06x} to the {1:s} of all ports!".format(value, regName), end='')
            self.i2cDevice.print_details()
            print(self.prefixErrorDevice + "Error code: {0:d}: ".format(ret))
            return -1
        return 0



    # Read the input logic levels of all ports.
    def read_input(self):
        ret, value = self.read_reg(0x00)
        return ret, value



    # Read the output logic levels of all ports.
    def read_output(self):
        ret, value = self.read_reg(0x04)
        return ret, value



    # Read the polarity inversion register of all ports.
    def read_polarity(self):
        ret, value = self.read_reg(0x08)
        return ret, value



    # Read the configuration register of all ports.
    def read_config(self):
        ret, value = self.read_reg(0x0c)
        return ret, value



    # Write the output logic levels of all ports.
    def write_output(self, value):
        ret = self.write_reg(0x04, value)
        return ret



    # Write the polarity inversion register of all ports.
    def write_polarity(self, value):
        ret = self.write_reg(0x08, value)
        return ret



    # Write the configuration register of all ports.
    def write_config(self, value):
        ret = self.write_reg(0x0c, value)
        return ret

