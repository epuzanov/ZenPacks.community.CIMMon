################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAChassisMap

SNIAChassisMap maps SNIA_Chassis class to CIM_Chassis class.

$Id: SNIAChassisMap.py,v 1.0 2012/01/23 23:46:12 egor Exp $"""

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMChassisMap \
    import CIMChassisMap

class SNIAChassisMap(CIMChassisMap):
    """Map SNIA_Chassis CIM class to CIM_Chassis class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Chassis":
                (
                    "SELECT * FROM CIM_Chassis",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_cptype":"ChassisPackageType",
                        "title":"ElementName",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                        "_pn":"PartNumber",
                        "id":"Tag",
                        "_sysname":"Tag",
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
            "CIM_ComputerSystemPackage":
                (
                    "SELECT Antecedent,Dependent FROM CIM_ComputerSystemPackage",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # Chassis
                        "dep":"Dependent", # ComputerSystem
                    },
                ),
            }
