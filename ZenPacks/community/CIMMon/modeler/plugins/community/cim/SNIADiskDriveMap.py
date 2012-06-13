################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIADiskDriveMap

SNIADiskDriveMap maps SNIA_DiskDrive class to CIM_DiskDrive class.

$Id: SNAIDiskDriveMap.py,v 1.0 2012/01/23 23:49:15 egor Exp $"""

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMDiskDriveMap \
    import CIMDiskDriveMap

class SNIADiskDriveMap(CIMDiskDriveMap):
    """Map CIM_DiskDrive CIM class to HardDisk class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_DiskDrive":
                (
                    "SELECT * FROM CIM_DiskDrive",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"DeviceID",
                        "diskType":"DiskType",
                        "formFactor":"FormFactor",
                        "size":"MaxMediaSize",
                        "description":"ElementName",
                        "title":"ElementName",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_PhysicalPackage":
                (
                    "SELECT * FROM CIM_PhysicalPackage",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "replaceable":"Replaceable",
                        "serialNumber":"SerialNumber",
                        "FWRev":"Version",
                    },
                ),
            "CIM_StoragePool":
                (
                    "SELECT * FROM CIM_StoragePool",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "_primordial":"Primordial",
                    },
                ),
            "CIM_Chassis":
                (
                    "SELECT * FROM CIM_Chassis",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
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
            "CIM_Realizes":
                (
                    "SELECT Antecedent,Dependent FROM CIM_Realizes",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # PhysicalPackage
                        "dep":"Dependent", # DiskDrive
                    },
                ),
            "CIM_Container":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_Container",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # Enclosure
                        "pc":"PartComponent", # PhysicalPackage
                    },
                ),
            "CIM_SoftwareIdentity":
                (
                    "SELECT __PATH,VersionString FROM CIM_SoftwareIdentity",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "FWRev":"VersionString",
                    },
                ),
            "CIM_ElementSoftwareIdentity":
                (
                    "SELECT Antecedent,Dependent FROM CIM_ElementSoftwareIdentity",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # Firmware
                        "dep":"Dependent", # DiskDrive
                    },
                ),
            "CIM_PhysicalElementLocation":
                (
                    "SELECT Element,PhysicalLocation FROM CIM_PhysicalElementLocation",
                    None,
                    cs,
                    {
                        "element":"Element", # PhysicalPackage
                        "location":"PhysicalLocation", # PhysicalLocation
                    },
                ),
            "CIM_ConcreteComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM CIM_ConcreteComponent",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # StoragePool
                        "pc":"PartComponent", # DiskExtent
                    },
                ),
            "CIM_MediaPresent":
                (
                    "SELECT Antecedent,Dependent FROM CIM_MediaPresent",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # DiskDrive
                        "dep":"Dependent", # DiskExtent
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
