// File: gpio_pins.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 24 Apr 2020
// Rev.: 19 Nov 2020
//
// Header file for the GPIO pin definitions and functions for the TI Tiva
// TM4C1290 MCU on the ATLAS MDT Trigger Processor (TP) Command Module (CM).
//



#ifndef __GPIO_PINS_H__
#define __GPIO_PINS_H__



// Default values.
#define GPIO_DEFAULT_CM_READY       0x0
#define GPIO_DEFAULT_LED_CM_STATUS  0x0     // 0..3: LED_CM_STATUS_CLOCK, LED_CM_STATUS_KU15P, LED_CM_STATUS_ZU11EG, LED_CM_STATUS_TEMP_ALERT
#define GPIO_DEFAULT_LED_CM_USER    0x00    // 0..7: LED_USER_BLUE_0, LED_USER_BLUE_1 LED_USER_ORANGE_0, LED_USER_ORANGE_1, LED_USER_GREEN_0, LED_USER_GREEN_1, LED_USER_RED_0, LED_USER_RED_1
#define GPIO_DEFAULT_MUX_SEL        0x1     // 0..2: B2B_MUX1_SEL, B2B_MUX2_SEL, LTTC_MUX1_SEL
// Hint: The power down (PD) pin of the multiplexers is active high.
#define GPIO_DEFAULT_MUX_PD         0x0     // 0..2: B2B_MUX1_PD, B2B_MUX2_PD, LTTC_MUX1_PD
#define GPIO_DEFAULT_CLOCK_SEL      0x00    // 0..4: AD_CLK2_KUP_SEL, AD_CLK3_KUP_SEL, AD_CLK4_KUP_SEL, AD_CLK5_ZUP_SEL, CLK_LHC_FPGA_SEL
#define GPIO_DEFAULT_POWER_CTRL     0x00    // 0..7: KUP_CORE_RUN, KUP_P3V3_IO_RUN, KUP_DDR4_TERM_EN, ZUP_CORE_RUN, ZUP_PS_DDR4_TERM_EN, ZUP_PL_DDR4_TERM_EN, FIREFY_P1V8_RUN, FIREFY_P3V3_RUN
#define GPIO_DEFAULT_KUP_CTRL_STAT  0x3     // 0..2: KUP_PROG_B_3V3, KUP_INIT_B_3V3, KUP_DONE_3V3
#define GPIO_DEFAULT_ZUP_CTRL_STAT  0xB     // 0..5: ZUP_PS_PROG_B, ZUP_PS_INIT_B, ZUP_PS_DONE, ZUP_PS_nPOR, ZUP_PS_ERR_STATUS, ZUP_PS_ERR_OUT
#define GPIO_DEFAULT_RESET          0x3     // 0..1: I2C_MUX_nRST, MCU_PEx_nRST
#define GPIO_DEFAULT_SPARE_KUP_ZUP  0x00    // 0..7: MCU_2_KUP_SE0, MCU_2_KUP_SE1, MCU_2_KUP_SE2, MCU_2_KUP_SE3, MCU_2_ZUP_SE0, MCU_2_ZUP_SE1, MCU_2_ZUP_SE2, MCU_2_ZUP_SE3
#define GPIO_DEFAULT_RESERVED       0x00    // 0..2: PWR_CLK, PWR_KU15P, PWR_ZU11EG



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
void GpioInit_Reserved(void);
void GpioSet_Reserved(uint32_t ui32Val);
uint32_t GpioGet_Reserved(void);



#endif  // __GPIO_PINS_H__

