// File: gpio_led.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Apr 2020
// Rev.: 24 Apr 2020
//
// Header file for the GPIO LED control GPIO LED control for the TI Tiva
// TM4C1290 MCU on the ATLAS MDT Trigger Processor (TP) Command Module (CM).
//



#ifndef __GPIO_LED_H__
#define __GPIO_LED_H__



// Function prototypes.
void GpioLedInit(void);
void GpioLedSet(uint32_t val);
uint32_t GpioLedGet(void);



#endif  // __GPIO_LED_H__

