/* File: cm_mcu_hwtest.ld
 * Auth: M. Fras, Electronics Division, MPI for Physics, Munich
 * Mod.: M. Fras, Electronics Division, MPI for Physics, Munich
 * Date: 08 Apr 2020
 * Rev.: 27 Aug 2020
 *
 * Linker configuration file of the firmware running on the ATLAS MDT Trigger
 * Processor (TP) Command Module (CM) MCU.
 */



MEMORY
{
/*    FLASH (rx) : ORIGIN = 0x00000000, LENGTH = 0x00100000 */
    /* Offset 0x4000 for boot loader. */
    FLASH (rx) : ORIGIN = 0x00004000, LENGTH = 0x000fc000
    SRAM (rwx) : ORIGIN = 0x20000000, LENGTH = 0x00040000
}

SECTIONS
{
    .text :
    {
        _text = .;
        KEEP(*(.isr_vector))
        *(.text*)
        *(.rodata*)
        _etext = .;
    } > FLASH

    .data : AT(ADDR(.text) + SIZEOF(.text))
    {
        _data = .;
        _ldata = LOADADDR (.data);
        *(vtable)
        *(.data*)
        _edata = .;
    } > SRAM

    .bss :
    {
        _bss = .;
        *(.bss*)
        *(COMMON)
        _ebss = .;
    } > SRAM
}

