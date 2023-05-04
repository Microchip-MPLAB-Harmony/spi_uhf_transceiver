######################  Harmony SPI UHF transceiver #############
def loadModule():
    processor = Variables.get("__PROCESSOR")

    if "SAMC21" in processor:
        print("Load Module: Harmony SPI UHF transceiver")
        ata8510 = Module.CreateComponent("spi_ata8510", "ATA8510", "SPI UHF transceiver", "ata8510/config/spi_ata8510.py")
        ata8510.addDependency("spi_ata8510_SPI_dependency", "SPI", False, True)
        ata8510.setDisplayType("SPI command set")
