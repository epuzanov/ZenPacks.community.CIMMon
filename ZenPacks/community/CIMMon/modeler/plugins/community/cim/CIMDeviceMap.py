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

$Id: DeviceMap.py,v 1.2 2011/06/21 21:22:47 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs, ObjectMap

class CIMDeviceMap(SQLPlugin):
    """DeviceMap maps CIM_ComputerSystem and CIM_OperationSystem classes to get hw and
       os products.
    """

    maptype = "DeviceMap"
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
                    "SELECT PrimaryOwnerContact FROM CIM_ComputerSystem",
                    None,
                    cs,
                    {
                        'PrimaryOwnerContact': 'snmpContact',
                    },
                ),
            "CIM_OperatingSystem":
                (
                    "SELECT CSName,Description,Name,TotalVirtualMemorySize,TotalVisibleMemorySize FROM CIM_OperatingSystem",
                    None,
                    cs,
                    {
                        'CSName':'snmpSysName',
                        'Description':'setOSProductKey',
                        'Name':'_name',
                        'TotalVisibleMemorySize':'_totalMemory',
                        'TotalVirtualMemorySize':'_totalSwap',
                        'Version':'_version',
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
            maps.append(om)
            if om._name.startswith('Microsoft'):
                om.setOSProductKey = om._name.split('|', 1)[0]
                om.snmpDescr = '%s (%s)'%(om.setOSProductKey, om._version)
            elif om.setOSProductKey.startswith('A class'):
                om.setOSProductKey = om._version
                om.snmpDescr = om._version
            else:
                om.setOSProductKey = om.setOSProductKey.split('\n', 1)[0]
                om.snmpDescr = '%s (%s)'%(om.setOSProductKey, om._version)
            om.setOSProductKey =  MultiArgs(om.setOSProductKey,
                                            om.setOSProductKey.split(' ', 1)[0])
            maps.append(ObjectMap({"totalMemory": (
                            os.get('_totalMemory', 0) * 1024)}, compname="hw"))
            maps.append(ObjectMap({"totalSwap": (
                            os.get('_totalSwap', 0) * 1024)}, compname="os"))
        except:
            log.warning('processing error')
            return
        return maps

