################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMFileSystemMap

CIMFileSystemMap maps the CIM_FileSystem class to filesystems objects

$Id: CIMFileSystemMap.py,v 1.0 2011/06/07 20:33:39 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMFileSystemMap(SQLPlugin):

    maptype = "CIMFileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zFileSystemMapIgnoreNames',
                                                    'zFileSystemMapIgnoreTypes',
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
            "CIM_FileSystem":
                (
                "SELECT __PATH,BlockSize,FileSystemSize,FileSystemType,MaxFileNameLenght,Root FROM CIM_FileSystem",
                None,
                cs,
                    {
                    '__PATH':'snmpindex',
                    'BlockSize':'blockSize',
                    'FileSystemType':'type',
                    'MaxFileNameLenght':'maxNameLen',
                    'Root':'mount',
                    'FileSystemSize':'totalBlocks',
                    }
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        skipfstypes = getattr(device, 'zFileSystemMapIgnoreTypes', None)
        for instance in results.get("CIM_FileSystem", []):
            try:
                if skipfsnames and re.search(skipfsnames, instance['mount']):
                    log.info("Skipping %s as it matches zFileSystemMapIgnoreNames.",
                        instance['mount'])
                    continue
                if skipfstypes and instance['type'] in skipfstypes:
                    log.info("Skipping %s (%s) as it matches zFileSystemMapIgnoreTypes.",
                        instance['mount'], instance['type'])
                    continue
                om = self.objectMap(instance)
                om.id = self.prepId(om.mount)
                if ':' in om.snmpindex:om.snmpindex=om.snmpindex.split(':',1)[1]
                om.blockSize = getattr(om, 'blockSize', 4096) or 4096
                if not om.totalBlocks: continue
                om.totalBlocks = om.totalBlocks / om.blockSize
            except AttributeError:
                continue
            rm.append(om)
        return rm
