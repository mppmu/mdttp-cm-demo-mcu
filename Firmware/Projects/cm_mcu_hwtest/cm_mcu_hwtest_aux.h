// File: cm_mcu_hwtest_aux.h
// Auth: M. Fras, Electronics Division, MPI for Physics, Munich
// Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
// Date: 27 Aug 2020
// Rev.: 27 Aug 2020
//
// Header file for the auxiliary functions of the firmware running on the ATLAS
// MDT Trigger Processor (TP) Command Module (CM) MCU.
//



#ifndef __CM_MCU_HWTEST_AUX_H__
#define __CM_MCU_HWTEST_AUX_H__



// ******************************************************************
// Function prototypes.
// ******************************************************************

int DelayUs(uint32_t ui32DelayUs);
int DelayUsCmd(char *pcCmd, char *pcParam);
int McuReset(char *pcCmd, char *pcParam);
int JumpToBootLoader(char *pcCmd, char *pcParam);
int LedCmStatusUpdated(void);
int TemperatureAnalog(char *pcCmd, char *pcParam);
float Adc2Temp(uint32_t ui32Adc);
char *Adc2TempStr(uint32_t ui32Adc);



#endif  // __CM_MCU_HWTEST_AUX_H__

