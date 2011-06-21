################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMFanMap

CIMFanMap maps CIM_Fan class to Fan class.

$Id: CIMFanMap.py,v 1.1 2011/06/21 21:23:52 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMFanMap(SQLPlugin):
    """Map CIM_Fan class to Fan class"""

    maptype = "FanMap"
    modname = "ZenPacks.community.CIMMon.CIM_Fan"
    relname = "fans"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
                                                    )



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
            "CIM_Fan":
                (
                    "SELECT __PATH,__NAMESPACE,ActiveCooling,DeviceID FROM CIM_Fan",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'ActiveCooling':'type',
                        'DeviceID':'id',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_Fan", []):
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
            if str(getattr(om, 'type', 'true')).lower() == 'true':
                om.type = 'Active Cooling'
            else:
                om.type = 'Passive Cooling'
            rm.append(om)
        if len(rm.maps) > 0: return rm
        return
