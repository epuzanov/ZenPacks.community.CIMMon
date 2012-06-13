################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMDiskDriveMap

CIMDiskDriveMap maps CIM_DiskDrive class to CIM_DiskDrive class.

$Id: SNAIDiskDriveMap.py,v 1.1 2012/02/02 21:32:03 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, MultiArgs

class CIMDiskDriveMap(CIMPlugin):
    """Map CIM_DiskDrive CIM class to HardDisk class"""

    maptype = "HardDiskMap"
    modname = "ZenPacks.community.CIMMon.CIM_DiskDrive"
    relname = "harddisks"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ("zCIMHWConnectionString",)

    def queries(self, device):
        connectionString = getattr(device, "zCIMHWConnectionString", "")
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_DiskDrive":
                (
                    "SELECT * FROM CIM_DiskDrive",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"DeviceID",
                        "size":"MaxMediaSize",
                        "description":"Name",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                        "_sysname":"SystemName",
                    },
                ),
            }

    def _diskTypes(self, diskType):
        return {"0":"sas",
                "1":"sas",
                "2":"sas",
                "3":"ssd",
                }.get(str(diskType), "")

    def _formFactors(self, formFactor):
        return {"0":"lff",
                "1":"lff",
                "2":"lff",
                "3":"lff",
                "4":"lff",
                "5":"sff",
                "6":"sff",
                }.get(str(formFactor), "")

    def _getPackage(self, results, iPath):
        return  self._findInstance(results, "CIM_PhysicalPackage", "_path",
                self._findInstance(results, "CIM_Realizes", "dep",
                iPath).get("ant", ""))

    def _getChassis(self, results, iPath):
        if not iPath: return ""
        comp = self._findInstance(results, "CIM_Container", "pc", iPath)
        return self._getChassis(results, comp.get("gc")) or comp.get("pc") or ""

    def _getPool(self, results, iPath):
        mpPath = self._findInstance(results, "CIM_MediaPresent", "ant",
                iPath).get("dep", "")
        if not mpPath: return ""
        for sp in results.get("CIM_StoragePool", ()):
            if str(sp.get("_primordial")).lower() == "true": continue
            spPath = sp.get("_path") or "rimordial"
            if "rimordial" in spPath: continue
            for inst in results.get("CIM_ConcreteComponent") or ():
                if not str(inst.get("pc") or "").endswith(mpPath): continue
                if str(inst.get("gc") or "").endswith(spPath): return spPath
        return ""

    def _getFirmware(self, results, iPath):
        return  self._findInstance(results, "CIM_SoftwareIdentity", "_path",
                self._findInstance(results, "CIM_ElementSoftwareIdentity","dep",
                iPath).get("ant", "")).get("FWRev", "")

    def _getBay(self, results, iPath):
        if not iPath: return -1
        for pel in results.get("CIM_PhysicalElementLocation") or ():
            if not (pel.get("element") or "").endswith(iPath): continue
            loc = pel.get("location")
            if loc is None: return -1
            loc = loc.split("PhysicalPosition=")[-1].strip('"').split()[-1]
            return not loc.isdigit() and -1 or int(loc)
        else: return -1

    def process(self, device, results, log):
        """collect Disk Drive information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_DiskDrive")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_DiskDrive")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            instPath = inst.get("setPath") or ""
            try:
                inst.update(self._getPackage(results, instPath))
                packPath = inst.get("_path") or ""
                if "diskType" in inst:
                    inst["diskType"] = self._diskTypes(inst["diskType"])
                    if not inst["diskType"]: del inst["diskType"]
                if "formFactor" in inst:
                    inst["formFactor"] = self._formFactors(inst["formFactor"])
                    if not inst["formFactor"]: del inst["formFactor"]
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                om.size = int(getattr(om, "size", 0)) * 1024
                om._manuf = getattr(om, "_manuf", "") or "Unknown"
                om.setProductKey = MultiArgs(
                    getattr(om, "setProductKey", "") or "Unknown", om._manuf)
                if not getattr(om, "FWRev", ""):
                    om.FWRev = self._getFirmware(results, instPath)
                if not str(getattr(om, "bay", "")):
                    bay = self._getBay(results, packPath)
                    if bay > -1: om.bay = bay
                om.setChassis = self._getChassis(results, packPath)
                om.setStoragePool = self._getPool(results, instPath)
                om.setStatPath = self._getStatPath(results, instPath)
            except AttributeError:
                continue
            rm.append(om)
        return rm
