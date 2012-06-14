################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPowerSupplyMap

CIMPowerSupplyMap maps CIM_PowerSupply CIM class to CIMPowerSupply class.

$Id: CIMPowerSupplyMap.py,v 1.4 2012/06/14 21:22:50 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMPowerSupplyMap(CIMPlugin):
    """Map CIM_PowerSupply class to PowerSupply class"""

    maptype = "PowerSupplyMap"
    modname = "ZenPacks.community.CIMMon.CIM_PowerSupply"
    relname = "powersupplies"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_PowerSupply":
                (
                    "SELECT * FROM CIM_PowerSupply",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"DeviceID",
                        "watts":"TotalOutputPower",
                        "_sysname":"SystemName",
                    },
                ),
#            "CIM_VoltageSensor":
#                (
#                    "SELECT * FROM CIM_NumericSensor",
#                    None,
#                    cs,
#                    {
#                        "setStatPath":"__PATH",
#                        "lowerThresholdCritical":"LowerThresholdCritical",
#                        "lowerThresholdFatal":"LowerThresholdFatal",
#                        "lowerThresholdNonCritical":"LowerThresholdNonCritical",
#                        "unitModifier":"UnitModifier",
#                        "upperThresholdCritical":"UpperThresholdCritical",
#                        "upperThresholdFatal":"UpperThresholdFatal",
#                        "upperThresholdNonCritical":"UpperThresholdNonCritical",
#                    }
#                ),
#            "CIM_AssociatedSensor":
#                (
#                    "SELECT Antecedent,Dependent FROM CIM_AssociatedSensor",
#                    None,
#                    cs,
#                    {
#                        "ant":"Antecedent", # Tachometer
#                        "dep":"Dependent", # PowerSupply
#                    },
#                ),
            }

    def _getType(self, psType):
        return psType

    def _getStatPath(self, results, inst):
        comp =  self._findInstance(results, "CIM_VoltageSensor", "setStatPath",
                self._findInstance(results, "CIM_AssociatedSensor", "dep",
                inst.get("setPath")).get("ant"))
        if not comp: return {}
        return dict(((pn, comp[pn]) for pn in ('setStatPath',
                'lowerThresholdNonCritical', 'upperThresholdNoneCritical',
                'lowerThresholdCritical', 'upperThresholdCritical',
                'upperThresholdFatal', 'lowerThresholdFatal', 'unitModifier') \
                if comp.get(pn) is not None))

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_PowerSupply")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_PowerSupply")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            if "setStatPath" not in inst:
                inst.update(self._getStatPath(results, inst))
            if "type" in inst:
                inst["type"] = self._getType(inst["type"])
                if not inst["type"]: del inst["type"]
            om = self.objectMap(inst)
            om.id = self.prepId(om.id)
            if om.watts: om.watts = int(om.watts) / 1000
            rm.append(om)
        return rm


