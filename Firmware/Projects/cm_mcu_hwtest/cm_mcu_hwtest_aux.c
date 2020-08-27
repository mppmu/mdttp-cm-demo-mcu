// File: cm_mcu_hwtest_aux.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 27 Aug 2020
// Rev.: 27 Aug 2020
//
// Auxiliary functions of the hardware test firmware running on the ATLAS MDT
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
#include "cm_mcu_hwtest_aux.h"
#include "cm_mcu_hwtest_io.h"



// Delay execution for a given number of microseconds.
int DelayUs(char *pcCmd, char *pcParam, uint32_t ui32SysClock)
{
    uint32_t ui32DelayUs;

    if (pcParam == NULL) {
        UARTprintf("%s: Parameter required after command `%s'.", UI_STR_ERROR, pcCmd);
        return -1;
    }
    ui32DelayUs = strtoul(pcParam, (char **) NULL, 0);
    // Limit the delay to max. 10 seconds.
    if (ui32DelayUs > 1e7) ui32DelayUs = 1e7;
    // CAUTION: Calling SysCtlDelay(0) will hang the system.
    if (ui32DelayUs > 0)
        // Note: The SysCtlDelay executes a simple 3 instruction cycle loop.
        SysCtlDelay((ui32SysClock / 3e6) * ui32DelayUs);

    UARTprintf("%s.", UI_STR_OK);

    return 0;
}



// Update the status LEDs.
int LedCmStatusUpdated(void)
{
    uint32_t ui32LedCmStatus = 0;

    // Clock power domain.
    ui32LedCmStatus = GpioGet_LedCmStatus();
    if (GpioGet_Reserved() & POWER_RESERVED_CLOCK)
        ui32LedCmStatus |= LED_CM_STATUS_CLOCK;
    else
        ui32LedCmStatus &= ~LED_CM_STATUS_CLOCK;
    GpioSet_LedCmStatus(ui32LedCmStatus);

    // KU15P power domain.
    ui32LedCmStatus = GpioGet_LedCmStatus();
    if((GpioGet_PowerCtrl() & POWER_KU15P) && (GpioGet_Reserved() & POWER_RESERVED_KU15P))
        ui32LedCmStatus |= LED_CM_STATUS_KU15P;
    else
        ui32LedCmStatus &= ~LED_CM_STATUS_KU15P;
    GpioSet_LedCmStatus(ui32LedCmStatus);

    // ZU11EG power domain.
    ui32LedCmStatus = GpioGet_LedCmStatus();
    if((GpioGet_PowerCtrl() & POWER_ZU11EG) && (GpioGet_Reserved() & POWER_RESERVED_ZU11EG))
        ui32LedCmStatus |= LED_CM_STATUS_ZU11EG;
    else
        ui32LedCmStatus &= ~LED_CM_STATUS_ZU11EG;
    GpioSet_LedCmStatus(ui32LedCmStatus);

    // Temperature alert.
    // TODO.
    ui32LedCmStatus &= ~LED_CM_STATUS_TEMP_ALERT;
    GpioSet_LedCmStatus(ui32LedCmStatus);

    return 0;
}



// Read analog temperatures.
int TemperatureAnalog(char *pcCmd, char *pcParam)
{
    uint32_t ui32Adc;
    int iCnt;

    if (pcParam == NULL) {
        iCnt = 1;
    } else {
        iCnt = strtoul(pcParam, (char **) NULL, 0) & 0xffffff;
    }

    for (int i = 0; i < iCnt; i++) {
        UARTprintf("%s: ", UI_STR_OK);
        #ifdef TEMP_RAW_ADC_HEX
        ui32Adc = AdcConvert(&g_sAdc_KUP_MGTAVCC_ADC_AUX_TEMP);
        UARTprintf("KUP MGTAVCC/ADC/AUX: 0x%03x", ui32Adc);
        ui32Adc = AdcConvert(&g_sAdc_KUP_MGTAVTT_TEMP);
        UARTprintf(", KUP MGTAVTT: 0x%03x", ui32Adc);
        ui32Adc = AdcConvert(&g_sAdc_KUP_DDR4_IO_EXP_MISC_TEMP);
        UARTprintf(", KUP DDR4/IO/Exp. Con./Misc.: 0x%03x", ui32Adc);
        ui32Adc = AdcConvert(&g_sAdc_ZUP_MGTAVCC_MGTAVTT_TEMP);
        UARTprintf(", ZUP MGTAVCC/MGTAVTT: 0x%03x", ui32Adc);
        ui32Adc = AdcConvert(&g_sAdc_ZUP_DDR4_IO_ETH_USB_SD_LDO_TEMP);
        UARTprintf(", ZUP DDR4/IO/LDO/Misc.: 0x%03x", ui32Adc);
        #else
        ui32Adc = AdcConvert(&g_sAdc_KUP_MGTAVCC_ADC_AUX_TEMP);
        UARTprintf("KUP MGTAVCC/ADC/AUX: %s degC", (int) Adc2TempStr(ui32Adc));
        ui32Adc = AdcConvert(&g_sAdc_KUP_MGTAVTT_TEMP);
        UARTprintf(", KUP MGTAVTT: %s degC", (int) Adc2TempStr(ui32Adc));
        ui32Adc = AdcConvert(&g_sAdc_KUP_DDR4_IO_EXP_MISC_TEMP);
        UARTprintf(", KUP DDR4/IO/Exp. Con./Misc.: %s degC", (int) Adc2TempStr(ui32Adc));
        ui32Adc = AdcConvert(&g_sAdc_ZUP_MGTAVCC_MGTAVTT_TEMP);
        UARTprintf(", ZUP MGTAVCC/MGTAVTT: %s degC", (int) Adc2TempStr(ui32Adc));
        ui32Adc = AdcConvert(&g_sAdc_ZUP_DDR4_IO_ETH_USB_SD_LDO_TEMP);
        UARTprintf(", ZUP DDR4/IO/LDO/Misc.: %s degC", (int) Adc2TempStr(ui32Adc));
        #endif
        if (i < iCnt - 1) {
            SysCtlDelay(1000000);
            UARTprintf("\n");
        }
    }

    return 0;
}



// Calculate temperature value in degC from ADC counts.
float Adc2Temp(uint32_t ui32Adc)
{
    // Convert voltag to temperature. See datasheet of the LTM4644 device,
    // section "temperature monitoring".
    // T = -(V_G0 - V_D) / (dV_D / dT)
    // T = -(1200mV - voltage) / (-2 mV/K)
    // Voltage [mV] = (3300 / 0xfff) * ADC counts

    float fVolt = ((float) 3300 / 0xfff) * ui32Adc;
    float fTempDegK = ((float) 1200 - fVolt) / 2;
    float fTempDegC = fTempDegK - 273.15;

    return fTempDegC;
}



// Calculate temperature value from ADC counts and format it into a string.
char *Adc2TempStr(uint32_t ui32Adc)
{
    static char pcTempStr[24];
    float fTemp;

    fTemp = Adc2Temp(ui32Adc);
    usprintf(pcTempStr, "%3d.%02d", (int) fTemp, (int) abs((fTemp - (int) fTemp) * 100));

    return pcTempStr;
}

