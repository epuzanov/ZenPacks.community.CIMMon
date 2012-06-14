################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32DiskDriveMap

Win32DiskDriveMap maps Win32_DiskDrive class to CIM_DiskDrive class.

$Id: Win32DiskDriveMap.py,v 1.0 2012/06/14 23:04:48 egor Exp $"""

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMDiskDriveMap \
    import CIMDiskDriveMap

class Win32DiskDriveMap(CIMDiskDriveMap):
    """Map Win32_DiskDrive CIM class to HardDisk class"""

    deviceProperties = CIMPlugin.deviceProperties + ("zCIMHWConnectionString",)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_DiskDrive":
                (
                    "SELECT * FROM Win32_DiskDrive",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"DeviceID",
                        "diskType":"DiskInterface",
                        "size":"Size",
                        "description":"Caption",
                        "title":"Name",
                        "FWRev":"FirmwareRevision",
                        "_mediatype":"MediaType",
                        "bay":"SCSILogicalUnit",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_ElementStatisticalData":
                (
                    "SELECT ManagedElement,Stats FROM CIM_ElementStatisticalData",
                    None,
                    cs,
                    {
                        "me":"ManagedElement",
                        "stats":"Stats",
                    },
                ),
            }

    def _isHardDisk(self, inst):
        return str(inst.get("_mediatype")).startswith('Fixed')
