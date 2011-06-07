################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTemperatureSensorMap

CIMTemperatureSensorMap maps CIM_TemperatureSensor class to TemperatureSensor
class.

$Id: CIMTemperatureSensorMap.py,v 1.0 2011/06/07 20:37:19 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMTemperatureSensorMap(SQLPlugin):
    """Map CIM_TemperatureSensor class to TemperatureSensor class"""

    maptype = "CIMTemperatureSensorMap"
    modname = "ZenPacks.community.CIMMon.CIM_TemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
                                                    )

    numericSensorTypes = {
        0: "Unknown",
        1: "Other",
        2: "System board",
        3: "Host System board",
        4: "I/O board",
        5: "CPU board",
        6: "Memory board",
        7: "Storage bays",
        8: "Removable Media Bays",
        9: "Power Supply Bays",
        10:"Ambient / External / Room",
        11:"Chassis",
        12:"Bridge Card",
        13:"Management board",
        14:"Remote Management Card",
        15:"Generic Backplane",
        16:"Infrastructure Network",
        17:"Blade Slot in Chassis/Infrastructure",
        18:"Front Panel",
        19:"Back Panel",
        20:"IO Bus",
        21:"Peripheral Bay",
        22:"Device Bay",
        23:"Switch",
        24:"Software-defined",
        }


    def queries(self, device):
        args = [getattr(device, 'zCIMConnectionString',
                                        "'pywbemdb',scheme='https',port=5989")]
        kwargs = eval('(lambda *argsl,**kwargs:kwargs)(%s)'%args[0])
        if 'host' not in kwargs:
            args.append("host='%s'"%device.manageIp)
        if 'user' not in kwargs:
            args.append("user='%s'"%getattr(device, 'zWinUser', ''))
        if 'password' not in kwargs:
            args.append("password='%s'"%getattr(device, 'zWinPassword', ''))
        if 'namespace' not in kwargs:
            args.append("namespace='%s'"%getattr(device, 'zCIMHWNamespace',
                                                'root/cimv2'))
        cs = ','.join(args)
        return {
            "CIM_TemperatureSensor":
                (
                    "SELECT * FROM CIM_NumericSensor",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'BaseUnits':'baseUnits',
                        'Name':'id',
                        'NumericSensorType':'type',
                        'SensorType':'_sensorType',
                        'UnitModifier':'unitModifier',
                        'UpperThresholdCritical':'upperThresholdCritical',
                        'UpperThresholdFatal':'upperThresholdFatal',
                        'UpperThresholdNonCritical':'upperThresholdNonCritical',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_TemperatureSensor", []):
            if instance['_sensorType'] != 2: continue
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
            om.type=self.numericSensorTypes.get(int(getattr(om,'type',0) or 0),
                                                                    'Unknown')
            if om.cimClassName.upper().startswith('IBMPSG_'): om.baseUnits = 2
            rm.append(om)
        return rm
