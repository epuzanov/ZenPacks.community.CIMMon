################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """Win32IP4RouteTableMap

Win32IP4RouteTableMap gathers and stores IP4 routing information.

$Id: Win32IP4RouteTableMap.py,v 1.0 2012/06/13 20:52:16 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class Win32IP4RouteTableMap(CIMPlugin):
    """Map Win32_IP4RouteTable class to IpRouteEntry class"""

    maptype = "RouteMap"
    relname = "routes"
    compname = "os"
    modname = "Products.ZenModel.IpRouteEntry"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',
                                                'zRouteMapMaxRoutes',
                                                'zRouteMapCollectOnlyLocal',
                                                'zRouteMapCollectOnlyIndirect')

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "Win32_IP4RouteTable":
                (
                    "SELECT * FROM Win32_IP4RouteTable",
                    None,
                    cs,
                    {
                        "snmpindex":"__PATH",
                        "id":"Destination",
                        "routemask":"Mask",
                        "metric1":"Metric1",
                        "setInterfaceIndex":"InterfaceIndex",
                        "setNextHopIp":"NextHop",
                        "routeproto":"Protocol",
                        "routetype":"Type",
                    }
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        localOnly = getattr(device, 'zRouteMapCollectOnlyLocal', False)
        indirectOnly = getattr(device, 'zRouteMapCollectOnlyIndirect', False)
        maxRoutes = getattr(device, 'zRouteMapMaxRoutes', 500)
        rm = self.relMap()
        for route in results.get("Win32_IP4RouteTable", ()):
            if len(rm.maps) > maxRoutes:
                log.warning("Maximum number of routes (%d) exceeded", maxRoutes)
                break
            om = self.objectMap(route)
            if not hasattr(om, "id"): continue
            if not hasattr(om, "routemask"): continue
            om.routemask = self.maskToBits(om.routemask)

            # Workaround for existing but invalid netmasks
            if om.routemask is None: continue

            om.setTarget = "%s/%s"%(om.id, om.routemask)
            om.id = "%s_%s"%(om.id, om.routemask)
            if om.routemask == 32: continue
            routeproto = getattr(om, "routeproto", "") or "other"
            om.routeproto = self.mapSnmpVal(routeproto, self.routeProtoMap)
            if localOnly and om.routeproto != "local": continue
            if not hasattr(om, "routetype"): continue
            om.routetype = self.mapSnmpVal(om.routetype, self.routeTypeMap)
            if indirectOnly and om.routetype != "indirect": continue
            rm.append(om)
        return rm

    def mapSnmpVal(self, value, map):
        if len(map)+1 >= value:
            value = map[int(value-1)]
        return value

    routeTypeMap = ('other', 'invalid', 'direct', 'indirect')
    routeProtoMap = ('other', 'local', 'netmgmt', 'icmp',
            'egp', 'ggp', 'hello', 'rip', 'is-is', 'es-is',
            'ciscoIgrp', 'bbnSpfIgrp', 'ospf', 'bgp')
