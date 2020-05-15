// File: cm_mcu_hwtest.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 08 Apr 2020
// Rev.: 15 May 2020
//
// Header file of the firmware running on the ATLAS MDT Trigger Processor (TP)
// Command Module (CM) MCU.
//



#ifndef __CM_MCU_HWTEST_H__
#define __CM_MCU_HWTEST_H__



// ******************************************************************
// Firmware parameters.
// ******************************************************************
#define FW_NAME                     "cm_mcu_hwtest"
#define FW_VERSION                  "0.1.2"
#define FW_RELEASEDATE              "15 May 2020"



// ******************************************************************
// System clock settings.
// ******************************************************************
// Use an external 25 MHz crystal or oscillator.
//#define SYSTEM_CLOCK_SETTINGS       (SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480)
// CAUTION: No external crystal is installed on the Command Module!
//          => Only the internal oscillator can be used.
#define SYSTEM_CLOCK_SETTINGS       (SYSCTL_OSC_INT | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480)
#define SYSTEM_CLOCK_FREQ           120000000


// ******************************************************************
// User interface.
// ******************************************************************
#define UI_COMMAND_PROMPT           "> "
#define UI_STR_BUF_SIZE             256
#define UI_STR_DELIMITER            " \t"
#define UI_STR_OK                   "OK"
#define UI_STR_WARNING              "WARNING"
#define UI_STR_ERROR                "ERROR"
#define UI_STR_FATAL                "FATAL"



// ******************************************************************
// Hardware settings.
// ******************************************************************

// Show temperatures as raw hexadecimal ADC values.
#define TEMP_RAW_ADC_HEX

// I2C parameters.
#define I2C_MASTER_NUM              10

// UART parameters.
#define UART_BAUD_MIN               150
#define UART_BAUD_MAX               15000000



#endif  // __CM_MCU_HWTEST_H__

