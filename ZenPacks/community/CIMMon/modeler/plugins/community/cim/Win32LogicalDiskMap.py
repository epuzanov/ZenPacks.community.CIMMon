################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32LogicalDiskMap

Win32LogicalDiskMap maps the Win32_LogicalDisk class to filesystems objects

$Id: Win32LogicalDiskMap.py,v 1.1 2012/10/14 16:45:10 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMFileSystemMap \
    import CIMFileSystemMap

class Win32LogicalDiskMap(CIMFileSystemMap):
    """Map Win32_LogicalDisk class to FileSystem class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_FileSystem":
                (
                    "SELECT * FROM Win32_LogicalDisk",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "blockSize":"BlockSize",
                        "type":"FileSystem",
                        "maxNameLen":"MaximumComponentLenght",
                        "mount":"Name",
                        "totalBlocks":"Size",
                        "state":"Status",
                        "status":"OperationalStatus",
                    }
                ),
            }
