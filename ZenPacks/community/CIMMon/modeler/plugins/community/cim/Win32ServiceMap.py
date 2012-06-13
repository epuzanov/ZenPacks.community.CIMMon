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

$Id: Win32ServiceMap.py,v 1.0 2012/06/13 20:54:40 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class Win32ServiceMap(CIMPlugin):
    """Map Win32_Service class to WinService class"""

    maptype = "WinServiceMap"
    compname = "os"
    relname = "winservices"
    modname = "Products.ZenModel.WinService"

    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
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
        for instance in results.get("Win32_Service", ()):
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om._name)
                om.setServiceClass = {"name":om._name,
                                      "description":om._description}
                rm.append(om)
            except: continue
        return rm

