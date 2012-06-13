################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMFileSystemMap

CIMFileSystemMap maps the CIM_FileSystem class to filesystems objects

$Id: CIMFileSystemMap.py,v 1.2 2012/06/13 20:44:42 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

import re
from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMFileSystemMap(CIMPlugin):
    """Map CIM_FileSystem class to FileSystem class"""

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "ZenPacks.community.CIMMon.CIM_FileSystem"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',
                                                    'zFileSystemMapIgnoreNames',
                                                    'zFileSystemMapIgnoreTypes',
                                                    )

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_FileSystem":
                (
                    "SELECT * FROM CIM_FileSystem",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "blockSize":"BlockSize",
                        "type":"FileSystemType",
                        "maxNameLen":"MaxFileNameLenght",
                        "mount":"Root",
                        "totalBlocks":"FileSystemSize",
                        "_sysname":"CSName",
                    }
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        skipfsnames = getattr(device, "zFileSystemMapIgnoreNames", None)
        skipfstypes = getattr(device, "zFileSystemMapIgnoreTypes", None)
        instances = results.get("CIM_FileSystem")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_FileSystem")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                mount = inst.get("mount") or ""
                fstype = inst.get("type") or ""
                if skipfsnames and re.search(skipfsnames, mount):
                    log.info("Skipping %s as it matches zFileSystemMapIgnoreNames.",
                            mount)
                    continue
                if skipfstypes and fstype in skipfstypes:
                    log.info("Skipping %s (%s) as it matches zFileSystemMapIgnoreTypes.",
                            mount, fstype)
                    continue
                om = self.objectMap(inst)
                om.id = self.prepId(om.mount)
                om.blockSize = int(getattr(om, "blockSize", None) or 4096)
                om.totalBlocks = int(om.totalBlocks or 0) / om.blockSize
                om.setStatPath = self._getStatPath(results, inst.get("setPath"))
            except AttributeError:
                continue
            rm.append(om)
        return rm
