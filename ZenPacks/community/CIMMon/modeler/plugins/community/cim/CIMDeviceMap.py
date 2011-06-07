################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DeviceMap

DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
os products.

$Id: DeviceMap.py,v 1.0 2011/06/07 20:29:42 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs, ObjectMap

class CIMDeviceMap(SQLPlugin):
    """DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
       os products.
    """

    maptype = "CIMDeviceMap" 
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
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
            args.append("namespace='root/cimv2'")
        cs = ','.join(args)
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT Name,Description,PrimaryOwnerContact FROM CIM_ComputerSystem",
                    None,
                    cs,
                    {
                        'Name':'snmpSysName',
                        'Descriptions':'snmpDescr',
                        'PrimaryOwnerContact': 'snmpContact',
                    },
                ),
            "CIM_OperatingSystem":
                (
                    "SELECT Name,TotalVisibleMemorySize,SizeStoredInPagingFiles FROM CIM_OperatingSystem",
                    None,
                    cs,
                    {
                        'Name':'setOSProductKey',
                        'TotalVisibleMemorySize':'_totalMemory',
                        'SizeStoredInPagingFiles':'_totalSwap',
                    },
                ),
            }


    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        try:
            os = results.get('CIM_OperatingSystem', [{}])[0]
            os.update(results.get('CIM_ComputerSystem', [{}])[0])
            if not os: return
            maps = []
            om = self.objectMap(os)
            om.snmpLocation = ''
            om.snmpOid = ''
            maps.append(om)
            maps.append(ObjectMap({"totalMemory": (os['_totalMemory'] * 1024)},
                                                                compname="hw"))
            maps.append(ObjectMap({"totalSwap": (os['_totalSwap'] * 1024)},
                                                                compname="os"))
        except:
            log.warning('processing error')
            return
        return maps

