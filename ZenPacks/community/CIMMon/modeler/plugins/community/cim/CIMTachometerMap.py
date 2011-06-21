################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTachometerMap

CIMTachometerMap maps CIM_Tachometer class to CIMTachometer class.

$Id: CIMTachometerMap.py,v 1.1 2011/06/21 21:27:24 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMTachometerMap(SQLPlugin):
    """Map CIM_Tachometer class to Fan class"""

    maptype = "FanMap"
    modname = "ZenPacks.community.CIMMon.CIM_Tachometer"
    relname = "fans"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
                                                    )


    fanTypes = {0: 'Unknown',
                1: 'System Fan',
                2: 'Power Supply Fan',
                3: 'CPU Fan',
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
            "CIM_Tachometer":
                (
                    "SELECT * FROM CIM_NumericSensor",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'Description':'description',
                        'ElementName':'id',
                        'FanType':'type',
                        'SensorType':'_sensorType',
                        'UnitModifier':'unitModifier',
                        'LowerThresholdCritical':'lowerThresholdCritical',
                        'LowerThresholdFatal':'lowerThresholdFatal',
                        'LowerThresholdNonCritical':'lowerThresholdNonCritical',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_Tachometer", []):
            if instance['_sensorType'] != 5: continue
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
            om.type=self.fanTypes.get(int(getattr(om,'type',0) or 0),'Unknown')
            rm.append(om)
        if len(rm.maps) > 0: return rm
        return
