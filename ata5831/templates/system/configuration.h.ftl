/* ATA5831 Driver Configuration Options */
    /* UHF SPI SERCOM mapping */
    #define UHF_SPI_TRANSFER                ${SPI_ATA5831_PLIB?string}_SPI_WriteRead
    /* UHF SPI Chip Select mapping */
    #define UHF_SPI_CS_ENABLE               SYS_PORT_PinClear(${SPI_ATA5831_CHIP_SELECT_PIN?string})
    #define UHF_SPI_CS_DISABLE              SYS_PORT_PinSet(${SPI_ATA5831_CHIP_SELECT_PIN?string})
    /* UHF NRESET mapping */
    #define UHF_NRESET_CLEAR                SYS_PORT_PinClear(${SPI_ATA5831_NRESET_PIN?string})
    #define UHF_NRESET_SET                  SYS_PORT_PinSet(${SPI_ATA5831_NRESET_PIN?string})
    /* UHF NPWRON1 mapping */
    #define UHF_NPWRON1_CLEAR               SYS_PORT_PinClear(${SPI_ATA5831_NPWRON1_PIN?string})
    #define UHF_NPWRON1_SET                 SYS_PORT_PinSet(${SPI_ATA5831_NPWRON1_PIN?string})