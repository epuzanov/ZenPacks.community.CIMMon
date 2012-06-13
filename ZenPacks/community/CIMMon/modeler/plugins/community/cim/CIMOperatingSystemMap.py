################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OperatingSystemMap

OperatingSystemMap maps CIM_OperationSystem class to os product.

$Id: OperatingSystemMap.py,v 1.0 2012/01/23 19:40:01 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs, ObjectMap

class CIMOperatingSystemMap(CIMPlugin):
    """
    OperatingSystemMap maps CIM_OperationSystem class to os product.
    """

    maptype = "DeviceMap"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_OperatingSystem":
                (
                    "SELECT * FROM CIM_OperatingSystem",
                    None,
                    cs,
                    {
                        "_sysname":"CSName",
                        "setOSProductKey":"Description",
                        "_name":"Name",
                        "_totalMemory":"TotalVisibleMemorySize",
                        "_totalSwap":"TotalVirtualMemorySize",
                        "_version":"Version",
                    }
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        maps = []
        try:
            instances = results.get("CIM_OperatingSystem")
            if not instances: return
            sysnames = self._getSysnames(device, results, "CIM_OperatingSystem")
            for os in instances:
                if (os.get("_sysname") or "").lower() in sysnames: break
            else:
                os = instances[0]
            om = self.objectMap(os)
            osVersion = os.get("_version", "unknown")
            if os.get("_name", "").startswith('Microsoft'):
                setOSProductKey = om._name.split("|", 1)[0]
                manuf = "Microsoft"
                om.snmpDescr = '%s (%s)'%(setOSProductKey, osVersion)
            elif om.setOSProductKey.startswith("A class"):
                setOSProductKey = osVersion
                manuf = setOSProductKey.split(" ", 1)[0]
                om.snmpDescr = osVersion
            else:
                setOSProductKey = om.setOSProductKey.split("\n", 1)[0]
                manuf = setOSProductKey.split(" ", 1)[0]
                om.snmpDescr = "%s (%s)"%(om.setOSProductKey, osVersion)
            om.setOSProductKey =  MultiArgs(setOSProductKey, manuf)
            maps.append(om)
            maps.append(ObjectMap({"totalMemory": (
                            os.get("_totalMemory", 0) * 1024)}, compname="hw"))
            maps.append(ObjectMap({"totalSwap": (
                            os.get("_totalSwap", 0) * 1024)}, compname="os"))
        except:
            log.warning('processing error')
            return
        return maps
