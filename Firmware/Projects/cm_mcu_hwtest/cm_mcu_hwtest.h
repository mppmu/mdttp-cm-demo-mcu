// File: cm_mcu_hwtest.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 08 Apr 2020
// Rev.: 20 Sep 2022
//
// Header file of the firmware running on the ATLAS MDT Trigger Processor (TP)
// Command Module (CM) demonstrator MCU.
//



#ifndef __CM_MCU_HWTEST_H__
#define __CM_MCU_HWTEST_H__



// ******************************************************************
// Firmware parameters.
// ******************************************************************

#define FW_NAME                     "cm_mcu_hwtest"
#define FW_VERSION                  "0.4.0"
#define FW_RELEASEDATE              "20 Sep 2022"



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
// Use this to optionally select the front-panel USB UART. Default will be the
// SM SoC UART. If not defined, the default will be the front-panel USB UART.
#define UI_UART_SELECT
#define UI_UART_SELECT_TIMEOUT      10



// ******************************************************************
// Hardware settings.
// ******************************************************************

// Show temperatures as raw hexadecimal ADC values.
//#define TEMP_RAW_ADC_HEX

// I2C parameters.
#define I2C_MASTER_NUM              10

// QSSI parameters.
#define QSSI_FREQ_MIN               2000
#define QSSI_FREQ_MAX               50000000

// UART parameters.
#define UART_BAUD_MIN               150
#define UART_BAUD_MAX               15000000

// Status LEDs.
#define LED_CM_STATUS_CLOCK         0x01
#define LED_CM_STATUS_KU15P         0x02
#define LED_CM_STATUS_ZU11EG        0x04
#define LED_CM_STATUS_TEMP_ALERT    0x08

// User LEDs.
#define LED_USER_BLUE_0             0x01
#define LED_USER_BLUE_1             0x02
#define LED_USER_ORANGE_0           0x04
#define LED_USER_ORANGE_1           0x08
#define LED_USER_GREEN_0            0x10
#define LED_USER_GREEN_1            0x20
#define LED_USER_RED_0              0x40
#define LED_USER_RED_1              0x80

// Enable power up/down handshaking between the Service Module and the Command
// Module using the PWR_EN (drive by the SM) and the READY (driven by the CM)
// signals (SM-CM handshaking).
#define SM_CM_POWER_HANDSHAKING_ENABLE
#define SM_CM_POWER_HANDSHAKING_SHOW_MESSAGE



// ******************************************************************
// Function prototypes.
// ******************************************************************



#endif  // __CM_MCU_HWTEST_H__

