################################################################################
#
# This program is part of the CIMMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMComputerSystemMap

CIMComputerSystemMap maps CIM_ComputerSystem class to hw product.

$Id: CIMComputerSystemMap.py,v 1.5 2012/06/27 19:45:38 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]


from ZenPacks.community.CIMMon.CIMPlugin import CIMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs, ObjectMap

class CIMComputerSystemMap(CIMPlugin):
    """
    CIMComputerSystemMap maps CIM_ComputerSystem classes to get
    hw and os products.
    """

    maptype = "DeviceMap"
    modname = "ZenPacks.community.CIMMon.CIM_ComputerSystem"
    relname = "cards"
    compname = "hw"
    deviceProperties = CIMPlugin.deviceProperties + ('zCIMHWConnectionString',)

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_descr":"Description",
                        "_contact":"PrimaryOwnerContact",
                        "_sysname":"Name",
                    },
                ),
            }

    def _getPackage(self, results, inst):
        if "CIM_PhysicalPackage" not in results: return {}
        return  self._findInstance(results, "CIM_PhysicalPackage", "_path",
                self._findInstance(results, "CIM_ComputerSystemPackage", "dep",
                inst.get("setPath")).get("ant"))

    def _getSlot(self, results, inst):
        try: return int(inst.get("slot") or 0)
        except: return 0

    def _monitor(self, inst):
        return True

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        maps = []
        rm = self.relMap()
        instances = results.get("CIM_ComputerSystem")
        if not instances: return rm
        sysnames = self._getSysnames(device, results, "CIM_ComputerSystem")
        sysname = sysnames[0]
        for inst in instances:
            subsysname = (inst.get("_sysname") or "").lower()
            if subsysname not in sysnames: continue
            try:
                inst.update(self._getPackage(results, inst))
                productKey = inst.get("setProductKey")
                if (len(instances)==1) or (not maps and (sysname in subsysname)):
                    om = ObjectMap()
                    om.snmpindex = inst.get("setPath") or ""
                    om.snmpSysName = subsysname
                    om.snmpDescr = inst.get("_descr") or ""
                    om.snmpContact = inst.get("_contact") or ""
                    if productKey:
                        om.setHWProductKey = MultiArgs(productKey,
                                            inst.get("_manuf") or "Unknown")
                    serialNumber = inst.get("serialNumber")
                    if serialNumber:
                        om.setHWSerialNumber = serialNumber
                    tag = inst.get("tag")
                    if tag:
                        om.setHWTag = tag
                    maps.append(om)
                    continue
                om = self.objectMap(inst)
                om.id = self.prepId(inst.get("_sysname") or "")
                if not om.id: continue
                if productKey:
                    om.setProductKey = MultiArgs(productKey,
                                        inst.get("_manuf") or "Unknown")
                om.slot = self._getSlot(results, inst)
                collections = self._getCollections(results, inst)
                if collections:
                    om.setCollections = collections
                statPath = self._getStatPath(results, inst)
                if statPath:
                    om.setStatPath = statPath
                om.monitor = self._monitor(inst)
                rm.append(om)
            except:
                log.warning('processing error')
        if len(rm.maps) > 0:
            maps.append(rm)
        return maps
