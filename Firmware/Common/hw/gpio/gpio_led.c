// File: gpio_led.c
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Apr 2020
// Rev.: 24 Apr 2020
//
// GPIO LED control for the TI Tiva TM4C1290 MCU on the ATLAS MDT Trigger
// Processor (TP) Command Module (CM).
//



#include <stdbool.h>
#include <stdint.h>
#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "gpio.h"
#include "gpio_led.h"



// GPIO definitions.
// MCU_USER_LED0: PM0
tGPIO g_sMcuUserLed0 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_0,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED1: PM1
tGPIO g_sMcuUserLed1 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_1,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED2: PM2
tGPIO g_sMcuUserLed2 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_2,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED3: PM3
tGPIO g_sMcuUserLed3 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_3,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED4: PM4
tGPIO g_sMcuUserLed4 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_4,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED5: PM5
tGPIO g_sMcuUserLed5 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_5,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED6: PM6
tGPIO g_sMcuUserLed6 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_6,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};
// MCU_USER_LED7: PM7
tGPIO g_sMcuUserLed7 = {
    SYSCTL_PERIPH_GPIOM,
    GPIO_PORTM_BASE,
    GPIO_PIN_7,             // ui8Pins
    GPIO_STRENGTH_2MA,      // ui32Strength
    GPIO_PIN_TYPE_STD,      // ui32PinType
    false,                  // bInput: false = output, true = input
    0                       // ui32IntType
};



// Initialize the GPIO LEDs.
void GpioLedInit(void)
{
    GpioInit(&g_sMcuUserLed0);
    GpioInit(&g_sMcuUserLed1);
    GpioInit(&g_sMcuUserLed2);
    GpioInit(&g_sMcuUserLed3);
    GpioInit(&g_sMcuUserLed4);
    GpioInit(&g_sMcuUserLed5);
    GpioInit(&g_sMcuUserLed6);
    GpioInit(&g_sMcuUserLed7);
}



// Set the GPIO LEDs.
void GpioLedSet(uint32_t ui32Val)
{
    GpioOutputSetBool(&g_sMcuUserLed0, (bool) (ui32Val & 0x01));
    GpioOutputSetBool(&g_sMcuUserLed1, (bool) (ui32Val & 0x02));
    GpioOutputSetBool(&g_sMcuUserLed2, (bool) (ui32Val & 0x04));
    GpioOutputSetBool(&g_sMcuUserLed3, (bool) (ui32Val & 0x08));
    GpioOutputSetBool(&g_sMcuUserLed4, (bool) (ui32Val & 0x10));
    GpioOutputSetBool(&g_sMcuUserLed5, (bool) (ui32Val & 0x20));
    GpioOutputSetBool(&g_sMcuUserLed6, (bool) (ui32Val & 0x40));
    GpioOutputSetBool(&g_sMcuUserLed7, (bool) (ui32Val & 0x80));
}



// Read back the GPIO LEDs.
uint32_t GpioLedGet(void)
{
    uint32_t ui32Val = 0;

    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed0) & 0x1) << 0;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed1) & 0x1) << 1;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed2) & 0x1) << 2;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed3) & 0x1) << 3;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed4) & 0x1) << 4;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed5) & 0x1) << 5;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed6) & 0x1) << 6;
    ui32Val |= (GpioOutputGetBool(&g_sMcuUserLed7) & 0x1) << 7;

    return ui32Val;
}

