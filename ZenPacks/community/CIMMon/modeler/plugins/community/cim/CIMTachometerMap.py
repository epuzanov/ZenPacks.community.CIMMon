################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTachometerMap

CIMTachometerMap maps CIM_Tachometer class to CIM_Tachometer class.

$Id: CIMTachometerMap.py,v 1.3 2012/06/13 20:48:37 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMFanMap \
    import CIMFanMap

class CIMTachometerMap(CIMFanMap):
    """Map CIM_Tachometer class to Fan class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Fan":
                (
                    "SELECT * FROM CIM_NumericSensor",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "setStatPath":"__PATH",
                        "title":"Description",
                        "id":"DeviceID",
                        "lowerThresholdCritical":"LowerThresholdCritical",
                        "lowerThresholdFatal":"LowerThresholdFatal",
                        "lowerThresholdNonCritical":"LowerThresholdNonCritical",
                        "_sensorType":"SensorType",
                        "_sysname":"SystemName",
                        "unitModifier":"UnitModifier",
                    }
                ),
            }
