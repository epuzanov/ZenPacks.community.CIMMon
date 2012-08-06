################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """CIMNetworkAdapterMap

Gather IP network interface information from CIMMOM, and 
create DMD interface objects

$Id: CIMNetworkAdapterMap.py,v 1.4 2012/08/06 20:35:05 egor Exp $"""

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


class CIMNetworkAdapterMap(CIMPlugin):
    """
    Map IP network names and aliases to DMD 'interface' objects
    """
    maptype = "InterfaceMap"
    compname = "os"
    relname = "interfaces"
    modname = "ZenPacks.community.CIMMon.CIM_NetworkAdapter"
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
            "CIM_NetworkAdapter":
                (
                    "SELECT * FROM CIM_NetworkAdapter",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "interfaceName":"Name",
                        "description":"Description",
                        "duplex":"FullDuplex",
                        "macaddress":"PermanentAddress",
                        "snmpindex":"DeviceID",
                        "speed":"MaxSpeed",
                        "adminStatus":"StatusInfo",
                        "_sysname":"SystemName",
                    }
                ),
            }

    def _getMacAddress(self, value):
        """
        Return the formated string
        """
        if not value: return ""
        if len(str(value)) == 12 and ":" not in value:
            return ":".join([value[s*2:s*2+2] for s in range(6)])
        return value

    def _getAdapterConfig(self, results, inst, dontCollectIpAddresses):
        return

    def _getLinkType(self, inst):
        return "ethernetCsmacd"

    def _getOperStatus(self, inst):
        return 1

    def _getAdminStatus(self, inst):
        return int(inst.get("adminStatus") or 3) in (3,) and 1 or 2

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
        instances = results.get("CIM_NetworkAdapter")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_NetworkAdapter")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                interfaceName = inst.get("interfaceName")
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
                self._getAdapterConfig(results, inst, dontCollectIpAddresses)
                om = self.objectMap(inst)
                om.id = prepId(om.interfaceName)
                om.macaddress = self._getMacAddress(inst.get("macaddress"))
                om.operStatus = self._getOperStatus(inst)
                if om.operStatus == 2: continue
                om.adminStatus = self._getAdminStatus(inst)
                statPath = self._getStatPath(results, inst)
                if statPath:
                    om.setStatPath = statPath
            except AttributeError:
                continue
            for a,v in om.__dict__.iteritems():
                if v is None: print om
            rm.append(om)
        return rm
