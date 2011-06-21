################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMStorageVolumeMap

CIMStorageVolumeMap maps CIM_StorageVolume class to LogicalDisk class.

$Id: CIMStorageVolumeMap.py,v 1.1 2011/06/21 21:27:05 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMStorageVolumeMap(SQLPlugin):
    """Map CIM_StorageVolume class to LogicalDisk"""

    maptype = "LogicalDiskMap"
    modname = "ZenPacks.community.CIMMon.CIM_StorageVolume"
    relname = "logicaldisks"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zCIMHWNamespace',
                                                    )

    raidLevels = {
        (0, 1): 'RAID0',
        (1, 1): 'RAID5',
        (1, 2): 'RAID1+0',
        (2, 1): 'RAID6',
        (2, 2): 'RAID5+1',
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
            "CIM_StorageVolume":
                (
                    "SELECT __PATH,__NAMESPACE,BlockSize,DataRedundancy,DeviceID,ElementName,NumberOfBlocks,PackageRedundancy FROM CIM_StorageVolume",
                    None,
                    cs,
                    {
                        '__PATH':'_path',
                        '__NAMESPACE':'cimNamespace',
                        'BlockSize':'_blocksize',
                        'DataRedundancy':'_dr',
                        'DeviceID':'id',
                        'ElementName':'description',
                        'NumberOfBlocks':'_blocks',
                        'PackageRedundancy':'_pr',
                    },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_StorageVolume", []):
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                om.cimClassName, om.cimKeybindings = om._path.split('.', 1)
                om._pr = int(getattr(om, '_pr', 0) or 0)
                om._dr = int(getattr(om, '_dr', 0) or 0)
                if om._dr > 2: om._dr = 2
                om.diskType = self.raidLevels.get((om._pr, om._dr), 'unknown')
                if om._blocksize and om._blocks:
                    om.size = int(om._blocksize) * int(om._blocks)
            except AttributeError:
                continue
            rm.append(om)
        return rm
