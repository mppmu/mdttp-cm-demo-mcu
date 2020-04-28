// File: gpio_pins.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Apr 2020
// Rev.: 28 Apr 2020
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
// Initialize all GPIO pins.
// ******************************************************************

void GpioInit_All(void)
{
    GpioInit_SmPowerEna();
    GpioInit_CmReady();
    GpioSet_CmReady(GPIO_DEFAULT_CM_READY);
    GpioInit_LedCmStatus();
    GpioSet_LedCmStatus(GPIO_DEFAULT_LED_CM_STATUS);
    GpioInit_LedMcuUser();
    GpioSet_LedMcuUser(GPIO_DEFAULT_LED_CM_USER);
    GpioInit_MuxSel();
    GpioSet_MuxSel(GPIO_DEFAULT_MUX_SEL);
    GpioInit_MuxPD();
    GpioSet_MuxPD(GPIO_DEFAULT_MUX_PD);
    GpioInit_ClockSel();
    GpioSet_ClockSel(GPIO_DEFAULT_CLOCK_SEL);
    GpioInit_PowerCtrl();
    GpioSet_PowerCtrl(GPIO_DEFAULT_POWER_CTRL);
    GpioInit_KupCtrlStat();
    GpioSet_KupCtrlStat(GPIO_DEFAULT_KUP_CTRL_STAT);
    GpioInit_ZupCtrlStat();
    GpioSet_ZupCtrlStat(GPIO_DEFAULT_ZUP_CTRL_STAT);
    GpioInit_Reset();
    GpioSet_Reset(GPIO_DEFAULT_RESET);
    GpioInit_PEInt();
    GpioInit_SpareKupZup();
    GpioSet_SpareKupZup(GPIO_DEFAULT_SPARE_KUP_ZUP);
}



// ******************************************************************
// Service Module power enable.
// ******************************************************************

// SM_PWR_ENA: PN3, 110
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

// CM_READY: PN2, 109
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

// KUP_DOMAIN_PG: PN4, 111
tGPIO g_sGpio_LedCmStatus0 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_DOMAIN_PG: PN5, 112
tGPIO g_sGpio_LedCmStatus1 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// CLK_DOMAIN_PG: PQ0, 5
tGPIO g_sGpio_LedCmStatus2 = {
    SYSCTL_PERIPH_GPIOQ,
    GPIO_PORTQ_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// TEMP_ERROR: PQ1, 6
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

// MCU_USER_LED0: PM0, 78
tGPIO g_sGpio_LedMcuUser0 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED1: PM1, 77
tGPIO g_sGpio_LedMcuUser1 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED2: PM2, 76
tGPIO g_sGpio_LedMcuUser2 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED3: PM3, 75
tGPIO g_sGpio_LedMcuUser3 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED4: PM4, 74
tGPIO g_sGpio_LedMcuUser4 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED5: PM5,73
tGPIO g_sGpio_LedMcuUser5 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED6: PM6, 72
tGPIO g_sGpio_LedMcuUser6 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED7: PM7, 71
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

// B2B_MUX1_SEL: PA2, 35
tGPIO g_sGpio_MuxSel0 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// B2B_MUX2_SEL: PA4, 37
tGPIO g_sGpio_MuxSel1 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// LTTC_MUX_SEL: PC4, 25
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

// B2B_MUX1_PD: PA3, 36
tGPIO g_sGpio_MuxPD0 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// B2B_MUX2_PD: PA5, 38
tGPIO g_sGpio_MuxPD1 = {
    SYSCTL_PERIPH_GPIOA,
    GPIO_PORTA_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// LTTC_MUX_PD: PC5, 24
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

// AD_CLK2_KUP_SEL: PE0, 15
tGPIO g_sGpio_ClockSel0 = {
    SYSCTL_PERIPH_GPIOE,
    GPIO_PORTE_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// AD_CLK3_KUP_SEL: PE1, 14
tGPIO g_sGpio_ClockSel1 = {
    SYSCTL_PERIPH_GPIOE,
    GPIO_PORTE_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// AD_CLK4_KUP_SEL: PE2, 13
tGPIO g_sGpio_ClockSel2 = {
    SYSCTL_PERIPH_GPIOE,
    GPIO_PORTE_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// AD_CLK5_ZUP_SEL: PN0, 107
tGPIO g_sGpio_ClockSel3 = {
    SYSCTL_PERIPH_GPION,
    GPIO_PORTN_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// CLK_LHC_FPGA_SEL: PN1, 108
tGPIO g_sGpio_ClockSel4 = {
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
    GpioInit(&g_sGpio_ClockSel2);
    GpioInit(&g_sGpio_ClockSel3);
    GpioInit(&g_sGpio_ClockSel4);
}

void GpioSet_ClockSel(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_ClockSel0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_ClockSel1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sGpio_ClockSel2, (bool) (ui32Val & 0x04));
    GpioOutputSetBool(&g_sGpio_ClockSel3, (bool) (ui32Val & 0x08));
    GpioOutputSetBool(&g_sGpio_ClockSel4, (bool) (ui32Val & 0x10));
}

uint32_t GpioGet_ClockSel(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel3) & 0x1) << 3;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_ClockSel4) & 0x1) << 4;

    return ui32Val;
}



// ******************************************************************
// Power control.
// ******************************************************************

// KUP_CORE_RUN: PF3, 45
tGPIO g_sGpio_PowerCtrl0 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_P3V3_IO_RUN: PH0, 29
tGPIO g_sGpio_PowerCtrl1 = {
    SYSCTL_PERIPH_GPIOH,
    GPIO_PORTH_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_DDR4_TERM_EN: PF4, 46
tGPIO g_sGpio_PowerCtrl2 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_CORE_RUN: PD6, 127
tGPIO g_sGpio_PowerCtrl3 = {
    SYSCTL_PERIPH_GPIOD,
    GPIO_PORTD_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_DDR4_TERM_EN: PD7, 128
tGPIO g_sGpio_PowerCtrl4 = {
    SYSCTL_PERIPH_GPIOD,
    GPIO_PORTD_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PL_DDR4_TERM_EN: PF0, 42
tGPIO g_sGpio_PowerCtrl5 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// FIREFY_P1V8_RUN: PF1, 43
tGPIO g_sGpio_PowerCtrl6 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// FIREFY_P3V3_RUN: PF2, 44
tGPIO g_sGpio_PowerCtrl7 = {
    SYSCTL_PERIPH_GPIOF,
    GPIO_PORTF_BASE,
    GPIO_PIN_2,             // ui8Pins
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
    GpioInit(&g_sGpio_PowerCtrl7);
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
    GpioOutputSetBool(&g_sGpio_PowerCtrl7, (bool) (ui32Val & 0x80));
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
    ui32Val |= (GpioOutputGetBool(&g_sGpio_PowerCtrl7) & 0x1) << 7;

    return ui32Val;
}



// ******************************************************************
// Control/status of the KU15P.
// ******************************************************************

// KUP_PROG_B_3V3: PK6, 60
tGPIO g_sGpio_KupCtrlStat0 = {
    SYSCTL_PERIPH_GPIOK,
    GPIO_PORTK_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_DONE_3V3: PK7, 59
tGPIO g_sGpio_KupCtrlStat1 = {
    SYSCTL_PERIPH_GPIOK,
    GPIO_PORTK_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// KUP_INIT_B_3V3: PK5, 61
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

// ZUP_PS_PROG_B_3V3: PP0, 118
tGPIO g_sGpio_ZupCtrlStat0 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_DONE_3V3: PP2, 103
tGPIO g_sGpio_ZupCtrlStat1 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_INIT_B_3V3: PP1, 119
tGPIO g_sGpio_ZupCtrlStat2 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_nPOR: PP3, 104
tGPIO g_sGpio_ZupCtrlStat3 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_ERR_STATUS: PP4, 105
tGPIO g_sGpio_ZupCtrlStat4 = {
    SYSCTL_PERIPH_GPIOP,
    GPIO_PORTP_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};
// ZUP_PS_ERR_OUT: PP5, 106
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
// Reset for multiplexers and I2C port expanders.
// ******************************************************************

// I2C_MUX_nRST: PQ6, 58
tGPIO g_sGpio_Reset0 = {
    SYSCTL_PERIPH_GPIOQ,
    GPIO_PORTQ_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_PEx_nRST: PQ3, 27
tGPIO g_sGpio_Reset1 = {
    SYSCTL_PERIPH_GPIOQ,
    GPIO_PORTQ_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_Reset(void)
{
    GpioInit(&g_sGpio_Reset0);
    GpioInit(&g_sGpio_Reset1);
}

void GpioSet_Reset(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sGpio_Reset0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sGpio_Reset1, (bool) (ui32Val & 0x02));
}

uint32_t GpioGet_Reset(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sGpio_Reset0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sGpio_Reset1) & 0x1) << 1;

    return ui32Val;
}



// ******************************************************************
// Interrupt of I2C port expanders.
// ******************************************************************

// MCU_PEx_nINT: PQ2, 11
tGPIO g_sGpio_PEInt = {
    SYSCTL_PERIPH_GPIOQ,
    GPIO_PORTQ_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    true,                   // bInput: false = output, true = input
    0                       // ui32IntType
};

void GpioInit_PEInt(void)
{
    GpioInit(&g_sGpio_SmPwerEna);
}

uint32_t GpioGet_PEInt(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioInputGetBool(&g_sGpio_SmPwerEna) & 0x1) << 0;

    return ui32Val;
}



// ******************************************************************
// Spare signals routed to KU15P / ZU11EG.
// ******************************************************************

// MCU_2_KUP_SE0: PL4, 85
tGPIO g_sGpio_SpareKup0 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_KUP_SE1: PL5, 86
tGPIO g_sGpio_SpareKup1 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_KUP_SE2: PL6, 94
tGPIO g_sGpio_SpareKup2 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_KUP_SE3: PL7, 93
tGPIO g_sGpio_SpareKup3 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE0: PL0, 81
tGPIO g_sGpio_SpareZup0 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE1: PL1, 82
tGPIO g_sGpio_SpareZup1 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE2: PL2, 83
tGPIO g_sGpio_SpareZup2 = {
    SYSCTL_PERIPH_GPIOL,
    GPIO_PORTL_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_2_ZUP_SE3: PL3, 84
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

