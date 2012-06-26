################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMProductMap

CIMProductMap maps CIM_Product class to Product class.

$Id: CIMProductMap.py,v 1.2 2012/06/26 23:17:59 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CIMProductMap(CIMPlugin):
    """Map CIM_Product class to Product class"""

    maptype = "ProductMap"
    modname = "ZenPacks.community.CIMMon.CIM_Product"
    relname = "collections"
    compname = "os"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Product":
                (
                    "SELECT * FROM CIM_Product",
                    None,
                    cs,
                    {
                        "setProductKey":"Name",
                        "_manuf":"Vendor",
                        "id":"Name",
                    },
                ),
            }

    def _getInstallDate(self, inst):
        return "1968/01/08 00:00:00"

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for inst in results.get("CIM_Product") or ():
            try:
                om = self.objectMap(inst)
                if not om.setProductKey: continue
                om.id = self.prepId(om.id)
                om._manuf = str(om._manuf).split()[0] or "Unknown"
                om.setProductKey = MultiArgs(om.setProductKey, om._manuf)
                if "setInstallDate" in inst:
                    om.setInstallDate = self._getInstallDate(inst)
                rm.append(om)
            except AttributeError:
                continue
        return rm
