// File: gpio_pins.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Apr 2020
// Rev.: 28 Apr 2020
//
// Header file for the GPIO pin definitions and functions for the TI Tiva
// TM4C1290 MCU on the ATLAS MDT Trigger Processor (TP) Command Module (CM).
//



#ifndef __GPIO_PINS_H__
#define __GPIO_PINS_H__



// Default values.
#define GPIO_DEFAULT_CM_READY       0x0
#define GPIO_DEFAULT_LED_CM_STATUS  0x0
#define GPIO_DEFAULT_LED_CM_USER    0x00
#define GPIO_DEFAULT_MUX_SEL        0x2
#define GPIO_DEFAULT_MUX_PD         0x0
#define GPIO_DEFAULT_CLOCK_SEL      0x00
#define GPIO_DEFAULT_POWER_CTRL     0x00
#define GPIO_DEFAULT_KUP_CTRL_STAT  0x1
#define GPIO_DEFAULT_ZUP_CTRL_STAT  0x9
#define GPIO_DEFAULT_RESET          0x3
#define GPIO_DEFAULT_SPARE_KUP_ZUP  0x00



// Function prototypes.
void GpioInit_All(void);
void GpioInit_SmPowerEna(void);
uint32_t GpioGet_SmPowerEna(void);
void GpioInit_CmReady(void);
void GpioSet_CmReady(uint32_t ui32Val);
uint32_t GpioGet_CmReady(void);
void GpioInit_LedCmStatus(void);
void GpioSet_LedCmStatus(uint32_t ui32Val);
uint32_t GpioGet_LedCmStatus(void);
void GpioInit_LedMcuUser(void);
void GpioSet_LedMcuUser(uint32_t ui32Val);
uint32_t GpioGet_LedMcuUser(void);
void GpioInit_MuxSel(void);
void GpioSet_MuxSel(uint32_t ui32Val);
uint32_t GpioGet_MuxSel(void);
void GpioInit_MuxPD(void);
void GpioSet_MuxPD(uint32_t ui32Val);
uint32_t GpioGet_MuxPD(void);
void GpioInit_ClockSel(void);
void GpioSet_ClockSel(uint32_t ui32Val);
uint32_t GpioGet_ClockSel(void);
void GpioInit_PowerCtrl(void);
void GpioSet_PowerCtrl(uint32_t ui32Val);
uint32_t GpioGet_PowerCtrl(void);
void GpioInit_KupCtrlStat(void);
void GpioSet_KupCtrlStat(uint32_t ui32Val);
uint32_t GpioGet_KupCtrlStat(void);
void GpioInit_ZupCtrlStat(void);
void GpioSet_ZupCtrlStat(uint32_t ui32Val);
uint32_t GpioGet_ZupCtrlStat(void);
void GpioInit_Reset(void);
void GpioSet_Reset(uint32_t ui32Val);
uint32_t GpioGet_Reset(void);
void GpioInit_PEInt(void);
uint32_t GpioGet_PEInt(void);
void GpioInit_SpareKupZup(void);
void GpioSet_SpareKupZup(uint32_t ui32Val);
uint32_t GpioGet_SpareKupZup(void);



#endif  // __GPIO_PINS_H__

