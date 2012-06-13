################################################################################
#
# This program is part of the SMISMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIAComputerSystemMap

SNIAComputerSystemMap maps SNIA_ComputerSystem class to CIM_ComputerSystem class.

$Id: SNAIComputerSystemMap.py,v 1.0 2012/01/23 23:47:24 egor Exp $"""

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMComputerSystemMap \
    import CIMComputerSystemMap

class SNIAComputerSystemMap(CIMComputerSystemMap):
    """Map SNIA_ComputerSystem CIM class to CIM_ComputerSystem class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_descr":"Description",
                        "_contact":"PrimaryOwnerContact",
                        "_sysname":"Name",
                        "title":"ElementName",
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
                        "ant":"Antecedent", # Controller
                        "dep":"Dependent", # ComputerSystem
                    },
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
                        "serialNumber":"SerialNumber",
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
