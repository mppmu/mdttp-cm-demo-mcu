// File: cm_mcu_hwtest.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 08 Apr 2020
// Rev.: 06 Aug 2020
//
// Hardware test firmware running on the ATLAS MDT Trigger Processor (TP)
// Command Module (CM) MCU.
//



#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "driverlib/i2c.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"
#include "utils/ustdlib.h"
#include "hw/adc/adc.h"
#include "hw/gpio/gpio.h"
#include "hw/gpio/gpio_pins.h"
#include "hw/i2c/i2c.h"
#include "hw/uart/uart.h"
#include "uart_ui.h"
#include "power_control.h"
#include "sm_cm.h"
#include "cm_mcu_hwtest.h"
#include "cm_mcu_hwtest_aux.h"
#include "cm_mcu_hwtest_gpio.h"
#include "cm_mcu_hwtest_i2c.h"
#include "cm_mcu_hwtest_io.h"
#include "cm_mcu_hwtest_uart.h"



// The error routine that is called if the driver library encounters an error.
#ifdef DEBUG
void __error__(char *pcFilename, uint32_t ui32Line)
{
    UARTprintf("%s: Unhandled error occurred in file `%s', line %d.\n", UI_STR_FATAL, pcFilename, ui32Line);
}
#endif



// Function prototypes.
void Help(void);
void Info(void);



// Global variables.
tUartUi *g_psUartUi;



// Initialize hardware, get and process commands.
int main(void)
{
    uint32_t ui32SysClock;
    char pcUartStr[UI_STR_BUF_SIZE];
    char *pcUartCmd;
    char *pcUartParam;

    uint8_t ui8McuUserLeds;

    // Setup the system clock.
    ui32SysClock = MAP_SysCtlClockFreqSet(SYSTEM_CLOCK_SETTINGS, SYSTEM_CLOCK_FREQ);

    // Initialize the ADCs.
    AdcReset(&g_sAdc_KUP_MGTAVCC_ADC_AUX_TEMP);
    AdcInit(&g_sAdc_KUP_MGTAVCC_ADC_AUX_TEMP);
    AdcInit(&g_sAdc_KUP_MGTAVTT_TEMP);
    AdcInit(&g_sAdc_KUP_DDR4_IO_EXP_MISC_TEMP);
    AdcReset(&g_sAdc_ZUP_MGTAVCC_MGTAVTT_TEMP);
    AdcInit(&g_sAdc_ZUP_MGTAVCC_MGTAVTT_TEMP);
    AdcInit(&g_sAdc_ZUP_DDR4_IO_ETH_USB_SD_LDO_TEMP);

    // Initialize all GPIO pins.
    GpioInit_All();

    // Initialize the I2C masters.
    for (int i = 0; i < I2C_MASTER_NUM; i++) {
        g_psI2C[i].ui32I2CClk = ui32SysClock;
        I2CMasterInit(&g_psI2C[i]);
    }

    // Initialize power up/down handshaking between the Service Module and the
    // Command Module.
    #ifdef SM_CM_POWER_HANDSHAKING_ENABLE
    SmCm_PowerHandshakingInit();
    #endif

    // Turn on an LED to indicate MCU activity.
    ui8McuUserLeds = 0;
    GpioSet_LedMcuUser(ui8McuUserLeds |= LED_USER_GREEN_0);
    
    // Choose the front panel UART as UI first and check if somebody requests access.
    // Note: This must be done *before* setting up the user UARTs!
    g_psUartUi = &g_sUartUi3;     // Front-panel USB UART.
    #ifdef UI_UART_SELECT
    g_psUartUi->ui32SrcClock = ui32SysClock;
    UartUiInit(g_psUartUi);
    UARTprintf("\nPress any key to use the front panel USB UART.\n");
    // Clear all pending characters to avoid false activation of the front
    // panel USB UART.
    while (UARTCharsAvail(g_psUartUi->ui32Base)) {
        UARTCharGetNonBlocking(g_psUartUi->ui32Base);
    }
    // Wait for key press on the front panel USB UART.
    for (int i = UI_UART_SELECT_TIMEOUT; i >= 0; i--) {
        UARTprintf("%d ", i);
        // Blink the LED with 1 second period.
        // Note: The SysCtlDelay executes a simple 3 instruction cycle loop.
        SysCtlDelay((ui32SysClock / 3e6) * 5e5);
        GpioSet_LedMcuUser(ui8McuUserLeds &= ~LED_USER_BLUE_0);
        SysCtlDelay((ui32SysClock / 3e6) * 5e5);
        GpioSet_LedMcuUser(ui8McuUserLeds |= LED_USER_BLUE_0);
        // Character received on the UART UI.
        if (UARTCharsAvail(g_psUartUi->ui32Base)) break;
    }
    // No character received. => Switch to the SM SoC UART.
    if (!UARTCharsAvail(g_psUartUi->ui32Base)) {
        UARTprintf("\nSwitching to the SM SoC UART. This port will be disabled now.\n");
        // Wait some time for UART to send out the last message.
        SysCtlDelay((ui32SysClock / 3e6) * 1e5);
        GpioSet_LedMcuUser(ui8McuUserLeds &= ~LED_USER_BLUE_0);
        GpioSet_LedMcuUser(ui8McuUserLeds |= LED_USER_BLUE_1);
        g_psUartUi = &g_sUartUi5;     // SM SoC UART.
    }
    #endif  // UI_UART_SELECT
            
    // Initialize the UARTs.
    g_sUart1.ui32UartClk = ui32SysClock;
    g_sUart1.bLoopback = true;      // Enable loopback for testing.
    UartInit(&g_sUart1);
    g_sUart3.ui32UartClk = ui32SysClock;
    g_sUart3.bLoopback = true;      // Enable loopback for testing.
    UartInit(&g_sUart3);
    g_sUart5.ui32UartClk = ui32SysClock;
    g_sUart5.bLoopback = true;      // Enable loopback for testing.
    UartInit(&g_sUart5);

    // Initialize the UART for the user interface.
    // CAUTION: This must be done *after* the initialization of the UARTs.
    //          Otherwise, the UART UI settings would be overwritten.
    g_psUartUi->ui32SrcClock = ui32SysClock;
    UartUiInit(g_psUartUi);

    // Send initial information to the UART UI.
    UARTprintf("\n\n*******************************************************************************\n");
    UARTprintf("MDT-TP CM MCU `%s' firmware version %s, release date: %s\n", FW_NAME, FW_VERSION, FW_RELEASEDATE);
    UARTprintf("*******************************************************************************\n\n");
    UARTprintf("Type `help' to get an overview of available commands.\n");

    GpioSet_LedMcuUser(ui8McuUserLeds |= LED_USER_GREEN_1);

    while(1)
    {
        UARTprintf("%s", UI_COMMAND_PROMPT);
        UARTgets(pcUartStr, UI_STR_BUF_SIZE);
        pcUartCmd = strtok(pcUartStr, UI_STR_DELIMITER);
        pcUartParam = strtok(NULL, UI_STR_DELIMITER);
        if (pcUartCmd == NULL) {
            continue;
        } else if (!strcasecmp(pcUartCmd, "help")) {
            Help();
        } else if (!strcasecmp(pcUartCmd, "info")) {
            Info();
        // Delay execution for a given number of microseconds.
        } else if (!strcasecmp(pcUartCmd, "delay")) {
            DelayUs(pcUartCmd, pcUartParam, ui32SysClock);
        // GPIO based functions.
        } else if (!strcasecmp(pcUartCmd, "gpio")) {
            GpioGetSet(pcUartCmd, pcUartParam);            
        // I2C based functions.
        } else if (!strcasecmp(pcUartCmd, "i2c")) {
            I2CAccess(pcUartCmd, pcUartParam);
        } else if (!strcasecmp(pcUartCmd, "i2c-det")) {
            I2CDetect(pcUartCmd, pcUartParam);
        // Analog temperature functions.
        } else if (!strcasecmp(pcUartCmd, "temp-a")) {
            TemperatureAnalog(pcUartCmd, pcUartParam);
        // UART based functions.
        } else if (!strcasecmp(pcUartCmd, "uart")) {
            UartAccess(pcUartCmd, pcUartParam);
        } else if (!strcasecmp(pcUartCmd, "uart-s")) {
            UartSetup(pcUartCmd, pcUartParam);
        // Power control.
        } else if (!strcasecmp(pcUartCmd, "power")) {
            PowerControl(pcUartCmd, pcUartParam);            
        // Unknown command.
        } else {
            UARTprintf("ERROR: Unknown command `%s'.", pcUartCmd);
        }
        UARTprintf("\n");
        // Update the status LEDs.
        if ((!strcasecmp(pcUartCmd, "gpio")) || (!strcasecmp(pcUartCmd, "power"))) {
            LedCmStatusUpdated();
        }
    }
}



// Show help.
void Help(void)
{
    UARTprintf("Available commands:\n");
    UARTprintf("  help                                Show this help text.\n");
    UARTprintf("  delay   MICROSECONDS                Delay execution.\n");
    UARTprintf("  gpio    TYPE [VALUE]                Get/Set the value of a GPIO type.\n");
    UARTprintf("  i2c     PORT SLV-ADR ACC NUM|DATA   I2C access (ACC bits: R/W, Sr, nP, Q).\n");
    UARTprintf("  i2c-det PORT [MODE]                 I2C detect devices (MODE: 0 = auto,\n");
    UARTprintf("                                          1 = quick command, 2 = read).\n");
    UARTprintf("  info                                Show information about this firmware.\n");
    UARTprintf("  temp-a  [COUNT]                     Read analog temperatures.\n");
    UARTprintf("  uart    PORT R/W NUM|DATA           UART access (R/W: 0 = write, 1 = read).\n");
    UARTprintf("  uart-s  PORT BAUD [PARITY] [LOOP]   Set up the UART port.\n");
    UARTprintf("  power   DOMAIN [MODE]               Power domain control (0 = down, 1 = up).");
}



// Show information.
void Info(void)
{
    UARTprintf("MDT-TP CM MCU `%s' firmware version %s, release date: %s\n", FW_NAME, FW_VERSION, FW_RELEASEDATE);
    UARTprintf("It was compiled using gcc %s at %s on %s.", __VERSION__, __TIME__, __DATE__);
}

