################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTemperatureSensorMap

CIMTemperatureSensorMap maps CIM_TemperatureSensor class to TemperatureSensor
class.

$Id: CIMTemperatureSensorMap.py,v 1.3 2012/06/13 20:49:01 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMTemperatureSensorMap(CIMPlugin):
    """Map CIM_TemperatureSensor class to TemperatureSensor class"""

    maptype = "TemperatureSensorMap"
    modname = "ZenPacks.community.CIMMon.CIM_TemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_TemperatureSensor":
                (
                    "SELECT * FROM CIM_NumericSensor",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "baseUnits":"BaseUnits",
                        "id":"Name",
                        "unitModifier":"UnitModifier",
                        "upperThresholdCritical":"UpperThresholdCritical",
                        "upperThresholdFatal":"UpperThresholdFatal",
                        "upperThresholdNonCritical":"UpperThresholdNonCritical",
                        "_sensorType":"SensorType",
                        "_sysname":"SystemName",
                    },
                ),
            }

    def _getType(self, sensorType):
        return sensorType

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_TemperatureSensor")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_TemperatureSensor")
        for inst in instances:
            if int(inst.get("_sensorType") or 0) != 2: continue
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            if "type" in inst:
                inst["type"] = self._getType(inst["type"])
                if not inst["type"]: del inst["type"]
            om = self.objectMap(inst)
            om.id = self.prepId(om.id)
            rm.append(om)
        return rm
