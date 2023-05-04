# coding: utf-8
"""*****************************************************************************
* Copyright (C) 2023, Microchip Technology Inc., and its subsidiaries. All rights reserved.
* 
* The software and documentation is provided by microchip and its contributors
* "as is" and any express, implied or statutory warranties, including, but not
* limited to, the implied warranties of merchantability, fitness for a particular
* purpose and non-infringement of third party intellectual property rights are
* disclaimed to the fullest extent permitted by law. In no event shall microchip
* or its contributors be liable for any direct, indirect, incidental, special,
* exemplary, or consequential damages (including, but not limited to, procurement
* of substitute goods or services; loss of use, data, or profits; or business
* interruption) however caused and on any theory of liability, whether in contract,
* strict liability, or tort (including negligence or otherwise) arising in any way
* out of the use of the software and documentation, even if advised of the
* possibility of such damage.
* 
* Except as expressly permitted hereunder and subject to the applicable license terms
* for any third-party software incorporated in the software and any applicable open
* source software license terms, no license or other rights, whether express or
* implied, are granted under any patent or other intellectual property rights of
* Microchip or any third party.
*****************************************************************************"""

################################################################################
#### Component ####
################################################################################

ata8510MemoryInterruptEnable = None

global sort_alphanumeric

spi_ata8510_mcc_helpkeyword = "mcc_h3_spi_ata8510_configurations"

def handleMessage(messageID, args):

    result_dict = {}

    if (messageID == "REQUEST_CONFIG_PARAMS"):
        if args.get("localComponentID") != None:
            result_dict = Database.sendMessage(args["localComponentID"], "SPI_MASTER_MODE", {"isReadOnly":True, "isEnabled":True})
            result_dict = Database.sendMessage(args["localComponentID"], "SPI_MASTER_INTERRUPT_MODE", {"isReadOnly":True, "isEnabled":False})
            result_dict = Database.sendMessage(args["localComponentID"], "SPI_MASTER_HARDWARE_CS", {"isReadOnly":True, "isEnabled":False})

    return result_dict

def sort_alphanumeric(l):
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

#def ata8510SetMemoryDependency(symbol, event):
#
#    symbol.setVisible(event["value"])

def instantiateComponent(ata8510Component):
    res = Database.activateComponents(["HarmonyCore"])
    res = Database.activateComponents(["sys_time"])

    # Enable "Generate Harmony System Service Common Files" option in MHC
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_COMMON", {"isEnabled":True})

    # Enable "Generate Harmony System Port Files" option in MHC
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_PORTS", {"isEnabled":True})
    
    ata8510PLIB = ata8510Component.createStringSymbol("SPI_ATA8510_PLIB", None)
    ata8510PLIB.setLabel("PLIB Used")
    ata8510PLIB.setHelp(spi_ata8510_mcc_helpkeyword)
    ata8510PLIB.setReadOnly(True)

    ata8510SymChipSelectPin = ata8510Component.createKeyValueSetSymbol("SPI_ATA8510_CHIP_SELECT_PIN", None)
    ata8510SymChipSelectPin.setLabel("Chip Select Pin (PB5)")
    ata8510SymChipSelectPin.setHelp(spi_ata8510_mcc_helpkeyword)
    ata8510SymChipSelectPin.setOutputMode("Key")
    ata8510SymChipSelectPin.setDisplayMode("Description")

    ata8510SymNresetPin = ata8510Component.createKeyValueSetSymbol("SPI_ATA8510_NRESET_PIN", None)
    ata8510SymNresetPin.setLabel("NRESET Pin (PC0)")
    ata8510SymNresetPin.setHelp(spi_ata8510_mcc_helpkeyword)
    ata8510SymNresetPin.setOutputMode("Key")
    ata8510SymNresetPin.setDisplayMode("Description")

    ata8510SymNpwron1Pin = ata8510Component.createKeyValueSetSymbol("SPI_ATA8510_NPWRON1_PIN", None)
    ata8510SymNpwron1Pin.setLabel("NPWRON1 Pin (PC1)")
    ata8510SymNpwron1Pin.setHelp(spi_ata8510_mcc_helpkeyword)
    ata8510SymNpwron1Pin.setOutputMode("Key")
    ata8510SymNpwron1Pin.setDisplayMode("Description")

    availablePinDictionary = {}

    # Send message to core to get available pins
    availablePinDictionary = Database.sendMessage("core", "PIN_LIST", availablePinDictionary)

    for pad in sort_alphanumeric(availablePinDictionary.values()):
        key = "SYS_PORT_PIN_" + pad
        value = list(availablePinDictionary.keys())[list(availablePinDictionary.values()).index(pad)]
        description = pad
        ata8510SymChipSelectPin.addKey(key, value, description)
        ata8510SymNresetPin.addKey(key, value, description)
        ata8510SymNpwron1Pin.addKey(key, value, description)

    ata8510SymPinConfigComment = ata8510Component.createCommentSymbol("SPI_ATA8510_PINS_CONFIG_COMMENT", None)
    ata8510SymPinConfigComment.setLabel("***Above selected pins must be configured as GPIO Output in Pin Manager***")

    ############################################################################
    #### Code Generation ####
    ############################################################################

    configName = Variables.get("__CONFIGURATION_NAME")

    ata8510HeaderFile = ata8510Component.createFileSymbol("ATA8510_HEADER", None)
    ata8510HeaderFile.setSourcePath("ata8510/spi_ata8510.h")
    ata8510HeaderFile.setOutputName("spi_ata8510.h")
    ata8510HeaderFile.setDestPath("spi/ata8510/")
    ata8510HeaderFile.setProjectPath("config/" + configName + "/spi/spi_ata8510/")
    ata8510HeaderFile.setType("HEADER")
    ata8510HeaderFile.setOverwrite(True)

    ata8510SourceFile = ata8510Component.createFileSymbol("ATA8510_SOURCE", None)
    ata8510SourceFile.setSourcePath("ata8510/src/spi_ata8510.c")
    ata8510SourceFile.setOutputName("spi_ata8510.c")
    ata8510SourceFile.setDestPath("spi/ata8510/src")
    ata8510SourceFile.setProjectPath("config/" + configName + "/spi/spi_ata8510/")
    ata8510SourceFile.setType("SOURCE")
    ata8510SourceFile.setOverwrite(True)
    ata8510SourceFile.setMarkup(False)

    ata8510HeaderLocalFile = ata8510Component.createFileSymbol("SPI_ATA8510_HEADER_LOCAL", None)
    ata8510HeaderLocalFile.setSourcePath("ata8510/src/spi_ata8510_local.h")
    ata8510HeaderLocalFile.setOutputName("spi_ata8510_local.h")
    ata8510HeaderLocalFile.setDestPath("spi/ata8510/src")
    ata8510HeaderLocalFile.setProjectPath("config/" + configName + "/spi/spi_ata8510/")
    ata8510HeaderLocalFile.setType("SOURCE")
    ata8510HeaderLocalFile.setOverwrite(True)
    

    ata8510SystemDefFile = ata8510Component.createFileSymbol("ATA8510_DEF", None)
    ata8510SystemDefFile.setType("STRING")
    ata8510SystemDefFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
    ata8510SystemDefFile.setSourcePath("ata8510/templates/system/definitions.h.ftl")
    ata8510SystemDefFile.setMarkup(True)

    ata8510SymSystemDefObjFile = ata8510Component.createFileSymbol("SPI_ATA8510_SYSTEM_DEF_EXTERN", None)
    ata8510SymSystemDefObjFile.setType("STRING")
    ata8510SymSystemDefObjFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_EXTERNS")
    ata8510SymSystemDefObjFile.setSourcePath("ata8510/templates/system/definitions_externs.h.ftl")
    ata8510SymSystemDefObjFile.setMarkup(True)

    ata8510SymSystemConfigFile = ata8510Component.createFileSymbol("SPI_ATA8510_CONFIGIRUTION", None)
    ata8510SymSystemConfigFile.setType("STRING")
    ata8510SymSystemConfigFile.setOutputName("core.LIST_SYSTEM_CONFIG_H_DRIVER_CONFIGURATION")
    ata8510SymSystemConfigFile.setSourcePath("ata8510/templates/system/configuration.h.ftl")
    ata8510SymSystemConfigFile.setMarkup(True)

def onAttachmentConnected(source, target):

    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]

    if connectID == "spi_ata8510_SPI_dependency":
        plibUsed = localComponent.getSymbolByID("SPI_ATA8510_PLIB")
        plibUsed.clearValue()
        ata8510PlibId = remoteID.upper()
        plibUsed.setValue(ata8510PlibId.upper())

def onAttachmentDisconnected(source, target):

    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]

    if connectID == "spi_ata8510_SPI_dependency":
        plibUsed = localComponent.getSymbolByID("SPI_ATA8510_PLIB")
        plibUsed.clearValue()
        ata8510PlibId = remoteID.upper()

        dummyDict = {}
        dummyDict = Database.sendMessage(remoteID, "SPI_MASTER_MODE", {"isReadOnly":False})
        dummyDict = Database.sendMessage(remoteID, "SPI_MASTER_INTERRUPT_MODE", {"isReadOnly":False})
        dummyDict = Database.sendMessage(remoteID, "SPI_MASTER_HARDWARE_CS", {"isReadOnly":False})

def destroyComponent(ata8510Component):
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_COMMON", {"isEnabled":False})
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_PORTS", {"isEnabled":False})
