######################  Harmony SPI UHF transceiver #############
def loadModule():
    processor = Variables.get("__PROCESSOR")

    if "SAMC21" in processor:
        print("Load Module: Harmony SPI UHF transceiver")
        ata5831 = Module.CreateComponent("spi_ata5831", "ATA5831", "SPI UHF transceiver", "ata5831/config/spi_ata5831.py")
        ata5831.addDependency("spi_ata5831_SPI_dependency", "SPI", False, True)
        ata5831.setDisplayType("SPI command set")
