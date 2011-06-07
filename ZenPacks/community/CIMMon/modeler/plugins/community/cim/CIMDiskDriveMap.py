################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMDiskDriveMap

CIMDiskDriveMap maps CIM_DiskDrive class to HardDisk class.

$Id: CIMDiskDriveMap.py,v 1.0 2011/06/07 20:32:16 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CIMDiskDriveMap(SQLPlugin):
    """Map CIM_DiskDrive class to HardDisk"""

    maptype = "CIMDiskDriveMap"
    modname = "ZenPacks.community.CIMMon.CIM_DiskDrive"
    relname = "harddisks"
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
            "CIM_DiskDrive":
                (
                    "SELECT __PATH,__NAMESPACE,DeviceID FROM CIM_DiskDrive",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'DeviceID':'id',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_DiskDrive", []):
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
            rm.append(om)
        return rm
