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

ata5831MemoryInterruptEnable = None

global sort_alphanumeric

spi_ata5831_mcc_helpkeyword = "mcc_h3_spi_ata5831_configurations"

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

#def ata5831SetMemoryDependency(symbol, event):
#
#    symbol.setVisible(event["value"])

def instantiateComponent(ata5831Component):
    res = Database.activateComponents(["HarmonyCore"])
    res = Database.activateComponents(["sys_time"])

    # Enable "Generate Harmony System Service Common Files" option in MHC
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_COMMON", {"isEnabled":True})

    # Enable "Generate Harmony System Port Files" option in MHC
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_PORTS", {"isEnabled":True})
    
    ata5831PLIB = ata5831Component.createStringSymbol("SPI_ATA5831_PLIB", None)
    ata5831PLIB.setLabel("PLIB Used")
    ata5831PLIB.setHelp(spi_ata5831_mcc_helpkeyword)
    ata5831PLIB.setReadOnly(True)

    ata5831SymChipSelectPin = ata5831Component.createKeyValueSetSymbol("SPI_ATA5831_CHIP_SELECT_PIN", None)
    ata5831SymChipSelectPin.setLabel("Chip Select Pin (PB5)")
    ata5831SymChipSelectPin.setHelp(spi_ata5831_mcc_helpkeyword)
    ata5831SymChipSelectPin.setOutputMode("Key")
    ata5831SymChipSelectPin.setDisplayMode("Description")

    ata5831SymNresetPin = ata5831Component.createKeyValueSetSymbol("SPI_ATA5831_NRESET_PIN", None)
    ata5831SymNresetPin.setLabel("NRESET Pin (PC0)")
    ata5831SymNresetPin.setHelp(spi_ata5831_mcc_helpkeyword)
    ata5831SymNresetPin.setOutputMode("Key")
    ata5831SymNresetPin.setDisplayMode("Description")

    ata5831SymNpwron1Pin = ata5831Component.createKeyValueSetSymbol("SPI_ATA5831_NPWRON1_PIN", None)
    ata5831SymNpwron1Pin.setLabel("NPWRON1 Pin (PC1)")
    ata5831SymNpwron1Pin.setHelp(spi_ata5831_mcc_helpkeyword)
    ata5831SymNpwron1Pin.setOutputMode("Key")
    ata5831SymNpwron1Pin.setDisplayMode("Description")

    availablePinDictionary = {}

    # Send message to core to get available pins
    availablePinDictionary = Database.sendMessage("core", "PIN_LIST", availablePinDictionary)

    for pad in sort_alphanumeric(availablePinDictionary.values()):
        key = "SYS_PORT_PIN_" + pad
        value = list(availablePinDictionary.keys())[list(availablePinDictionary.values()).index(pad)]
        description = pad
        ata5831SymChipSelectPin.addKey(key, value, description)
        ata5831SymNresetPin.addKey(key, value, description)
        ata5831SymNpwron1Pin.addKey(key, value, description)

    ata5831SymPinConfigComment = ata5831Component.createCommentSymbol("SPI_ATA5831_PINS_CONFIG_COMMENT", None)
    ata5831SymPinConfigComment.setLabel("***Above selected pins must be configured as GPIO Output in Pin Manager***")

    ############################################################################
    #### Code Generation ####
    ############################################################################

    configName = Variables.get("__CONFIGURATION_NAME")

    ata5831HeaderFile = ata5831Component.createFileSymbol("ATA5831_HEADER", None)
    ata5831HeaderFile.setSourcePath("ata5831/spi_ata5831.h")
    ata5831HeaderFile.setOutputName("spi_ata5831.h")
    ata5831HeaderFile.setDestPath("spi/ata5831/")
    ata5831HeaderFile.setProjectPath("config/" + configName + "/spi/spi_ata5831/")
    ata5831HeaderFile.setType("HEADER")
    ata5831HeaderFile.setOverwrite(True)

    ata5831SourceFile = ata5831Component.createFileSymbol("ATA5831_SOURCE", None)
    ata5831SourceFile.setSourcePath("ata5831/src/spi_ata5831.c")
    ata5831SourceFile.setOutputName("spi_ata5831.c")
    ata5831SourceFile.setDestPath("spi/ata5831/src")
    ata5831SourceFile.setProjectPath("config/" + configName + "/spi/spi_ata5831/")
    ata5831SourceFile.setType("SOURCE")
    ata5831SourceFile.setOverwrite(True)
    ata5831SourceFile.setMarkup(False)

    ata5831HeaderLocalFile = ata5831Component.createFileSymbol("SPI_ATA5831_HEADER_LOCAL", None)
    ata5831HeaderLocalFile.setSourcePath("ata5831/src/spi_ata5831_local.h")
    ata5831HeaderLocalFile.setOutputName("spi_ata5831_local.h")
    ata5831HeaderLocalFile.setDestPath("spi/ata5831/src")
    ata5831HeaderLocalFile.setProjectPath("config/" + configName + "/spi/spi_ata5831/")
    ata5831HeaderLocalFile.setType("SOURCE")
    ata5831HeaderLocalFile.setOverwrite(True)
    

    ata5831SystemDefFile = ata5831Component.createFileSymbol("ATA5831_DEF", None)
    ata5831SystemDefFile.setType("STRING")
    ata5831SystemDefFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
    ata5831SystemDefFile.setSourcePath("ata5831/templates/system/definitions.h.ftl")
    ata5831SystemDefFile.setMarkup(True)

    ata5831SymSystemDefObjFile = ata5831Component.createFileSymbol("SPI_ATA5831_SYSTEM_DEF_EXTERN", None)
    ata5831SymSystemDefObjFile.setType("STRING")
    ata5831SymSystemDefObjFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_EXTERNS")
    ata5831SymSystemDefObjFile.setSourcePath("ata5831/templates/system/definitions_externs.h.ftl")
    ata5831SymSystemDefObjFile.setMarkup(True)

    ata5831SymSystemConfigFile = ata5831Component.createFileSymbol("SPI_ATA5831_CONFIGIRUTION", None)
    ata5831SymSystemConfigFile.setType("STRING")
    ata5831SymSystemConfigFile.setOutputName("core.LIST_SYSTEM_CONFIG_H_DRIVER_CONFIGURATION")
    ata5831SymSystemConfigFile.setSourcePath("ata5831/templates/system/configuration.h.ftl")
    ata5831SymSystemConfigFile.setMarkup(True)

def onAttachmentConnected(source, target):

    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]

    if connectID == "spi_ata5831_SPI_dependency":
        plibUsed = localComponent.getSymbolByID("SPI_ATA5831_PLIB")
        plibUsed.clearValue()
        ata5831PlibId = remoteID.upper()
        plibUsed.setValue(ata5831PlibId.upper())

def onAttachmentDisconnected(source, target):

    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]

    if connectID == "spi_ata5831_SPI_dependency":
        plibUsed = localComponent.getSymbolByID("SPI_ATA5831_PLIB")
        plibUsed.clearValue()
        ata5831PlibId = remoteID.upper()

        dummyDict = {}
        dummyDict = Database.sendMessage(remoteID, "SPI_MASTER_MODE", {"isReadOnly":False})
        dummyDict = Database.sendMessage(remoteID, "SPI_MASTER_INTERRUPT_MODE", {"isReadOnly":False})
        dummyDict = Database.sendMessage(remoteID, "SPI_MASTER_HARDWARE_CS", {"isReadOnly":False})

def destroyComponent(ata5831Component):
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_COMMON", {"isEnabled":False})
    Database.sendMessage("HarmonyCore", "ENABLE_SYS_PORTS", {"isEnabled":False})
