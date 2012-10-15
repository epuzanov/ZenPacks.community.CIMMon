################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPhysicalMemoryMap

CIMPhysicalMemoryMap maps the CIM_PhysicalMemory to CIMPhysicalMemory objects

$Id: CIMPhysicalMemoryMap.py,v 1.5 2012/10/15 17:26:03 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CIMPhysicalMemoryMap(CIMPlugin):
    """Map CIM_PhysicalMemoryMap class to CIMPhysicalMemory class"""

    maptype = "PhysicalMemoryMap"
    modname = "ZenPacks.community.CIMMon.CIM_PhysicalMemory"
    relname = "physicalmemorymodules"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ("zCIMHWConnectionString",)

    def queries(self, device):
        connectionString = getattr(device, "zCIMHWConnectionString", "")
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_PhysicalMemory":
                (
                    "SELECT * FROM CIM_PhysicalMemory",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "size":"Capacity",
                        "_slottype":"FormFactor",
                        "_manuf":"Manufacturer",
                        "_technology":"MemoryType",
                        "setProductKey":"Model",
#                        "slot":"Name",
                        "serialNumber":"SerialNumber",
                        "_speed":"Speed",
                        "id":"Tag",
                        "state":"Status",
                        "status":"OperationalStatus",
                    },
                ),
            }

    slottypes  =  { 1: "Slot",
                    2: "SIP",
                    3: "DIP",
                    4: "ZIP",
                    5: "SOJ",
                    6: "Proprietary",
                    7: "SIMM",
                    8: "DIMM",
                    9: "TSOP",
                    10:"PGA",
                    11:"RIMM",
                    12:"SO-DIMM",
                    13:"SRIMM",
                    14:"SMD",
                    15:"SSMP",
                    16:"QFP",
                    17:"TQFP",
                    18:"SOIC",
                    19:"LCC",
                    20:"PLCC",
                    21:"BGA",
                    22:"FPBGA",
                    23:"LGA",
                    }

    technologies = {1: "Other",
                    2: "DRAM",
                    3: "Synchronous DRAM",
                    4: "Cache DRAM",
                    5: "EDO",
                    6: "EDRAM",
                    7: "VRAM",
                    8: "SRAM",
                    9: "RAM",
                    10:"ROM",
                    11:"Flash",
                    12:"EEPROM",
                    13:"FEPROM",
                    14:"EPROM",
                    15:"CDRAM",
                    16:"3DRAM",
                    17:"SDRAM",
                    18:"SGRAM",
                    19:"RDRAM",
                    20:"DDR",
                    21:"DDR2",
                    22:"BRAM",
                    23:"FB-DIMM",
                    24:"DDR3",
                    25:"FBD2",
                    }

    def _getProductKey(self, results, inst):
        model = []
        manuf = inst.get("_manuf") or "Unknown"
        model = inst.get("setProductKey") or []
        if model: return MultiArgs(model, manuf)
        model.append(manuf)
        try:
            if int((inst.get("_technology") or 0)) in self.technologies:
                model.append(self.technologies[int(inst["_technology"])])
            if int((inst.get("_slottype") or 0)) in self.slottypes:
                model.append(self.slottypes[int(inst["_slottype"])])
            model.append(convToUnits(int((inst.get("size") or 0))))
        except: pass
        if int((inst.get("_frequency") or 0)) > 0:
            model.append("%sMHz"%inst["_frequency"])
        if int((inst.get("_speed") or 0)) > 0:
            model.append("%sns"%inst["_speed"])
        return MultiArgs(" ".join(model), manuf)

    def _getBoardSlot(self, results, inst):
        try: return 0, int(str(inst.get("slot") or inst.get("id") or 0)[-1])
        except: return 0, 0

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_PhysicalMemory")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_PhysicalMemory")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                self._setCimStatusName(inst)
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                board, om.slot = self._getBoardSlot(results, inst)
                om.title = "Board%s %s%s"%(board, self.slottypes.get(
                    int(inst.get("_slottype") or 0), "Slot"), om.slot)
                if int(getattr(om, "size", 0) or 0) > 0:
                    om.setProductKey = self._getProductKey(results, inst)
            except AttributeError:
                continue
            rm.append(om)
        return rm
