################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32VolumeMap

Win32VolumeMap maps the Win32_Volume class to filesystems objects

$Id: Win32VolumeMap.py,v 1.1 2012/10/14 16:46:13 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMFileSystemMap \
    import CIMFileSystemMap

class Win32VolumeMap(CIMFileSystemMap):
    """Map Win32_Volume class to FileSystem class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_FileSystem":
                (
                    "SELECT * FROM Win32_Volume",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "blockSize":"BlockSize",
                        "totalBlocks":"Capacity",
                        "type":"FileSystem",
                        "maxNameLen":"MaximumFileNameLength",
                        "mount":"Name",
                        "state":"Status",
                        "status":"OperationalStatus",
                    }
                ),
            }
