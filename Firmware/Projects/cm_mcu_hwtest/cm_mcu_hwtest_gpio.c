// File: cm_mcu_hwtest_gpio.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 27 Aug 2020
// Rev.: 27 Aug 2020
//
// GPIO functions of the hardware test firmware running on the ATLAS MDT
// Trigger Processor (TP) Command Module (CM) MCU.
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
#include "cm_mcu_hwtest_gpio.h"
#include "cm_mcu_hwtest_io.h"



// Get/Set the value of a GPIO type.
int GpioGetSet(char *pcCmd, char *pcParam)
{
    char *pcGpioType = pcParam;
    bool bGpioWrite;
    uint32_t ui32GpioSet = 0, ui32GpioGet = 0;

    if (pcGpioType == NULL) {
        UARTprintf("%s: GPIO type required after command `%s'.\n", UI_STR_ERROR, pcCmd);
        GpioGetSetHelp();
        return -1;
    }
    pcParam = strtok(NULL, UI_STR_DELIMITER);
    // Read the current value of the user GPIO pins if no parameter is given.
    if (pcParam == NULL) {
        bGpioWrite = false;
    } else {
        bGpioWrite = true;
        ui32GpioSet = strtol(pcParam, (char **) NULL, 0);
    }
    // GPIO type.
    if (!strcasecmp(pcGpioType, "help")) {
        GpioGetSetHelp();
        return 0;
    } else if (!strcasecmp(pcGpioType, "sm-pwr-en")) {
        if (bGpioWrite) {
            UARTprintf("%s: GPIO %s is read-only!", UI_STR_WARNING, pcGpioType);
            return 1;
        }
        ui32GpioGet = GpioGet_SmPowerEna();
    } else if (!strcasecmp(pcGpioType, "cm-ready")) {
        if (bGpioWrite) GpioSet_CmReady(ui32GpioSet);
        ui32GpioGet =  GpioGet_CmReady();
    } else if (!strcasecmp(pcGpioType, "led-status")) {
        if (bGpioWrite) GpioSet_LedCmStatus(ui32GpioSet);
        ui32GpioGet = GpioGet_LedCmStatus();
    } else if (!strcasecmp(pcGpioType, "led-user")) {
        if (bGpioWrite) GpioSet_LedMcuUser(ui32GpioSet);
        ui32GpioGet = GpioGet_LedMcuUser();
    } else if (!strcasecmp(pcGpioType, "mux-hs-sel")) {
        if (bGpioWrite) GpioSet_MuxSel(ui32GpioSet);
        ui32GpioGet = GpioGet_MuxSel();
    } else if (!strcasecmp(pcGpioType, "mux-hs-pd")) {
        if (bGpioWrite) GpioSet_MuxPD(ui32GpioSet);
        ui32GpioGet =  GpioGet_MuxPD();
    } else if (!strcasecmp(pcGpioType, "mux-clk-sel")) {
        if (bGpioWrite) GpioSet_ClockSel(ui32GpioSet);
        ui32GpioGet = GpioGet_ClockSel();
    } else if (!strcasecmp(pcGpioType, "power")) {
        if (bGpioWrite) GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
    } else if (!strcasecmp(pcGpioType, "kup")) {
        if (bGpioWrite) GpioSet_KupCtrlStat(ui32GpioSet);
        ui32GpioGet = GpioGet_KupCtrlStat();
    } else if (!strcasecmp(pcGpioType, "zup")) {
        if (bGpioWrite) GpioSet_ZupCtrlStat(ui32GpioSet);
        ui32GpioGet = GpioGet_ZupCtrlStat();
    } else if (!strcasecmp(pcGpioType, "reset")) {
        if (bGpioWrite) GpioSet_Reset(ui32GpioSet);
        ui32GpioGet = GpioGet_Reset();
    } else if (!strcasecmp(pcGpioType, "reserved")) {
        if (bGpioWrite) GpioSet_Reserved(ui32GpioSet);
        ui32GpioGet = GpioGet_Reserved();        
    } else if (!strcasecmp(pcGpioType, "pe-int")) {
        if (bGpioWrite) {
            UARTprintf("%s: GPIO %s is read-only!", UI_STR_WARNING, pcGpioType);
            return 1;
        }
        ui32GpioGet = GpioGet_PEInt();
    } else if (!strcasecmp(pcGpioType, "spare")) {
        if (bGpioWrite) GpioSet_SpareKupZup(ui32GpioSet);
        ui32GpioGet = GpioGet_SpareKupZup();
    } else {
        UARTprintf("%s: Unknown GPIO type `%s'!\n", UI_STR_ERROR, pcGpioType);
        GpioGetSetHelp();
        return -1;
    }
    if (bGpioWrite) {
        if (ui32GpioGet == ui32GpioSet) {
            UARTprintf("%s: GPIO %s set to 0x%02x.", UI_STR_OK, pcGpioType, ui32GpioGet);
        } else {
            UARTprintf("%s: Setting GPIO %s to 0x%02x failed!", UI_STR_ERROR, pcGpioType, ui32GpioSet);
            UARTprintf(" It was set to 0x%02x instead.", ui32GpioGet);
        }
    } else {
        UARTprintf("%s: Current GPIO %s value: 0x%02x", UI_STR_OK, pcGpioType, ui32GpioGet);
    }
    return 0;
}



// Show help on GPIO command.
void GpioGetSetHelp(void)
{
    UARTprintf("Available GPIO types:\n");
    UARTprintf("  help                                Show this help text.\n");
    UARTprintf("  sm-pwr-en                           SM power enable driven to CM.\n");
    UARTprintf("  cm-ready                            CM ready signal driven to SM.\n");
    UARTprintf("  led-status                          CM status LEDs.\n");
    UARTprintf("  led-user                            User LEDs.\n");
    UARTprintf("  mux-hs-sel                          High speed signal multiplexer selection.\n");
    UARTprintf("  mux-hs-pd                           High speed signal multiplexer power down.\n");
    UARTprintf("  mux-clk-sel                         Clock multiplexer selection.\n");
    UARTprintf("  power                               Switch on/off power domains.\n");
    UARTprintf("  kup                                 Control/status of the KU15P.\n");
    UARTprintf("  zup                                 Control/status of the ZU11EG.\n");
    UARTprintf("  reset                               Reset for muxes and I2C port expanders.\n");
    UARTprintf("  reserved                            Reserved pins.\n");
    UARTprintf("  pe-int                              Interrupt of I2C port expanders.\n");
    UARTprintf("  spare                               Spare signals routed to KU15P / ZU11EG.");
}

