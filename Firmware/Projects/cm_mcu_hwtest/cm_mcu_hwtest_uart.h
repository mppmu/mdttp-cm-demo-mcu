// File: cm_mcu_hwtest_uart.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 27 Aug 2020
// Rev.: 27 Aug 2020
//
// Header file for the UART functions of the firmware running on the ATLAS MDT
// Trigger Processor (TP) Command Module (CM) MCU.
//



#ifndef __CM_MCU_HWTEST_UART_H__
#define __CM_MCU_HWTEST_UART_H__



// ******************************************************************
// Function prototypes.
// ******************************************************************

int UartAccess(char *pcCmd, char *pcParam);
int UartPortCheck(uint8_t ui8UartPort, tUART **psUart);
int UartSetup(char *pcCmd, char *pcParam);
void UartSetupHelp(void);



#endif  // __CM_MCU_HWTEST_UART_H__

