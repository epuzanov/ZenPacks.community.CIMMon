################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32NetworkAdapterMap

Win32NetworkAdapterMap maps the Win32_NetworkAdapter class to filesystems objects

$Id: Win32NetworkAdapterMap.py,v 1.1 2012/06/14 21:32:55 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMNetworkAdapterMap \
    import CIMNetworkAdapterMap

class Win32NetworkAdapterMap(CIMNetworkAdapterMap):
    """
    Map IP network names and aliases to DMD 'interface' objects
    """
    modname = "ZenPacks.community.CIMMon.CIM_NetworkAdapter"

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_NetworkAdapter":
                (
                    "SELECT * FROM Win32_NetworkAdapter",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "description":"Description",
                        "type":"AdapterType",
                        "snmpindex":"DeviceID",
                        "ifindex":"InterfaceIndex",
                        "interfaceName":"Name",
                        "macaddress":"MACAddress",
                        "speed":"MaxSpeed",
                        "operStatus":"NetConnectionStatus",
                        "adminStatus":"StatusInfo",
                    }
                ),
            "Win32_NetworkAdapterConfiguration":
                (
                    "SELECT * FROM Win32_NetworkAdapterConfiguration",
                    None,
                    cs,
                    {
                        "_descr":"Description",
                        "snmpindex":"Index",
                        "_ipAddress":"IPAddress",
                        "_ipEnabled":"IPEnabled",
                        "_ipSubnet":"IPSubnet",
                        "mtu":"MTU",
                    }
                ),
            "Win32_PerfRawData_Tcpip_NetworkInterface":
                (
                    "SELECT * FROM Win32_PerfRawData_Tcpip_NetworkInterface",
                    None,
                    cs,
                    {
                        "setStatPath":"__PATH",
                        "Name":"Name",
                        "speed":"CurrentBandwidth",
                    }
                )
            }

    def _getOperStatus(self, inst):
        return {0:2,1:3,2:1,3:2,4:6,5:6,6:5,7:7,8:3,9:1,10:2,11:5,12:5}.get(
            int(inst.get("operStatus", 2))) or 1

    def _getAdapterConfig(self, results, inst, dontCollectIpAddresses):
        intIdx = str(inst.get("snmpindex") or "")
        if not intIdx: return
        if "setIpAddresses" not in inst:
            inst["setIpAddresses"] = []
        for conf in results.get("Win32_NetworkAdapterConfiguration") or ():
            if str(conf.get("_ipEnabled")).lower() != "true": continue
            if str(int(conf.get("snmpindex") or 0)) == intIdx: break
        else: return
        if ("mtu" in conf) and not inst.get("mtu"):
            inst["mtu"] = int(conf.get("mtu") or 1500)
        ips = conf.get("_ipAddress", "") or []
        if not isinstance(ips, (list, tuple)):
            ips = [ips]
        if ips:
            netmasks = conf.get("_ipSubnet", "") or ""
            if not isinstance(netmasks, (list, tuple)):
                netmasks = [netmasks or '255.255.255.0' for x in ips]
            for ip, mask in zip(ips, netmasks):
                if not ip.strip() or (dontCollectIpAddresses
                    and re.search(dontCollectIpAddresses, ip)):
                    continue
                if ip.__contains__('.'):
                    ip = '/'.join((ip, str(self.maskToBits(mask))))
                if ip in inst["setIpAddresses"]: continue
                inst["setIpAddresses"].append(ip)
        perfName = str(conf.get("_descr") or "").replace("#", "_")
        if not perfName or "setStatPath" in inst: return
        for perf in results.get("Win32_PerfRawData_Tcpip_NetworkInterface", ()):
            if str(perf.get("Name")) == perfName: break
        else: return
        if ("speed" in perf) and not inst.get("speed"):
            inst["speed"] = int(perf.get("speed") or 0)
        inst["setStatPath"] = str(perf.get("setStatPath") or "")

    def _getLinkType(self, inst):
        return inst.get('type') or "Ethernet 802.3"

    def _getStatPath(self, results, inst):
        iPath = inst.get("setPath")
        if not iPath: return ""
        for perf in results.get("CIM_NetworkAdapter") or ():
            if perf.get("setPath") == iPath: break
        else: return ""
        return str(perf.get("setStatPath") or "")

