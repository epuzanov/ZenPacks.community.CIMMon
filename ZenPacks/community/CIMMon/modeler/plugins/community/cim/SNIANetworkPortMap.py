################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""SNIANetworkPortMap

SNIANetworkPortMap maps SNIA_NetworkPort class to CIM_NetworkPort class.

$Id: SNIANetworkPortMap.py,v 1.0 2012/01/23 23:50:55 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMNetworkPortMap \
    import CIMNetworkPortMap

class SNIANetworkPortMap(CIMNetworkPortMap):
    """Map SNIA_NetworkPort CIM class to CIM_NetworkPort class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_NetworkPort":
                (
                    "SELECT * FROM CIM_NetworkPort",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "description":"Description",
                        "mtu":"ActiveMaximumTransmissionUnit",
                        "interfaceName":"ElementName",
                        "adminStatus":"EnabledDefault",
                        "operStatus":"EnabledState",
                        "type":"LinkTechnology",
                        "macaddress":"PermanentAddress",
                        "speed":"Speed",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_IPProtocolEndpoint":
                (
                    "SELECT * FROM CIM_IPProtocolEndpoint",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "_ipAddress":"Address",
                        "_ipSubnet":"SubnetMask",
                    }
                ),
            "CIM_PortImplementsEndpoint":
                (
                    "SELECT Antecedent,Dependent FROM CIM_PortImplementsEndpoint",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # LogicalPort
                        "dep":"Dependent", # ProtocolEndpoint
                    }
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
