################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMControllerMap

CIMControllerMap maps CIM_Controller class to Controller class.

$Id: CIMControllerMap.py,v 1.4 2012/06/26 19:47:23 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CIMControllerMap(CIMPlugin):
    """Map CIM_Controller class to Controller class"""

    maptype = "ExpansionCardMap"
    modname = "ZenPacks.community.CIMMon.CIM_Controller"
    relname = "cards"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ("zCIMHWConnectionString",)

    def queries(self, device):
        connectionString = getattr(device, "zCIMHWConnectionString", "")
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Controller":
                (
                    "SELECT * FROM CIM_PCIController",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_cc":"ClassCode",
                        "setProductKey":"Description",
                        "id":"DeviceID",
                        "_sysname":"SystemName",
                    },
                ),
            }

    def _ignoreController(self, inst):
        return inst.get("_cc") not in (None, 1, 2, 3, 12)

    def _getPackage(self, results, inst):
        return {}

    def _getSlot(self, results, inst):
        try: return int(inst["slot"])
        except: return 0

    def _monitor(self, inst):
        return True

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_Controller")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_Controller")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            if self._ignoreController(inst): continue
            inst.update(self._getPackage(results, inst))
            try:
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                manuf = getattr(om, "_manuf", "") or "Unknown"
                if not hasattr(om,"title") and getattr(om, "setProductKey", ""):
                    om.title = om.setProductKey
                om.setProductKey = MultiArgs(
                    getattr(om, "setProductKey", "") or "Unknown",
                    getattr(om, "_manuf", "") or "Unknown")
                if hasattr(om, "slot"):
                    om.slot = self._getSlot(results, inst)
                om.setCollections = self._getCollections(results, inst)
                om.setStatPath = self._getStatPath(results, inst)
                om.monitor = self._monitor(inst)
            except AttributeError:
                continue
            rm.append(om)
        return rm
