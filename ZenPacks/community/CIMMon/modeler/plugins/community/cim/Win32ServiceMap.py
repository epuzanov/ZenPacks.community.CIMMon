################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """Win32ServiceMap

Win32ServiceMap gathers status of Windows services

$Id: Win32ServiceMap.py,v 1.3 2012/10/15 17:32:15 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class Win32ServiceMap(CIMPlugin):
    """Map Win32_Service class to WinService class"""

    maptype = "WinServiceMap"
    compname = "os"
    relname = "winservices"
    modname = "Products.ZenModel.WinService"

    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "Win32_Service":
                (
                    "SELECT * FROM Win32_Service",
                    None,
                    cs,
                    {
                        "_acceptPause":"AcceptPause",
                        "_acceptStop":"AcceptStop",
                        "_description":"Caption",
                        "_name":"Name",
                        "pathName":"PathName",
                        "serviceType":"ServiceType",
                        "startMode":"StartMode",
                        "startName":"StartName",
                        "_state":"State",
                    }
                ),
            }

    def process(self, device, results, log):
        """Collect win service info from this device.
        """
        log.info('Processing WinServices for device %s' % device.id)
        rm = self.relMap()
        instances = results.get("Win32_Service")
        if not instances: return rm
        for inst in instances:
            try:
                om = self.objectMap(inst)
                om.id = self.prepId(om._name)
                if not om.id: continue
                om.setServiceClass = {"name":om._name,
                                      "description":om._description}
                rm.append(om)
            except: continue
        return rm

