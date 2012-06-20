################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMStoragePoolMap

CIMStoragePoolMap maps CIM_StoragePool class to CIM_StoragePool class.

$Id: CIMStoragePoolMap.py,v 1.2 2012/06/20 20:40:55 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMStoragePoolMap(CIMPlugin):
    """Map CIM_StoragePool CIM class to CIM_StoragePool class"""

    maptype = "StoragePoolMap"
    modname = "ZenPacks.community.CIMMon.CIM_StoragePool"
    relname = "storagepools"
    compname = "os"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_StoragePool":
                (
                    "SELECT * FROM CIM_StoragePool",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"InstanceID",
                        "title":"ElementName",
                        "poolId":"PoolID",
                        "_primordial":"Primordial",
                        "totalManagedSpace":"TotalManagedSpace",
                        "usage":"Usage",
                    },
                ),
            }

    def _getUsage(self, usage):
        try:
            return {
                1:"Other",
                2:"Unrestricted",
                3:"Block Server",
                4:"Delta Replica Container",
                5:"Migration Services",
                6:"Local Replication Services",
                7:"Remote Replication Services",
                8:"Sparing",
                }.get(int(usage or 2)) or "Unrestricted"
        except:
            return usage

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_StoragePool")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_StoragePool")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            if (str(inst.get("_primordial")).lower() == "true" or (
                        'rimordial' in (inst.get("setPath") or ""))): continue
            try:
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                if not hasattr(om, "title"):
                    om.title = om.poolId
                if hasattr(om, "usage"):
                    om.usage = self._getUsage(om.usage)
            except AttributeError:
                continue
            rm.append(om)
        return rm
