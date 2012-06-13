################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMChassisMap

CIMChassisMap maps CIM_Chassis class to CIM_Chassis class.

$Id: CIMChassisMap.py,v 1.0 2012/01/04 21:32:34 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs, ObjectMap

class CIMChassisMap(CIMPlugin):
    """Map CIM_Chassis CIM class to CIM_Chassis class"""

    maptype = "ChassisMap"
    modname = "ZenPacks.community.CIMMon.CIM_Chassis"
    relname = "chassis"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Chassis":
                (
                    "SELECT * FROM CIM_Chassis",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_cptype":"ChassisPackageType",
                        "title":"Name",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                        "_pn":"PartNumber",
                        "id":"Tag",
                        "_sysname":"Tag",
                    },
                ),
            }

    def _isSystemChassis(self, results, sysname, inst):
        p = inst.get("setPath")
        if not p: return False
        if len(results.get("CIM_Chassis", ())) > 1:
            for sp in results.get("CIM_ComputerSystemPackage", ()):
                if not sp.get("ant","").endswith(p): continue
                if sysname in sp.get("dep","").lower(): break
            else: return False
        return True

    def _getComputerSystemPath(self, results, iPath):
        if not iPath: return ""
        if "Tag=" in iPath:
            for sp in results.get("CIM_ComputerSystemPackage", ()):
                if sp.get("ant", "").endswith(iPath): break
            else: sp = {}
            iPath = sp.get("dep") or ""
        return CIMPlugin._getComputerSystemPath(self, results, iPath)

    def _getLayout(self, results, iPath):
        return None

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        maps = []
        rm = self.relMap()
        instances = results.get("CIM_Chassis")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_Chassis")
        sysname = sysnames[0]
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            manuf = inst.get("_manuf") or "Unknown"
            productKey = inst.get("setProductKey") or ""
            try:
                if not maps and self._isSystemChassis(results, sysname, inst):
                    if not inst: continue
                    om = ObjectMap()
                    if productKey:
                        om.setHWProductKey = MultiArgs(productKey, manuf)
                    serialNumber = inst.get("serialNumber") or ""
                    if serialNumber:
                        om.setHWSerialNumber = serialNumber
                    tag = inst.get("tag") or inst.get("id") or ""
                    if tag:
                        if tag.startswith(serialNumber) and tag != serialNumber:
                            tag = tag[len(serialNumber):]
                        om.setHWTag = tag
                    maps.append(om)
                    continue
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                manuf = inst.get("_manuf") or "Unknown"
                if productKey:
                    om.setProductKey = MultiArgs(productKey, manuf)
                layout = self._getLayout(results, inst.get("setPath") or "")
                if layout:
                    om.layout = layout
            except AttributeError:
                continue
            rm.append(om)
        maps.append(rm)
        return maps
