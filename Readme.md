# ATLAS MDT Trigger Processor (TP) Command Module (CM) Microcontroller (MCU)

Auth: M. Fras, Electronics Division, MPI for Physics, Munich  
Mod.: M. Fras, Electronics Division, MPI for Physics, Munich  
Date: 09 Apr 2020  
Rev.: 07 Aug 2020  



## Prerequisites

### Software

* ARM GCC.
* GNU make.
* Firmware flashing tool lm4flash.
* Minicom terminal program.
* ARM GDB and nemiver graphical debugger.
* Python 3 and required modules.



### Hardware

* ATLAS MDT Trigger Processor (TP) Command Module (CM).
* TI Tiva TM4C1294 Connected LaunchPad Evaluation Kit board (for programming
  and debugging).



## Getting Started

1. Install required packages. Example for Ubuntu 18.04.  
    ARM cross compiler toolchain.
    ```shell
    sudo apt-get install build-essential gcc-arm-none-eabi binutils-arm-none-eabi openocd
    ```
    Firmware flashing tool.
    ```shell
    sudo apt-get install lm4flash
    ```
    Minicom terminal program.
    ```shell
    sudo apt-get install minicom
    ```
    ARM GDB and nemiver graphical debugger.
    ```shell
    sudo apt-get install gdb-multiarch nemiver
    ```
    Python 3 and required modules.
    ```shell
    sudo apt-get install python3 python3-serial python3-tk
    ```

2. Compile and download the firmware project for hardware testing.  
    Change to the ```Firmware/Projects/cm_mcu_hwtest``` directory. Then clean
    the firmware project directory.
    ```shell
    make clean
    ```
    This will wipe all compiled files and backups of source files from the
    project.
    ```shell
    make mrproper
    ```
    Build the firmware project.
    ```shell
    make
    ```
    Download the firmware. Make sure that these conditions are met:
    * The TM4C1294 Connected LaunchPad™ Evaluation Kit is connected to an USB
      port of the PC.
    * Its resistors R8, R10, R11, R15 and R16 are removed.
    * Its header U6 is connected with a 10-pin 50 mil pitch flat cable to X113
      of the CM.
    * The jumpers X122, X123, X125 and X126 on the CM are in the correct
      position to connect the MCU SWD pins to the header X113.
    * By default, always download the MCU firmware with no other power source
      provided to the CM. Alternatively, if the CM is powered with +12 V, cut
      the pin 1 of the flat cable to avoid connecting to power supplies.
    ```shell
    make install
    ```
    Compile and download a debug version of the firmware, then start the
    nemiver graphical debugger. Please note that there is a breakpoint set at
    the start of the program! This prevents it from running until the program
    is continued from the debugger.
    ```shell
    make debug
    ```
    After you have finished debugging, build and download the normal firmware
    version again.
    ```shell
    make clean install
    ```

3. Communicate with the MCU using the minicom terminal program.  
    Create a file ```.minirc.cm_mcu``` in your home directory with this
    content:
    ```
    pu port             /dev/ttyUSB0
    pu rtscts           No
    ```
    Adapt the ```pu port``` to the serial input to which your TM4C1294
    Connected LaunchPad™ Evaluation Kitis connected.

    Launch minicom either by calling ```make minicom``` inside the firmware
    folder or by starting minicom from the shell ```minicom hw_demo```. To quit
    minicom, press ```Ctrl-A```, then ```Q```. To edit the minicom settings,
    press ```Ctrl-A```, then ```Z```.

    Example minicom session:
    ```
    *******************************************************************************
    MDT-TP CM MCU `cm_mcu_hwtest' firmware version 0.0.1, release date: 09 Apr 2020
    *******************************************************************************
    
    Type `help' to get an overview of available commands.
    >
    ```



## Literature

### TM4C1290NCPDT High performance 32-bit ARM® Cortex®-M4F based MCU

![TM4C1290NCPDT High performance 32-bit ARM® Cortex®-M4F based MCU](http://www.ti.com/graphics/folders/partimages/TM4C1290NCPDT.jpg)
* [TM4C1290NCPDT product page](http://www.ti.com/product/TM4C1290NCPDT)
* [Tiva C Series TM4C1290NCPDT Microcontroller Data Sheet datasheet (Rev. B)](http://www.ti.com/lit/ds/symlink/tm4c1290ncpdt.pdf)
* [TivaWare™ Peripheral Driver Library for C Series User's Guide (Rev. D)](http://www.ti.com/lit/ug/spmu298d/spmu298d.pdf)



### Getting Started, HOWTOs, Tutorials

[![Tiva C Series Connected Launchpad Getting Started EK-TM4C1294XL](https://img.youtube.com/vi/JpGNNCYjtFw/1.jpg)](https://www.youtube.com/watch?v=JpGNNCYjtFw "Tiva C Series Connected Launchpad Getting Started EK-TM4C1294XL")

* [HowTo: Develop on the TI Tiva LaunchPad using Linux](http://chrisrm.com/howto-develop-on-the-ti-tiva-launchpad-using-linux/)
* [Tiva TM4C123G LaunchPad Blink the RGB](https://processors.wiki.ti.com/index.php/Tiva_TM4C123G_LaunchPad_Blink_the_RGB)
* [Tiva Tutorials - Tiva Peripherals with TivaWare](https://sites.google.com/site/luiselectronicprojects/tutorials/tiva-tutorials)
* [Getting Started with the TI Stellaris LaunchPad on Linux](https://www.jann.cc/2012/12/11/getting_started_with_the_ti_stellaris_launchpad_on_linux.html)

