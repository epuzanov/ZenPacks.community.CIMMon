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

$Id: Win32DiskDriveMap.py,v 1.2 2012/06/18 23:29:23 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMDiskDriveMap \
    import CIMDiskDriveMap

class Win32DiskDriveMap(CIMDiskDriveMap):
    """Map Win32_DiskDrive CIM class to HardDisk class"""

    deviceProperties = CIMPlugin.deviceProperties+("zCIMConnectionString",)

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
                        "_index":"Index",
                        "diskType":"InterfaceType",
                        "size":"Size",
                        "description":"Caption",
                        "title":"Caption",
                        "FWRev":"FirmwareRevision",
                        "_mediatype":"MediaType",
                        "bay":"SCSILogicalUnit",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_ElementStatisticalData":
                (
                    "SELECT Name FROM Win32_PerfRawData_PerfDisk_PhysicalDisk",
                    None,
                    cs,
                    {
                        "name":"Name",
                    },
                ),
            }

    def _diskTypes(self, diskType):
        return str(diskType).lower()

    def _isHardDisk(self, inst):
        return str(inst.get("_mediatype")).startswith('Fixed')

    def _getStatPath(self, results, inst):
        idx = str(int(inst.get("_index") or -1))
        if idx is "-1": return ""
        for stat in results.get("CIM_ElementStatisticalData") or ():
            name = str(stat.get("name") or "")
            if name.split()[0] == idx: break
        else: return ""
        return 'Win32_PerfRawData_PerfDisk_PhysicalDisk.Name="%s"'%name
