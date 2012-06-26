################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMStorageVolumeMap

CIMStorageVolumeMap maps CIM_StorageVolume class to CIM_StorageVolume class.

$Id: CIMStorageVolumeMap.py,v 1.5 2012/06/26 23:18:29 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin

class CIMStorageVolumeMap(CIMPlugin):
    """Map CIM_StorageVolume class to LogicalDisk"""

    maptype = "LogicalDiskMap"
    modname = "ZenPacks.community.CIMMon.CIM_StorageVolume"
    relname = "storagevolumes"
    compname = "os"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_StorageVolume":
                (
                    "SELECT * FROM CIM_StorageVolume",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "accessType":"Access",
                        "blockSize":"BlockSize",
                        "_dr":"DataRedundancy",
                        "id":"DeviceID",
                        "title":"ElementName",
                        "_pr":"PackageRedundancy",
                        "_sysname":"SystemName",
                    },
                ),
            }

    def _accessTypes(self, aType):
        return {0: "Unknown",
                1: "Readable",
                2: "Writable",
                3: "Read/Write Supported",
                4: "Write Once",
                }.get(aType, 'Unknown')

    def _getDiskType(self, inst):
        if "diskType" in inst:
            return inst["diskType"]
        dr = int(inst.get("_dr") or 0)
        if dr > 2: dr = 2
        return {(0, 1): "RAID0",
                (1, 1): "RAID5",
                (1, 2): "RAID1+0",
                (2, 1): "RAID6",
                (2, 2): "RAID5+1",
                }.get((int(inst.get("_pr") or 0), dr), "Unknown")

    def _getPool(self, results, inst):
        if "setStoragePool" in inst:
            return inst["setStoragePool"]
        return self._findInstance(results, "CIM_AllocatedFromStoragePool",
                                    "dep", inst.get("setPath")).get("ant") or ""

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        instances = results.get("CIM_StorageVolume")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_StorageVolume")
        for inst in instances:
            if (inst.get("_sysname") or "").lower() not in sysnames: continue
            try:
                om = self.objectMap(inst)
                om.id = self.prepId(om.id)
                om.diskType = self._getDiskType(inst)
                om.accessType=self._accessTypes(int(inst.get("accessType") or 0))
                collections = self._getCollections(results, inst)
                if collections:
                    om.setCollections = collections
                storagePool = self._getPool(results, inst)
                if storagePool:
                    om.setStoragePool = storagePool
                statPath = self._getStatPath(results, inst)
                if statPath:
                    om.setStatPath = statPath
            except AttributeError:
                continue
            rm.append(om)
        return rm
