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

$Id: SNIADiskDriveMap.py,v 1.5 2012/06/21 19:33:14 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

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
                }.get(str(diskType)) or "scsi"

    def _diskTypeImg(self, diskType):
        return diskType

    def _formFactors(self, formFactor):
        return {"0":"lff",
                "1":"lff",
                "2":"lff",
                "3":"lff",
                "4":"lff",
                "5":"sff",
                "6":"sff",
                }.get(str(formFactor)) or "lff"

    def _getPackage(self, results, inst):
        return  self._findInstance(results, "CIM_PhysicalPackage", "_pPath",
                self._findInstance(results, "CIM_Realizes", "dep",
                inst.get("setPath")).get("ant"))

    def _getChassis(self, results, inst):
        iPath = inst.get("_pPath") or inst.get("gc")
        if not iPath: return ""
        comp = self._findInstance(results, "CIM_Container", "pc", iPath)
        if not comp: return "gc" in inst and iPath or ""
        return self._getChassis(results, comp) or comp.get("pc") or ""

    def _getPool(self, results, inst):
        mpPath = self._findInstance(results, "CIM_MediaPresent", "ant",
                inst.get("setPath")).get("dep")
        if not mpPath: return ""
        for sp in results.get("CIM_StoragePool", ()):
            if str(sp.get("_primordial")).lower() == "true": continue
            spPath = sp.get("_path") or "rimordial"
            if "rimordial" in spPath: continue
            for inst in results.get("CIM_ConcreteComponent") or ():
                if not str(inst.get("pc") or "").endswith(mpPath): continue
                if str(inst.get("gc") or "").endswith(spPath): return spPath
        return ""

    def _getFirmware(self, results, inst):
        return  self._findInstance(results, "CIM_SoftwareIdentity", "_path",
                self._findInstance(results, "CIM_ElementSoftwareIdentity","dep",
                inst.get("setPath")).get("ant")).get("FWRev") or ""

    def _getBay(self, results, inst):
        iPath = inst.get("_pPath")
        if not iPath: return -1
        for pel in results.get("CIM_PhysicalElementLocation") or ():
            if not (pel.get("element") or "").endswith(iPath): continue
            loc = pel.get("location")
            if loc is None: return -1
            loc = loc.split("PhysicalPosition=")[-1].strip('"').split()[-1]
            return not loc.isdigit() and -1 or int(loc)
        else: return -1

    def _isHardDisk(self, inst):
        return True

    def process(self, device, results, log):
        """collect Disk Drive information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_DiskDrive")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_DiskDrive")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            if not self._isHardDisk(inst): continue
            try:
                inst.update(self._getPackage(results, inst))
                if "diskType" in inst:
                    inst["diskType"] = self._diskTypes(inst["diskType"])
                    inst["diskTypeImg"] = self._diskTypeImg(inst["diskType"])
                    if not inst["diskType"]: del inst["diskType"]
                if "formFactor" in inst:
                    inst["formFactor"] = self._formFactors(inst["formFactor"])
                    if not inst["formFactor"]: del inst["formFactor"]
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                om.size = int(getattr(om, "size", 0)) * 1000
                om._manuf = getattr(om, "_manuf", "") or "Unknown"
                om.setProductKey = MultiArgs(
                    getattr(om, "setProductKey", "") or "Unknown", om._manuf)
                if not getattr(om, "FWRev", ""):
                    om.FWRev = self._getFirmware(results, inst)
                if not str(getattr(om, "bay", "")):
                    bay = self._getBay(results, inst)
                    if bay > -1: om.bay = bay
                om.setChassis = self._getChassis(results, inst)
                om.setStoragePool = self._getPool(results, inst)
                om.setStatPath = self._getStatPath(results, inst)
            except AttributeError:
                continue
            rm.append(om)
        return rm
