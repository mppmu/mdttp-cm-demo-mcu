// File: power_control.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Jul 2020
// Rev.: 24 Jul 2020
//
// Header file of the power control functions for the hardware test firmware
// running on the ATLAS MDT Trigger Processor (TP) Command Module (CM) MCU.
//



#ifndef __POWER_CONTROL_H__
#define __POWER_CONTROL_H__



// Hardware constants.
#define POWER_KU15P_CORE                0x01
#define POWER_KU15P_P3V3_IO             0x02
#define POWER_KU15P_DDR4_TERM_EN        0x04
#define POWER_KU15P                     (POWER_KU15P_CORE | POWER_KU15P_P3V3_IO | POWER_KU15P_DDR4_TERM_EN)
#define POWER_ZU11EG_CORE               0x08
#define POWER_ZU11EG_PS_DDR4_TERM_EN    0x10
#define POWER_ZU11EG_PL_DDR4_TERM_EN    0x20
#define POWER_ZU11EG                    (POWER_ZU11EG_CORE | POWER_ZU11EG_PS_DDR4_TERM_EN | POWER_ZU11EG_PL_DDR4_TERM_EN)
#define POWER_FIREFLY_P1V8              0x40
#define POWER_FIREFLY_P3V3              0x80
// There is a problem when both the 1.8 V and 3.3 V supply of the FireFly
// modules is turned on at the same time. The MCU reboots then. According to Mr.
// Kohl, the FireFly modules used on the Command Module don't need the 1.8 V.
// So as a fix, the 1.8 V is excluded from the total FireFly power.
//#define POWER_FIREFLY                   (POWER_FIREFLY_P1V8 | POWER_FIREFLY_P3V3)
#define POWER_FIREFLY                   (POWER_FIREFLY_P3V3)
#define POWER_ALL                       (POWER_KU15P | POWER_ZU11EG | POWER_FIREFLY)
#define POWER_RESERVED_CLOCK            0x01
#define POWER_RESERVED_KU15P            0x02
#define POWER_RESERVED_ZU11EG           0x04
#define POWER_RESERVED_CLOCK_KU15P      (POWER_RESERVED_CLOCK | POWER_RESERVED_KU15P)
#define POWER_RESERVED_CLOCK_ZU11EG     (POWER_RESERVED_CLOCK | POWER_RESERVED_ZU11EG)
#define POWER_RESERVED_ALL              (POWER_RESERVED_CLOCK | POWER_RESERVED_KU15P | POWER_RESERVED_ZU11EG)



// Function prototypes.
int PowerControl(char *pcCmd, char *pcParam);
void PowerControlHelp(void);
int PowerControl_All(bool bPowerSet, uint32_t ui32PowerVal);
int PowerControl_Clock(bool bPowerSet, uint32_t ui32PowerVal);
int PowerControl_FireFly(bool bPowerSet, uint32_t ui32PowerVal);
int PowerControl_KU15P(bool bPowerSet, uint32_t ui32PowerVal);
int PowerControl_ZU11EG(bool bPowerSet, uint32_t ui32PowerVal);



#endif  // __POWER_CONTROL_H__

