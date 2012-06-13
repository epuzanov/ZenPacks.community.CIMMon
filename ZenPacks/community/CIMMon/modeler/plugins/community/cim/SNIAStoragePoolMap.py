################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAStoragePoolMap

SNIAStoragePoolMap maps SNIA_StoragePool class to CIM_StoragePool class.

$Id: SNAIStoragePoolMap.py,v 1.0 2012/01/23 23:51:14 egor Exp $"""

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMStoragePoolMap \
    import CIMStoragePoolMap

class SNIAStoragePoolMap(CIMStoragePoolMap):
    """Map SNIA_StoragePool CIM class to CIM_StoragePool class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_StoragePool":
                (
                    "SELECT * FROM CIM_StoragePool",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"InstanceID",
                        "title":"ElementName",
                        "poolId":"PoolID",
                        "_primordial":"Primordial",
                        "totalManagedSpace":"TotalManagedSpace",
                        "usage":"Usage",
                        "_sysname":"InstanceID",
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
            }
