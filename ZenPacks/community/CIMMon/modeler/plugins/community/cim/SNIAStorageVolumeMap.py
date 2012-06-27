################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStorageVolumeMap

SNIAStorageVolumeMap maps SNIA_StorageVolume class to CIM_StorageVolume class.

$Id: SNIAStorageVolumeMap.py,v 1.1 2012/06/27 19:47:05 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMStorageVolumeMap \
    import CIMStorageVolumeMap

class SNIAStorageVolumeMap(CIMStorageVolumeMap):
    """Map SNIA_StorageVolume CIM class to CIM_StorageVolume class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_StorageVolume":
                (
                    "SELECT * FROM CIM_StorageVolume",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "accessType":"Access",
                        "blockSize":"BlockSize",
                        "_dr":"DataRedundancy",
                        "id":"DeviceID",
                        "title":"ElementName",
                        "_pr":"PackageRedundancy",
                        "totalBlocks":"NumberOfBlocks",
                        "_sysname":"SystemName",
                    },
                ),
            "CIM_SystemComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_SystemComponent",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            "CIM_AllocatedFromStoragePool":
                (
                    "SELECT Antecedent,Dependent FROM CIM_AllocatedFromStoragePool",
                    None,
                    cs,
                    {
                        "ant":"Antecedent",
                        "dep":"Dependent",
                    },
                ),
            "CIM_MemberOfCollection":
                (
                    "SELECT Member,Collection FROM CIM_MemberOfCollection",
                    None,
                    cs,
                    {
                        "member":"Member",
                        "collection":"Collection",
                    },
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
