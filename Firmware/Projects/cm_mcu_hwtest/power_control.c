// File: power_control.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Jul 2020
// Rev.: 24 Jul 2020
//
// Power control functions for the hardware test firmware running on the ATLAS
// MDT Trigger Processor (TP) Command Module (CM) MCU.
//



#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "utils/uartstdio.h"
#include "hw/gpio/gpio_pins.h"
#include "power_control.h"
#include "cm_mcu_hwtest.h"



// Control power domains.
int PowerControl(char *pcCmd, char *pcParam)
{
    char *pcPowerDomain = pcParam;
    bool bPowerSet = false;
    uint32_t ui32PowerVal = 0;
    int status = 0;

    if (pcPowerDomain == NULL) {
        UARTprintf("%s: Power domain required after command `%s'.\n", UI_STR_ERROR, pcCmd);
        PowerControlHelp();
        return -1;
    }
    pcParam = strtok(NULL, UI_STR_DELIMITER);
    // Read the current value of a power domain if no parameter is given.
    if (pcParam == NULL) {
        bPowerSet = false;
    } else {
        bPowerSet = true;
        ui32PowerVal = strtol(pcParam, (char **) NULL, 0);
    }
    // Power domain.
    if (!strcasecmp(pcPowerDomain, "help")) {
        PowerControlHelp();
        return 0;
    } else if (!strcasecmp(pcPowerDomain, "all")) {
        status = PowerControl_All(bPowerSet, ui32PowerVal);
    } else if (!strcasecmp(pcPowerDomain, "clock")) {
        status = PowerControl_Clock(bPowerSet, ui32PowerVal);
    } else if (!strcasecmp(pcPowerDomain, "firefly")) {
        status = PowerControl_FireFly(bPowerSet, ui32PowerVal);
    } else if (!strcasecmp(pcPowerDomain, "kup")) {
        status = PowerControl_KU15P(bPowerSet, ui32PowerVal);
    } else if (!strcasecmp(pcPowerDomain, "zup")) {
        status = PowerControl_ZU11EG(bPowerSet, ui32PowerVal);
    } else {
        UARTprintf("%s: Unknown power domains `%s'!\n", UI_STR_ERROR, pcPowerDomain);
        PowerControlHelp();
        return -1;
    }

    if (bPowerSet && !status) {
        UARTprintf("%s.", UI_STR_OK);
    }

    return status;
}



// Show help on power control command.
void PowerControlHelp(void)
{
    UARTprintf("Available domains:\n");
    UARTprintf("  help                                Show this help text.\n");
    UARTprintf("  all                                 All switchable power domains.\n");
    UARTprintf("  clock                               Clock power domain.\n");
    UARTprintf("  firefly                             FireFly power domain.\n");
    UARTprintf("  kup                                 KU15P power, incl. clock domain.\n");
    UARTprintf("  zup                                 ZU11EG power, incl. clock domain.");
}



// Power control for all power domains.
int PowerControl_All(bool bPowerSet, uint32_t ui32PowerVal)
{
    uint32_t ui32GpioGet;
    int status;

    // Get the power status of all power domains.
    if (!bPowerSet) {
        uint32_t ui32GpioGetReserved;
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioGetReserved = GpioGet_Reserved();
        if (((ui32GpioGet & POWER_ALL) == POWER_ALL) && ((ui32GpioGetReserved & POWER_RESERVED_ALL) == POWER_RESERVED_ALL)) {
            UARTprintf("%s: All power domains are completely ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if (((ui32GpioGet & POWER_ALL) == 0) && ((ui32GpioGetReserved & POWER_RESERVED_ALL) == 0)) {
            UARTprintf("%s: All power domains are completely OFF. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else {
            UARTprintf("%s: The power domains are PARTIALLY ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_ERROR, ui32GpioGet, ui32GpioGetReserved);
            return -1;
        }
    // Set the power status of all power domains.
    } else {
        // Power up the clock domain first.
        if (ui32PowerVal != 0) {
            // Set the power of the clock domain.
            status = PowerControl_Clock(bPowerSet, ui32PowerVal);
            if (status) return status;
        }
        // Set the power of the KU15P.
        status = PowerControl_KU15P(bPowerSet, ui32PowerVal);
        if (status) return status;
        // Set the power of the ZU11EG.
        status = PowerControl_ZU11EG(bPowerSet, ui32PowerVal);
        if (status) return status;
        // Set the power of the FireFly domain.
        status = PowerControl_FireFly(bPowerSet, ui32PowerVal);
        if (status) return status;
        // Power down the clock domain last.
        if (ui32PowerVal == 0) {
            // Set the power of the clock domain.
            status = PowerControl_Clock(bPowerSet, ui32PowerVal);
            if (status) return status;
        }
    }

    return 0;
}



// Power control for the clock domain.
int PowerControl_Clock(bool bPowerSet, uint32_t ui32PowerVal)
{
    uint32_t ui32GpioGet = 0, ui32GpioSet = 0;

    // Get the power status of the clock domain.
    if (!bPowerSet) {
        uint32_t ui32GpioGetReserved;
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioGetReserved = GpioGet_Reserved();
        if ((ui32GpioGetReserved & POWER_RESERVED_CLOCK) == POWER_RESERVED_CLOCK) {
            UARTprintf("%s: The clock power is completely ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if ((ui32GpioGetReserved & POWER_RESERVED_CLOCK) == 0) {
            UARTprintf("%s: The clock power is completely OFF. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else {
            UARTprintf("%s: The clock power is PARTIALLY ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_ERROR, ui32GpioGet, ui32GpioGetReserved);
            return -1;
        }
    }

    // Power down the clock domain.
    if (ui32PowerVal == 0) {
        ui32GpioGet = GpioGet_Reserved();
        // Check if the KU15P or the ZU11EG are powered.
        if ((ui32GpioGet & (POWER_RESERVED_KU15P | POWER_RESERVED_ZU11EG)) != 0) {
            UARTprintf("%s: Cannot power off the clock domain while the KU15P or the ZU11EG are powered. Turn them off first.", UI_STR_ERROR);
            return -1;
        } else {
            ui32GpioSet = ui32GpioGet & (~POWER_RESERVED_CLOCK);
            GpioSet_Reserved(ui32GpioSet);
            ui32GpioGet = GpioGet_Reserved();
            if (ui32GpioGet != ui32GpioSet) {
                UARTprintf("%s: Could not power down the clock domain.\n", UI_STR_ERROR);
                return -1;
            }
        }
    // Power up the clock domain.
    } else {
        ui32GpioGet = GpioGet_Reserved();
        ui32GpioSet = ui32GpioGet | POWER_RESERVED_CLOCK;
        GpioSet_Reserved(ui32GpioSet);
        ui32GpioGet = GpioGet_Reserved();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the clock domain.\n", UI_STR_ERROR);
            return -1;
        }
    }

    return 0;
}



// Power control for the FireFly domain.
int PowerControl_FireFly(bool bPowerSet, uint32_t ui32PowerVal)
{
    uint32_t ui32GpioGet = 0, ui32GpioSet = 0;

    // Get the power status of the FireFly domain.
    if (!bPowerSet) {
        uint32_t ui32GpioGetReserved;
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioGetReserved = GpioGet_Reserved();
        if ((ui32GpioGet & POWER_FIREFLY) == POWER_FIREFLY) {
            UARTprintf("%s: The FireFly power is completely ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if ((ui32GpioGet & POWER_FIREFLY) == 0) {
            UARTprintf("%s: The FireFly power is completely OFF. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else {
            UARTprintf("%s: The clock power is PARTIALLY ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_ERROR, ui32GpioGet, ui32GpioGetReserved);
            return -1;
        }
    }

    // Power down the FireFly domain.
    if (ui32PowerVal == 0) {
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet & (~POWER_FIREFLY);
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the FireFly domain.\n", UI_STR_ERROR);
            return -1;
        }
    // Power up the FireFly domain.
    } else {
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet | POWER_FIREFLY;
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the FireFly domain.\n", UI_STR_ERROR);
            return -1;
        }
    }

    return 0;
}



// Power control for the KU15P.
int PowerControl_KU15P(bool bPowerSet, uint32_t ui32PowerVal)
{
    uint32_t ui32GpioGet = 0, ui32GpioSet = 0;

    // Get the power status of the KU15P.
    if (!bPowerSet) {
        uint32_t ui32GpioGetReserved;
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioGetReserved = GpioGet_Reserved();
        if (((ui32GpioGet & POWER_KU15P) == POWER_KU15P) && ((ui32GpioGetReserved & POWER_RESERVED_CLOCK_KU15P) == POWER_RESERVED_CLOCK_KU15P)) {
            UARTprintf("%s: The KU15P power is completely ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if (((ui32GpioGet & POWER_KU15P) == 0) && ((ui32GpioGetReserved & POWER_RESERVED_CLOCK_KU15P) == 0)) {
            UARTprintf("%s: The KU15P power is completely OFF. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if (((ui32GpioGet & POWER_KU15P) == 0) && ((ui32GpioGetReserved & POWER_RESERVED_CLOCK_KU15P) == POWER_RESERVED_CLOCK)) {
            UARTprintf("%s: The KU15P power is OFF, but the clock domain power is ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else {
            UARTprintf("%s: The KU15P power is PARTIALLY ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_ERROR, ui32GpioGet, ui32GpioGetReserved);
            return -1;
        }
    }

    // Power down the KU15P.
    if (ui32PowerVal == 0) {
        // Power down P3V3_IO first.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet & (~POWER_KU15P_P3V3_IO);
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the KU15P 3.3 V IO.", UI_STR_ERROR);
            return -1;
        }
        // Then power down the peripherals.
        ui32GpioGet = GpioGet_Reserved();
        ui32GpioSet = ui32GpioGet & (~POWER_RESERVED_KU15P);
        GpioSet_Reserved(ui32GpioSet);
        ui32GpioGet = GpioGet_Reserved();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the KU15P peripherals.", UI_STR_ERROR);
            return -1;
        }
        // Then power down the core.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet & (~POWER_KU15P_CORE);
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the KU15P core.", UI_STR_ERROR);
            return -1;
        }
        // Then power down the DDR4 termination.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet & (~POWER_KU15P_DDR4_TERM_EN);
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the KU15P DDR4 termination.", UI_STR_ERROR);
            return -1;
        }
    // Power up the KU15P.
    } else {
        // Power up the core first.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet | POWER_KU15P_CORE;
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
          UARTprintf("%s: Could not power up the KU15P core.\n", UI_STR_ERROR);
          return -1;
        }
        // Then power up the DDR4 termination.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet | POWER_KU15P_DDR4_TERM_EN;
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the KU15P DDR4 termination.", UI_STR_ERROR);
            return -1;
        }
        // Then power up the peripherals.
        ui32GpioGet = GpioGet_Reserved();
        // Turn on both the KU15P and the clock domain, otherwise you will get a PGOOD error.
        ui32GpioSet = ui32GpioGet | POWER_RESERVED_CLOCK_KU15P;
        GpioSet_Reserved(ui32GpioSet);
        ui32GpioGet = GpioGet_Reserved();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the KU15P peripherals.\n", UI_STR_ERROR);
            return -1;
        }
        // Then power up the P3V3_IO.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet | POWER_KU15P_P3V3_IO;
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the KU15P 3.3 V IO.\n", UI_STR_ERROR);
            return -1;
        }
    }

    return 0;
}



// Power control for the ZU11EG.
int PowerControl_ZU11EG(bool bPowerSet, uint32_t ui32PowerVal)
{
    uint32_t ui32GpioGet = 0, ui32GpioSet = 0;

    // Get the power status of the ZU11EG.
    if (!bPowerSet) {
        uint32_t ui32GpioGetReserved;
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioGetReserved = GpioGet_Reserved();
        if (((ui32GpioGet & POWER_ZU11EG) == POWER_ZU11EG) && ((ui32GpioGetReserved & POWER_RESERVED_CLOCK_ZU11EG) == POWER_RESERVED_CLOCK_ZU11EG)) {
            UARTprintf("%s: The ZU11EG power is completely ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if (((ui32GpioGet & POWER_ZU11EG) == 0) && ((ui32GpioGetReserved & POWER_RESERVED_CLOCK_ZU11EG) == 0)) {
            UARTprintf("%s: The ZU11EG power is completely OFF. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else if (((ui32GpioGet & POWER_ZU11EG) == 0) && ((ui32GpioGetReserved & POWER_RESERVED_CLOCK_ZU11EG) == POWER_RESERVED_CLOCK)) {
            UARTprintf("%s: The ZU11EG power is OFF, but the clock domain power is ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_OK, ui32GpioGet, ui32GpioGetReserved);
            return 0;
        } else {
            UARTprintf("%s: The ZU11EG power is PARTIALLY ON. GPIO power = 0x%02x, GPIO reserved = 0x%02x", UI_STR_ERROR, ui32GpioGet, ui32GpioGetReserved);
            return -1;
        }
    }

    // Power down the ZU11EG.
    if (ui32PowerVal == 0) {
        // Power down the peripherals first.
        ui32GpioGet = GpioGet_Reserved();
        ui32GpioSet = ui32GpioGet & (~POWER_RESERVED_ZU11EG);
        GpioSet_Reserved(ui32GpioSet);
        ui32GpioGet = GpioGet_Reserved();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the ZU11EG peripherals.\n", UI_STR_ERROR);
            return -1;
        }
        // Then power down the core.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet & (~POWER_ZU11EG_CORE);
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the ZU11EG core.\n", UI_STR_ERROR);
            return -1;
        }
        // Then power down the DDR4 termination.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet & (~(POWER_ZU11EG_PS_DDR4_TERM_EN | POWER_ZU11EG_PL_DDR4_TERM_EN));
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power down the ZU11EG DDR4 termination.", UI_STR_ERROR);
            return -1;
        }
    // Power up the ZU11EG.
    } else {
        // Power up the core first.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet | POWER_ZU11EG_CORE;
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the ZU11EG core.\n", UI_STR_ERROR);
            return -1;
        }
        // Then power up the DDR4 termination.
        ui32GpioGet = GpioGet_PowerCtrl();
        ui32GpioSet = ui32GpioGet | (POWER_ZU11EG_PS_DDR4_TERM_EN | POWER_ZU11EG_PL_DDR4_TERM_EN);
        GpioSet_PowerCtrl(ui32GpioSet);
        ui32GpioGet = GpioGet_PowerCtrl();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the ZU11EG DDR4 termination.", UI_STR_ERROR);
            return -1;
        }
        // Then power up the peripherals.
        ui32GpioGet = GpioGet_Reserved();
        // Turn on both the ZU11EG and the clock domain, otherwise you will get a PGOOD error.
        ui32GpioSet = ui32GpioGet | POWER_RESERVED_CLOCK_ZU11EG;
        GpioSet_Reserved(ui32GpioSet);
        ui32GpioGet = GpioGet_Reserved();
        if (ui32GpioGet != ui32GpioSet) {
            UARTprintf("%s: Could not power up the ZU11EG peripherals.\n", UI_STR_ERROR);
            return -1;
        }
    }

    return 0;
}

