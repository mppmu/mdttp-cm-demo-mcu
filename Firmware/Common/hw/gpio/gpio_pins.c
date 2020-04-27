// File: gpio_pins.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Apr 2020
// Rev.: 27 Apr 2020
//
// GPIO pin definitions and functions for the TI Tiva TM4C1290 MCU on the ATLAS
// MDT Trigger Processor (TP) Command Module (CM).
//



#include <stdbool.h>
#include <stdint.h>
#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "gpio.h"
#include "gpio_pins.h"



// ******************************************************************
// Service Module power enable,
// ******************************************************************

// SM_PWR_ENA: PN3
tGPIO g_sGpio_SmPwerEna = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};



// Initialize the Service Module power enable GPIO.
void GpioInit_SmPowerEna(void)
{
    GpioInit(&g_sGpio_SmPwerEna);
}

// Read the Service Module power enable GPIO.
uint32_t GpioGet_SmPowerEna(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioInputGetBool(&g_sGpio_SmPwerEna) & 0x1) << 0;

    return ui32Val;
}



// ******************************************************************
// Command Module ready.
// ******************************************************************

// CM_READY: PN2
tGPIO g_sGpio_CmReady = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_CmReady(void)
{
    GpioInit(&g_sGpio_CmReady);
}

void GpioSet_CmReady(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_CmReady, (bool) (ui32Val & 0x01));
}

uint32_t GpioGet_CmReady(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_CmReady) & 0x1) << 0;

    return ui32Val;
}



// ******************************************************************
// Command Module status LEDs.
// ******************************************************************

// KUP_DOMAIN_PG: PN4
tGPIO g_sGpio_LedCmStatus0 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_DOMAIN_PG: PN5
tGPIO g_sGpio_LedCmStatus1 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// CLK_DOMAIN_PG: PQ0
tGPIO g_sGpio_LedCmStatus2 = {
    SYSCTL_PERIPH_GPIOQ,
    GPIO_PORTQ_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// TEMP_ERROR: PQ1
tGPIO g_sGpio_LedCmStatus3 = {
    SYSCTL_PERIPH_GPIOQ,
    GPIO_PORTQ_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_LedCmStatus(void)
{
    GpioInit(&g_sGpio_LedCmStatus0);
    GpioInit(&g_sGpio_LedCmStatus1);
    GpioInit(&g_sGpio_LedCmStatus2);
    GpioInit(&g_sGpio_LedCmStatus3);
}

void GpioSet_LedCmStatus(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_LedCmStatus0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_LedCmStatus1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_LedCmStatus2, (bool) (ui32Val & 0x04));
    GpioOutputSetBool(&g_sGpio_LedCmStatus3, (bool) (ui32Val & 0x08));
}

uint32_t GpioGet_LedCmStatus(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedCmStatus0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedCmStatus1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedCmStatus2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedCmStatus3) & 0x1) << 3;

    return ui32Val;
}



// ******************************************************************
// MCU user LEDs.
// ******************************************************************

// MCU_USER_LED0: PM0
tGPIO g_sGpio_LedMcuUser0 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED1: PM1
tGPIO g_sGpio_LedMcuUser1 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED2: PM2
tGPIO g_sGpio_LedMcuUser2 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED3: PM3
tGPIO g_sGpio_LedMcuUser3 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED4: PM4
tGPIO g_sGpio_LedMcuUser4 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED5: PM5
tGPIO g_sGpio_LedMcuUser5 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED6: PM6
tGPIO g_sGpio_LedMcuUser6 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED7: PM7
tGPIO g_sGpio_LedMcuUser7 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

// Initialize the MCU user LEDs.
void GpioInit_LedMcuUser(void)
{
    GpioInit(&g_sGpio_LedMcuUser0);
    GpioInit(&g_sGpio_LedMcuUser1);
    GpioInit(&g_sGpio_LedMcuUser2);
    GpioInit(&g_sGpio_LedMcuUser3);
    GpioInit(&g_sGpio_LedMcuUser4);
    GpioInit(&g_sGpio_LedMcuUser5);
    GpioInit(&g_sGpio_LedMcuUser6);
    GpioInit(&g_sGpio_LedMcuUser7);
}

// Set the MCU user LEDs.
void GpioSet_LedMcuUser(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_LedMcuUser0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_LedMcuUser1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_LedMcuUser2, (bool) (ui32Val & 0x04));
    GpioOutputSetBool(&g_sGpio_LedMcuUser3, (bool) (ui32Val & 0x08));
    GpioOutputSetBool(&g_sGpio_LedMcuUser4, (bool) (ui32Val & 0x10));
    GpioOutputSetBool(&g_sGpio_LedMcuUser5, (bool) (ui32Val & 0x20));
    GpioOutputSetBool(&g_sGpio_LedMcuUser6, (bool) (ui32Val & 0x40));
    GpioOutputSetBool(&g_sGpio_LedMcuUser7, (bool) (ui32Val & 0x80));
}

// Read back the MCU user LEDs.
uint32_t GpioGet_LedMcuUser(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser3) & 0x1) << 3;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser4) & 0x1) << 4;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser5) & 0x1) << 5;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser6) & 0x1) << 6;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_LedMcuUser7) & 0x1) << 7;

    return ui32Val;
}



// ******************************************************************
// High speed signal multiplexer selection.
// ******************************************************************

// B2B_MUX1_SEL: PA2
tGPIO g_sGpio_MuxSel0 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// B2B_MUX2_SEL: PA4
tGPIO g_sGpio_MuxSel1 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// LTTC_MUX_SEL: PC4
tGPIO g_sGpio_MuxSel2 = {
    SYSCTL_PERIPH_GPIOC,
    GPIO_PORTC_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_MuxSel(void)
{
    GpioInit(&g_sGpio_MuxSel0);
    GpioInit(&g_sGpio_MuxSel1);
    GpioInit(&g_sGpio_MuxSel2);
}

void GpioSet_MuxSel(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_MuxSel0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_MuxSel1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_MuxSel2, (bool) (ui32Val & 0x04));
}

uint32_t GpioGet_MuxSel(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_MuxSel0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_MuxSel1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_MuxSel2) & 0x1) << 2;

    return ui32Val;
}



// ******************************************************************
// High speed signal multiplexer power down.
// ******************************************************************

// B2B_MUX1_PD: PA2
tGPIO g_sGpio_MuxPD0 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// B2B_MUX2_PD: PA4
tGPIO g_sGpio_MuxPD1 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// LTTC_MUX_PD: PC4
tGPIO g_sGpio_MuxPD2 = {
    SYSCTL_PERIPH_GPIOC,
    GPIO_PORTC_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_MuxPD(void)
{
    GpioInit(&g_sGpio_MuxPD0);
    GpioInit(&g_sGpio_MuxPD1);
    GpioInit(&g_sGpio_MuxPD2);
}

void GpioSet_MuxPD(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_MuxPD0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_MuxPD1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_MuxPD2, (bool) (ui32Val & 0x04));
}

uint32_t GpioGet_MuxPD(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_MuxPD0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_MuxPD1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_MuxPD2) & 0x1) << 2;

    return ui32Val;
}




// ******************************************************************
// Clock multiplexer selection.
// ******************************************************************

// AD_CLK5_ZUP_SEL: PN0
tGPIO g_sGpio_ClockSel0 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// CLK_LHC_FPGA_SEL: PN1
tGPIO g_sGpio_ClockSel1 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_ClockSel(void)
{
    GpioInit(&g_sGpio_ClockSel0);
    GpioInit(&g_sGpio_ClockSel1);
}

void GpioSet_ClockSel(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_ClockSel0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_ClockSel1, (bool) (ui32Val & 0x02));
}

uint32_t GpioGet_ClockSel(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel1) & 0x1) << 1;

    return ui32Val;
}



// ******************************************************************
// Power control.
// ******************************************************************

// KUP_CORE_RUN: PF3
tGPIO g_sGpio_PowerCtrl0 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_CORE_RUN: PD6
tGPIO g_sGpio_PowerCtrl1 = {
    SYSCTL_PERIPH_GPIOD,
    GPIO_PORTD_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// FIREFY_P1V8_RUN: PF1
tGPIO g_sGpio_PowerCtrl2 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// FIREFY_P3V3_RUN: PF2
tGPIO g_sGpio_PowerCtrl3 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_DDR4_TERM_EN: PF4
tGPIO g_sGpio_PowerCtrl4 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_DDR4_TERM_EN: PD7
tGPIO g_sGpio_PowerCtrl5 = {
    SYSCTL_PERIPH_GPIOD,
    GPIO_PORTD_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PL_DDR4_TERM_EN: PF0
tGPIO g_sGpio_PowerCtrl6 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_PowerCtrl(void)
{
    GpioInit(&g_sGpio_PowerCtrl0);
    GpioInit(&g_sGpio_PowerCtrl1);
    GpioInit(&g_sGpio_PowerCtrl2);
    GpioInit(&g_sGpio_PowerCtrl3);
    GpioInit(&g_sGpio_PowerCtrl4);
    GpioInit(&g_sGpio_PowerCtrl5);
    GpioInit(&g_sGpio_PowerCtrl6);
}

void GpioSet_PowerCtrl(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_PowerCtrl0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_PowerCtrl1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_PowerCtrl2, (bool) (ui32Val & 0x04));
    GpioOutputSetBool(&g_sGpio_PowerCtrl3, (bool) (ui32Val & 0x08));
    GpioOutputSetBool(&g_sGpio_PowerCtrl4, (bool) (ui32Val & 0x10));
    GpioOutputSetBool(&g_sGpio_PowerCtrl5, (bool) (ui32Val & 0x20));
    GpioOutputSetBool(&g_sGpio_PowerCtrl6, (bool) (ui32Val & 0x40));
}

uint32_t GpioGet_PowerCtrl(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl3) & 0x1) << 3;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl4) & 0x1) << 4;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl5) & 0x1) << 5;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl6) & 0x1) << 6;

    return ui32Val;
}



// ******************************************************************
// Control/status of the KU15P.
// ******************************************************************

// KUP_PROG_B_3V3: PK6
tGPIO g_sGpio_KupCtrlStat0 = {
    SYSCTL_PERIPH_GPIOK,
    GPIO_PORTK_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_DONE_3V3: PK7
tGPIO g_sGpio_KupCtrlStat1 = {
    SYSCTL_PERIPH_GPIOK,
    GPIO_PORTK_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_INIT_B_3V3: PK5
tGPIO g_sGpio_KupCtrlStat2 = {
    SYSCTL_PERIPH_GPIOK,
    GPIO_PORTK_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_KupCtrlStat(void)
{
    GpioInit(&g_sGpio_KupCtrlStat0);
    GpioInit(&g_sGpio_KupCtrlStat1);
    GpioInit(&g_sGpio_KupCtrlStat2);
}

void GpioSet_KupCtrlStat(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_KupCtrlStat0, (bool) (ui32Val & 0x01));
}

uint32_t GpioGet_KupCtrlStat(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_KupCtrlStat0) & 0x1) << 0;
    ui32Val |= (GpioInputGetBool(&g_sGpio_KupCtrlStat1) & 0x1) << 1;
    ui32Val |= (GpioInputGetBool(&g_sGpio_KupCtrlStat2) & 0x1) << 2;

    return ui32Val;
}



// ******************************************************************
// Control/status of the ZU11EG.
// ******************************************************************

// ZUP_PS_PROG_B_3V3: PP0
tGPIO g_sGpio_ZupCtrlStat0 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_DONE_3V3: PP2
tGPIO g_sGpio_ZupCtrlStat1 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_INIT_B_3V3: PP1
tGPIO g_sGpio_ZupCtrlStat2 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_nPOR: PP3
tGPIO g_sGpio_ZupCtrlStat3 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_ERR_STATUS: PP4
tGPIO g_sGpio_ZupCtrlStat4 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_ERR_OUT: PP5
tGPIO g_sGpio_ZupCtrlStat5 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_ZupCtrlStat(void)
{
    GpioInit(&g_sGpio_ZupCtrlStat0);
    GpioInit(&g_sGpio_ZupCtrlStat1);
    GpioInit(&g_sGpio_ZupCtrlStat2);
    GpioInit(&g_sGpio_ZupCtrlStat3);
    GpioInit(&g_sGpio_ZupCtrlStat4);
    GpioInit(&g_sGpio_ZupCtrlStat5);
}

void GpioSet_ZupCtrlStat(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_ZupCtrlStat0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_ZupCtrlStat3, (bool) (ui32Val & 0x08));
}

uint32_t GpioGet_ZupCtrlStat(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_ZupCtrlStat0) & 0x1) << 0;
    ui32Val |= (GpioInputGetBool(&g_sGpio_ZupCtrlStat1) & 0x1) << 1;
    ui32Val |= (GpioInputGetBool(&g_sGpio_ZupCtrlStat2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_ZupCtrlStat3) & 0x1) << 3;
    ui32Val |= (GpioInputGetBool(&g_sGpio_ZupCtrlStat4) & 0x1) << 4;
    ui32Val |= (GpioInputGetBool(&g_sGpio_ZupCtrlStat5) & 0x1) << 5;

    return ui32Val;
}



// ******************************************************************
// Spare signals routed to KU15P / ZU11EG.
// ******************************************************************

// MCU_2_KUP_SE0: PL4
tGPIO g_sGpio_SpareKup0 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_KUP_SE1: PL5
tGPIO g_sGpio_SpareKup1 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_KUP_SE2: PL6
tGPIO g_sGpio_SpareKup2 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_KUP_SE3: PL7
tGPIO g_sGpio_SpareKup3 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE0: PL0
tGPIO g_sGpio_SpareZup0 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE1: PL1
tGPIO g_sGpio_SpareZup1 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE2: PL2
tGPIO g_sGpio_SpareZup2 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE3: PL3
tGPIO g_sGpio_SpareZup3 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_SpareKupZup(void)
{
    GpioInit(&g_sGpio_SpareKup0);
    GpioInit(&g_sGpio_SpareKup1);
    GpioInit(&g_sGpio_SpareKup2);
    GpioInit(&g_sGpio_SpareKup3);
    GpioInit(&g_sGpio_SpareZup0);
    GpioInit(&g_sGpio_SpareZup1);
    GpioInit(&g_sGpio_SpareZup2);
    GpioInit(&g_sGpio_SpareZup3);
}

void GpioSet_SpareKupZup(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_SpareKup0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_SpareKup1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_SpareKup2, (bool) (ui32Val & 0x04));
    GpioOutputSetBool(&g_sGpio_SpareKup3, (bool) (ui32Val & 0x08));
    GpioOutputSetBool(&g_sGpio_SpareZup0, (bool) (ui32Val & 0x10));
    GpioOutputSetBool(&g_sGpio_SpareZup1, (bool) (ui32Val & 0x20));
    GpioOutputSetBool(&g_sGpio_SpareZup2, (bool) (ui32Val & 0x40));
    GpioOutputSetBool(&g_sGpio_SpareZup3, (bool) (ui32Val & 0x80));
}

uint32_t GpioGet_SpareKupZup(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareKup0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareKup1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareKup2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareKup3) & 0x1) << 3;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareZup0) & 0x1) << 4;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareZup1) & 0x1) << 5;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareZup2) & 0x1) << 6;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_SpareZup3) & 0x1) << 7;

    return ui32Val;
}

