################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMFanMap

CIMFanMap maps CIM_Fan class to Fan class.

$Id: CIMFanMap.py,v 1.4 2012/06/26 21:16:51 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMFanMap(CIMPlugin):
    """Map CIM_Fan class to Fan class"""

    maptype = "FanMap"
    modname = "ZenPacks.community.CIMMon.CIM_Fan"
    relname = "fans"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Fan":
                (
                    "SELECT * FROM CIM_Fan",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "type":"ActiveCooling",
                        "title":"Description",
                        "id":"DeviceID",
                        "_sysname":"SystemName",
                    }
                ),
#            "CIM_Tachometer":
#                (
#                    "SELECT * FROM CIM_NumericSensor",
#                    None,
#                    cs,
#                    {
#                        "setStatPath":"__PATH",
#                        "lowerThresholdCritical":"LowerThresholdCritical",
#                        "lowerThresholdFatal":"LowerThresholdFatal",
#                        "lowerThresholdNonCritical":"LowerThresholdNonCritical",
#                        "_sensorType":"SensorType",
#                        "_sysname":"SystemName",
#                        "unitModifier":"UnitModifier",
#                    }
#                ),
#            "CIM_AssociatedSensor":
#                (
#                    "SELECT Antecedent,Dependent FROM CIM_AssociatedSensor",
#                    None,
#                    cs,
#                    {
#                        "ant":"Antecedent", # Tachometer
#                        "dep":"Dependent", # Fan
#                    },
#                ),
            }

    def _getType(self, fanType):
        fanTypeStr = str(fanType).lower()
        if fanTypeStr not in ("true", "false"):
            return fanType
        return "%s Cooling"%(fanTypeStr == "true" and "Active" or "Passive")

    def _getStatPath(self, results, inst):
        if "CIM_Tachometer" not in results: return {}
        comp =  self._findInstance(results, "CIM_Tachometer", "setStatPath",
                self._findInstance(results, "CIM_AssociatedSensor", "dep",
                inst.get("setPath")).get("ant"))
        if not comp: return {}
        return dict(((pn, comp[pn]) for pn in ('setStatPath',
                    'lowerThresholdCritical', 'lowerThresholdFatal',
                    'lowerThresholdNonCritical', 'unitModifier') \
                    if comp.get(pn) is not None))

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_Fan")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_Fan")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                inst.update(self._getStatPath(results, inst))
                if "type" in inst:
                    inst["type"] = self._getType(inst["type"])
                    if not inst['type']: del inst["type"]
                elif "setStatPath" in inst:
                    inst["type"] = "Active Cooling"
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                collections = self._getCollections(results, inst)
                if collections:
                    om.setCollections = collections
                rm.append(om)
            except AttributeError:
                continue
        if len(rm.maps) == 0: return
        return rm
