################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """CIMNetworkPortMap

Gather IP network interface information from CIMMOM, and 
create DMD interface objects

$Id: CIMNetworkPortMap.py,v 1.2 2011/06/21 22:13:12 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

import re
import types
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

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


class CIMNetworkPortMap(SQLPlugin):
    """
    Map IP network names and aliases to DMD 'interface' objects
    """
    maptype = "InterfaceMap" 
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMConnectionString',
                                                    'zInterfaceMapIgnoreNames',
                                                    'zInterfaceMapIgnoreTypes',
                                               'zInterfaceMapIgnoreIpAddresses')

    def queries(self, device):
        args = [getattr(device, 'zCIMConnectionString',
                                        "'pywbemdb',scheme='https',port=5989")]
        kwargs = eval('(lambda *argsl,**kwargs:kwargs)(%s)'%args[0])
        if 'host' not in kwargs:
            args.append("host='%s'"%device.manageIp)
        if 'user' not in kwargs:
            args.append("user='%s'"%getattr(device, 'zWinUser', ''))
        if 'password' not in kwargs:
            args.append("password='%s'"%getattr(device, 'zWinPassword', ''))
        if 'namespace' not in kwargs:
            args.append("namespace='root/cimv2'")
        cs = ','.join(args)
        return {
            "CIM_NetworkPort": (
                "SELECT __PATH,ActiveMaximumTransmissionUnit,ElementName,EnabledDefault,EnabledState,LinkTechnology,PermanentAddress,Speed FROM CIM_NetworkPort",
                None,
                cs,
                {
                    '__PATH':'snmpindex',
                    'ActiveMaximumTransmissionUnit':'mtu',
                    'ElementName':'interfaceName',
                    'EnabledDefault':'adminStatus',
                    'EnabledState':'operStatus',
                    'LinkTechnology':'type',
                    'PermanentAddress':'macaddress',
                    'Speed':'speed',
                }
            ),
            "CIM_IPProtocolEndpoint": (
                "SELECT ElementName,IPv4Address,ProtocolIFType,SubnetMask FROM CIM_IPProtocolEndpoint",
                None,
                cs,
                {
                    'ElementName':'name',
                    'IPv4Address':'ipAddress',
                    'SubnetMask':'netmask',
                }
            ),
        }

    linkTypes = {
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
    }

    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        dontCollectIntNames = getattr(device, 'zInterfaceMapIgnoreNames', None)
        dontCollectIntTypes = getattr(device, 'zInterfaceMapIgnoreTypes', None)
        dontCollectIpAddresses = getattr(device, 'zInterfaceMapIgnoreIpAddresses', None)
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
        for instance in results.get("CIM_NetworkPort", []):
            try:
                om = self.objectMap(instance)
                om.type = self.linkTypes.get(getattr(om, 'type', 0), 'Unknown')
                if dontCollectIntNames and re.search(dontCollectIntNames,
                                                            om.interfaceName):
                    log.debug("Interface %s matched the zInterfaceMapIgnoreNames zprop '%s'" % (
                                om.interfaceName, getattr(device, 'zInterfaceMapIgnoreNames')))
                    continue
                if dontCollectIntTypes and re.search(dontCollectIntTypes,
                                                                    om.type):
                    log.debug( "Interface %s type %s matched the zInterfaceMapIgnoreTypes zprop '%s'" % (
                                om.interfaceName, om.type, getattr(device, 'zInterfaceMapIgnoreTypes')))
                    continue
                om.id = prepId(om.interfaceName)
                om.setIpAddresses = []
                for ep in results.get("CIM_IPProtocolEndpoint", []):
                    if om.id not in ep.get('name', ''): continue
                    ip = ep.get('ipAddress', '')
                    if not ip or not ip.strip() or (dontCollectIpAddresses
                        and re.search(dontCollectIpAddresses, ip)):
                        continue
                    # ignore IPv6 Addresses
                    if ip.__contains__(':'): continue
                    netmask = self.maskToBits(ep.get('netmask','255.255.255.0'))
                    om.setIpAddresses.append("/".join((ip, str(netmask))))
                om.ifindex = om.snmpindex
                if om.operStatus in [None, 2, 9]: om.operStatus = 1
                else: om.operStatus = 2
                if om.adminStatus in [0, 2]: om.adminStatus = 1
                else:om.adminStatus = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm


