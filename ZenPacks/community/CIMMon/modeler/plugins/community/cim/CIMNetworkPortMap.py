################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """CIMNetworkPortMap

Gather IP network interface information from CIMMOM, and 
create DMD interface objects

$Id: CIMNetworkPortMap.py,v 1.4 2012/06/14 21:20:53 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]

import re
import types
from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

def prepId(id, subchar='_'):
    """
    Make an id with valid url characters. Subs [^a-zA-Z0-9-_,.$\(\) ]
    with subchar.  If id then starts with subchar it is removed.

    @param id: user-supplied id
    @type id: string
    @return: valid id
    @rtype: string
    """
    _prepId = re.compile(r'[^a-zA-Z0-9-_,.$ ]').sub
    _cleanend = re.compile(r"%s+$" % subchar).sub
    if id is None: 
        raise ValueError('Ids can not be None')
    if type(id) not in types.StringTypes:
        id = str(id)
    id = _prepId(subchar, id)
    while id.startswith(subchar):
        if len(id) > 1: id = id[1:]
        else: id = "-"
    id = _cleanend("",id)
    id = id.strip()
    return str(id)


class CIMNetworkPortMap(CIMPlugin):
    """
    Map IP network names and aliases to DMD 'interface' objects
    """
    maptype = "InterfaceMap" 
    compname = "os"
    relname = "interfaces"
    modname = "ZenPacks.community.CIMMon.CIM_NetworkPort"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',
                                                    'zInterfaceMapIgnoreNames',
                                                    'zInterfaceMapIgnoreTypes',
                                               'zInterfaceMapIgnoreIpAddresses')

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
                        "interfaceName":"Name",
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

    def _getMacAddress(self, value):
        """
        Return the wwn formatedstring
        """
        if not value: return ""
        if len(str(value)) == 16 and ":" not in value:
            return "-".join([value[s*4:s*4+4] for s in range(4)])
        return value

    def _getIpAddresses(self, results, inst, dontCollectIpAddresses):
        iPath = inst.get("setPath")
        if not iPath: return
        if "setIpAddresses" not in inst:
            inst["setIpAddresses"] = []
        for ep in results.get("CIM_IPProtocolEndpoint", ()):
            if not self._findInstance(results, "CIM_PortImplementsEndpoint",
                "dep",ep.get("_path","")).get("ant","").endswith(iPath):continue
            if ('mtu' in ep) and ('mtu' not in inst):
                inst["mtu"] = ep["mtu"]
            ip = ep.get("_ipAddress")
            if ip.__contains__('.'):
                netmasks = ep.get("_ipSubnet") or "255.255.255.0"
                ip = '/'.join((ip, str(self.maskToBits(netmask))))
            elif ip.__contains__(':'):
                continue
            else:
                continue
            inst["setIpAddresses"].append(ip)

    def _getLinkType(self, inst):
        return {
            0: 'Unknown',
            1: 'softwareLoopback',
            2: 'ethernetCsmacd',
            3: 'Infiniband',
            4: 'Fibre Channel',
            5: 'fddi',
            6: 'atm',
            7: 'iso88025TokenRing',
            8: 'frame-relay',
            9: 'Infrared',
            10: 'Bluetooth',
            11: 'Wireless LAN',
            }.get(int(inst.get("type") or 2)) or "ethernetCsmacd"

    def _getOperStatus(self, inst):
        return int(inst.get("operStatus") or 2) in (0, 2, 5, 9) and 1 or 2

    def _getAdminStatus(self, inst):
        return int(inst.get("adminStatus") or 0) in (0, 2) and 1 or 2

    def _getController(self, results, inst):
        return self._findInstance(results, "CIM_SystemComponent", "pc",
                                            inst.get("setPath")).get("gc") or ""

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        dontCollectIntNames = getattr(device, 'zInterfaceMapIgnoreNames', None)
        dontCollectIntTypes = getattr(device, 'zInterfaceMapIgnoreTypes', None)
        dontCollectIpAddresses = getattr(device,
                                        'zInterfaceMapIgnoreIpAddresses', None)
        rm = self.relMap()
        if (dontCollectIpAddresses and re.search(dontCollectIpAddresses,
                                device.manageIp)):
            om = self.objectMap()
            om.id = self.prepId("Virtual IP Address")
            om.title = om.id
            om.interfaceName = om.id
            om.type = "softwareLoopback"
            om.speed = 1000000000
            om.mtu = 1500
            om.ifindex = "1"
            om.adminStatus = 1
            om.operStatus = 1
            om.monitor = False
            om.setIpAddresses = [device.manageIp, ]
            rm.append(om)
            return rm
        instances = results.get("CIM_NetworkPort")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_NetworkPort")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                interfaceName = inst.get("interfaceName") or ""
                if not interfaceName or not inst.get("setPath"): continue
                inst["type"] = self._getLinkType(inst)
                if dontCollectIntNames and re.search(dontCollectIntNames,
                                                    interfaceName):
                    log.debug("Interface %s matched the zInterfaceMapIgnoreNames zprop '%s'" % (
                                    interfaceName, dontCollectIntNames))
                    continue
                if dontCollectIntTypes and re.search(dontCollectIntTypes,
                                                                inst["type"]):
                    log.debug( "Interface %s type %s matched the zInterfaceMapIgnoreTypes zprop '%s'" % (
                        interfaceName, inst["type"], dontCollectIntTypes))
                    continue
                self._getIpAddresses(results, inst, dontCollectIpAddresses)
                om = self.objectMap(inst)
                om.id = prepId(om.interfaceName)
                om.macaddress = self._getMacAddress(inst.get("macaddress"))
                om.operStatus = self._getOperStatus(inst)
                if om.operStatus == 2: continue
                om.setController = self._getController(results, inst)
                om.adminStatus = self._getAdminStatus(inst)
                om.setStatPath = self._getStatPath(results, inst)
            except AttributeError:
                continue
            rm.append(om)
        return rm
